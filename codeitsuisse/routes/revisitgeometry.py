import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def intersect(line1, line2, intersections=[]):
    if len(intersections) == 2:
        return
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
    if x.is_integer():
        x = int(x)
    else:
        x = round(x, 2)
    if y.is_integer():
        y = int(y)
    else:
        y = round(y, 2)
    intersections.append({"x": x, "y": y})
    return


@app.route('/revisitgeometry', methods=['POST'])
def findIntersections():
    data = request.get_json()
    shapes = data.get("shapeCoordinates")
    lines = data.get("lineCoordinates")

    inputLine = [
        [lines[0].get('x'), lines[0].get('y'), ],
        [lines[1].get('x'), lines[1].get('y'), ],
    ]

    shapeLines = []
    for i in range(len(shapes)):
        if i == len(shapes)-1:
            shapeLines.append([
                [shapes[i].get('x'), shapes[i].get('y'), ],
                [shapes[0].get('x'), shapes[0].get('y'), ],
            ])
        else:
            shapeLines.append([
                [shapes[i].get('x'), shapes[i].get('y'), ],
                [shapes[i+1].get('x'), shapes[i+1].get('y'), ],
            ])

    intersections = []
    for shapeLine in shapeLines:
        intersect(inputLine, shapeLine, intersections)
    return json.dumps(intersections)
