from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

from views import *

CORS(app)

if __name__ == '__main__':
    app.run()
