import logging
import json
from flask import request, jsonify


from codeitsuisse import app

logger = logging.getLogger(__name__)


def nCombineR(n, r):

    return (fact(n) / (fact(r)
                       * fact(n - r)))

# Returns factorial of n


def fact(n):

    res = 1

    for i in range(2, n+1):
        res = res * i

    return res


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
