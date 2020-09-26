import logging
import json
import math

from flask import request, jsonify
from itertools import combinations

from codeitsuisse import app

logger = logging.getLogger(__name__)


def nCombineR(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


@app.route('/social_distancing', methods=['POST'])
def socialDistance():
    data = request.get_json()
    testInputs = data.get("tests")
    result = []
    output = {"answers": {}}
    for key in testInputs:
        seats = testInputs[key]["seats"]
        people = testInputs[key]["people"]
        spaces = testInputs[key]["spaces"]
        output["answers"][key] = nCombineR(seats-(spaces*(people-1)), people)
    logging.info("My result :{}".format(output))
    return json.dumps(output)
