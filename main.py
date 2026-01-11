from scripts.gdal_convert import tif_to_png   

def main():
    tif_file = "static/odm_orthophoto.tif"

    try:
        png_file = tif_to_png(tif_file)
        print("✅ Conversión exitosa")
        print("📸 Archivo generado:", png_file)

    except Exception as e:
        print("❌ Error en la conversión")
        print(e)

if __name__ == "__main__":
    main()
