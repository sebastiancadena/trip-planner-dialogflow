import json
import os
import requests

from datetime import timezone
from dateutil.parser import parse
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json';
    return r;
    
def makeResponse(req):
    result = req.get('queryResult')
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = parse(parameters.get('date')).replace(tzinfo=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=06f070197b1f60e55231f8c46658d077')
    json_object = r.json()
    weather = json_object['list']
    for i in range(0, len(weather)):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break
    speech = 'The forecast for '+city+ ' for '+date+ ' is ' + condition
    return {
        "fulfillmentText": speech,
        "source": "dialogflow-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Starting app on port %d' % port)
    app.run(debug=False, port = port, host="0.0.0.0")
