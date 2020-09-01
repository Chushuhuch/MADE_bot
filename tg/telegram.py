from flask import Flask, request
import telegram
from credentials import bot_token, bot_user_name,URL

app = Flask(__name__)


class Context:
    def __init__(self):
        self.TOKEN = bot_token
        self.bot = telegram.Bot(token=self.TOKEN)


context = Context()


@app.route('/{}'.format(context.TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), context.bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
        Hi there!
        """
        # send the welcoming message
        context.bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    else:
        try:
            # clear the message we got from any non alphabets
            # text = re.sub(r"\W", "_", text)
            url = "https://freesvg.org/img/1538298822.png"
            # note that you can send photos by url and telegram will fetch it for you
            context.bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            # if things went wrong
            context.bot.sendMessage(chat_id=chat_id, text="There was some problem", reply_to_message_id=msg_id)

    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = context.bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=context.TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == "__main__":
    app.run()
