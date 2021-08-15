import json
import hashlib
import uuid
import math

import services

import os
from app import app
from flask import request, redirect

USERNAME = os.environ.get('USER')
PASSWORD = os.environ.get('PASS')
HOST = os.environ.get('HOST')
URL_BASE = os.environ.get('URL_BASE')


@app.route('/<string:encurtada>', methods=['GET'])
def redirect_url(encurtada):
    if encurtada is None:
        return json.dumps({'mensagem': "Insira a url encurtada"}), 400

    session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')

    try:
        url = session['url'].find_one({"$and": [{"hash": encurtada}, {"status": 1}]})
        if url is None:
            return json.dumps({"mensagem": "Url nao encontrada"}), 404
        else:
            return redirect(url['base_url'])
    except:
        return json.dumps({"mensagem": "Erro interno"}), 500


@app.route('/url', methods=['POST'])
def short_url():
    body = request.get_json()

    session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')

    if 'url' in body:
        url = body['url']
    else:
        return json.dumps({"mensagem": "Insira a url no body"}), 400

    if 'shortUrl' in body:
        if not services.hash_exist(body['shortUrl'], session):
            url_encurtada = body['shortUrl']
        else:
            return json.dumps({"mensagem": "Essa url já está sendo utilizada"}), 400
    else:
        unique_id = uuid.uuid4()
        h = hashlib.blake2b(digest_size=5)
        h.update(str(unique_id).encode())
        url_encurtada = h.hexdigest()

    if 'expirateDate' in body:
        data_expiracao = body['expirateDate']
    else:
        data_expiracao = 7

    session['url'].insert_one(
            services.create_body_short_url(url_encurtada, data_expiracao, url, URL_BASE)
        )

    return json.dumps({"data": URL_BASE + url_encurtada})


@app.route('/url/<int:pages>', methods=['GET'])
def getAllUrl(pages: int = 1):
    per_page = 10
    count = pages - 1
    session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')
    count_pages = services.count_pages(session)

    return json.dumps({
                       "pages": pages,
                       "count_pages": math.ceil(count_pages/10),
                       "data": services.get_all_url(session, per_page, count)
                       })


@app.route('/login', methods=['POST'])
def create_user():
    body = request.get_json()

    if not services.verify_username_password(body):
        return json.dumps({'mensagem': 'Por favor insira o username e o password'}), 400

    username = body['username']
    password = body['password']

    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
    password = password_hash.hex()

    session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')
    try:
        if services.user_exist(username, session):
            session['login'].insert_one(
                services.create_dict_user(username, password)
            )
        else:
            return json.dumps({"mensagem": "Usuario já existe"}), 400

    except:
        return json.dumps({"mensagem": "erro na criação do usuario"}), 500

    return json.dumps({'mensagem': 'usuario criado com sucesso'})


@app.route('/login/autenticate', methods=['POST'])
def validate_user():
    body = request.get_json()

    if not services.verify_username_password(body):
        return json.dumps({'mensagem': 'Por favor insira o username e o password'}), 400

    username = body['username']
    password = body['password']

    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
    password = password_hash.hex()

    session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')

    try:
        if not services.autenticate_user(username, password, session):
            return json.dumps({'mensagem': 'usuario autenticado'}), 200
        else:
            return json.dumps({"mensagem": "Usuario ou senha incorreta"}), 400
    except:
        return json.dumps({"mensagem": "erro na autenticacao do usuario"}), 500
