import os
import fiona

# Folder with shapefiles
input_folder = r"D:\02 KCA\02 Project 4\Modelling\IlocosSur\SA\Ilocos_Sur_SA_E\#Output\#OQ_ChiouYoungs2014\SHP_Files"

# Scan for shapefiles
shapefiles = [f for f in os.listdir(input_folder) if f.endswith(".shp")]

print(f"\n📁 Found {len(shapefiles)} shapefile(s) in folder: {input_folder}\n")

for filename in shapefiles:
    shapefile_path = os.path.join(input_folder, filename)
    print(f"🔍 Checking: {filename}")

    try:
        with fiona.open(shapefile_path, "r") as src:
            # Basic summary
            print(f"   ✅ Valid shapefile")
            print(f"   📐 Geometry Type : {src.schema['geometry']}")
            print(f"   🔢 Feature Count : {len(src)}")

            # List fields
            print(f"   📋 Fields:")
            for field_name, field_type in src.schema["properties"].items():
                print(f"     - {field_name} ({field_type})")

    except Exception as e:
        print(f"   ❌ Error reading file: {e}")

    print("-" * 50)

print("\n🎯 Quality check complete.")
