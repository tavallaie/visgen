import os
import shutil
import subprocess
from typing import List, Optional, Tuple, Union

import cv2
import numpy as np
from PIL import Image, ImageDraw

from .audio import AudioProcessor
from .background import Background, ColorBackground
from .colors import ColorScheme
from .effects.base import FrameEffect
from .bars.base import BarEffect
from .overlay import BaseOverlay, TextOverlay, TimedText, VideoOverlay
from .utils import get_font, resolve_position
from .visualizer import CircularVisualizer

OverlayType = Union[TextOverlay, TimedText, BaseOverlay]


class AudioVisualizerVideo:
    """Main class to compose and render audio visualizer videos."""

    def __init__(
        self,
        audio_path: str,
        image_path: Optional[str] = None,
        output_path: str = "output.mp4",
        duration: Optional[float] = None,
        fps: int = 30,
        circle_radius: int = 150,
        bar_count: int = 64,
        bar_max_length: int = 200,
        colors: Optional[ColorScheme] = None,
        smooth_factor: float = 0.3,
        background: Optional[Background] = None,
        visualizers: Optional[List[CircularVisualizer]] = None,
        frame_effects: Optional[List[FrameEffect]] = None,
        bar_effects: Optional[List[BarEffect]] = None,
    ):
        self.audio_path = audio_path
        self.output_path = output_path
        self.fps = fps
        self.colors = colors or ColorScheme()
        self.smooth_factor = smooth_factor
        self.background = background or ColorBackground(self.colors.bg)

        self.audio = AudioProcessor(audio_path, fps=fps)
        self.duration = duration if duration is not None else self.audio.duration
        self.total_frames = int(self.duration * fps)

        if visualizers is not None:
            self.visualizers = visualizers
        elif image_path is not None:
            self.visualizers = [
                CircularVisualizer(
                    image_path=image_path,
                    circle_radius=circle_radius,
                    bar_count=bar_count,
                    bar_max_length=bar_max_length,
                    colors=self.colors,
                )
            ]
        else:
            raise ValueError("Either image_path or visualizers must be provided")

        # Backward-compat alias
        self.visualizer = self.visualizers[0]

        self.frame_effects = list(frame_effects) if frame_effects else []
        self.bar_effects = list(bar_effects) if bar_effects else []

    def _create_temp_dir(self, suffix: str = "") -> str:
        path = f"/tmp/visualizer_frames{suffix}"
        os.makedirs(path, exist_ok=True)
        return path

    def _encode_video(self, temp_dir: str, temp_video: str) -> None:
        """Encode frames to video using ffmpeg."""
        pattern = os.path.join(temp_dir, "frame_%06d.png")
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(self.fps),
            "-i",
            pattern,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "18",
            temp_video,
        ]
        subprocess.run(cmd, capture_output=True)

    def _mux_audio(self, temp_video: str) -> None:
        """Add audio to the final video."""
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            temp_video,
            "-i",
            self.audio_path,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "320k",
            "-shortest",
            self.output_path,
        ]
        subprocess.run(cmd, capture_output=True)

    def _draw_texts(
        self,
        draw: ImageDraw.Draw,
        frame_idx: int,
        overlays: Optional[List[OverlayType]] = None,
    ) -> None:
        """Draw text overlays onto the frame."""
        if not overlays:
            return

        current_time = frame_idx / self.fps

        for item in overlays:
            if isinstance(item, TimedText):
                if not (item.start_time <= current_time <= item.end_time):
                    continue
                font = get_font(item.font_path, item.font_size)
                self._draw_text_item(draw, item, font)
            elif isinstance(item, TextOverlay):
                font = get_font(item.font_path, item.font_size)
                self._draw_text_item(draw, item, font)

    def _draw_text_item(
        self,
        draw: ImageDraw.Draw,
        item: Union[TextOverlay, TimedText],
        font,
    ) -> None:
        """Draw a single text item with optional background box."""
        if item.bg_color is not None:
            bbox = draw.textbbox(
                item.position, item.text, font=font, anchor=item.anchor
            )
            pad = item.bg_padding
            padded = (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad)
            if item.bg_radius > 0:
                draw.rounded_rectangle(padded, radius=item.bg_radius, fill=item.bg_color)
            else:
                draw.rectangle(padded, fill=item.bg_color)

        draw.text(
            item.position,
            item.text,
            fill=item.color,
            font=font,
            anchor=item.anchor,
        )

    def _draw_media_overlays(
        self,
        canvas: Image.Image,
        frame_idx: int,
        overlays: Optional[List[OverlayType]] = None,
    ) -> None:
        """Draw image/video overlays onto the frame."""
        if not overlays:
            return

        current_time = frame_idx / self.fps

        for item in overlays:
            if isinstance(item, BaseOverlay):
                item.draw(canvas, current_time, self.fps)

    def _release_overlays(self, overlays: Optional[List[OverlayType]] = None) -> None:
        if not overlays:
            return
        for item in overlays:
            if isinstance(item, VideoOverlay):
                item.release()

    def render_single(
        self,
        width: int = 1080,
        height: int = 1080,
        start_angle: float = -np.pi / 2,
        position: Union[Tuple[int, int], str, None] = None,
        overlays: Optional[List[OverlayType]] = None,
        visualizer: Optional[CircularVisualizer] = None,
    ) -> str:
        """
        Render a single visualizer.

        position: (x, y) tuple, position string (e.g. "center", "top-left"),
                  or None for center.
        overlays: list of TextOverlay, TimedText, ImageOverlay, VideoOverlay.
        visualizer: optional CircularVisualizer to use instead of the default.
        """
        temp_dir = self._create_temp_dir("_single")
        temp_video = "/tmp/temp_video_single.mp4"

        viz = visualizer if visualizer is not None else self.visualizers[0]

        if position is None:
            center_x, center_y = width // 2, height // 2
        else:
            center_x, center_y = resolve_position(
                position, width, height,
                obj_width=viz.circle_radius * 2,
                obj_height=viz.circle_radius * 2,
            )

        prev_bars = np.zeros(viz.bar_count)

        for frame_idx in range(self.total_frames):
            img_pil = self.background.render(width, height, frame_idx)

            audio_chunk = self.audio.get_chunk(frame_idx)
            bar_values = self.audio.get_bar_values(
                frame_idx, viz.bar_count, prev_bars, self.smooth_factor
            )
            prev_bars = bar_values.copy()

            for effect in self.bar_effects:
                bar_values = effect.process(bar_values, frame_idx, audio_chunk)

            viz.render(
                img_pil,
                center_x,
                center_y,
                bar_values,
                frame_idx,
                phase_offset=start_angle + (np.pi / 2),
            )

            draw = ImageDraw.Draw(img_pil)
            self._draw_texts(draw, frame_idx, overlays)
            self._draw_media_overlays(img_pil, frame_idx, overlays)

            for effect in self.frame_effects:
                img_pil = effect.apply(img_pil, frame_idx, bar_values)

            frame = np.array(img_pil.convert("RGB"))
            cv2.imwrite(
                os.path.join(temp_dir, f"frame_{frame_idx:06d}.png"),
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

            if frame_idx % 30 == 0:
                print(f"Frame {frame_idx}/{self.total_frames}")

        self._encode_video(temp_dir, temp_video)
        self._mux_audio(temp_video)
        self._release_overlays(overlays)

        shutil.rmtree(temp_dir)
        os.remove(temp_video)

        print(f"Saved: {self.output_path}")
        return self.output_path

    def render_multi(
        self,
        configs: List[Tuple[CircularVisualizer, Union[Tuple[int, int], str], float]],
        width: int = 1080,
        height: int = 1080,
        overlays: Optional[List[OverlayType]] = None,
    ) -> str:
        """
        Render multiple visualizers on the same canvas.

        configs: list of (visualizer, position, start_angle)
                 position can be (x, y) tuple or string like "center", "top-left".
        All visualizers react to the same audio data.
        """
        temp_dir = self._create_temp_dir("_multi")
        temp_video = "/tmp/temp_video_multi.mp4"

        prev_bars = [np.zeros(c[0].bar_count) for c in configs]
        for effect in self.bar_effects:
            effect.reset()
        for effect in self.frame_effects:
            effect.reset()

        for frame_idx in range(self.total_frames):
            img_pil = self.background.render(width, height, frame_idx)

            audio_chunk = self.audio.get_chunk(frame_idx)
            for i, (viz, position, start_angle) in enumerate(configs):
                bar_values = self.audio.get_bar_values(
                    frame_idx, viz.bar_count, prev_bars[i], self.smooth_factor
                )
                prev_bars[i] = bar_values.copy()

                for effect in self.bar_effects:
                    bar_values = effect.process(bar_values, frame_idx, audio_chunk)

                cx, cy = resolve_position(
                    position, width, height,
                    obj_width=viz.circle_radius * 2,
                    obj_height=viz.circle_radius * 2,
                )

                viz.render(
                    img_pil,
                    cx,
                    cy,
                    bar_values,
                    frame_idx,
                    phase_offset=start_angle + (np.pi / 2),
                )

            draw = ImageDraw.Draw(img_pil)
            self._draw_texts(draw, frame_idx, overlays)
            self._draw_media_overlays(img_pil, frame_idx, overlays)

            for effect in self.frame_effects:
                img_pil = effect.apply(img_pil, frame_idx)

            frame = np.array(img_pil.convert("RGB"))
            cv2.imwrite(
                os.path.join(temp_dir, f"frame_{frame_idx:06d}.png"),
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

            if frame_idx % 30 == 0:
                print(f"Frame {frame_idx}/{self.total_frames}")

        self._encode_video(temp_dir, temp_video)
        self._mux_audio(temp_video)
        self._release_overlays(overlays)

        shutil.rmtree(temp_dir)
        os.remove(temp_video)

        print(f"Saved: {self.output_path}")
        return self.output_path

    def render_quad_repeated_bars(
        self,
        width: int = 1080,
        height: int = 1080,
        dividers: bool = True,
        quadrant_ranges: Optional[List[Tuple[float, float]]] = None,
        overlays: Optional[List[OverlayType]] = None,
    ) -> str:
        """
        One circle. The circumference is divided into 4 equal segments (quadrants).
        EACH segment contains the ENTIRE bar set repeated.
        """
        center_x, center_y = width // 2, height // 2

        if quadrant_ranges is None:
            quadrant_ranges = [
                (-np.pi / 2, 0),
                (-np.pi, -np.pi / 2),
                (np.pi / 2, np.pi),
                (0, np.pi / 2),
            ]

        temp_dir = self._create_temp_dir("_quad_repeat")
        temp_video = "/tmp/temp_video_quad_repeat.mp4"
        prev_bars = np.zeros(self.visualizer.bar_count)
        for effect in self.bar_effects:
            effect.reset()
        for effect in self.frame_effects:
            effect.reset()

        for frame_idx in range(self.total_frames):
            img_pil = self.background.render(width, height, frame_idx)
            draw = ImageDraw.Draw(img_pil)

            audio_chunk = self.audio.get_chunk(frame_idx)
            bar_values = self.audio.get_bar_values(
                frame_idx, self.visualizer.bar_count, prev_bars, self.smooth_factor
            )
            prev_bars = bar_values.copy()

            for effect in self.bar_effects:
                bar_values = effect.process(bar_values, frame_idx, audio_chunk)

            gap = self.visualizer.gap
            inner_r = self.visualizer.inner_radius

            for q_start, q_end in quadrant_ranges:
                for i in range(self.visualizer.bar_count):
                    angle = q_start + (q_end - q_start) * (i / self.visualizer.bar_count)

                    val = bar_values[i]
                    val *= 0.7 + 0.3 * np.sin(frame_idx * 0.05 + i * 0.1)
                    bar_length = val * self.visualizer.bar_max_length

                    x1 = center_x + inner_r * np.cos(angle)
                    y1 = center_y + inner_r * np.sin(angle)
                    x2 = center_x + (inner_r + bar_length) * np.cos(angle)
                    y2 = center_y + (inner_r + bar_length) * np.sin(angle)

                    intensity = val
                    r, g, b = self.visualizer.colors.bar_with_intensity(intensity)

                    bar_width = max(2, int(8 * (1 - 0.3 * intensity)))
                    draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=bar_width)

                    glow_radius = int(3 + 5 * intensity)
                    gx, gy = int(x2), int(y2)
                    for gr in range(glow_radius, 0, -1):
                        alpha = int(50 * (1 - gr / glow_radius) * intensity)
                        if alpha > 5:
                            bbox = (gx - gr, gy - gr, gx + gr, gy + gr)
                            draw.ellipse(bbox, fill=(r, g, b, alpha))

            img_pos = (
                center_x - self.visualizer.circle_radius,
                center_y - self.visualizer.circle_radius,
            )
            img_pil.paste(self.visualizer.image, img_pos, self.visualizer.image)

            bw = 4
            bbox = (
                center_x - self.visualizer.circle_radius - bw,
                center_y - self.visualizer.circle_radius - bw,
                center_x + self.visualizer.circle_radius + bw,
                center_y + self.visualizer.circle_radius + bw,
            )
            draw.ellipse(bbox, outline=self.colors.circle_border, width=bw)

            if dividers:
                draw.line(
                    [(center_x, 0), (center_x, height)], fill=self.colors.cross, width=1
                )
                draw.line(
                    [(0, center_y), (width, center_y)], fill=self.colors.cross, width=1
                )

            self._draw_texts(draw, frame_idx, overlays)
            self._draw_media_overlays(img_pil, frame_idx, overlays)

            for effect in self.frame_effects:
                img_pil = effect.apply(img_pil, frame_idx, bar_values)

            frame = np.array(img_pil.convert("RGB"))
            cv2.imwrite(
                os.path.join(temp_dir, f"frame_{frame_idx:06d}.png"),
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

            if frame_idx % 30 == 0:
                print(f"Frame {frame_idx}/{self.total_frames}")

        self._encode_video(temp_dir, temp_video)
        self._mux_audio(temp_video)
        self._release_overlays(overlays)

        shutil.rmtree(temp_dir)
        os.remove(temp_video)

        print(f"Saved: {self.output_path}")
        return self.output_path

    def render_quad_repeated_bars_multi_color(
        self,
        quarter_colors: List[ColorScheme],
        width: int = 1080,
        height: int = 1080,
        dividers: bool = True,
        quadrant_ranges: Optional[List[Tuple[float, float]]] = None,
        overlays: Optional[List[OverlayType]] = None,
    ) -> str:
        """
        One circle. Full bars repeated in each of 4 quadrants.
        Each quadrant uses its own ColorScheme from quarter_colors.
        """
        if len(quarter_colors) != 4:
            raise ValueError("quarter_colors must have exactly 4 ColorScheme objects")

        cx, cy = width // 2, height // 2

        if quadrant_ranges is None:
            quadrant_ranges = [
                (-np.pi / 2, 0),
                (-np.pi, -np.pi / 2),
                (np.pi / 2, np.pi),
                (0, np.pi / 2),
            ]

        temp_dir = self._create_temp_dir("_quad_repeat_mc")
        temp_video = "/tmp/temp_video_quad_repeat_mc.mp4"
        prev_bars = np.zeros(self.visualizer.bar_count)
        for effect in self.bar_effects:
            effect.reset()
        for effect in self.frame_effects:
            effect.reset()

        for frame_idx in range(self.total_frames):
            img_pil = self.background.render(width, height, frame_idx)
            draw = ImageDraw.Draw(img_pil)
            inner_r = self.visualizer.inner_radius

            audio_chunk = self.audio.get_chunk(frame_idx)
            bar_values = self.audio.get_bar_values(
                frame_idx, self.visualizer.bar_count, prev_bars, self.smooth_factor
            )
            prev_bars = bar_values.copy()

            for effect in self.bar_effects:
                bar_values = effect.process(bar_values, frame_idx, audio_chunk)

            for qi, (q_start, q_end) in enumerate(quadrant_ranges):
                for i in range(self.visualizer.bar_count):
                    angle = q_start + (q_end - q_start) * (i / self.visualizer.bar_count)

                    val = bar_values[i]
                    val *= 0.7 + 0.3 * np.sin(frame_idx * 0.05 + i * 0.1)
                    bar_length = val * self.visualizer.bar_max_length

                    x1 = cx + inner_r * np.cos(angle)
                    y1 = cy + inner_r * np.sin(angle)
                    x2 = cx + (inner_r + bar_length) * np.cos(angle)
                    y2 = cy + (inner_r + bar_length) * np.sin(angle)

                    r, g, b = quarter_colors[qi].bar_with_intensity(val)

                    bar_width = max(2, int(8 * (1 - 0.3 * val)))
                    draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=bar_width)

                    glow_radius = int(3 + 5 * val)
                    gx, gy = int(x2), int(y2)
                    for gr in range(glow_radius, 0, -1):
                        alpha = int(50 * (1 - gr / glow_radius) * val)
                        if alpha > 5:
                            bbox = (gx - gr, gy - gr, gx + gr, gy + gr)
                            draw.ellipse(bbox, fill=(r, g, b, alpha))

            img_pos = (
                cx - self.visualizer.circle_radius,
                cy - self.visualizer.circle_radius,
            )
            img_pil.paste(self.visualizer.image, img_pos, self.visualizer.image)

            bw = 4
            bbox = (
                cx - self.visualizer.circle_radius - bw,
                cy - self.visualizer.circle_radius - bw,
                cx + self.visualizer.circle_radius + bw,
                cy + self.visualizer.circle_radius + bw,
            )
            draw.ellipse(bbox, outline=self.colors.circle_border, width=bw)

            if dividers:
                draw.line([(cx, 0), (cx, height)], fill=self.colors.cross, width=1)
                draw.line([(0, cy), (width, cy)], fill=self.colors.cross, width=1)

            self._draw_texts(draw, frame_idx, overlays)
            self._draw_media_overlays(img_pil, frame_idx, overlays)

            for effect in self.frame_effects:
                img_pil = effect.apply(img_pil, frame_idx, bar_values)

            frame = np.array(img_pil.convert("RGB"))
            cv2.imwrite(
                os.path.join(temp_dir, f"frame_{frame_idx:06d}.png"),
                cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
            )

            if frame_idx % 30 == 0:
                print(f"Frame {frame_idx}/{self.total_frames}")

        self._encode_video(temp_dir, temp_video)
        self._mux_audio(temp_video)
        self._release_overlays(overlays)

        shutil.rmtree(temp_dir)
        os.remove(temp_video)

        print(f"Saved: {self.output_path}")
        return self.output_path

