import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def intersect(line1, line2, intersections=[]):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def determinant(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = determinant(xdiff, ydiff)
    if div == 0:
        return

    d = (determinant(*line1), determinant(*line2))
    x = determinant(d, xdiff) / div
    y = determinant(d, ydiff) / div
    intersections.append({"x": x, "y": y})


@app.route('/revisitgeometry', methods=['POST'])
def findMinimumPrice():
    data = request.get_json()
    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")
    inputLine = [
        [lineCoordinates[0]["x"], lineCoordinates[0]["y"], ]
        [lineCoordinates[1]["x"], lineCoordinates[1]["y"], ]
    ]
    shapeLines = []
    for i in range(len(shapeCoordinates)):
        if i == len(shapeCoordinates)-1:
            shapeLines.append([
                [shapeCoordinates[i]["x"], shapeCoordinates[i]["y"], ]
                [shapeCoordinates[0]["x"], shapeCoordinates[0]["y"], ]
            ])
        else:
            shapeLines.append([
                [shapeCoordinates[i]["x"], shapeCoordinates[i]["y"], ]
                [shapeCoordinates[i+1]["x"], shapeCoordinates[i+1]["y"], ]
            ])

    intersections = []
    for shapeLine in shapeLines:
        intersect(inputLine, shapeLine, intersections)
    return json.dumps(intersections)
