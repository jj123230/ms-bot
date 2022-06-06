
line_channel_secret = 'b1f08e6874aa051cf7497a23a9998685'
line_token = '3SyceMSn5KrW0F8q9VWGn3Ul4nZujVt8zM93tyeNWDQp2gZ0tsWUIa/ZQHEa9P/nFqq6OS9B1GfsEoRHCW3+sa7Y'+\
    'cnVwrM16XJkRrEw6PImMWCwC5crWQWfPzk6SKk5N1Dxuw92t1n+8lSegfluPqQdB04t89/1O/w1cDnyilFU='

from datetime import datetime

from flask import Flask, abort, request

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(line_token)
handler = WebhookHandler(line_channel_secret)


@app.route("/", methods=["POST"])
def callback():
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)

