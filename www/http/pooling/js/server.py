#!/usr/bin/env python3

import flask
import json


app = flask.Flask(__name__)
tasks = {}


@app.route('/')
def main():
	return flask.render_template('./client.html')


@app.route('/pool', methods=['POST'])
def pool():
	# uaktualnij taski
	for task_key in tasks.keys():
		tasks[task_key] += 1

	return flask.Response(json.dumps({
			'tasks': tasks
		}), 'text/plain', {
		'Access-Control-Allow-Origin': '*'
	})


@app.route('/add-task', methods=['POST'])
def addTask():
	task_key = flask.request.form['name']
	tasks[task_key] = 0
	return flask.Response('ok', 'text/html', {
		'Access-Control-Allow-Origin': '*'
	})


app.run(debug=True)
