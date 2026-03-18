import pytest, sys, json
from project import function_1, function_2, function_3

def main():
    test_function_1_valid_args()
    test_function_1_wrong_argument_count()
    test_function_1_invalid_file_format()
    test_function_1_file_not_found()
    test_function_2_valid_csv()
    test_function_2_missing_columns()
    test_function_2_file_not_found()
    test_function_3_point_geometry()
    test_function_3_linestring_geometry()
    test_function_3_polygon_geometry()
    test_function_3_mixed_geometry()

def test_function_1_valid_args(monkeypatch):
    monkeypatch.setattr(sys,"argv",["project.py", "input.csv", "output.geojson"])
    with pytest.raises(SystemExit) as excinfo:
        function_1()
        assert excinfo.type is not SystemExit

def test_function_1_wrong_argument_count(monkeypatch):
    monkeypatch.setattr(sys,"argv",["project.py", "input.csv"])
    with pytest.raises(SystemExit) as e:
        function_1()
    assert str(e.value)=="wrong argument"

def test_function_1_invalid_file_format(monkeypatch):
    monkeypatch.setattr(sys,"argv",["project.py", "input.txt", "output.txt"])
    with pytest.raises(SystemExit) as e:
        function_1()
    assert str(e.value)=="wrong input file"

def test_function_1_file_not_found(monkeypatch):
    monkeypatch.setattr(sys,"argv",["project.py", "nonexistent.csv", "output.geojson"])
    with pytest.raises(SystemExit) as e:
        function_1()
    assert "Input file 'nonexistent.csv' not found" in str(e.value)
def test_function_2_valid_csv(monkeypatch, tmp_path):
    csv_file=tmp_path / "test.csv"
    csv_file.write_text(
        "latitude,longitude,attribute\n10.0,20.0,point\n30.0,40.0,polygon"
    )
    monkeypatch.setattr(sys,"argv",["program.py", str(csv_file),"output.geojson"])
    result=function_2()
    assert result==[{"Latitude": "10.0","Longitude": "20.0","Attribute":"point"},
    {"Latitude": "30.0","Longitude": "40.0","Attribute":"polygon"}]

def test_function_2_missing_columns(monkeypatch, tmp_path):
    csv_file= tmp_path / "test.csv"
    csv_file.write_text("latitude,longitude\n10.0,20.0\n30.0,40.0")
    monkeypatch.setattr(sys,"argv",["program.py", str(csv_file),"output.geojson"])
    with pytest.raises(SystemExit):
        function_2()
def test_function_2_file_not_found(monkeypatch):
    monkeypatch.setattr(sys,"argv",["program.py","nonexistent.csv","output.geojson"])
    with pytest.raises(SystemExit):
        function_2()

def test_function_3_point_geometry(tmp_path, monkeypatch):
    output_file= tmp_path/"output.geojson"
    monkeypatch.setattr(sys, "argv", ["program.py", "input.csv", str(output_file)])
    geodata=[
        {"Latitude": "10.0","Longitude": "20.0","Attribute":"point"},
        {"Latitude": "30.0","Longitude": "40.0","Attribute":"polygon"}
    ]
    function_3(geodata)
    with open(output_file) as f:
        geojson= json.load(f)
    assert geojson["type"]=="FeatureCollection"
    assert len(geojson["features"])==2
    assert geojson["features"][0]["geometry"]["type"]=="Point"

def test_function_3_linestring_geometry(tmp_path, monkeypatch):
    output_file=tmp_path/"output.geojson"
    monkeypatch.setattr(sys, "argv", ["program.py", "input.csv",str(output_file)])
    geodata=[
        {"Latitude": "10.0","Longitude": "20.0","Attribute":"polyline"},
        {"Latitude": "30.0","Longitude": "40.0","Attribute":"polyline"}
    ]
    function_3(geodata)
    with open(output_file) as f:
        geojson= json.load(f)
    assert geojson["type"]=="FeatureCollection"
    assert len(geojson["features"])==1
    assert geojson["features"][0]["geometry"]["type"]=="LineString"

def test_function_3_polygon_geometry(tmp_path, monkeypatch):
    output_file=tmp_path/"output.geojson"
    monkeypatch.setattr(sys, "argv", ["program.py", "input.csv",str(output_file)])
    geodata=[
        {"Latitude": "10.0","Longitude": "20.0","Attribute":"polygon"},
        {"Latitude": "30.0","Longitude": "40.0","Attribute":"polygon"}
    ]
    function_3(geodata)
    with open(output_file) as f:
        geojson= json.load(f)
    assert geojson["type"]=="FeatureCollection"
    assert len(geojson["features"])==1
    assert geojson["features"][0]["geometry"]["type"]=="Polygon"
    assert geojson["features"][0]["geometry"]["coordinates"][0][0]==[20.0,10.0]

def test_function_3_mixed_geometry(tmp_path, monkeypatch):
    output_file=tmp_path/"output.geojson"
    monkeypatch.setattr(sys, "argv", ["program.py", "input.csv",str(output_file)])
    geodata=[
        {"Latitude": "10.0","Longitude": "20.0","Attribute":"point"},
        {"Latitude": "30.0","Longitude": "40.0","Attribute":"polyline"},
        {"Latitude": "35.0","Longitude": "45.0","Attribute":"polygon"},
        {"Latitude": "30.0","Longitude": "40.0","Attribute":"polygon"},
        {"Latitude": "35.0","Longitude": "45.0","Attribute":"polygon"}
    ]
    function_3(geodata)
    with open(output_file) as f:
        geojson= json.load(f)
    assert geojson["type"]=="FeatureCollection"
    assert len(geojson["features"])==3
    assert geojson["features"][0]["geometry"]["type"]=="Point"
    assert geojson["features"][1]["geometry"]["type"]=="LineString"
    assert geojson["features"][2]["geometry"]["type"]=="Polygon"


if __name__=="__main__":
    main()

