import sys
from pathlib import Path

import trimesh

# pngtosvg.py lives in image_processing/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "image_processing"))
from pngtosvg import convert_png_to_svg


def _to_trimesh(obj):
    if isinstance(obj, list):
        return trimesh.util.concatenate([_to_trimesh(o) for o in obj])
    if hasattr(obj, "to_mesh"):
        return obj.to_mesh()
    return obj


def svg_to_stl(svg_path, stl_path, thickness_mm=3.0, scale_mm=0.2):
    path = trimesh.load_path(svg_path)
    mesh = _to_trimesh(path.extrude(float(thickness_mm)))

    mesh.apply_scale([scale_mm, scale_mm, 1.0])
    mesh.merge_vertices()
    mesh.update_faces(mesh.unique_faces())
    mesh.remove_unreferenced_vertices()
    mesh.export(stl_path)
    return mesh


def png_to_stl(
    png_path,
    stl_path,
    svg_path=None,
    thickness_mm=3.0,
    scale_mm=0.2,
    save_svg=True,
):
    png_path = str(png_path)
    stl_path = str(stl_path)

    if svg_path is None:
        svg_path = str(Path(png_path).with_suffix(".svg"))
    else:
        svg_path = str(svg_path)

    # polygon paths mesh cleaner than spline for STL
    convert_png_to_svg(
        png_path,
        svg_path,
        colormode="binary",
        mode="polygon",
        path_precision=2,
    )

    if not save_svg:
        pass  # svg kept for inspection; set save_svg=False + delete if unwanted

    mesh = svg_to_stl(svg_path, stl_path, thickness_mm, scale_mm)
    return mesh, svg_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python png_to_stl.py <input.svg> [output.stl]")
        sys.exit(1)

    svg_in = sys.argv[1]
    stl_out = sys.argv[2] if len(sys.argv) > 2 else str(Path(svg_in).with_suffix(".stl"))
    mesh = svg_to_stl(svg_in, stl_out)
    size = mesh.bounds[1] - mesh.bounds[0]
    print(f"STL saved: {stl_out}")
    print(f"Width: {size[0]:.1f} mm  Height: {size[1]:.1f} mm  Depth: {size[2]:.1f} mm")
    print(f"Triangles: {len(mesh.faces)}")
