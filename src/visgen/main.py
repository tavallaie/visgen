"""
Visgen — Audio Visualizer Examples
==================================
Every example below runs automatically when you execute this file.
All output files are saved to the `output/` directory.
"""

import os
import numpy as np

from visgen import (
    AudioVisualizerVideo,
    CircularVisualizer,
    ColorScheme,
    ColorBackground,
    ImageBackground,
    TextOverlay,
    TimedText,
    ImageOverlay,
    VideoOverlay,
)

# ---------------------------------------------------------------------------
# Helper: create output directory
# ---------------------------------------------------------------------------
os.makedirs("output", exist_ok=True)

# ---------------------------------------------------------------------------
# Color presets (reused across examples)
# ---------------------------------------------------------------------------
single_colors = ColorScheme(
    bg=(15, 15, 30),
    bar=(0, 220, 255),
    bar_glow=(0, 220, 255),
    circle_border=(150, 150, 200),
    divider=(40, 40, 60),
    cross=(60, 60, 80),
)

quad_colors = [
    ColorScheme(bar=(0, 200, 255), bar_glow=(0, 200, 255)),  # Cyan
    ColorScheme(bar=(255, 100, 100), bar_glow=(255, 100, 100)),  # Red-pink
    ColorScheme(bar=(100, 255, 100), bar_glow=(100, 255, 100)),  # Green
    ColorScheme(bar=(255, 200, 50), bar_glow=(255, 200, 50)),  # Gold
]


if __name__ == "__main__":
    # =====================================================================
    # EXAMPLE 1: Minimal single visualizer (default background + center)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/01_minimal.mp4",
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 2: Solid color background
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/02_color_bg.mp4",
    #     background=ColorBackground(color=(30, 10, 40)),  # dark purple
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 3: Image background — cover fit (no effect)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/03_image_bg_cover.mp4",
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 4: Image background — blur effect (great for readability)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/04_image_bg_blur.mp4",
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="blur",
    #         blur_radius=12.0,
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 5: Image background — grayscale effect
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/05_image_bg_grayscale.mp4",
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="grayscale",
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 6: Image background — sepia effect + lowered opacity
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/06_image_bg_sepia.mp4",
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="sepia",
    #         opacity=0.5,
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single()

    # =====================================================================
    # EXAMPLE 7: Position — top-left corner
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/07_position_topleft.mp4",
    # )
    # viz.render_single(position="top-left")

    # =====================================================================
    # EXAMPLE 8: Position — bottom-right corner
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/08_position_bottomright.mp4",
    # )
    # viz.render_single(position="bottom-right")

    # =====================================================================
    # EXAMPLE 9: Position — custom pixel coordinates
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/09_position_custom.mp4",
    # )
    # viz.render_single(position=(300, 800))

    # =====================================================================
    # EXAMPLE 10: Text overlay — static title
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/10_text_title.mp4",
    #     colors=single_colors,
    # )
    # viz.render_single(
    #     overlays=[
    #         TextOverlay(
    #             text="My Awesome Track",
    #             position=(540, 80),
    #             color=(255, 255, 255),
    #             font_size=60,
    #             anchor="mm",
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 11: Timed text — lyrics / captions
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/11_timed_lyrics.mp4",
    #     colors=single_colors,
    # )
    # viz.render_single(
    #     overlays=[
    #         TextOverlay(text="Song Title", position=(540, 80), font_size=55, anchor="mm"),
    #         TimedText(0.0, 3.5, "First line of lyrics", (540, 980), font_size=38, anchor="mm"),
    #         TimedText(4.0, 7.5, "Second line appears",  (540, 980), font_size=38, anchor="mm"),
    #         TimedText(8.0, 11.5, "Third line of song",  (540, 980), font_size=38, anchor="mm"),
    #         TimedText(12.0, 15.5, "Fourth line goes on", (540, 980), font_size=38, anchor="mm"),
    #         TimedText(16.0, 20.0, "Final line...",       (540, 980), font_size=38, anchor="mm"),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 12: Image overlay — static logo (no time limit)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/12_image_overlay_static.mp4",
    # )
    # viz.render_single(
    #     overlays=[
    #         ImageOverlay(
    #             image_path="assets/logo.png",
    #             position=(100, 100),
    #             size=(120, 120),
    #             anchor="mm",
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 13: Image overlay — timed badge (appears only 2s-6s)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/13_image_overlay_timed.mp4",
    # )
    # viz.render_single(
    #     overlays=[
    #         ImageOverlay(
    #             image_path="assets/logo.png",
    #             position=(540, 540),
    #             size=(200, 200),
    #             anchor="mm",
    #             start_time=2.0,
    #             end_time=6.0,
    #             opacity=0.9,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 14: Image overlay — corner watermark with opacity
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/14_image_watermark.mp4",
    # )
    # viz.render_single(
    #     overlays=[
    #         ImageOverlay(
    #             image_path="assets/logo.png",
    #             position=(1020, 1020),  # near bottom-right for 1080x1080
    #             size=(80, 80),
    #             anchor="rb",
    #             opacity=0.4,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 15: Video overlay — looping corner animation (no time limit)
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/15_video_overlay_loop.mp4",
    # )
    # viz.render_single(
    #     overlays=[
    #         VideoOverlay(
    #             video_path="assets/loop.mp4",
    #             position=(100, 980),
    #             size=(200, 200),
    #             anchor="mm",
    #             loop=True,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 16: Video overlay — timed, no loop
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/16_video_overlay_timed.mp4",
    # )
    # viz.render_single(
    #     overlays=[
    #         VideoOverlay(
    #             video_path="assets/loop.mp4",
    #             position=(540, 540),
    #             size=(400, 400),
    #             anchor="mm",
    #             start_time=1.0,
    #             end_time=6.0,
    #             loop=False,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 17: Mixed overlays — text + image + video + background
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/17_mixed_overlays.mp4",
    #     circle_radius=160,
    #     bar_count=72,
    #     colors=single_colors,
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="blur",
    #         blur_radius=10.0,
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single(
    #     position="center",
    #     overlays=[
    #         TextOverlay("Mixed Overlay Demo", (540, 60), font_size=50, anchor="mm"),
    #         ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
    #         TimedText(
    #             2.0, 5.0, "Now playing...", (540, 1000), font_size=36, anchor="mm"
    #         ),
    #         VideoOverlay(
    #             "assets/loop.mp4",
    #             position=(980, 100),
    #             size=(150, 150),
    #             anchor="mm",
    #             loop=True,
    #         ),
    #         ImageOverlay(
    #             "assets/logo.png",
    #             position=(980, 980),
    #             size=(120, 120),
    #             anchor="mm",
    #             start_time=4.0,
    #             end_time=10.0,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 18: Visualizer on the left, text & media on the right layout
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/18_left_visualizer.mp4",
    #     circle_radius=200,
    #     bar_count=80,
    #     colors=single_colors,
    #     background=ColorBackground((10, 10, 20)),
    # )
    # viz.render_single(
    #     position=(300, 540),  # left of center
    #     overlays=[
    #         TextOverlay("Artist Name", (800, 300), font_size=50, anchor="mm"),
    #         TextOverlay("Track Title", (800, 380), font_size=36, anchor="mm"),
    #         ImageOverlay("assets/logo.png", (800, 600), size=(200, 200), anchor="mm"),
    #         TimedText(1.0, 4.0, "Intro", (800, 800), font_size=30, anchor="mm"),
    #         TimedText(4.5, 8.0, "Verse 1", (800, 800), font_size=30, anchor="mm"),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 19: Quad same — now using render_multi
    # =====================================================================
    # qv = CircularVisualizer("assets/photo.jpg", circle_radius=180, bar_count=80, colors=single_colors)
    # video = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     output_path="output/19_quad_same_bg.mp4",
    #     visualizers=[qv],
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="blur",
    #         blur_radius=8.0,
    #         fit_mode="cover",
    #     ),
    # )
    # video.render_multi(
    #     configs=[
    #         (qv, (540, 540), 0),
    #         (qv, (1620, 540), np.pi / 2),
    #         (qv, (540, 1620), np.pi),
    #         (qv, (1620, 1620), -np.pi / 2),
    #     ],
    #     width=2160,
    #     height=2160,
    #     overlays=[
    #         TextOverlay("Quad Same via render_multi", (1080, 60), font_size=50, anchor="mm"),
    #         ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
    #         VideoOverlay(
    #             "assets/loop.mp4", (2000, 2000), size=(200, 200), anchor="mm", loop=True
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 20: Quad different colors — now using render_multi
    # =====================================================================
    # v1 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[0])
    # v2 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[1])
    # v3 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[2])
    # v4 = CircularVisualizer("assets/photo.jpg", 180, 80, 250, colors=quad_colors[3])
    # video = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     output_path="output/20_quad_diff_colors.mp4",
    #     visualizers=[v1, v2, v3, v4],
    #     background=ColorBackground((15, 15, 30)),
    # )
    # video.render_multi(
    #     configs=[
    #         (v1, (540, 540), 0),
    #         (v2, (1620, 540), np.pi / 3),
    #         (v3, (540, 1620), np.pi),
    #         (v4, (1620, 1620), -np.pi / 3),
    #     ],
    #     width=2160,
    #     height=2160,
    #     overlays=[
    #         TextOverlay("Multi-Color Quad via render_multi", (1080, 60), font_size=50, anchor="mm"),
    #         ImageOverlay(
    #             "assets/logo.png",
    #             position=(1080, 2050),
    #             size=(150, 150),
    #             start_time=2.0,
    #             end_time=8.0,
    #             anchor="mm",
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 21: Repeated bars single color + background image
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/21_repeat_single.mp4",
    #     circle_radius=180,
    #     bar_count=80,
    #     colors=single_colors,
    #     background=ImageBackground("assets/background.jpg", fit_mode="cover"),
    # )
    # viz.render_quad_repeated_bars(
    #     dividers=True,
    #     quadrant_ranges=[
    #         (0, np.pi / 2),
    #         (np.pi / 2, np.pi),
    #         (-np.pi, -np.pi / 2),
    #         (-np.pi / 2, 0),
    #     ],
    #     overlays=[
    #         TextOverlay("Repeated Bars", (540, 60), font_size=50, anchor="mm"),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 22: Repeated bars multi-color + all overlay types
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/22_repeat_multicolor_full.mp4",
    #     circle_radius=180,
    #     bar_count=80,
    #     colors=ColorScheme(bg=(15, 15, 30), circle_border=(150, 150, 200)),
    #     background=ColorBackground((15, 15, 30)),
    # )
    # viz.render_quad_repeated_bars_multi_color(
    #     quarter_colors=quad_colors,
    #     dividers=True,
    #     quadrant_ranges=[
    #         (0, np.pi / 2),
    #         (np.pi / 2, np.pi),
    #         (-np.pi, -np.pi / 2),
    #         (-np.pi / 2, 0),
    #     ],
    #     overlays=[
    #         TextOverlay("Full Feature Demo", (540, 60), font_size=50, anchor="mm"),
    #         TimedText(1.0, 4.0, "Intro...", (540, 1000), font_size=35, anchor="mm"),
    #         ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
    #         VideoOverlay(
    #             "assets/loop.mp4",
    #             position=(980, 100),
    #             size=(120, 120),
    #             anchor="mm",
    #             loop=True,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 23: Everything together — the "power user" demo
    # =====================================================================
    # viz = AudioVisualizerVideo(
    #     audio_path="assets/audio.wav",
    #     image_path="assets/photo.jpg",
    #     output_path="output/23_power_user.mp4",
    #     circle_radius=170,
    #     bar_count=72,
    #     bar_max_length=220,
    #     colors=single_colors,
    #     background=ImageBackground(
    #         "assets/background.jpg",
    #         effect="blur",
    #         blur_radius=15.0,
    #         opacity=0.7,
    #         fit_mode="cover",
    #     ),
    # )
    # viz.render_single(
    #     position=(400, 540),  # slightly left of center
    #     overlays=[
    #         # Static text
    #         TextOverlay("Power User Demo", (800, 200), font_size=48, anchor="mm"),
    #         TextOverlay("feat. VisGen", (800, 260), font_size=28, anchor="mm"),
    #         # Lyrics
    #         TimedText(
    #             0.5, 3.0, "Lights are flashing", (800, 700), font_size=32, anchor="mm"
    #         ),
    #         TimedText(
    #             3.5, 6.5, "Music is blasting", (800, 700), font_size=32, anchor="mm"
    #         ),
    #         TimedText(
    #             7.0, 10.0, "Feel the rhythm", (800, 700), font_size=32, anchor="mm"
    #         ),
    #         # Static image (logo)
    #         ImageOverlay("assets/logo.png", (100, 100), size=(100, 100), anchor="mm"),
    #         # Timed image (badge pops in)
    #         ImageOverlay(
    #             "assets/logo.png",
    #             position=(100, 980),
    #             size=(120, 120),
    #             anchor="mm",
    #             start_time=2.0,
    #             end_time=9.0,
    #         ),
    #         # Looping video in corner
    #         VideoOverlay(
    #             "assets/loop.mp4",
    #             position=(980, 980),
    #             size=(180, 180),
    #             anchor="mm",
    #             loop=True,
    #         ),
    #         # Another timed video overlay
    #         VideoOverlay(
    #             "assets/intro_clip.mp4",
    #             position=(800, 450),
    #             size=(250, 140),
    #             anchor="mm",
    #             start_time=1.0,
    #             end_time=5.0,
    #             loop=False,
    #         ),
    #     ],
    # )

    # =====================================================================
    # EXAMPLE 24: Position showcase — visualizer in every corner
    # =====================================================================
    # positions = ["top-left", "top-right", "bottom-left", "bottom-right", "center"]
    # for pos in positions:
    #     viz = AudioVisualizerVideo(
    #         audio_path="assets/audio.wav",
    #         image_path="assets/photo.jpg",
    #         output_path=f"output/24_position_{pos.replace('-', '_')}.mp4",
    #         background=ColorBackground((20, 20, 35)),
    #     )
    #     viz.render_single(position=pos)

    # =====================================================================
    # EXAMPLE 25: Background effect showcase
    # =====================================================================
    # effects = [
    #     ("none", None),
    #     ("blur", "blur"),
    #     ("grayscale", "grayscale"),
    #     ("sepia", "sepia"),
    # ]
    # for name, effect in effects:
    #     viz = AudioVisualizerVideo(
    #         audio_path="assets/audio.wav",
    #         image_path="assets/photo.jpg",
    #         output_path=f"output/25_bg_{name}.mp4",
    #         background=ImageBackground(
    #             "assets/background.jpg",
    #             effect=effect,
    #             blur_radius=10.0 if effect == "blur" else 5.0,
    #             fit_mode="cover",
    #         ),
    #     )
    #     viz.render_single()

    # =====================================================================
    # EXAMPLE 26: Two visualizers side by side (render_multi)
    # =====================================================================
    left_viz = CircularVisualizer(
        image_path="assets/photo.jpg",
        circle_radius=140,
        bar_count=64,
        colors=ColorScheme(bar=(0, 200, 255), bar_glow=(0, 200, 255)),
    )
    right_viz = CircularVisualizer(
        image_path="assets/scene.jpg",
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

    # =====================================================================
    # EXAMPLE 27: Three visualizers in a row
    # =====================================================================
    viz_a = CircularVisualizer(
        "assets/photo_a.jpg", 100, 48, 150, colors=quad_colors[0]
    )
    viz_b = CircularVisualizer(
        "assets/photo_b.jpg", 100, 48, 150, colors=quad_colors[1]
    )
    viz_c = CircularVisualizer(
        "assets/photo_c.jpg", 100, 48, 150, colors=quad_colors[2]
    )
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

    # =====================================================================
    # EXAMPLE 28: Four visualizers in each corner
    # =====================================================================
    v1 = CircularVisualizer("assets/photo.jpg", 120, 56, 160, colors=quad_colors[0])
    v2 = CircularVisualizer("assets/scene.jpg", 120, 56, 160, colors=quad_colors[1])
    v3 = CircularVisualizer("assets/photo3.jpg", 120, 56, 160, colors=quad_colors[2])
    v4 = CircularVisualizer("assets/photo4.jpg", 120, 56, 160, colors=quad_colors[3])
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

    # =====================================================================
    # EXAMPLE 29: Big + small visualizer combo
    # =====================================================================
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

    # =====================================================================
    # EXAMPLE 30: render_single with a custom visualizer passed inline
    # =====================================================================
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
