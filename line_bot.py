# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:33:13 2022

@author: admin
"""

line_channel_id = '1657120442'
line_channel_secret = 'b1f08e6874aa051cf7497a23a9998685'
line_token = '3SyceMSn5KrW0F8q9VWGn3Ul4nZujVt8zM93tyeNWDQp2gZ0tsWUIa/ZQHEa9P/\
    nFqq6OS9B1GfsEoRHCW3+sa7YcnVwrM16XJkRrEw6PImMWCwC5crWQWfPzk6SKk5N1Dxuw92t1n+8lSegfluPqQdB04t89/1O/w1cDnyilFU='
    
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random

app = Flask(__name__)

line_bot_api = LineBotApi(line_token)
handler = WebhookHandler(line_channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''
        
        for i in event.message.text:
        
            pretty_text += i
            pretty_text += random.choice(pretty_note)
    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )

if __name__ == "__main__":
    app.run()