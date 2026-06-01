import os
import sys

import vtracer

VTRACER_DEFAULTS = {
    "colormode": "color",
    "hierarchical": "cutout",
    "mode": "spline",
    "filter_speckle": 4,
    "color_precision": 6,
    "layer_difference": 16,
    "corner_threshold": 60,
    "length_threshold": 10,
    "max_iterations": 10,
    "splice_threshold": 45,
    "path_precision": 3,
}


def convert_png_to_svg(input_file, output_file=None, **overrides):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Could not find '{input_file}'")

    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.svg"

    settings = {**VTRACER_DEFAULTS, **overrides}
    vtracer.convert_image_to_svg_py(input_file, output_file, **settings)
    return output_file


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.png"
    print(f"Converting '{input_file}'...")
    try:
        output_file = convert_png_to_svg(input_file)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Done! Saved to {output_file}")
