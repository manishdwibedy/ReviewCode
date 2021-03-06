import hashlib
import hmac
import random
import string
import requests
from flask import Flask, render_template, request, redirect, make_response, jsonify

import DB
# from config import
ACCOUNTKIT_APP_ID='183987662160596'
ACCOUNTKIT_APP_SECRET='95c6ef9a92d2843b8223b6f32d2dac3c'
ACCOUNTKIT_CLIENT_TOKEN='d06a9c41bf33fb45822b518b8c0b0b08'
from model import user, question, review

app = Flask(__name__)

db = DB.DB()

app_id = ACCOUNTKIT_APP_ID
app_secret = ACCOUNTKIT_APP_SECRET
client_token = ACCOUNTKIT_CLIENT_TOKEN

accountkit_version = 'v1.1'


@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/stack_login')
def getStackLogin():
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

        # appsecret_proof = hmac.new(app_secret, user_access_token, hashlib.sha256)

        identity_params = {'access_token': user_access_token,
                           # 'appsecret_proof': appsecret_proof.hexdigest()
                           }

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
        return render_template('home.html', questions = questions, key='OjpCuT)4u3QHIUrc2O)iQw((')

@app.route('/get_stack_info')
def stackInfo():
    stack_token = request.cookies.get('stack_token')
    url = 'https://api.stackexchange.com/2.2/me?order=desc&sort=reputation&site=stackoverflow&key=OjpCuT)4u3QHIUrc2O)iQw((&access_token=' + stack_token
    r = requests.get(url)
    response = r.json()

@app.route('/codes/<question_id>')
def code(question_id):
    if request.args.get("access_token", None) is not None:
        redirect('/')
    else:
        question = db.getQuestion(question_id)
        reviews = db.getReviews(question_id)

        for review in reviews:
            review['review_text'] = review['review_text'].replace('\n', '<br />')
        if len(question) == 1:
            return render_template('codes.html', question=question[0], reviews=reviews, question_id=question_id)
        else:
            return render_template('codes.html', question=None)

@app.route('/ask', methods=['POST', 'GET'])
def ask():
    if request.method == 'POST':
        code = request.form['code']
        title = request.form['title']

        question_asked = question.Question()
        question_asked.language = 'javascript'
        question_asked.question_code = code
        question_asked.question_title = title
        question_asked.author_id = request.cookies.get('user_id')
        question_asked.author_username = request.cookies.get('')
        response = db.addQuestion(question_asked)
        return jsonify(
            acknowledged=response.acknowledged,
        )
    else:
        return render_template('ask_question.html')

@app.route('/submit-review', methods=['POST', 'GET'])
def submitReview():
    if request.method == 'POST' or True:
        review_text = request.form['review']
        question_id = request.form['question-id']

        question_review = review.Review()
        question_review.question_id = question_id
        question_review.user_id = request.cookies.get('user_id')
        question_review.review_text = review_text

        response = db.addReview(question_review)

        return jsonify(
            acknowledged=response.acknowledged,
        )
    else:
        return ''

@app.route('/logout')
def logout():
    resp = make_response(redirect(''))
    resp.set_cookie('user_id', expires=0)
    resp.set_cookie('phone_number', expires=0)
    resp.set_cookie('email_address', expires=0)
    resp.set_cookie('user_access_token', expires=0)
    resp.set_cookie('stack_token', expires=0)
    resp.set_cookie('stack_expires', expires=0)
    return resp




if __name__ == '__main__':
    # db.addUser(user.User())
    # db.getUsers()

    # resp = db.addQuestion(question.Question())
    # db.getQuestions()

    # db.addReview(review.Review())
    # db.getReviews()

    app.run()
