import services
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get('USER')
PASSWORD = os.environ.get('PASS')
HOST = os.environ.get('HOST')
URL_BASE = os.environ.get('URL_BASE')



session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')

urls = services.get_all_url_active(session)

time_now = datetime.now()

for url in urls:
    if str(time_now) >= url['expirate_date']:
        status = {"$set": {"status": 0}}
        query = {"hash": url['hash']}
        session['url'].update_one(query, status)

