from flask import Flask

app = Flask(__name__)
app.secret_key = '7ae1087a-c86c-470b-9cdb-1253b9a0c4e6'
from app import views