import read_game as rg
import os
import dotenv
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import read_activity as ra
import random
import MongoDB_profile as mp
import quick_reply as qr
import gpt_path as gp
import gpt_db as gd
app = Flask(__name__)
handler = WebhookHandler('c344b99b7772e6dba5881b32bed91db9')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK', 200


class LineBot:
    def __init__(self, ID, event, msg) -> None:
        self.line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_TOKEN"))
        self.event = event
        self.ID = ID
        self.msg = msg
        profile = self.check_profil_exist()
        self.status = profile["status"]
        self.level = profile["level"]
        self.answer = profile["answer"]

    def reply_msg(self, msg) -> None:
        self.line_bot_api.reply_message(
            self.event.reply_token, msg)

    def push_msg(self, msg) -> None:
        self.line_bot_api.push_message(self.ID, msg)

    def check_profil_exist(self):
        if mp.check_profil_exist(self.ID):
            return mp.find_profile(self.ID)
        else:
            dict = {"user_id": self.ID, "status": "standard",
                    "level": 0, "answer": "none"}
            mp.store_profile(dict)
            return dict


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    dotenv.load_dotenv
    Linebot = LineBot(event.source.user_id, event, event.message.text)

    if Linebot.status == "standard":
        msg = ""
        if Linebot.msg == "活動詳情":
            msg = TextSendMessage("""【2024 年陽明交大歡樂耶誕城】🎅🎄🎉🥂\n\n▪️活動主辦方: 國立陽明交通大學 2024 聖誕市集籌辦小組🥰！\n\n▫️活動地點: 交大校區：新竹市東區大學路1001號✅！\n\n▪️活動時間: ➡️2024/12/23（一）2024/12/24（二）兩天皆是15:00-20:00😁\n\n▫️商家指南：\n🪵木藝聖誕坊: \n➡️在這邊你可以用雕刻好的木頭DIY(黏貼及彩繪)屬於2023年的聖誕節裝飾小物\n\n
🍭糖餅屋:  \n➡️這裡可以買到烤棉花糖跟薑餅人。這些食物都很應景呢! 買來跟聖誕樹一起拍照吧!\n\n🥐小食街角:  \n➡️這裡可以買到墨西哥捲餅、三明治等等的輕食，他們家的食物份量小，很適合逛街時嘴饞的你們!\n\n🪮卡哇伊小屋:  \n➡️這家店有很多CP值高又精美的頭飾，可以買來拍照!\n\n🍵飲品角--溫暖一杯:  \n➡️這家店賣許多熱飲，在飲控中的朋友們，他們也有提供熱水~\n\n🕯️燭火時光:  \n➡️這家是賣香氛蠟燭的店。不覺得買一小個蠟燭回家點燃，就很有過節的氣氛嗎？\n\n🎉快閃活動指南:\n(詳細地點皆會標示在地圖上)\n➡️12/23（一）15:00-19:30 薑餅人製作工坊\n➡️16:00-17:00 音樂表演\n➡️16:00-18:00 話劇表演（睡美人）\n➡️19:00-19:30 聖誕老人來發送小點心\n➡️12/24（二）17:00-18:00 音樂表演\n➡️16:00-18:00 話劇表演（羅密歐與茱麗葉）\n➡️19:00-19:30 聖誕老人發送小點心\n➡️20:00 煙火秀""")
        elif Linebot.msg == "活動主辦方":
            msg = TextSendMessage(ra.read_organizer())
        elif Linebot.msg == "活動地點":
            msg = TextSendMessage(ra.read_location())
        elif Linebot.msg == "活動時間":
            msg = TextSendMessage(ra.read_time())
        elif Linebot.msg == "商家指南":
            msg = TextSendMessage(ra.read_merchant_guide())
        elif Linebot.msg == "🎉快閃活動指南":
            msg = TextSendMessage(ra.read_flash_event_guide())
        elif Linebot.msg == "排隊等待路線":
            if Linebot.level == 0:
                image_1 = os.getenv("IMAGE_1")
                image_2 = os.getenv("IMAGE_2")
                image_3 = os.getenv("IMAGE_3")
                image_urls = [image_1, image_2, image_3]
                for image in image_urls:
                    Linebot.push_msg(ImageSendMessage(
                        original_content_url=image,
                        preview_image_url=image
                        )
                    )
                msg = qr.send_message_with_quick_reply("請問你要選擇哪種路線呢～",["路線一","路線二","路線三","隨機","你來幫我分析！"])
                mp.update_Status(Linebot.ID, "wait")
                mp.update_Level(Linebot.ID, 1)
        elif Linebot.msg == "快問快答":
            if Linebot.level == 0:
                Linebot.push_msg(
                    TextSendMessage("為了緩解我們 I 人小夥伴的無聊等待時間😉，就讓我來陪你輕鬆遊玩【閃電搶答QA小遊戲】吧！"))
                question, answer = rg.get_question_and_answer("請問本次聖誕市集的活動吉祥物是？")
                msg = qr.send_message_with_quick_reply("請問本次聖誕市集的活動吉祥物是？",[question["A"],question["B"],question["C"]])
                mp.update_Answer(Linebot.ID, answer)
                mp.update_Status(Linebot.ID, "game")
                mp.update_Level(Linebot.ID, 1)
    elif Linebot.status == "game":
        if Linebot.level == 1:
            correct_answer, incorrect_answers = rg.get_quiestion_reply("請問本次聖誕市集的活動吉祥物是？")
            if Linebot.msg == Linebot.answer:
                Linebot.push_msg(TextSendMessage(correct_answer))
            else:
                Linebot.push_msg(TextSendMessage(incorrect_answers))
            mp.update_Level(Linebot.ID, 2)
            question, answer = rg.get_question_and_answer("請問12/23的話劇表演主題是？")
            msg = qr.send_message_with_quick_reply("請問12/23的話劇表演主題是？",[question["A"],question["B"],question["C"]])
            mp.update_Answer(Linebot.ID, answer)
        if Linebot.level == 2:
            correct_answer, incorrect_answers = rg.get_quiestion_reply("請問12/23的話劇表演主題是？")
            if Linebot.msg == Linebot.answer:
                Linebot.push_msg(TextSendMessage(correct_answer))
            else:
                Linebot.push_msg(TextSendMessage(incorrect_answers))
            mp.update_Level(Linebot.ID, 0)
            mp.update_Status(Linebot.ID, "standard")    
            msg = TextSendMessage("快問快答遊戲結束！！！")
    elif Linebot.status == "wait":
        if Linebot.level == 1:
            if Linebot.msg == "路線一":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_1"),
                    preview_image_url=os.getenv("IMAGE_1")
                )
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
            elif Linebot.msg == "路線二":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_2"),
                    preview_image_url=os.getenv("IMAGE_2")
                    )
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
            elif Linebot.msg == "路線三":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_3"),
                    preview_image_url=os.getenv("IMAGE_3")
                    )
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
            elif Linebot.msg == "隨機":
                image_1 = os.getenv("IMAGE_1")
                image_2 = os.getenv("IMAGE_2")
                image_3 = os.getenv("IMAGE_3")
                image_urls = [image_1, image_2, image_3]
                image = random.choice(image_urls)
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=image,
                    preview_image_url=image
                    )
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
                
            elif Linebot.msg == "你來幫我分析！":
                path = gd.get_msg()
                Linebot.push_msg(TextSendMessage(path["msg"]))
                msg = qr.send_message_with_quick_reply("看完分析想選那一組路線呢",["路線一","路線二","路線三"])
                mp.update_Level(Linebot.ID, 2)
            else:
                msg = TextSendMessage("續水，我們賣永續的水")
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
        elif Linebot.level == 2:
            if Linebot.msg == "路線一":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_1"),
                    preview_image_url=os.getenv("IMAGE_1")
                )
            elif Linebot.msg == "路線二":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_2"),
                    preview_image_url=os.getenv("IMAGE_2")
                    )
            elif Linebot.msg == "路線三":
                Linebot.push_msg(TextSendMessage("這份地圖就送給你拉！"))
                msg = ImageSendMessage(
                    original_content_url=os.getenv("IMAGE_3"),
                    preview_image_url=os.getenv("IMAGE_3")
                    )
            else:
                msg = TextSendMessage("續水，我們賣永續的水")
                mp.update_Level(Linebot.ID, 0)
                mp.update_Status(Linebot.ID, "standard")
            Linebot.reply_msg(msg)
            mp.update_Level(Linebot.ID, 0)
            mp.update_Status(Linebot.ID, "standard")
            gd.update_msg(gp.create_chat_response())

    Linebot.reply_msg(msg)
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
