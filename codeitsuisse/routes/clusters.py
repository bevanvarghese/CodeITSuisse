import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


def checkNeighbours(row, col, nR, nC, visited, area):
    if area[row][col] == '*' or visited[row][col] == 1:
        return
    visited[row][col] = 1
    # corners
    if (row == 0 and col == 0):
        checkNeighbours(1, 1, nR, nC, visited, area)
        checkNeighbours(1, 0, nR, nC, visited, area)
        checkNeighbours(0, 1, nR, nC, visited, area)
    elif (row == nR-1 and col == nC-1):
        checkNeighbours(row-1, col-1, nR, nC, visited, area)
        checkNeighbours(row-1, col, nR, nC, visited, area)
        checkNeighbours(row, col-1, nR, nC, visited, area)
    elif (row == 0 and col == nC-1):
        checkNeighbours(1, col-1, nR, nC, visited, area)
        checkNeighbours(1, col, nR, nC, visited, area)
        checkNeighbours(0, col-1, nR, nC, visited, area)
    elif (row == nR-1 and col == 0):
        checkNeighbours(row, 1, nR, nC, visited, area)
        checkNeighbours(row-1, 0, nR, nC, visited, area)
        checkNeighbours(row-1, 1, nR, nC, visited, area)

    # edges
    elif row == 0:
        checkNeighbours(row, col-1, nR, nC, visited, area)
        checkNeighbours(row, col+1, nR, nC, visited, area)
        checkNeighbours(row+1, col-1, nR, nC, visited, area)
        checkNeighbours(row+1, col, nR, nC, visited, area)
        checkNeighbours(row+1, col+1, nR, nC, visited, area)
    elif row == nR-1:
        checkNeighbours(row, col-1, nR, nC, visited, area)
        checkNeighbours(row, col+1, nR, nC, visited, area)
        checkNeighbours(row-1, col-1, nR, nC, visited, area)
        checkNeighbours(row-1, col, nR, nC, visited, area)
        checkNeighbours(row-1, col+1, nR, nC, visited, area)
    elif col == 0:
        checkNeighbours(row-1, col, nR, nC, visited, area)
        checkNeighbours(row+1, col, nR, nC, visited, area)
        checkNeighbours(row-1, col+1, nR, nC, visited, area)
        checkNeighbours(row+1, col+1, nR, nC, visited, area)
        checkNeighbours(row, col+1, nR, nC, visited, area)
    elif col == nC-1:
        checkNeighbours(row-1, col, nR, nC, visited, area)
        checkNeighbours(row+1, col, nR, nC, visited, area)
        checkNeighbours(row-1, col-1, nR, nC, visited, area)
        checkNeighbours(row+1, col-1, nR, nC, visited, area)
        checkNeighbours(row, col-1, nR, nC, visited, area)

    # midpieces
    else:
        checkNeighbours(row-1, col-1, nR, nC, visited, area)
        checkNeighbours(row-1, col, nR, nC, visited, area)
        checkNeighbours(row-1, col+1, nR, nC, visited, area)
        checkNeighbours(row, col-1, nR, nC, visited, area)
        checkNeighbours(row, col, nR, nC, visited, area)
        checkNeighbours(row, col+1, nR, nC, visited, area)
        checkNeighbours(row+1, col-1, nR, nC, visited, area)
        checkNeighbours(row+1, col, nR, nC, visited, area)
        checkNeighbours(row+1, col+1, nR, nC, visited, area)


@app.route('/cluster', methods=['POST'])
def findNumOfClusters():
    area = request.get_json()
    logging.info("data sent for evaluation {}".format(area))

    numRows = len(area)
    numCols = len(area[0])
    clusters = 0
    visited = [[0 for i in range(numCols)]for j in range(numRows)]
    for i in range(numRows):
        for j in range(numCols):
            if area[i][j] == "1":
                if visited[i][j] != 1:
                    clusters += 1
                    checkNeighbours(i, j, numRows, numCols, visited, area)
    output = {
        "answer": clusters
    }
    return json.dumps(output)
