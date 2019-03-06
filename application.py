from flask import Flask, jsonify, redirect, url_for, request, render_template
from flask_cors import CORS
import random

application = Flask(__name__)
cors = CORS(application)
partners = ['grimaldi', 'louisa']

@application.route('/', methods=['GET', 'POST'])
def date():

    partner = request.form.get('partner', random.choice(partners))
    emotion = request.form.get('emotion', 'Normal')

    date = {'emotion': emotion,
            'partner': partner
            }
    return render_template('date.html', date=date)


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True) 