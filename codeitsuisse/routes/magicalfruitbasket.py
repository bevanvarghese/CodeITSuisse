import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/fruitbasket', methods=['POST'])
def bestEstimate():
    data = json.loads(request.data.decode("utf-8"))
    logging.info("data sent for evaluation {}".format(data))
    guesses = {
        "maApple": 50,
        "maOrange": 50,
        "maBanana": 50,
        "maWatermelon": 50,
        "maPineapple": 50,
        "maPomegranate": 50,
        "maAvocado": 50,
        "maRamubutan": 50,
    }
    guess = 0
    for key in data:
        weight = 0
        try:
            weight = guesses[key]
        except:
            print(key)
            weight = 50
        finally:
            guess += data[key]*weight
    print(guess)
    # guess = 400
    logging.info("My result :{}".format(guess))
    return json.dumps(guess)
