import vtracer

input_file = "input.png"    # Replace with your file name
print(input_file)
output_file = "output.svg"     # The output file name

# Convert PNG to SVG with 3-color optimization
vtracer.convert_image_to_svg_py(
    input_file,
    output_file,
    colormode='color',        # 'color' or 'binary'
    hierarchical='cutout',    # 'stacked' (easier editing) or 'cutout' (cleaner geometry)
    mode='spline',            # 'spline' (smoother) or 'polygon' (straighter lines)
    filter_speckle=4,         # Removes noise (dots smaller than 4px)
    color_precision=6,        # Lower number = fewer colors. Try 6 or 7 for a 3-color image.
    layer_difference=16,      # Higher = merges similar colors
    corner_threshold=60,      # Smoother corners
    length_threshold=10,      # Simplifies small curves
    max_iterations=10,
    splice_threshold=45,
    path_precision=3          # Decimal places in the SVG (saves file size)
)

print(f"Successfully converted {input_file} to {output_file}")
