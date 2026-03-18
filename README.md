# GeoJSON Builder with CSV
#### Video Demo:  [CSV to GeoJSON/youtube](https://youtu.be/ZnZ2uGAWjEw?si=3T3ovqKYPC9ZGijX)
#### Description:
This project is a **GeoJSON Builder** that converts data from a CSV file into GeoJSON format. It facilitates the creation of spatial data representations for GIS applications with an efficient and accurate process.

---

## Features
- Converts CSV data to GeoJSON format.
- Supports Point, Polyline (LineString), and Polygon geometries.
- Handles custom properties for each feature.
- Includes error handling for invalid inputs.

---

## Technologies Used
- **Python**: Core programming language.
- **Libraries**:
  - `csv`: Reads and processes CSV files.
  - `json`: Generates GeoJSON format.
  - `os`: Validates file existence.
  - `sys`: Handles command-line arguments.

---

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd project
   ```
---

## TO DO

1. **Prepare Your CSV File**
   - Ensure the CSV contains these headers (case-sensitive):
     - `latitude`: Latitude coordinate.
     - `longitude`: Longitude coordinate.
     - `attribute`: Geometry type (e.g., `point`, `polyline`, `polygon`).
   - Additional columns will be included as properties in the GeoJSON.

2. **Run the Script**
   ```bash
   python project.py <input_file.csv> <output_file.geojson>
   ```

3. **Output**
   - The GeoJSON file will be saved to the specified path.

---

## Example

### Input (CSV)
```csv
latitude,longitude,attribute
23.8103,90.4125,point
24.3636,88.6241,point
23.8105,90.4127,polyline
23.8110,90.4130,polygon
```

### Output (GeoJSON)
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [90.4125, 23.8103]
      },
      "properties": {
        "type": "Point",
        "attribute": "point"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [88.6241, 24.3636]
      },
      "properties": {
        "type": "Point",
        "attribute": "point"
      }
    }
  ]
}
```

---

## Testing

A test file, `test_project.py`, ensures the correctness of the functionality:
- Verifies the input file format and required headers (`latitude`, `longitude`, `attribute`).
- Checks if the GeoJSON output is generated correctly.
- Validates Point, Polyline, and Polygon geometries.

### Run Tests
```bash
python test_project.py
```

---

## Contribution
Contributions are welcome! Report issues or suggest features via pull requests.

---

## Acknowledgments
- Inspired by GIS and Remote Sensing data requirements.
- Thanks to the Python and open-source community for their tools and libraries.
- I also acknowledge OpenAI for their ChatGPT which helped me a lot to show paths and ideation.
