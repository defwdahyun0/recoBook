from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api.chatbot import ChatbotMessageSender as CM
    
app = Flask(__name__)
# app.config['SQLALCHEMY_CATABASE_URI'] = 'sqlite:///posts.db'
# db = SQLAlchemy(app)

# @app.route('/', methods=['POST', 'GET'])
# def welcome():
    
#     return
    
# def index():
#     return render_template('index.html')

# @app.route('/bookcode')
# def start():
    
#     return render_template('bookcode.html')

if __name__ == '__main__':
    res = CM().req_message_send()
    print(res.status_code)
    if(res.status_code == 200):
        print(res.text)
        # print(res.read().d

    