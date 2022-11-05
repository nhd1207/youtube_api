from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

import urllib.parse as p
import re
import os
import json

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
app = Flask(__name__)
CORS(app)
client = MongoClient(MONGO_URI)

db = client.youtube_db
comments = db.comments

# @app.get("/drop")
# def drop():
#     comments.drop()
#     return("dropped")

@app.post("/url")
def save_youtube_url():
    url = request.json.get("url")
    pattern = '[a-zA-Z0-9:/.?]+'
    id = re.findall(pattern, url)
    comments.insert_one({ "id": id, "url": url, "signal": "start" })
    return("succeed" + url)