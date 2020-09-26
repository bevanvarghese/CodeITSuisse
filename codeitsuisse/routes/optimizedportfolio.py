import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def optimalHedgeRatio(coefficient, spotSD, futuresSD):
    ohr = (coefficient * spotSD / futuresSD)
    return ohr


def numOfFuturesContract(ohr, pfValue, futuresPrice, notionalVal):
    NFC = int(round(ohr * pfValue / (futuresPrice*notionalVal), 1))+1
    return NFC


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs")
    output = []
    for x in range(len(inputs)):
        portfolioValue = inputs[x]["Portfolio"]["Value"]
        spotPriceSD = inputs[x]["Portfolio"]["SpotPrcVol"]
        indexList = inputs[x]["IndexFutures"]
        OHRs = {}
        NFCs = {}
        #FPVs = {}
        for i in range(len(indexList)):
            ifName = indexList[i]['Name']
            futuresSD = indexList[i]['FuturePrcVol']
            coefficient = indexList[i]['CoRelationCoefficient']
            futuresPrice = indexList[i]['IndexFuturePrice']
            notionalVal = indexList[i]['Notional']
            #FPVs[ifName] = futuresSD
            OHRs[ifName] = round(optimalHedgeRatio(
                coefficient, spotPriceSD, futuresSD), 3)
            NFCs[ifName] = numOfFuturesContract(optimalHedgeRatio(
                coefficient, spotPriceSD, futuresSD), portfolioValue, futuresPrice, notionalVal)
        clashOfValues = False
        minOHR = 1.1
        for key, value in OHRs.items():
            if value == minOHR:
                clashOfValues = True
            if value < minOHR:
                minOHR = value
                clashOfValues = False
        res = {}
        if not clashOfValues:
            for key, value in OHRs.items():
                if value == minOHR:
                    res['HedgePositionName'] = key
                    res['OptimalHedgeRatio'] = value
                    res['NumFuturesContract'] = NFCs[key]
                    break
        else:
            minNFC = -1
            for key, value in OHRs.items():
                if value == minOHR:
                    if minNFC == -1 or NFCs[key] < minNFC:
                        minNFC = NFCs[key]
            for key, value in NFCs.items():
                if value == minNFC:
                    res['HedgePositionName'] = key
                    res['OptimalHedgeRatio'] = OHRs[key]
                    res['NumFuturesContract'] = value
        output.append(res)
    outputs = {
        "outputs": output
    }
    logging.info("My result :{}".format(outputs))
    return json.dumps(outputs)
