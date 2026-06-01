import numpy as np
from PIL import Image
from scipy import ndimage

from png_to_stl import png_to_stl

# ===== SETTINGS =====
INPUT_IMAGE = "logo.png"
OUTPUT_STL = "image1_reverse.stl"
TRACE_PNG = "logo_reverse_trace.png"
TRACE_SVG = "logo_reverse.svg"

WHITE_THRESHOLD = 180
THICKNESS_MM = 3
XY_SCALE_MM = 0.2
# ====================

img_array = np.array(Image.open(INPUT_IMAGE).convert("RGB"))

mask = np.min(img_array, axis=2) >= WHITE_THRESHOLD
mask = ndimage.binary_closing(mask, structure=np.ones((3, 3)))
mask = ndimage.binary_dilation(mask, structure=np.ones((3, 3)), iterations=1)
mask = np.flipud(mask)
mask = ~mask

Image.fromarray((mask * 255).astype(np.uint8)).save(TRACE_PNG)

print(f"Reversed PNG: {TRACE_PNG}")
print(f"Tracing '{TRACE_PNG}' -> '{TRACE_SVG}' -> '{OUTPUT_STL}'...")
mesh, _ = png_to_stl(
    TRACE_PNG,
    OUTPUT_STL,
    svg_path=TRACE_SVG,
    thickness_mm=THICKNESS_MM,
    scale_mm=XY_SCALE_MM,
)

size = mesh.bounds[1] - mesh.bounds[0]
print(f"STL saved as: {OUTPUT_STL}")
print("\nModel size:")
print(f"Width:  {size[0]:.1f} mm")
print(f"Height: {size[1]:.1f} mm")
print(f"Depth:  {size[2]:.1f} mm")
print(f"Triangles: {len(mesh.faces)}")
