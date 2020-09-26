import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def compareStrings(str1, str2):
    diff = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diff += 1
    return diff


@app.route('/contact_trace', methods=['POST'])
def contacts():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    infected = data.get("infected")
    origin = data.get("origin")
    cluster = data.get("cluster")

    specimens = []
    for specimen in cluster:
        specimens.append(specimen)

    result = []
    similarSpecimens = {}
    similarSpecimens[infected["name"]] = []
    diff = compareStrings(infected["genome"], origin["genome"])
    if diff == 2:
        similarSpecimens[infected["name"]].append("*"+origin["name"])
    elif diff == 1:
        similarSpecimens[infected["name"]].append(origin["name"])

    for specimen in specimens:
        diff = compareStrings(infected["genome"], specimen["genome"])
        if diff == 2:
            similarSpecimens[infected["name"]].append("*"+origin["name"])
        elif diff == 1:
            similarSpecimens[infected["name"]].append(origin["name"])
        diff = compareStrings(origin["genome"], specimen["genome"])
        if diff == 2:
            similarSpecimens[origin["name"]].append("*"+origin["name"])
        elif diff == 1:
            similarSpecimens[origin["name"]].append(origin["name"])

    logging.info("My result :{}".format(result))
    return json.dumps(result)
