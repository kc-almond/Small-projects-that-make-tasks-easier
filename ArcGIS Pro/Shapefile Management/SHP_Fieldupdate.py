import os
import fiona
import time
from datetime import datetime

# Input/output folders
input_folder = r"D:\Your\Folder\Path"
output_folder = os.path.join(input_folder, "renamed_shapefiles")
os.makedirs(output_folder, exist_ok=True)

# Field renaming rules
field_rename_map = {
    "SA(0.2)": "SA_02",
    "SA_02": "SA_1"
}

# Start processing
print(f"\n🔍 Scanning folder: {input_folder}")
shapefiles = [f for f in os.listdir(input_folder) if f.endswith(".shp")]
print(f"🗂️ Found {len(shapefiles)} shapefile(s) to process.\n")

# Track total time
batch_start = time.time()

for filename in shapefiles:
    start_time = time.time()
    start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    print(f"📄 Processing: {filename}")
    print(f"   🕒 Start time: {start_dt}")
    renamed_fields = []

    with fiona.open(input_path, "r") as src:
        old_schema = src.schema.copy()
        new_properties = {}

        # Build new schema and track renamed fields
        for old_name, field_type in old_schema["properties"].items():
            new_name = field_rename_map.get(old_name, old_name)
            new_properties[new_name] = field_type
            if new_name != old_name:
                renamed_fields.append((old_name, new_name))

        new_schema = {
            "geometry": src.schema["geometry"],
            "properties": new_properties
        }

        with fiona.open(output_path, "w",
                        driver=src.driver,
                        crs=src.crs,
                        schema=new_schema) as dst:
            for feature in src:
                new_props = {}
                for old_name in feature["properties"]:
                    new_name = field_rename_map.get(old_name, old_name)
                    new_props[new_name] = feature["properties"][old_name]

                dst.write({
                    "geometry": feature["geometry"],
                    "properties": new_props
                })

    if renamed_fields:
        for old, new in renamed_fields:
            print(f"   🔄 Renamed field: '{old}' → '{new}'")
    else:
        print("   ⚠️ No matching fields found to rename.")

    end_time = time.time()
    end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elapsed = end_time - start_time
    print(f"   🕒 End time  : {end_dt}")
    print(f"   ⏱️ Elapsed   : {elapsed:.2f} seconds")
    print(f"✅ Finished: {filename}\n")

# Total time
total_elapsed = time.time() - batch_start
print(f"🎉 All shapefiles processed.")
print(f"⏱️ Total processing time: {total_elapsed:.2f} seconds")
print(f"🗂️ Output saved to: {output_folder}")
