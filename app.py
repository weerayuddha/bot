from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    StickerMessage
)
from features.CarAnalytics import LicencePlate

import ptt
import tempfile
import os
import sys


app = Flask(__name__)

lastet_image_path = ""

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
   print('Specify LINE_CHANNEL_SECRET as environment variable.')
   sys.exit(1)
if channel_access_token is None:
   print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
   sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

#คำเขียว
line_bot_api = LineBotApi('25fh1/p3BJu916+Zs39hsZNgb50c1RPaMNl7QGRRhGgWxhE53obct8ss1lZuR9OovzRmgH6i9kBZtLRWagZZgGUAEGPmIUck3hTyJLoDwrOXPz0i+hb+EOLslTB9S+TFPr4F9zOHoWo+Cb8z12aE6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9ba5e5c4f5acef2daedfd744e34b6da0')

#คำแก้ว
line_bot_api = LineBotApi('etLFKVdRJ9GW/Je0Sj65jGnWHpUppbGbVVlKw0wQJjXHfJGGtHo9e6IPmRDZ7+an3K60aU4GlzvMuqv1mAn/HtkTQxrqgQ8lO/sR7AH/jiUGey7hSebC3l6upJWwPTdbxyW0BaYnBD5v/Dl0F3zVFAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4f8d9c9c7c6b29aaabcad4d6298a9a30')


static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
   # Handle webhook verification
    if event.reply_token == "ffffffffffffffffffffffffffffffff":
       return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Handle webhook verification
    if event.reply_token == "00000000000000000000000000000000":
       return 'OK'

    if event.message.text == 'ราคาน้ำมัน':
        l = ptt.get_prices()
        s = ""
        for p in l:
            s += "%s %.2f บาท\n" %(p[0], p[1])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s))
    elif event.message.text == 'วิเคราะห์รูป':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='สักครู่ค่ะ')
            ]
        )
        try:
            lp = LicencePlate()
            result = lp.process(lastet_image_path)
            s = lp.translate(result)

            line_bot_api.push_message(
                event.source.user_id,[
                    TextSendMessage(text=s)
                ])
        except Exception as e:
            print('Exception:', type(e),e)
            line_bot_api.push_message(
                event.source.user_id, [
                    TextSendMessage(text='ไม่สามารถวิเคราะห์รูปได้ค่ะ')
                ])

    else:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+'เจ้า'))

@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    global lastet_image_path
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    lastet_image_path = dist_path


if __name__ == "__main__":
    app.run()