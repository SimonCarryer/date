from flask import Flask, jsonify, redirect, url_for, request, render_template
from flask_cors import CORS
from date.date_env import DateEnv
from date.date_api import get_date_response
import json
import random

application = Flask(__name__)
cors = CORS(application)
partners = ['grimaldi', 'louisa']
actions = ['cars', 'sports', 'literature', 'history', 'machine learning and artificial intelligence', 'flirt', 'drink', 'leave']
def outcome_lookup(outcome):
    if outcome < -1:
        return 'worst'
    elif outcome >= 6:
        return 'best'
    else:
        return 'ok'

@application.route('/date', methods=['GET', 'POST'])
def date():

    partner = request.form.get('partner', random.choice(partners))
    action = request.form.get('action', None)
    counter = int(request.form.get('counter', 0))
    last_state = request.form.get('state_json', None)
    date = {'partner': partner}
    new_state, reward, done = get_date_response(last_state, action)
    if reward < 0 and new_state['previous']['last_action'] != 6:
        date['emotion'] = 'frown'
    elif reward > 0:
        date['emotion'] = 'blush'
    else:
        date['emotion'] = 'normal'
    date['counter'] = counter
    date['actions'] = actions
    date['state_json'] =  json.dumps(new_state)
    if done:
        outcome = outcome_lookup(reward)
        return redirect(f"/done/{outcome}")
    else:
        return render_template('date.html', date=date)

@application.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@application.route('/done/<string:outcome>', methods=['GET', 'POST'])
def done(outcome):
    return render_template('done.html', outcome=outcome)


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True) 