import pymongo
from datetime import datetime, timedelta
from bson import json_util, ObjectId
import json


def connect_database(user: str, password: str, host: str, database: str) -> any:
    client = pymongo.MongoClient(
        f"mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true&w=majority")
    db = client[database]
    return db


def verify_username_password(body) -> bool:
    if 'username' not in body or 'password' not in body:
        return False
    else:
        return True


def create_dict_user(username, password) -> object:
    return {
        "username": username,
        "password": password
    }


def user_exist(username: str, session: any) -> bool:
    user = session['login'].find_one(username)
    if user is not None:
        return False
    else:
        return True


def hash_exist(hash: str, session: any) -> bool:
    hash = session['login'].find_one({"hash": hash})
    if hash is not None:
        return True
    else:
        return False


def create_body_short_url(url_encurtada: str, data_expiracao: int, url_base: str, url_local: str) -> object:
    expirate_date = datetime.now() + timedelta(days=data_expiracao)
    return {
        "hash": url_encurtada,
        "days_for_expirate_date": data_expiracao,
        "base_url": url_base,
        "short_url": url_local + url_encurtada,
        "status": 1,
        "expirate_date": str(expirate_date)
    }


def count_pages(session: any) -> int:
    return session['url'].find().count(True)


def autenticate_user(username: str, password: str, session: any) -> bool:
    user = session['login'].find_one({"username": username, "password": password})
    if user is not None:
        return False
    else:
        return True


def get_all_url(session: any, per_pages: int, count: int) -> list:
    urls = [parse_json(url)
            for url in session['url'].find().skip(per_pages * count).limit(per_pages)]
    return urls


def get_all_url_active(session: any) -> list:
    urls = [parse_json(url)
            for url in session['url'].find({"status": 1})]
    return urls


def parse_json(data):
    return json.loads(json_util.dumps(data))
