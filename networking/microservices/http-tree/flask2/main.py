from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'flask2'


if __name__ == '__main__':
    app.run(debug=True, port=5002)
