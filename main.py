from flask import Flask, request, jsonify
from redis import Redis
import json


app = Flask(__name__)
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/delete_anchor', methods=['POST'])
def delete_anchor():
    sensorID = request.form["SensorID"]
    r.delete(sensorID)
    return 'Deleted anchor: "%s"' % sensorID
    
@app.route('/get_anchors')
def get_anchors():
    keys = r.scan()[1]
    vals = r.mget(keys)
    return dict(zip(keys, vals))

@app.route('/get_anchor')
def get_anchor():
    return r.get(request.form["SensorID"])

@app.route('/set_anchor', methods=['POST'])
def set_anchor():
    sensorID = request.form["SensorID"]
    anchorID = request.form["AnchorID"]
    r.set(sensorID, anchorID)
    return 'Created anchor: {%s: %s}' % (sensorID, anchorID)

