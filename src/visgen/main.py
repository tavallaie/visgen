"""
Visgen — Audio Visualizer Examples
==================================
Each example is a standalone function. Choose which ones to run by editing
the EXAMPLES list at the bottom of the file.

All output files are saved to the `output/` directory.
"""

import os

import numpy as np
from PIL import Image

from visgen import (
    AudioVisualizerVideo,
    BounceEffect,
    CircularVisualizer,
    ColorBackground,
    ColorScheme,
    GlowEffect,
    ImageBackground,
    ImageOverlay,
    ShakeEffect,
    SmoothDecayEffect,
    TextOverlay,
    TimedText,
    VideoOverlay,
    VignetteEffect,
    ZoomPulseEffect,
)
from visgen.bars.base import BarEffect
from visgen.effects.base import FrameEffect

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
os.makedirs("output", exist_ok=True)

single_colors = ColorScheme(
    bg=(15, 15, 30),
    bar=(0, 220, 255),
    bar_glow=(0, 220, 255),
    circle_border=(150, 150, 200),
    divider=(40, 40, 60),
    cross=(60, 60, 80),
)

quad_colors = [
    ColorScheme(bar=(0, 200, 255), bar_glow=(0, 200, 255)),
    ColorScheme(bar=(255, 100, 100), bar_glow=(255, 100, 100)),
    ColorScheme(bar=(100, 255, 100), bar_glow=(100, 255, 100)),
    ColorScheme(bar=(255, 200, 50), bar_glow=(255, 200, 50)),
]


# ============================================================================
# EXAMPLES
# ============================================================================


def example_01_minimal() -> None:
    """Minimal single visualizer (default background + center)."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/01_minimal.mp4",
    )
    viz.render_single()


def example_02_color_bg() -> None:
    """Solid color background."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/02_color_bg.mp4",
        background=ColorBackground(color=(30, 10, 40)),
    )
    viz.render_single()


def example_03_image_bg_cover() -> None:
    """Image background — cover fit (no effect)."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/03_image_bg_cover.mp4",
        background=ImageBackground("assets/background.jpg", fit_mode="cover"),
    )
    viz.render_single()


def example_04_image_bg_blur() -> None:
    """Image background — blur effect."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/04_image_bg_blur.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect="blur",
            blur_radius=12.0,
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_05_image_bg_grayscale() -> None:
    """Image background — grayscale effect."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/05_image_bg_grayscale.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect="grayscale",
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_06_image_bg_sepia() -> None:
    """Image background — sepia effect + lowered opacity."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/06_image_bg_sepia.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect="sepia",
            opacity=0.5,
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_07_position_topleft() -> None:
    """Position — top-left corner."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/07_position_topleft.mp4",
    )
    viz.render_single(position="top-left")


def example_08_position_bottomright() -> None:
    """Position — bottom-right corner."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/08_position_bottomright.mp4",
    )
    viz.render_single(position="bottom-right")


def example_09_position_custom() -> None:
    """Position — custom pixel coordinates."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/09_position_custom.mp4",
    )
    viz.render_single(position=(300, 800))


def example_10_text_title() -> None:
    """Text overlay — static title."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/10_text_title.mp4",
        colors=single_colors,
    )
    viz.render_single(
        overlays=[
            TextOverlay(
                text="My Awesome Track",
                position=(540, 80),
                color=(255, 255, 255),
                font_size=60,
                anchor="mm",
            ),
        ],
    )


def example_11_timed_lyrics() -> None:
    """Timed text — lyrics / captions."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/11_timed_lyrics.mp4",
        colors=single_colors,
    )
    viz.render_single(
        overlays=[
            TextOverlay("Song Title", (540, 80), font_size=55, anchor="mm"),
            TimedText(
                0.0, 3.5, "First line of lyrics", (540, 980), font_size=38, anchor="mm"
            ),
            TimedText(
                4.0, 7.5, "Second line appears", (540, 980), font_size=38, anchor="mm"
            ),
            TimedText(
                8.0, 11.5, "Third line of song", (540, 980), font_size=38, anchor="mm"
            ),
            TimedText(
                12.0, 15.5, "Fourth line goes on", (540, 980), font_size=38, anchor="mm"
            ),
            TimedText(
                16.0, 20.0, "Final line...", (540, 980), font_size=38, anchor="mm"
            ),
        ],
    )


def example_12_image_overlay_static() -> None:
    """Image overlay — static logo (no time limit)."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/12_image_overlay_static.mp4",
    )
    viz.render_single(
        overlays=[
            ImageOverlay(
                image_path="assets/logo.png",
                position=(100, 100),
                size=(120, 120),
                anchor="mm",
            ),
        ],
    )


def example_13_image_overlay_timed() -> None:
    """Image overlay — timed badge (appears only 2s-6s)."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/13_image_overlay_timed.mp4",
    )
    viz.render_single(
        overlays=[
            ImageOverlay(
                image_path="assets/logo.png",
                position=(540, 540),
                size=(200, 200),
                anchor="mm",
                start_time=2.0,
                end_time=6.0,
                opacity=0.9,
            ),
        ],
    )


def example_14_image_watermark() -> None:
    """Image overlay — corner watermark with opacity."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/14_image_watermark.mp4",
    )
    viz.render_single(
        overlays=[
            ImageOverlay(
                image_path="assets/watermark.png",
                position=(1020, 1020),
                size=(80, 80),
                anchor="rb",
                opacity=0.4,
            ),
        ],
    )


def example_15_video_overlay_loop() -> None:
    """Video overlay — looping corner animation (no time limit)."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/15_video_overlay_loop.mp4",
    )
    viz.render_single(
        overlays=[
            VideoOverlay(
                video_path="assets/loop.mp4",
                position=(100, 980),
                size=(200, 200),
                anchor="mm",
                loop=True,
            ),
        ],
    )


def example_16_video_overlay_timed() -> None:
    """Video overlay — timed, no loop."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/16_video_overlay_timed.mp4",
    )
    viz.render_single(
        overlays=[
            VideoOverlay(
                video_path="assets/loop.mp4",
                position=(540, 540),
                size=(400, 400),
                anchor="mm",
                start_time=1.0,
                end_time=6.0,
                loop=False,
            ),
        ],
    )


def example_17_mixed_overlays() -> None:
    """Mixed overlays — text + image + video + background."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/17_mixed_overlays.mp4",
        circle_radius=160,
        bar_count=72,
        colors=single_colors,
        background=ImageBackground(
            "assets/background.jpg",
            effect="blur",
            blur_radius=10.0,
            fit_mode="cover",
        ),
    )
    viz.render_single(
        position="center",
        overlays=[
            TextOverlay("Mixed Overlay Demo", (540, 60), font_size=50, anchor="mm"),
            ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
            TimedText(
                2.0, 5.0, "Now playing...", (540, 1000), font_size=36, anchor="mm"
            ),
            VideoOverlay(
                "assets/loop.mp4",
                position=(980, 100),
                size=(150, 150),
                anchor="mm",
                loop=True,
            ),
            ImageOverlay(
                "assets/logo.png",
                position=(980, 980),
                size=(120, 120),
                anchor="mm",
                start_time=4.0,
                end_time=10.0,
            ),
        ],
    )


def example_18_left_visualizer() -> None:
    """Visualizer on the left, text & media on the right layout."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/18_left_visualizer.mp4",
        circle_radius=200,
        bar_count=80,
        colors=single_colors,
        background=ColorBackground((10, 10, 20)),
    )
    viz.render_single(
        position=(300, 540),
        overlays=[
            TextOverlay("Artist Name", (800, 300), font_size=50, anchor="mm"),
            TextOverlay("Track Title", (800, 380), font_size=36, anchor="mm"),
            ImageOverlay(
                "assets/album_art_small.png", (800, 600), size=(200, 200), anchor="mm"
            ),
            TimedText(1.0, 4.0, "Intro", (800, 800), font_size=30, anchor="mm"),
            TimedText(4.5, 8.0, "Verse 1", (800, 800), font_size=30, anchor="mm"),
        ],
    )


def example_19_quad_same() -> None:
    """Quad same — now using render_multi."""
    qv = CircularVisualizer(
        "assets/photo.jpg", circle_radius=180, bar_count=80, colors=single_colors
    )
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/19_quad_same_bg.mp4",
        visualizers=[qv],
        background=ImageBackground(
            "assets/background.jpg",
            effect="blur",
            blur_radius=8.0,
            fit_mode="cover",
        ),
    )
    video.render_multi(
        configs=[
            (qv, (540, 540), 0),
            (qv, (1620, 540), np.pi / 2),
            (qv, (540, 1620), np.pi),
            (qv, (1620, 1620), -np.pi / 2),
        ],
        width=2160,
        height=2160,
        overlays=[
            TextOverlay(
                "Quad Same via render_multi", (1080, 60), font_size=50, anchor="mm"
            ),
            ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
            VideoOverlay(
                "assets/loop.mp4", (2000, 2000), size=(200, 200), anchor="mm", loop=True
            ),
        ],
    )


def example_20_quad_diff_colors() -> None:
    """Quad different colors — now using render_multi."""
    v1 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[0])
    v2 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[1])
    v3 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[2])
    v4 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[3])
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/20_quad_diff_colors.mp4",
        visualizers=[v1, v2, v3, v4],
        background=ColorBackground((15, 15, 30)),
    )
    video.render_multi(
        configs=[
            (v1, (540, 540), 0),
            (v2, (1620, 540), np.pi / 3),
            (v3, (540, 1620), np.pi),
            (v4, (1620, 1620), -np.pi / 3),
        ],
        width=2160,
        height=2160,
        overlays=[
            TextOverlay(
                "Multi-Color Quad via render_multi",
                (1080, 60),
                font_size=50,
                anchor="mm",
            ),
            ImageOverlay(
                "assets/logo.png",
                position=(1080, 2050),
                size=(150, 150),
                start_time=2.0,
                end_time=8.0,
                anchor="mm",
            ),
        ],
    )


def example_21_repeat_single() -> None:
    """Repeated bars single color + background image."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/21_repeat_single.mp4",
        circle_radius=180,
        bar_count=80,
        colors=single_colors,
        background=ImageBackground("assets/background.jpg", fit_mode="cover"),
    )
    viz.render_quad_repeated_bars(
        dividers=True,
        quadrant_ranges=[
            (0, np.pi / 2),
            (np.pi / 2, np.pi),
            (-np.pi, -np.pi / 2),
            (-np.pi / 2, 0),
        ],
        overlays=[
            TextOverlay("Repeated Bars", (540, 60), font_size=50, anchor="mm"),
        ],
    )


def example_22_repeat_multicolor() -> None:
    """Repeated bars multi-color + all overlay types."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/22_repeat_multicolor_full.mp4",
        circle_radius=180,
        bar_count=80,
        colors=ColorScheme(bg=(15, 15, 30), circle_border=(150, 150, 200)),
        background=ColorBackground((15, 15, 30)),
    )
    viz.render_quad_repeated_bars_multi_color(
        quarter_colors=quad_colors,
        dividers=True,
        quadrant_ranges=[
            (0, np.pi / 2),
            (np.pi / 2, np.pi),
            (-np.pi, -np.pi / 2),
            (-np.pi / 2, 0),
        ],
        overlays=[
            TextOverlay("Full Feature Demo", (540, 60), font_size=50, anchor="mm"),
            TimedText(1.0, 4.0, "Intro...", (540, 1000), font_size=35, anchor="mm"),
            ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
            VideoOverlay(
                "assets/loop.mp4",
                position=(980, 100),
                size=(120, 120),
                anchor="mm",
                loop=True,
            ),
        ],
    )


def example_23_power_user() -> None:
    """Everything together — the 'power user' demo."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/23_power_user.mp4",
        circle_radius=170,
        bar_count=72,
        bar_max_length=220,
        colors=single_colors,
        background=ImageBackground(
            "assets/background.jpg",
            effect="blur",
            blur_radius=15.0,
            opacity=0.7,
            fit_mode="cover",
        ),
    )
    viz.render_single(
        position=(400, 540),
        overlays=[
            TextOverlay("Power User Demo", (800, 200), font_size=48, anchor="mm"),
            TextOverlay("feat. VisGen", (800, 260), font_size=28, anchor="mm"),
            TimedText(
                0.5, 3.0, "Lights are flashing", (800, 700), font_size=32, anchor="mm"
            ),
            TimedText(
                3.5, 6.5, "Music is blasting", (800, 700), font_size=32, anchor="mm"
            ),
            TimedText(
                7.0, 10.0, "Feel the rhythm", (800, 700), font_size=32, anchor="mm"
            ),
            ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
            ImageOverlay(
                "assets/logo.png",
                position=(100, 980),
                size=(120, 120),
                anchor="mm",
                start_time=2.0,
                end_time=9.0,
            ),
            VideoOverlay(
                "assets/loop.mp4",
                position=(980, 980),
                size=(180, 180),
                anchor="mm",
                loop=True,
            ),
            VideoOverlay(
                "assets/loop.mp4",
                position=(800, 450),
                size=(250, 140),
                anchor="mm",
                start_time=1.0,
                end_time=5.0,
                loop=False,
            ),
        ],
    )


def example_24_position_showcase() -> None:
    """Position showcase — visualizer in every corner."""
    positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
    for pos in positions:
        viz = AudioVisualizerVideo(
            audio_path="assets/audio.wav",
            image_path="assets/photo.jpg",
            output_path=f"output/24_position_{pos.replace('-', '_')}.mp4",
            background=ColorBackground((20, 20, 35)),
        )
        viz.render_single(position=pos)


def example_25_bg_effects() -> None:
    """Background effect showcase."""
    effects = [
        ("none", None),
        ("blur", "blur"),
        ("grayscale", "grayscale"),
        ("sepia", "sepia"),
    ]
    for name, effect in effects:
        viz = AudioVisualizerVideo(
            audio_path="assets/audio.wav",
            image_path="assets/photo.jpg",
            output_path=f"output/25_bg_{name}.mp4",
            background=ImageBackground(
                "assets/background.jpg",
                effect=effect,
                blur_radius=10.0 if effect == "blur" else 5.0,
                fit_mode="cover",
            ),
        )
        viz.render_single()


def example_25b_blur_grayscale() -> None:
    """Chained background effects — blur + grayscale."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/25b_bg_blur_grayscale.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect=["blur", "grayscale"],
            blur_radius=12.0,
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_25c_blur_sepia() -> None:
    """Chained background effects — blur + sepia + opacity."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/25c_bg_blur_sepia.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect=["blur", "sepia"],
            blur_radius=8.0,
            opacity=0.6,
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_26_multi_two_side() -> None:
    """Two visualizers side by side (render_multi)."""
    left_viz = CircularVisualizer(
        "assets/photo.jpg",
        circle_radius=140,
        bar_count=64,
        colors=ColorScheme(bar=(0, 200, 255), bar_glow=(0, 200, 255)),
    )
    right_viz = CircularVisualizer(
        "assets/scene.jpg",
        circle_radius=140,
        bar_count=64,
        colors=ColorScheme(bar=(255, 100, 100), bar_glow=(255, 100, 100)),
    )
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/26_multi_two_side.mp4",
        visualizers=[left_viz, right_viz],
        background=ColorBackground((10, 10, 20)),
    )
    video.render_multi(
        configs=[
            (left_viz, (300, 540), 0),
            (right_viz, (780, 540), np.pi),
        ],
        overlays=[
            TextOverlay("Duo Visualizer", (540, 60), font_size=50, anchor="mm"),
        ],
    )


def example_27_multi_three_row() -> None:
    """Three visualizers in a row."""
    viz_a = CircularVisualizer("assets/photo.jpg", 100, 48, 150, colors=quad_colors[0])
    viz_b = CircularVisualizer("assets/photo.jpg", 100, 48, 150, colors=quad_colors[1])
    viz_c = CircularVisualizer("assets/photo.jpg", 100, 48, 150, colors=quad_colors[2])
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/27_multi_three_row.mp4",
        visualizers=[viz_a, viz_b, viz_c],
        background=ImageBackground(
            "assets/background.jpg", effect="blur", blur_radius=10.0
        ),
    )
    video.render_multi(
        configs=[
            (viz_a, (200, 540), -np.pi / 2),
            (viz_b, (540, 540), -np.pi / 2),
            (viz_c, (880, 540), -np.pi / 2),
        ],
        overlays=[
            TextOverlay("Triple Threat", (540, 60), font_size=50, anchor="mm"),
        ],
    )


def example_28_multi_four_corners() -> None:
    """Four visualizers in each corner."""
    v1 = CircularVisualizer("assets/photo.jpg", 120, 56, 160, colors=quad_colors[0])
    v2 = CircularVisualizer("assets/scene.jpg", 120, 56, 160, colors=quad_colors[1])
    v3 = CircularVisualizer("assets/photo.jpg", 120, 56, 160, colors=quad_colors[2])
    v4 = CircularVisualizer("assets/scene.jpg", 120, 56, 160, colors=quad_colors[3])
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/28_multi_four_corners.mp4",
        visualizers=[v1, v2, v3, v4],
        background=ColorBackground((15, 15, 30)),
    )
    video.render_multi(
        configs=[
            (v1, "top-left", 0),
            (v2, "top-right", np.pi / 2),
            (v3, "bottom-left", np.pi),
            (v4, "bottom-right", -np.pi / 2),
        ],
        width=1080,
        height=1080,
        overlays=[
            TextOverlay("Quad Squad", (540, 540), font_size=40, anchor="mm"),
        ],
    )


def example_29_multi_big_small() -> None:
    """Big + small visualizer combo."""
    big = CircularVisualizer("assets/photo.jpg", 200, 80, 220, colors=single_colors)
    small = CircularVisualizer(
        "assets/logo.png", 80, 32, 100, colors=ColorScheme(bar=(255, 255, 255))
    )
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/29_multi_big_small.mp4",
        visualizers=[big, small],
        background=ImageBackground("assets/background.jpg", fit_mode="cover"),
    )
    video.render_multi(
        configs=[
            (big, (400, 540), -np.pi / 2),
            (small, (900, 900), 0),
        ],
        overlays=[
            TextOverlay("Big & Small", (800, 200), font_size=45, anchor="mm"),
            ImageOverlay("assets/logo.png", (900, 200), size=(80, 80), anchor="mm"),
        ],
    )


def example_30_custom_viz_inline() -> None:
    """render_single with a custom visualizer passed inline."""
    custom_viz = CircularVisualizer(
        image_path="assets/photo.jpg",
        circle_radius=180,
        bar_count=80,
        bar_max_length=240,
        colors=ColorScheme(bg=(0, 0, 0), bar=(255, 50, 150), bar_glow=(255, 50, 150)),
    )
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/30_custom_viz_inline.mp4",
    )
    video.render_single(
        position="center",
        visualizer=custom_viz,
        overlays=[
            TextOverlay("Custom Viz Inline", (540, 80), font_size=55, anchor="mm"),
        ],
    )


def example_31_frame_effects() -> None:
    """Frame effects — glow + vignette."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/31_frame_effects.mp4",
        colors=single_colors,
        frame_effects=[
            GlowEffect(strength=0.4, radius=10.0),
            VignetteEffect(strength=0.5),
        ],
    )
    viz.render_single()


def example_32_bar_effects() -> None:
    """Bar effects — bounce + smooth decay."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/32_bar_effects.mp4",
        colors=single_colors,
        bar_effects=[
            BounceEffect(speed=0.15, amplitude=0.2),
            SmoothDecayEffect(decay=0.9),
        ],
    )
    viz.render_single()


def example_33_shake_effect() -> None:
    """Shake effect synced to bass."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/33_shake_effect.mp4",
        colors=single_colors,
        frame_effects=[ShakeEffect(max_offset=15, bass_bins=10)],
    )
    viz.render_single()


def example_34_zoom_pulse() -> None:
    """Zoom pulse effect."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/34_zoom_pulse.mp4",
        colors=single_colors,
        frame_effects=[ZoomPulseEffect(max_zoom=0.08)],
    )
    viz.render_single()


def example_35_custom_effects() -> None:
    """Custom inline effect + plugin registry."""

    class MyGreenTint(FrameEffect):
        def apply(self, frame, frame_idx, bar_values=None):
            arr = np.array(frame, dtype=np.float32)
            arr[:, :, 1] *= 1.15
            return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    class MySquashBars(BarEffect):
        def process(self, bar_values, frame_idx, audio_chunk=None):
            return np.power(bar_values, 1.5)

    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/35_custom_effects.mp4",
        colors=single_colors,
        frame_effects=[MyGreenTint()],
        bar_effects=[MySquashBars()],
    )
    viz.render_single(
        overlays=[
            TextOverlay("Custom Effects Demo", (540, 80), font_size=50, anchor="mm"),
        ],
    )


def example_36_multi_with_effects() -> None:
    """Multi-viz + effects combined."""
    left = CircularVisualizer("assets/photo.jpg", 140, 64, 180, colors=quad_colors[0])
    right = CircularVisualizer("assets/scene.jpg", 140, 64, 180, colors=quad_colors[1])
    video = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        output_path="output/36_multi_with_effects.mp4",
        visualizers=[left, right],
        background=ColorBackground((10, 10, 20)),
        frame_effects=[GlowEffect(strength=0.3, radius=8.0)],
        bar_effects=[BounceEffect(speed=0.1, amplitude=0.15)],
    )
    video.render_multi(
        configs=[
            (left, (300, 540), 0),
            (right, (780, 540), np.pi),
        ],
        overlays=[
            TextOverlay("Multi + Effects", (540, 60), font_size=50, anchor="mm"),
        ],
    )


def example_37_bg_blur_grayscale() -> None:
    """Chained background effects — blur + grayscale."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/37_bg_blur_grayscale.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect=["blur", "grayscale"],
            blur_radius=12.0,
            fit_mode="cover",
        ),
    )
    viz.render_single()


def example_38_bg_blur_sepia() -> None:
    """Chained background effects — blur + sepia + opacity."""
    viz = AudioVisualizerVideo(
        audio_path="assets/audio.wav",
        image_path="assets/photo.jpg",
        output_path="output/38_bg_blur_sepia.mp4",
        background=ImageBackground(
            "assets/background.jpg",
            effect=["blur", "sepia"],
            blur_radius=8.0,
            opacity=0.6,
            fit_mode="cover",
        ),
    )
    viz.render_single()


# ============================================================================
# RUNNER — edit this list to choose which examples execute
# ============================================================================

EXAMPLES: list = [
    # example_01_minimal,
    # example_02_color_bg,
    # example_03_image_bg_cover,
    # example_04_image_bg_blur,
    # example_05_image_bg_grayscale,
    # example_06_image_bg_sepia,
    # example_07_position_topleft,
    # example_08_position_bottomright,
    # example_09_position_custom,
    # example_10_text_title,
    # example_11_timed_lyrics,
    # example_12_image_overlay_static,
    # example_13_image_overlay_timed,
    # example_14_image_watermark,
    # example_15_video_overlay_loop,
    # example_16_video_overlay_timed,
    # example_17_mixed_overlays,
    # example_18_left_visualizer,
    # example_19_quad_same,
    # example_20_quad_diff_colors,
    # example_21_repeat_single,
    # example_22_repeat_multicolor,
    # example_23_power_user,
    # example_24_position_showcase,
    # example_25_bg_effects,
    # example_25b_blur_grayscale,
    # example_25c_blur_sepia,
    # example_26_multi_two_side,
    # example_27_multi_three_row,
    # example_28_multi_four_corners,
    # example_29_multi_big_small,
    # example_30_custom_viz_inline,
    # example_31_frame_effects,
    # example_32_bar_effects,
    # example_33_shake_effect,
    # example_34_zoom_pulse,
    # example_35_custom_effects,
    example_36_multi_with_effects,
    example_37_bg_blur_grayscale,
    example_38_bg_blur_sepia,
]

if __name__ == "__main__":
    if not EXAMPLES:
        print("No examples selected. Uncomment items in the EXAMPLES list to run them.")
    else:
        for fn in EXAMPLES:
            print(f"\n>>> Running {fn.__name__}...")
            fn()
