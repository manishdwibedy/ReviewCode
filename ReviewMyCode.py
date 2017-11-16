import hashlib
import hmac
import random
import string

import requests
from flask import Flask, render_template, request, redirect, make_response

import DB
import config
from model import user, question, review

app = Flask(__name__)


import pyrebase

config_firebase = {
  "apiKey": "AIzaSyAoskz4tPPIuZXRXkZxvzsQ59xbHssTHv0",
  "authDomain": "review-code-38d2b.firebaseapp.com",
  "databaseURL": "https://review-code-38d2b.firebaseio.com",
  "storageBucket": "",
  # "serviceAccount": "./secret.json"
}


firebase = pyrebase.initialize_app(config_firebase)

# https://review-code-38d2b.firebaseio.com/code?auth=7E1hzaOHPNC8DenDj39n7GMsahQX7uiDG45oRimN
# app.config.from_pyfile('config.cfg')
app_id = config.ACCOUNTKIT_APP_ID
app_secret = config.ACCOUNTKIT_APP_SECRET
client_token = config.ACCOUNTKIT_CLIENT_TOKEN

accountkit_version = 'v1.1'


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/stack_login')
def getStackLogin():
    # https://api.stackexchange.com/2.2/me?order=desc&sort=reputation&site=stackoverflow&access_token=RrgzV*kWSo2MOMzBsW4raA))&key=OjpCuT)4u3QHIUrc2O)iQw((&

    # https://api.stackexchange.com/2.2/me?order=desc&sort=reputation&site=stackoverflow&access_token=SqgClNdfdfVLsm8lIp3edw))&key=OjpCuT)4u3QHIUrc2O)iQw((&
    resp = make_response(redirect('/home'))
    return resp

# @app.route('')
@app.route('/')
def hello_world():
    user_id = request.cookies.get('user_id')
    if user_id:
        return redirect('/home')
    else:
        csrf_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
        return render_template('index.html', app_id=app_id, csrf=csrf_token, accountkit_version=accountkit_version)

@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':
        code = request.form['code']
        csrf = request.form['csrf']

        token_url = 'https://graph.accountkit.com/' + accountkit_version + '/access_token'
        token_params = {'grant_type': 'authorization_code',
                        'code': code,
                        'access_token': 'AA|%s|%s' % (app_id, app_secret)
                        }

        r = requests.get(token_url, params=token_params)
        token_response = r.json()


        user_id = token_response.get('id')
        user_access_token = token_response.get('access_token')
        refresh_interval = token_response.get('token_refresh_interval_sec')

        identity_url = 'https://graph.accountkit.com/' + accountkit_version + '/me'

        appsecret_proof = hmac.new(app_secret, user_access_token, hashlib.sha256)

        identity_params = {'access_token': user_access_token,
                           'appsecret_proof': appsecret_proof.hexdigest()}

        r = requests.get(identity_url, params=identity_params)
        identity_response = r.json()

        phone_number = identity_response.get('phone', {}).get('number', 'N/A')
        email_address = identity_response.get('email', {}).get('address', 'N/A')

        resp = make_response(redirect('/home'))
        resp.set_cookie('user_id', user_id)
        resp.set_cookie('phone_number', phone_number)
        resp.set_cookie('email_address', email_address)
        resp.set_cookie('user_access_token', user_access_token)
        # resp.set_cookie('refresh_interval', refresh_interval)

        return resp
        # return render_template('home.html', user_id=user_id,
        #         phone_number=phone_number,
        #         email_address=email_address,
        #         user_access_token=user_access_token,
        #         refresh_interval=refresh_interval)
    else:
        user_id = request.cookies.get('user_id')

        if user_id and len(user_id) > 0:
            return redirect('/home')
        else:
            return redirect('/')

@app.route('/home')
def home():
    user_id = request.cookies.get('user_id')
    print(user_id)
    if request.args.get("access_token", None) is not None:
        redirect(request.path)
    else:
        questions = db.getQuestions()
        return render_template('home.html', questions = questions)

@app.route('/codes/<question_id>')
def code(question_id):
    if request.args.get("access_token", None) is not None:
        redirect('/')
    else:
        question = db.getQuestion(question_id)

        if len(question) == 1:
            return render_template('codes.html', question=question[0])
        else:
            return render_template('codes.html', question=None)

@app.route('/ask')
def ask():
    return render_template('ask_question.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(''))
    resp.set_cookie('user_id', expires=0)
    resp.set_cookie('phone_number', expires=0)
    resp.set_cookie('email_address', expires=0)
    resp.set_cookie('user_access_token', expires=0)

    return resp




if __name__ == '__main__':
    db = DB.DB()
    # db.addUser(user.User())
    # db.getUsers()

    # resp = db.addQuestion(question.Question())
    # db.getQuestions()

    # db.addReview(review.Review())
    # db.getReviews()

    app.run()
