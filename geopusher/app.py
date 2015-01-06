import ckanapi
import shapefile
import json

from flask import Flask
app = Flask(__name__)

def convert_file(shapefile_path, outfile_path):
    reader = shapefile.Reader(shapefile_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    geojson = open(outfile_path, "w")
    geojson.write(json.dumps(
                    {"type": "FeatureCollection",
                     "features": buffer
                    },
                  indent=2) + "\n"
                  )
    geojson.close()

@app.route('/')
def process_webhook():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
