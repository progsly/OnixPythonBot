from flask import Flask, request
import telegram
import config
import helpers
import sys
sys.path.append('./object_detection')
# tensorflow object detection api imports
import json
import cv2
import object_detection_api

# CONFIG
TOKEN = config.get('TOKEN')
HOST = config.get('HOST')
THRESHOLD = config.get('THRESHOLD')

bot = telegram.Bot(TOKEN)
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    app.logger.info(data)

    update = telegram.update.Update.de_json(request.get_json(force=True), bot)

    if update.message.text == '/help':
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=helpers.help_text())
        return 'OK'

    photo_id, status = helpers.get_is_photo(data)

    app.logger.info(photo_id)
    if status == 1:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Sorry. Unsupported file type. Please use jpg (jpeg) or png file.')
        return 'OK'

    if photo_id:
        photo = helpers.download_file(app, photo_id, 'photos/downloads/')

        image = cv2.imread(photo)
        orig_height, orig_width, _ = image.shape

        objects = object_detection_api.get_objects(image, THRESHOLD)

        objects = json.loads(objects)
        if len(objects) > 1:
            app.logger.info(objects)

            font = cv2.FONT_HERSHEY_SIMPLEX

            result_msg = ''
            for item in objects:
                if item['name'] != 'Object':
                    continue

                x = int(orig_width * item['x'])
                y = int(orig_height * item['y'])

                width = int(orig_width * item['width'])
                height = int(orig_height * item['height'])

                cv2.rectangle(image, (x, y), (width, height), (0, 255, 0), 2)

                scope = float('{:.2f}'.format(item['score'] * 100))
                cv2.putText(image, item['class_name'] + " - " + str(scope) + '%', (x + 5, y + 20), font, 1,
                            (255, 255, 255), 1, cv2.LINE_AA)

                result_msg += item['class_name'] + " - " + str(scope) + '% \n'

            new_name = 'photos/detected/photo_detected_' + str(photo_id) + '.jpg'
            cv2.imwrite(new_name, image)

            bot.sendPhoto(update.message.chat_id, photo=open(new_name, 'rb'), caption="Result")
            bot.sendMessage(chat_id=update.message.chat_id, text=result_msg)

        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Sorry! No objects were found. Please try another photo.')
        return 'OK'

    bot.sendMessage(chat_id=update.message.chat_id, text='Please send a photo for recognition!')

    return 'OK'


def set_webhook():
    bot.setWebhook(url='https://%s/%s' % (HOST, TOKEN))


if __name__ == '__main__':
    set_webhook()

    app.run(host='0.0.0.0', port=8000, debug=True)
