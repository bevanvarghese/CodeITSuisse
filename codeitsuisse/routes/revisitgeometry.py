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
def findIntersections():
    data = request.get_json()
    shapes = data.get("shapeCoordinates")
    lines = data.get("lineCoordinates")
    print()
    # inputLine = []
    # point0 = lines[0]
    # point1 = lines[1]
    # [
    #     [point0['x'], point0['y'], ]
    #     [point1['x'], point1['y'], ]
    # ]
    inputLine = []
    for point in lines:
        inputLine.append([
            point['x'], point['y']
        ])
    shapeLines = []
    # for i in range(len(shapes)):
    #     if i == len(shapes)-1:
    #         shapeLines.append([
    #             [shapes[i]['x'], shapes[i]['y'], ]
    #             [shapes[0]['x'], shapes[0]['y'], ]
    #         ])
    #     else:
    #         shapeLines.append([
    #             [shapes[i]['x'], shapes[i]['y'], ]
    #             [shapes[i+1]['x'], shapes[i+1]['y'], ]
    #         ])
    shapeList = []
    for point in shapes:
        shapeList.append([
            point['x'], point['y']
        ])
    for i in range(len(shapeList)):
        if i == len(shapeList)-1:
            shapeLines.append([
                [shapeList[i][0], shapeList[i][1], ]
                [shapeList[0][0], shapeList[0][1], ]
            ])
        else:
            shapeLines.append([
                [shapeList[i][0], shapeList[i][1], ]
                [shapeList[int(i+1)][0], shapeList[int(i+1)][1], ]
            ])

    intersections = []
    for shapeLine in shapeLines:
        intersect(inputLine, shapeLine, intersections)
    return json.dumps(intersections)
