import numpy as np
from PIL import Image
from scipy import ndimage

from png_to_stl import png_to_stl

# ===== SETTINGS =====
INPUT_IMAGE = "symbol.png"
OUTPUT_STL = "black_symbol.stl"
TRACE_PNG = "symbol_trace.png"
TRACE_SVG = "symbol.svg"

BLACK_THRESHOLD = 80
THICKNESS_MM = 3
XY_SCALE_MM = 0.2
# ====================

img_array = np.array(Image.open(INPUT_IMAGE).convert("RGB"))

mask = np.all(img_array < BLACK_THRESHOLD, axis=2)
mask = ndimage.binary_fill_holes(mask)
mask = ndimage.binary_opening(mask)
mask = ndimage.binary_closing(mask)
mask = np.flipud(mask)

Image.fromarray((mask * 255).astype(np.uint8)).save(TRACE_PNG)

print(f"Tracing '{TRACE_PNG}' -> '{TRACE_SVG}' -> '{OUTPUT_STL}'...")
mesh, _ = png_to_stl(
    TRACE_PNG,
    OUTPUT_STL,
    svg_path=TRACE_SVG,
    thickness_mm=THICKNESS_MM,
    scale_mm=XY_SCALE_MM,
)

size = mesh.bounds[1] - mesh.bounds[0]
print(f"STL saved: {OUTPUT_STL}")
print("\nDimensions:")
print(f"Width:  {size[0]:.1f} mm")
print(f"Height: {size[1]:.1f} mm")
print(f"Depth:  {size[2]:.1f} mm")
print(f"Triangles: {len(mesh.faces)}")
