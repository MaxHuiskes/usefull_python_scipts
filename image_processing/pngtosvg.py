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

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.png"
    print(f"Converting '{input_file}'...")
    try:
        output_file = convert_png_to_svg(input_file)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

print(f"Done! Saved to {output_file}")
