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
    s = '你吃飯了嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()
