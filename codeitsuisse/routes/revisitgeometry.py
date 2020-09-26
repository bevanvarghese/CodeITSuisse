import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def fixPrecision(i):
    if i.is_integer():
        i = int(i)
    else:
        i = round(i, 2)
    return i


def lineAndLineIntersect(line1, line2):
    #source: stackoverflow
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def determinant(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = determinant(xdiff, ydiff)
    if div == 0:
        return None

    d = (determinant(*line1), determinant(*line2))
    x = determinant(d, xdiff) / div
    y = determinant(d, ydiff) / div
    return (x, y)


def segmentAndLineIntersect(segment, line):
    intersection = lineAndLineIntersect(segment, line)
    if intersection is not None:
        if intersection[0] < min(segment[0][0], segment[1][0]) or intersection[0] > max(segment[0][0], segment[1][0]) or intersection[1] < min(segment[0][1], segment[1][1]) or intersection[1] > max(segment[0][1], segment[1][1]):
            return None
    return intersection


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
        shapeLines.append([
            [shapes[i].get('x'), shapes[i].get('y'), ],
            [shapes[(i+1) % len(shapes)].get('x'), shapes[0].get('y'), ],
        ])

    intersections = []
    for shapeLine in shapeLines:
        result = segmentAndLineIntersect(shapeLine, inputLine)
        if result is not None:
            x = fixPrecision(result[0])
            y = fixPrecision(result[1])
            intersections.append({
                "x": x,
                "y": y
            })
    return json.dumps(intersections)
