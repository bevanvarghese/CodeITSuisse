import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/intelligent-farming', methods=['POST'])
def farm():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    inputList = data.get("list")
    results = []
    for i in range(len(inputList)):
        inputSeq = inputList[i].get("geneSequence")
        code = {"A": 0, "G": 0, "C": 0, "T": 0}
        for i in range(len(inputSeq)):
            code[inputSeq[i]] += 1
        output = ""
        # place even C's first
        if code['C'] % 2 == 0:
            for i in range(code['C']):
                output += "C"
        else:
            for i in range(code['C']-1):
                output += 'C'
        # place ACGTs if possible
        ACGTpresent = True
        count = code['A']
        for key, value in code.items():
            if value == 0:
                ACGTpresent = False
                count = 0
            else:
                if value < count:
                    count = value
        if ACGTpresent:
            output += (count*"ACGT")
            for key, value in code.items():
                code[key] -= count
        others = code['G']+code['C']+code['T']
        while others > 0 and code['A'] >= 2:
            output += 'AA'
            code['A'] -= 2
            for key, value in code.items():
                if key == 'A':
                    continue
                if value > 0:
                    output += key
                    code[key] -= 1
                    others -= 1
                    break
        for key, value in code.items():
            if value > 0:
                output += value*key
                code[key] = 0
        inputList[i]["geneSequence"] = output
    data["list"] = inputList
    logging.info("My result :{}".format(data))
    return jsonify(data)
