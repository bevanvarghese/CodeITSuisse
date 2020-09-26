import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def bestEstimate():
    data = request.get_json()
    numApples = data.get("maApple")
    numWatermelons = data.get("maWatermelon")
    numBananas = data.get("maBanana")

    applePrice = 10
    watermelonPrice = 20
    bananaPrice = 30
    output = applePrice*numApples + watermelonPrice * \
        numWatermelons + bananaPrice*numBananas
    return output
