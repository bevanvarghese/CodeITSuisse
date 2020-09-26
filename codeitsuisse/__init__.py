from flask import Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
import codeitsuisse.routes.saladspree
import codeitsuisse.routes.magicalfruitbasket
import codeitsuisse.routes.revisitgeometry
import codeitsuisse.routes.clusters
import codeitsuisse.routes.intelligentfarming
import codeitsuisse.routes.socialdistance
import codeitsuisse.routes.optimizedportfolio
import codeitsuisse.routes.cleanfloor
import codeitsuisse.routes.olympiad
import codeitsuisse.routes.yinyang
import codeitsuisse.routes.inventory