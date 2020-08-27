# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging


from flask import Flask, request
app = Flask(__name__)
# uncomment to get traceback
app.debug = True

@app.route("/privet", methods=['POST'])    
def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False,
            "text": "Ну привет!"
        }
    }

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

if __name__ == "__main__":
    app.run()
