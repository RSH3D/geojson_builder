import sys, csv, json, os


def main():
    function_1()
    listeds = function_2()
    function_3(listeds)


# checking the file formats and handling errors.
def function_1():
    try:
        if len(sys.argv) != 3:
            sys.exit("wrong argument")
        before = sys.argv[1]
        after = sys.argv[2]
        if not (before.endswith(".csv")) or not after.endswith(".geojson"):
            sys.exit("wrong input file")
        if not os.path.exists(before):
            sys.exit(f"Input file '{before}' not found")

    except (ValueError, FileNotFoundError, EOFError):
        print("program not executed")


# Reading the csv file and returning as list of dictionaries.
def function_2():
    try:
        before = sys.argv[1]
        geo = []
        with open(before) as file:
            reader = csv.DictReader(file)
            req_col = {"latitude", "longitude", "attribute"}
            if not req_col.issubset(reader.fieldnames):
                sys.exit(f"Error: csv file doesn't have some fields")
            for row in reader:
                geo.append(
                    {
                        "Latitude": row["latitude"],
                        "Longitude": row["longitude"],
                        "Attribute": row["attribute"],
                    }
                )
    except FileNotFoundError:
        sys.exit(f"Input file '{before}' not found")
    except Exception as ex:
        sys.exit(f"An error occured while reading the file: {ex}")
    return geo


# geojson builder
def function_3(geodata):
    m = sys.argv[2]
    geojson = {"type": "FeatureCollection", "features": []}
    points = []
    linestring = []
    polygon = []
    for item in geodata:
        geometry_type = item.get("Attribute", "").strip().lower()
        coordinates = [float(item["Longitude"]), float(item["Latitude"])]
        if geometry_type == "point":
            points.append({"coordinates": coordinates, "properties": item})
        elif geometry_type == "polyline":
            linestring.append(coordinates)
        elif geometry_type == "polygon":
            polygon.append(coordinates)
        else:
            print(f"Unknown geometry type in {item}")
    for point in points:
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": point["coordinates"]},
            "properties": {
                "type": "Point",
                "attribute": point["properties"]["Attribute"],
            },
        }
        geojson["features"].append(feature)

    if linestring:
        feature = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": linestring},
            "properties": {"type": "Polyline"},
        }
        geojson["features"].append(feature)

    if polygon:
        if polygon[0] != polygon[-1]:
            polygon.append(polygon[0])
        feature = {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [polygon]},
            "properties": {"type": "Polygon"},
        }
        geojson["features"].append(feature)

    with open(m, "w") as json_file:
        json.dump(geojson, json_file, indent=4)


if __name__ == "__main__":
    main()
