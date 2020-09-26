import logging
import json
import random

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/yin-yang', methods=['POST'])
def yinYangExpected():
    data = json.loads(request.data.decode("utf-8"))
    logging.info("data sent for evaluation {}".format(data))
    numElements = data.get("number_of_elements")
    numOperations = data.get("number_of_operations")
    elements = data.get("elements")
    elementList = []
    elementList[:0] = elements
    elementList
    yinCount = 0
    yangCount = 0
    for i in elementList:
        if i == 'y':
            yinCount += 1
        else:
            yangCount += 1
    expected = 0
    for i in range(1, numOperations+1):
        denominator = 0
        numerator = 0
        for j in range(1, numElements-i+2):
            denominator += 1
            if elementList[j-1] == 'Y' or elementList[-j] == 'Y':
                numerator += 1
        probabilityOfYang = numerator/denominator
        expected += probabilityOfYang
        if probabilityOfYang != 0:
            yangCount -= 1
    output = '{0:.10f}'.format(expected)
    result = {
        "result": output
    }
    logging.info("My result :{}".format(result))
    return json.dumps(result)
