from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

import re
import os
import pickle

load_dotenv()
app = Flask(__name__)
MONGO_URI = os.getenv("MONGO_URI")
cors = CORS(app, origins=["https://is402.ndxcode.tk", "localhost:3000"])
client = MongoClient(MONGO_URI)

db = client.Youtube
results = db.results

@app.get("/result")
def result():
    url = request.args.get("url")
    response = {
        "success": True,
        "data": []
    }
    for document in results.find({ "youtube_url": url }):
        comment = document["content"]
        label_id = document["label_id"]
        response["data"].append({ "comment": comment, "label_id": label_id})

    if len(response["data"]) == 0: return {"success": False, "message": "data not found"}, 200
    return response