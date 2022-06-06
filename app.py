# -*- coding: utf-8 -*-
"""
Created on Tue May 10 15:33:13 2022

@author: admin
"""

api_後台 = "http://192.168.1.203:5566/"

fb_token = 'EAAKpyNnSGZAwBACSGbotTlNSZBi8rPAzf0SWczUwLmxAejZCNn2eg7nyP5iu0xPcW4EglkMafUksQ3FZAyhJhXY0N8Fl4OcvYegpsSl3T7FZC7fCZ'+\
'CRjkOPJbVNZB0ffljhPypQzEdJXULZAMZAGioPHl28Rmh14WoHRZClal7MOYAqmN7KperNwdZAX9B1z2mvInMZD'
            
            
#Python libraries that we need to import for our bot
from flask import Flask, request
from pymessenger.bot import Bot
from datetime import datetime
import requests
import time


app = Flask(__name__)
bot = Bot(fb_token)

def form(value):
    return format(round(value, 4),',.4f')

def search_coin(coin, unit, bot):
    try:
        list_coin = requests.get("%sapi/Cryptocurrency/getPrice?coin=%s" % (api_後台, coin)).json()
        if unit == '':
            if bot == 'tg':
                return '%s\n最新價格: %s元\n市值: %s元\n24小時漲跌幅: %s \n交易量: %s元\n回報時間: %s' \
                    % (coin, ' '*12+form(list_coin['avgPrice']), ' '*20+form(list_coin['marketCap']), \
                       ' '*3+(str(list_coin['change'])+'%'), ' '*16+form(list_coin['volume']), \
                           datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
            elif bot == 'ln':
                return '%s\n最新價格: %s元\n市值: %s元\n日漲跌幅: %s \n交易量: %s元\n回報時間: %s' \
                    % (coin, ' '+form(list_coin['avgPrice']), ' '*9+form(list_coin['marketCap']), ' '+(str(list_coin['change'])+'%'), \
                       ' '*5+form(list_coin['volume']), ' '+datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
            elif bot == 'ms':
                return '%s \n最新價格: \n%s元\n市值: \n%s元\n24小時漲跌幅: %s \n交易量: \n%s元\n回報時間: \n%s' \
                    % (coin, form(list_coin['avgPrice']), form(list_coin['marketCap']), (str(list_coin['change'])+'%'), \
                       form(list_coin['volume']), datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
        else:
            try:
                u = requests.get("%sapi/Cryptocurrency/getPrice?coin=%s" % (api_後台, unit)).json()['avgPrice']
                if bot == 'tg':
                    return '%s (單位為%s)\n(%s=%s元)\n最新價格: %s元\n市值: %s元\n24小時漲跌幅: %s \n交易量: %s元\n回報時間: %s' \
                        % (coin, unit.upper(), unit.upper(), form(u), ' '*12+form(list_coin['avgPrice']/u), \
                           ' '*20+form(list_coin['marketCap']/u), ' '*3+(str(list_coin['change'])+'%'), \
                               ' '*16+form(list_coin['volume']/u), datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
                elif bot == 'ln':
                    return '%s (單位為%s)\n(%s=%s元)\n最新價格: %s元\n市值: %s元\n日漲跌幅: %s \n交易量: %s元\n回報時間: %s' \
                        % (coin, unit.upper(), unit.upper(), form(u), ' '+form(list_coin['avgPrice']/u), \
                           ' '*9+form(list_coin['marketCap']/u), ' '+(str(list_coin['change'])+'%'), \
                           ' '*5+form(list_coin['volume']/u), ' '+datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
                elif bot == 'ms':
                    return '%s (單位為%s)\n(%s=%s元)\n最新價格: \n%s\n市值: \n%s\n24小時漲跌幅: %s \n交易量: \n%s\n回報時間: \n%s' \
                        % (coin, unit.upper(), unit.upper(), form(u), form(list_coin['avgPrice']/u), form(list_coin['marketCap']/u), \
                           (str(list_coin['change'])+'%'), form(list_coin['volume']/u), datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
            except Exception:
                return '抱歉無法辨識該單位幣種，請輸入正確的幣種代號'
    except Exception:
        return '抱歉無法辨識該幣種，請輸入正確的幣種代號'
    
def form_list(value, bot, unit=1, ln=0):
    if bot == 'ms':
        space = 31- len(value['fromCurrency'])*2- len(format(round(value['amount']/unit ,4),'.4f'))*2- ln
        amount = ' '*space + format(round(value['amount']/unit ,4),',.4f')
        return amount
    else:
        space = 39- len(value['fromCurrency'])*2- len(format(round(value['amount']/unit ,4),'.4f'))*2 -ln
        amount = ' '*space + format(round(value['amount']/unit ,4),',.4f')
        return amount
    

def search_coin_list(unit, bot):
    list_5 = requests.get("%sapi/Cryptocurrency/getPriceList" % api_後台).json()
    search_coin1 = list_5[0]['fromCurrency']
    search_coin2 = list_5[1]['fromCurrency']
    search_coin3 = list_5[2]['fromCurrency']
    search_coin4 = list_5[3]['fromCurrency']
    search_coin5 = list_5[4]['fromCurrency']
    if unit=='TWD':
        return '以下為五種最大幣種的即時報價 (新台幣):\n%s: %s元\n%s: %s元\n%s: %s元\n%s: %s元\n%s: %s元\n回報時間:\n%s\n點選按鈕獲取更多資訊' \
            % (search_coin1, form_list(list_5[0], bot), search_coin2, form_list(list_5[1], bot), \
               search_coin3, form_list(list_5[2], bot, ln=1), search_coin4, form_list(list_5[3], bot), \
               search_coin5, form_list(list_5[4], bot), datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
    else:
        try:
            time.sleep(2)
            u = requests.get("%sapi/Cryptocurrency/getPrice?coin=%s" % (api_後台, unit)).json()['avgPrice']
            return '以下為五種最大幣種的即時報價 (%s):\n(%s=%s元)\n%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s\n回報時間:\n%s\n點選按鈕獲取更多資訊' \
                % (unit.upper(), unit.upper(), form(u), search_coin1, form_list(list_5[0], bot, u), \
                   search_coin2, form_list(list_5[1], bot, u), search_coin3, form_list(list_5[2], bot, u, 1), \
                   search_coin4, form_list(list_5[3], bot, u), search_coin5, form_list(list_5[4], bot, u), \
                       datetime.now().strftime("%Y/%m/%d, %H:%M:%S"))
        except Exception:
            return '抱歉無法辨識該單位幣種，請輸入正確的幣種代號'
        


#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    try:
                        msg = message['message'].get('text')
                        response_sent_text = search_coin_list(msg, 'ms')
                        send_message(recipient_id, response_sent_text)
                    except Exception:
                        send_message(recipient_id, '抱歉無法辨識該幣種，請輸入正確的幣種代號')
                    
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = '123'
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == fb_token:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()

