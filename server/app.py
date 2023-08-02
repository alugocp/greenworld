import re
import copy
from urllib.parse import unquote_plus
from intervals import DecimalInterval
import sqlalchemy
from flask import (
    Flask,
    render_template,
    request
)
from greenworld.lib import orm
from greenworld.lib import Greenworld
import pages
import api
import lib

app = Flask(
    'Greenworld',
    template_folder = 'server/templates',
    static_folder = 'server/static'
)

# Custom filters
@app.template_filter()
def citation_regex(href):
    return lib.citation_regex(href)

# Initialization method
def main():
    Greenworld()
    db = orm.init_db()

    # Import other server code
    pages.main(app, db)
    api.main(app, db)

    # Run the server
    # TODO this function is not intended for production use, please rewrite before launch
    # https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.run
    app.run(host = '0.0.0.0', port = 2017)

# Main script
if __name__ == '__main__':
    main()
