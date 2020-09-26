import logging
import json
from difflib import SequenceMatcher, get_close_matches, Differ
import itertools

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def get_close_matches_icase(word, possibilities, *args, **kwargs):
    """ Case-insensitive version of difflib.get_close_matches """
    lword = word.lower()
    lpos = {}
    for p in possibilities:
        if p.lower() not in lpos:
            lpos[p.lower()] = [p]
        else:
            lpos[p.lower()].append(p)
    lmatches = get_close_matches(lword, lpos.keys(), *args, **kwargs)
    ret = [lpos[m] for m in lmatches]
    ret = itertools.chain.from_iterable(ret)
    return set(ret)


def fixCapitals(diff):
    for i in range(len(diff)):
        if i == 0:
            diff[i] = diff[i].upper()
        elif diff[i-1] == '   ':
            diff[i] = diff[i].upper()
    return diff


def fixSubstitutions(diff):
    for i in range(len(diff)-1):
        if diff[i][0:1] == '+':
            if i != 0:
                if diff[i+1][0:1] == '-':
                    diff.pop(i+1)
                    diff[i] = diff[i][1:3]
    return diff


def countOperations(diff):
    ops = 0
    for i in range(len(diff)):
        if diff[i][0:1] == '+':
            if i != len(diff)-1:
                if diff[i+1][0:1] == '-':
                    ops += 2
                    i += 1
                else:
                    ops += 1
            else:
                ops += 1
        elif diff[i][0:1] == '-':
            if diff[i][0:1] == '-':
                ops += 1
    return ops


def buildStringFromList(diff):
    string = ""
    for i in range(len(diff)):
        if diff[i] == '   ':
            string += ' '
        elif diff[i][0:1] == '+' or diff[i][0:1] == '-':
            string += diff[i][0:1]
        string += diff[i][-1]
    return string


@app.route('/inventory-management', methods=['POST'])
def inventory():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    items = []
    searched = []
    results = []
    for i in range(len(data)):
        items.append(data[i].get("items"))
        searched.append(data[i].get("searchItemName"))
    for x in range(len(items)):
        matches = get_close_matches_icase(searched[x], items[x], n=10)
        tempMatches = []
        for i in matches:
            tempMatches.append(i)
        tempSearched = searched[x].lower()
        dif = Differ()
        differences = []
        operations = {}
        for item in tempMatches:
            str = buildStringFromList(fixSubstitutions(fixCapitals(
                list(dif.compare(tempSearched, item.lower())))))
            operations[str] = countOperations(
                list(dif.compare(tempSearched, item.lower())))
            # differences.append(str)
        processedOperations = sorted(
            operations.items(), key=lambda x: (x[1], x[0]), reverse=False)
        for po in processedOperations:
            differences.append(po[1])
        res = {}
        res["searchItemName"] = data[0].get("searchItemName")
        res["searchResult"] = differences
        results.append(res)
    logging.info("My result :{}".format(results))
    return json.dumps(results)
