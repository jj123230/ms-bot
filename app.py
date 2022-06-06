
line_channel_id = '1657120442'

api_後台 = "http://192.168.1.203:5566/"
api_FAQ = "http://192.168.1.204:9982/"

save_api = 'http://192.168.1.109:4001/'


'''
code
'''
import requests
import re
import time

from datetime import datetime

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (PostbackEvent, MessageEvent, TextMessage, 
                            TextSendMessage, StickerSendMessage, LocationSendMessage, ImageSendMessage, VideoSendMessage, 
                            TemplateSendMessage, FlexSendMessage, 
                            ButtonsTemplate, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, 
                            QuickReply, QuickReplyButton, ConfirmTemplate,
                            MessageAction, MessageTemplateAction, URIAction, PostbackTemplateAction,
                            ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea, Video, ExternalLink,
                            RichMenuSwitchAction, RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, RichMenuAlias)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

status_dic = {}

'''
Function
'''
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
        if len(format(round(value['amount']/unit ,4),',.4f'))<=12:
            space = 32- len(value['fromCurrency'])*2- len(format(round(value['amount']/unit ,4),',.4f'))*2 -ln
            amount = ' '*space + format(round(value['amount']/unit ,4),',.4f')
            return amount
        else:
            space = 39- len(value['fromCurrency'])*2- len(format(round(value['amount']/unit ,4),',.4f'))*2 -ln
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
    

'''
Rich Menu
'''
for i in line_bot_api.get_rich_menu_list():
    line_bot_api.delete_rich_menu(i.rich_menu_id)
    
for i in line_bot_api.get_rich_menu_alias_list().aliases:
    line_bot_api.delete_rich_menu_alias(i.rich_menu_alias_id)

areas= [RichMenuArea(bounds= RichMenuBounds(x= 0,
                                           y= 0,
                                           width= 833,
                                           height= 843),
                    action= PostbackTemplateAction(label='Show Image Map', data='image_map833')
                    ),
        RichMenuArea(bounds= RichMenuBounds(x= 833,
                                           y= 0,
                                           width= 833,
                                           height= 843),
                    action= PostbackTemplateAction(label='Show Image Map', data='image_map1250')
                    ),
        RichMenuArea(bounds= RichMenuBounds(x= 1667,
                                            y= 0,
                                            width= 833,
                                            height= 843),
                     action= URIAction(label= '真人客服' , uri= 'http://bot.ppap.io?id=123')
                     ),
        RichMenuArea(bounds= RichMenuBounds(x= 0,
                                           y= 843,
                                           width= 833,
                                           height= 843),
                    action= PostbackTemplateAction(label='最新幣價', data='search_coin')
                    ),
        RichMenuArea(bounds= RichMenuBounds(x= 833,
                                           y= 843,
                                           width= 833,
                                           height= 843),
                    action= URIAction(label= '註冊登入' , uri= 'http://bot.ppap.io?id=123')
                    ),
        RichMenuArea(bounds= RichMenuBounds(x= 1667,
                                            y= 843,
                                            width= 833,
                                            height= 843),
                    action= PostbackTemplateAction(label='常見問題', text= '常見問題', data='common_questions')
                    )]

rich_menu_demo = RichMenu(
    size= RichMenuSize(width= 2500, height= 1686),
    selected= True,
    name= 'Demo',
    chat_bar_text= 'Demo',
    areas= areas
)

rich_menu_demo_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_demo)
    
with open('D:/backup/demo.jpg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_demo_id, 'image/jpeg', f)

line_bot_api.set_default_rich_menu(rich_menu_demo_id)

print('success')

'''
Chat
'''
# 接收 LINE 的資訊
@app.route("/", methods=['POST'])
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


@handler.add(MessageEvent, message=TextMessage)
def dscbot(event):
    message = event.message.text
    if message== '報價':
        list_5 = requests.get("%sapi/Cryptocurrency/getPriceList" % api_後台).json()
        search_coin1 = list_5[0]['fromCurrency']
        search_coin2 = list_5[1]['fromCurrency']
        search_coin3 = list_5[2]['fromCurrency']
        search_coin4 = list_5[3]['fromCurrency']
        search_coin5 = list_5[4]['fromCurrency']
        reply_button = TextSendMessage(text = search_coin(),
                                       quick_reply= QuickReply(items=[
                                            QuickReplyButton(action= PostbackTemplateAction(label= search_coin1, \
                                                                                            data = 'search_coin'+search_coin1)),
                                            QuickReplyButton(action= PostbackTemplateAction(label= search_coin2, \
                                                                                            data = 'search_coin'+search_coin2)),
                                            QuickReplyButton(action= PostbackTemplateAction(label= search_coin3, \
                                                                                            data = 'search_coin'+search_coin3)),
                                            QuickReplyButton(action= PostbackTemplateAction(label= search_coin4, \
                                                                                            data = 'search_coin'+search_coin4)),
                                            QuickReplyButton(action= PostbackTemplateAction(label= search_coin5, \
                                                                                            data = 'search_coin'+search_coin5)),
                                            QuickReplyButton(action= PostbackTemplateAction(label= '查詢其他幣種', \
                                                                                            data = 'enter_search'+'查詢其他幣種')),
                                           ]))
        line_bot_api.reply_message(event.reply_token, reply_button)
    elif message== '最新幣價':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(search_coin()))
    elif message == 'common_questions':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('常見問題'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(search_coin_list(message, 'ln')))

@handler.add(PostbackEvent)
def dscbot_call(event):
    message = event.postback.data
    if message == 'search_coin':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(search_coin()))
        
    elif message == 'common_questions':
        line_bot_api.reply_message(event.reply_token, TextSendMessage('常見問題'))
        
    elif message == 'image_map1250':
        img = ImagemapSendMessage(
            base_url = 'https://imgur.com/f2hBoXQ.jpg#',
            alt_text = 'IMG',
            base_size=BaseSize(height= 843, width= 1250),
            actions=[
                URIImagemapAction(link_uri= 'http://bot.ppap.io?id=123', #真人客服
                                  area=ImagemapArea(x= 833, y= 0, width= 417, height= 433)),
                URIImagemapAction(link_uri= 'http://bot.ppap.io?id=123', #註冊登入
                                  area=ImagemapArea(x= 417, y= 433, width= 417, height= 433)),
                MessageImagemapAction(text= '最新幣價',
                                      area=ImagemapArea(x=0, y= 433, width= 417, height= 433)),
                MessageImagemapAction(text= '常見問題',
                                      area=ImagemapArea(x= 833, y= 433, width= 417, height= 433))
            ]
        )
        
        line_bot_api.reply_message(event.reply_token, img)
    
    elif message == 'image_map833':
        img = ImagemapSendMessage(
            base_url = 'https://imgur.com/am1KSVX.jpg#',
            alt_text = 'IMG',
            base_size=BaseSize(height= 562, width= 833),
            actions=[
                URIImagemapAction(link_uri= 'http://bot.ppap.io?id=123', #真人客服
                                  area=ImagemapArea(x= 555, y= 0, width= 278, height= 281)),
                URIImagemapAction(link_uri= 'http://bot.ppap.io?id=123', #註冊登入
                                  area=ImagemapArea(x= 278, y= 281, width= 278, height= 281)),
                MessageImagemapAction(text= '最新幣價',
                                      area=ImagemapArea(x=0, y= 281, width= 278, height= 281)),
                MessageImagemapAction(text= '常見問題',
                                      area=ImagemapArea(x= 555, y= 281, width= 278, height= 281))
            ]
        )
        
        line_bot_api.reply_message(event.reply_token, img)
        
    elif 'search_coin' in message[:12]:
        coin = message[11:].upper()
        list_coin = requests.get("%sapi/Cryptocurrency/getPrice?coin=%s" % (api_後台, coin)).json()
        line_bot_api.reply_message(event.reply_token, \
                                   TextSendMessage(text = search_coin(coin, list_coin),
                                                quick_reply= QuickReply(items=[
                                                     QuickReplyButton(action= \
                                                                      PostbackTemplateAction(label= '查詢其他幣種', \
                                                                                             data = 'enter_search'+'查詢其他幣種'))
                                                    ])))
            
    if 'enter_search' in message[:12]:
        line_bot_api.reply_message(event.reply_token, \
                                   TextSendMessage(text = "進入查價模式! 請輸入幣種代號，如 btc, eth",
                                                quick_reply= QuickReply(items=[
                                                     QuickReplyButton(action= \
                                                                      PostbackTemplateAction(label= '退出查價模式', \
                                                                                             data = 'exit_search'+'退出查價模式'))
                                                    ])))

