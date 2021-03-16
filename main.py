from flask import Flask, request, jsonify
from redis import Redis
import json


app = Flask(__name__)
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/delete', methods=['POST'])
def delete_anchor():
    sensorID = request.form["AnchorID"]
    r.delete(sensorID)
    return 'Deleted anchor/sensor pair: "%s"' % sensorID
    
@app.route('/get_all')
def get_anchors():
    keys = r.scan()[1]
    vals = r.mget(keys)
    return dict(zip(keys, vals))

@app.route('/get', methods=['GET','POST'])
def get_anchor():
    return r.get(request.form["AnchorID"])

@app.route('/set', methods=['POST'])
def set_anchor():
    anchorID = request.form["AnchorID"]
    sensorID = request.form["SensorID"]
    r.set(anchorID, sensorID)
    return 'Created anchor/sensor pair: {%s: %s}' % (anchorID, sensorID)

