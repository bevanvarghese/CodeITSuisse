import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def bestSubset(x, y):
    if x is None and y is None:
        return None
    elif x is not None and y is None:
        return x
    elif y is not None and x is None:
        return y
    elif len(x) > len(y):
        return x
    elif len(y) > len(x):
        return y
    else:
        if sum(x) > sum(y):
            return x
        else:
            return y


def longestSubset(A,  target, presentSum=0, index=0, answerSet={}):
    # case 1: the target has been achieved
    if presentSum == target:
        answer = []
        for i in range(len(answerSet)):
            if answerSet[i] == 1:
                answer.append(A[i])
        return answer
    elif presentSum > target:
        return None

    # case 2: the target hasn't been achieved and the index is out of bounds
    elif index == len(A):
        return None

    # case 3: the target hasn't been achieved but more indices are left
    else:
        tempSum = presentSum
        a1 = None
        if presentSum+A[index] <= target:
            answerSet[index] = 1
            presentSum += A[index]
            a1 = longestSubset(A, target, presentSum, index+1,  answerSet)
        presentSum = tempSum
        answerSet[index] = 0
        a2 = longestSubset(A, target, presentSum, index+1,  answerSet)
        if a2 is None:
            a2 = []
            for i in range(len(answerSet)):
                if answerSet[i] == 1:
                    a2.append(A[i])
        answer = bestSubset(a1, a2)
        return answer


@app.route('/olympiad-of-babylon', methods=['POST'])
def findBooks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    numBooks = data.get("numberOfBooks")
    numDays = data.get("numberOfDays")
    bookList = data.get("books")
    dayList = data.get("days")
    optimalBooks = 0
    for day in dayList:
        used = longestSubset(bookList,  day, presentSum=0,
                             index=0, answerSet={})
        if used is not None:
            #print("Day", day, " had", used)
            optimalBooks += len(used)
            for book in used:
                bookList.remove(book)
        # print(bookList)
        # else: print("None on", day)
    result = {
        "optimalNumberOfBooks": optimalBooks
    }
    logging.info("My result :{}".format(result))
    return json.dumps(result)
