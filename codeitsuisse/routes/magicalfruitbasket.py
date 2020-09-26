import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def bestEstimate():
    data = request.get_data()
    dict = json.loads(data)
    logging.info("data sent for evaluation {}".format(data))
    units = list(dict.values())
    guesses = [100, 0, 100]
    output = 0
    for i in range(len(units)):
        output += units[i]*guesses[i]
    logging.info("My result :{}".format(output))
    return str(output)
