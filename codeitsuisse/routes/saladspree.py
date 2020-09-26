import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def findMinimumPrice():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    numOfSalads = data.get("number_of_salads")
    streetMap = data.get("salad_prices_street_map")

    minPrice = -1
    for street in streetMap:
        for i in range(len(street)-numOfSalads+1):
            streakPrice = 0
            for j in range(i, i+numOfSalads):
                if street[j] != "X":
                    streakPrice += int(street[j])
                else:
                    streakPrice = 0
                    break
            if streakPrice != 0:
                if minPrice == -1 or minPrice > streakPrice:
                    minPrice = streakPrice
    if minPrice == -1:
        result = 0
    else:
        result = minPrice

    logging.info("My result :{}".format(result))
    return json.dumps(result)
