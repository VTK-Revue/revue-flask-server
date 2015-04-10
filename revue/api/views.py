from revue.api import api

@api.route("/")
def hello():
    return "42"
