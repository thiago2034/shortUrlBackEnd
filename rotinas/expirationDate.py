import services
import os
from datetime import  datetime

USERNAME = os.environ.get('USER')
PASSWORD = os.environ.get('PASS')
HOST = os.environ.get('HOST')
URL_BASE = os.environ.get('URL_BASE')


session = services.connect_database(USERNAME, PASSWORD, HOST, 'login')

urls = services.get_all_url_active(session, URL_BASE)

time_now = datetime.now()

for url in urls:
    if time_now >= url['expiration_date']:
        url['status'] = 0
        session['url'].update_many(url)

