from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import rasterio
from rasterio.warp import transform_bounds
from PIL import Image
import uuid
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")


@app.post("/convert-orthomosaic")
async def convert_orthomosaic(file: UploadFile = File(...)):
    tif_path = f"{OUTPUT_DIR}/{uuid.uuid4()}.tif"
    png_path = tif_path.replace(".tif", ".png")

    with open(tif_path, "wb") as f:
        f.write(await file.read())

    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        crs = src.crs

        if crs.to_string() != "EPSG:4326":
            bounds = transform_bounds(
                crs,
                "EPSG:4326",
                bounds.left,
                bounds.bottom,
                bounds.right,
                bounds.top
            )

    with Image.open(tif_path) as img:
        img.save(png_path)

    return {
        "image_url": f"http://localhost:8000/static/{os.path.basename(png_path)}",
        "bounds": [
            [bounds[1], bounds[0]], 
            [bounds[3], bounds[2]]
        ]
    }
