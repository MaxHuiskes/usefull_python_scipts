import vtracer
import sys
import os

# 1. Get the input filename from the command line, or default to "input.png"
if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = "input.png"

# 2. Check if file exists before crashing
if not os.path.exists(input_file):
    print(f"Error: Could not find '{input_file}'")
    sys.exit(1)

# 3. Create an output filename (e.g., "image.png" -> "image.svg")
filename_without_ext = os.path.splitext(input_file)[0]
output_file = f"{filename_without_ext}.svg"

print(f"Converting '{input_file}' to '{output_file}'...")

# Convert PNG to SVG
vtracer.convert_image_to_svg_py(
    input_file,
    output_file,
    colormode='color',
    hierarchical='cutout',
    mode='spline',
    filter_speckle=4,
    color_precision=6,
    layer_difference=16,
    corner_threshold=60,
    length_threshold=10,
    max_iterations=10,
    splice_threshold=45,
    path_precision=3
)

print(f"Done! Saved to {output_file}")
