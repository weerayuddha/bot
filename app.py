from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage, VideoMessage, AudioMessage
)
from features.CarAnalytics import LicencePlate

import ptt
import tempfile
import os
import sys


app = Flask(__name__)

lastet_image_path = ""

line_bot_api = LineBotApi('+XTN3ua125UwCByjfRBLDddm8e0pXjYRsv1SChDKNM+nhewODx92TpLXvKMzh2GwvzRmgH6i9kBZtLRWagZZgGUAEGPmIUck3hTyJLoDwrMHwB4B2p0QDW9PIXL+r1OQDVFOoEwnCUCfOqy/DS3pIQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9ba5e5c4f5acef2daedfd744e34b6da0')

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
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