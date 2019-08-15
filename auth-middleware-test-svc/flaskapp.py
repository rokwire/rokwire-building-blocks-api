import flask
import auth_middleware

app = flask.Flask(__name__)


################################################
# Call middleware here!
# ⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇
app.before_request(auth_middleware.authenticate)


@app.route('/')
def hello_world():
    return "Hello world!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
