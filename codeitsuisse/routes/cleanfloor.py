import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def dirtChange(dirtLevel):
    if dirtLevel > 0:
        return -1
    return 1


def calculateMoves(floor):
    position = 0
    moveCount = 0
    totalDirt = sum(floor)
    while totalDirt > 0:
        dirt = 0
        # move left
        if position > 0 or position == len(floor)-1 or floor[position-1] > 0:
            position -= 1
            dirt = dirtChange(floor[position])
        # move right
        elif position < len(floor)-1:
            position += 1
            dirt = dirtChange(floor[position])
        floor[position] += dirt
        totalDirt += dirt
        moveCount += 1
    return moveCount


@app.route('/clean_floor', methods=['POST'])
def cleanFloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    res = {}
    for key in tests:
        test = tests[key]
        floor = test["floor"]
        res[key] = calculateMoves(floor)
    output = {
        'answers': res
    }

    logging.info("My result :{}".format(output))
    return json.dumps(output)
