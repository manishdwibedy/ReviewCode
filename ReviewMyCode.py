from flask import Flask, render_template, request, redirect
import random
import string
import requests
import hmac
import hashlib
import config
app = Flask(__name__)


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
    return redirect('/success')


@app.route('/')
def hello_world():
    csrf_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    # bottle.response.set_cookie('csrf', csrf_token, secret=cookie_secret)
    # return bottle.template('index',
    #                        app_id=app_id,
    #                        csrf=csrf_token,
    #                        accountkit_version=accountkit_version)
    # return 'Hello World!'
    return render_template('hello.html', app_id = app_id, csrf=csrf_token, accountkit_version = accountkit_version)

@app.route('/success', methods=['POST'])
def success():
    code = request.form['code']
    csrf = request.form['csrf']

    token_url = 'https://graph.accountkit.com/' + accountkit_version + '/access_token'
    token_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'access_token': 'AA|%s|%s' % (app_id, app_secret)
                    }

    r = requests.get(token_url, params=token_params)
    token_response = r.json()

    print repr(token_response)

    user_id = token_response.get('id')
    user_access_token = token_response.get('access_token')
    refresh_interval = token_response.get('token_refresh_interval_sec')

    identity_url = 'https://graph.accountkit.com/' + accountkit_version + '/me'

    appsecret_proof = hmac.new(app_secret, user_access_token, hashlib.sha256)
    # #
    identity_params = {'access_token': user_access_token,
                       'appsecret_proof': appsecret_proof.hexdigest()}

    r = requests.get(identity_url, params=identity_params)
    identity_response = r.json()

    # print repr(identity_response)
    #
    phone_number = identity_response.get('phone', {}).get('number', 'N/A')
    email_address = identity_response.get('email', {}).get('address', 'N/A')

    return render_template('home.html', user_id=user_id,
            phone_number=phone_number,
            email_address=email_address,
            user_access_token=user_access_token,
            refresh_interval=refresh_interval)
if __name__ == '__main__':
    app.run()
