from flask import Flask, jsonify, request
import os
from flask_cors import CORS
from bardapi import Bard
import requests
import re

app = Flask(__name__)
CORS(app, origins=["*"])

URL = "https://maps.googleapis.com/maps/api/geocode/json"
API_KEY = os.getenv("google_maps_api_key")
token = os.getenv("token")



@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/getWaterBodies', methods=['POST'])
def waterBodies():
    bard = Bard(token=token)
    body = request.form
    lat = body.getlist("lat")
    lon = body.getlist("lon")
    num = body.getlist("num")
    lat = lat[0]
    lon = lon[0]
    num = num[0]
    ltlg = "{}, {}".format(lat, lon)
    PARAMS = {'latlng':ltlg, 'key':API_KEY}
    res = requests.get(url = URL, params = PARAMS)
    dat = res.json()
    add = dat['results'][0]['formatted_address']
    print(add)
    text = "Return me a list of {} small water bodies like ponds, lakes, and rivers but not oceans along with their address which lie very near to the {} the response should be in plain text  and should follow the 'waterbody':'address'".format(num, add)
    print(text)
    ans = bard.get_answer(text)['content']
    x = ans.split('---\n')
    x[1]
    result = [item.strip() for item in re.split(r'\||\n', x[1])]
    result = result[0:10]
    ls = []
    count = -1
    adrs = []
    for i in result:
        count = count +1
        if(count%2 ==0):
            ls.append(i)
        else:
            adrs.append(i)
    print(adrs)
    latlon = []
    for j in adrs:
        latlon.append(GetLatLong(j))
    print(latlon)
    print(ls)
    response = {}
    for i in range(0, 5):
        response[ls[i]] = latlon[i]
    print(response)
    return jsonify({"response":response})


@app.route('/talk', methods=['POST'])
def bard():
    bard = Bard(token=token)
    result = request.form
    query = result.getlist("query")
    query = query[0]
    print(query)
    reply = bard.get_answer(query)['content']
    return jsonify({"reply":reply})




def GetLatLong(location):

  PARAMS = {'address':location, 'key':API_KEY}

  r = requests.get(url = URL, params = PARAMS)

  data = r.json()

  latitude = data['results'][0]['geometry']['location']['lat']
  longitude = data['results'][0]['geometry']['location']['lng']
  lt = []
  lt.append(latitude)
  lt.append(longitude)
  return lt

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
