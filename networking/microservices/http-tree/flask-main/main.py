from flask import Flask, render_template
import requests


app = Flask(__name__)


@app.route('/')
def index():
    responses = {}
    for i in range(1, 4):
        responses[f'flask{i}'] = requests.get(f'http://localhost:500{i}').content
    return render_template('index.html', resp=responses)


if __name__ == '__main__':
    app.run(debug=True, port=5004)
