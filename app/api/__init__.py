from flask import Flask, jsonify, Response
from ..models import RideService, Connect
from ..utils import date_to_str
from flask.ext.cors import CORS
import json

app = Flask(__name__)
db = Connect()
CORS(app)

@app.route('/rides/<int:direction>/<geo_filter>', methods=['GET'])
def filter_ride_data(direction, geo_filter):
    geo_filter = geo_filter[1:].replace('_', ' ')
    geo_filter = 'POLYGON(({}))'.format(geo_filter)
    direction = direction

    ride_service = RideService(db)
    ride_service.prepare(direction, geo_filter)

    resp = {
        'type': 'FeatureCollection',
        'features': []
    }

    for r in ride_service.gen_filter_rides():

        gj = json.loads(r[1])
        gj = {
            'type': 'Feature',
            'geometry': gj,
            'properties': {'time': r[0] }
        }

        resp['features'].append(gj)


    return jsonify(resp);


@app.route('/rides/stream/<int:direction>/<geo_filter>', methods=['GET'])
def filter_ride_data_stream(direction, geo_filter):

    geo_filter = geo_filter[1:].replace('_', ' ')
    geo_filter = 'POLYGON(({}))'.format(geo_filter)
    direction = direction
    def gen_ride_data():

            ride_service = RideService(db)
            ride_service.prepare(direction, geo_filter)

            yield '{"type": "FeatureCollection","features": ['

            gen = ride_service.gen_filter_rides()
            r = next(gen)

            if r:

                prev = r
                prev = json.loads(r[1])
                prev = {
                        'type': 'Feature',
                        'geometry': prev,
                        'properties': {'time': date_to_str(r[0]) }
                }

                while r:

                    yield json.dumps(prev) + ', '

                    gj = json.loads(r[1])
                    gj = {
                            'type': 'Feature',
                            'geometry': gj,
                            'properties': {'time': date_to_str(r[0]) }
                    }

                    prev = gj

                    r = next(gen)


                yield json.dumps(prev) + ']}'

            else:

                yield ']}'

    return Response(gen_ride_data(), content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
