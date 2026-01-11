import subprocess
from pathlib import Path

GDAL_TRANSLATE = r"C:\Program Files\QGIS 3.44.6\bin\gdal_translate.exe"

def tif_to_png(tif_path: str, output_dir: str = "temp") -> str:
    tif = Path(tif_path)

    if not tif.exists():
        raise FileNotFoundError(f"No existe el archivo: {tif}")
    
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    png = out_dir / tif.with_suffix(".png").name

    cmd = [
        GDAL_TRANSLATE,
        "-of", "PNG",
        str(tif),
        str(png),
    ]

    print("▶ Ejecutando:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    return str(png)
