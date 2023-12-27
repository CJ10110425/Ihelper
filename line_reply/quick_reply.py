from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction


def send_message_with_quick_reply( text, options):

    quick_reply_buttons = [
        QuickReplyButton(
            action=MessageAction(label=option, text=option)
        ) for option in options
    ]

    quick_reply = QuickReply(items=quick_reply_buttons)

    text_message = TextSendMessage(
        text=text,
        quick_reply=quick_reply
    )

    return text_message