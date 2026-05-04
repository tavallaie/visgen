import os
import subprocess
import numpy as np
from typing import Optional


class AudioProcessor:
    """Handles audio extraction and FFT analysis."""

    def __init__(self, audio_path: str, sample_rate: int = 44100, fps: int = 30):
        self.audio_path = audio_path
        self.sample_rate = sample_rate
        self.fps = fps
        self.samples_per_frame = sample_rate // fps
        self.audio_data = self._extract_audio()
        self.duration = len(self.audio_data) / sample_rate

    def _extract_audio(self) -> np.ndarray:
        """Extract raw mono audio data using ffmpeg."""
        raw_audio_path = "/tmp/raw_audio_oop.raw"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            self.audio_path,
            "-ar",
            str(self.sample_rate),
            "-ac",
            "1",
            "-f",
            "s16le",
            raw_audio_path,
        ]
        subprocess.run(cmd, capture_output=True)
        data = np.fromfile(raw_audio_path, dtype=np.int16)
        os.remove(raw_audio_path)
        return data.astype(np.float32) / 32768.0

    def get_chunk(self, frame_idx: int) -> np.ndarray:
        """Get audio chunk for a specific frame."""
        start = frame_idx * self.samples_per_frame
        end = start + self.samples_per_frame
        chunk = self.audio_data[start:end]
        if len(chunk) == 0:
            return np.zeros(self.samples_per_frame, dtype=np.float32)
        return chunk

    def get_bar_values(
        self,
        frame_idx: int,
        bar_count: int,
        smooth_prev: Optional[np.ndarray] = None,
        smooth_factor: float = 0.3,
    ) -> np.ndarray:
        """Compute FFT bar values for a frame."""
        chunk = self.get_chunk(frame_idx)

        if len(chunk) > 0:
            window = np.hanning(len(chunk))
            fft = np.fft.rfft(chunk * window)
            magnitude = np.abs(fft)
            if np.max(magnitude) > 0:
                magnitude = magnitude / np.max(magnitude)
        else:
            magnitude = np.zeros(bar_count)

        freq_bins = np.linspace(0, len(magnitude) - 1, bar_count)
        bar_values = np.interp(freq_bins, np.arange(len(magnitude)), magnitude)
        bar_values = np.clip(bar_values, 0, 1)

        if smooth_prev is not None:
            bar_values = smooth_factor * bar_values + (1 - smooth_factor) * smooth_prev

        return bar_values
