# flask, django 架設伺服器
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('GoH/MwV/eXHlffcKT11q8dXYdLTLL3goWPy18EgWu4xeZeaViOPHh7EWnDwayuGR/SVSuUO7kT91shxaXidZDITd8gmABGHpnGUUgKC/VBf48FjegL8nz4I56ekO3bWGvuwQCiN3hhKUfE+cWvz2BQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('06f35d078e5487cf32079f9588ea3609')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，你在說什麼？'
   
    if msg == ['hi', 'Hi']:
        r = '嗨'
    elif msg == '你吃飯了嗎':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是施翔豪'
    elif '訂位' in msg:
        r = '你想訂位，是嗎？'
    elif '在幹嘛' in msg:
        r = '我在休息中，晚一點再找我'
    elif '睡覺了嗎' in msg:
        r = '我已經睡覺了哦'
    elif msg == ['你幾歲了', '你幾歲了？']:
        r = '我今年17歲'
    elif ['你在哪裡？', '你在哪裡', '你現在在哪裡', '你現在在哪裡？'] in msg:
        r = '我現在在澳洲留學'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
