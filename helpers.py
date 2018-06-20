import os
import requests
import time
import config


class DownloadError(Exception):
    pass


def help_text():
    text_str = "💡How it works: \n"

    text_str += "Send any photos 🏞, and I will recognize objects on it and tell you what I found!\n"

    text_str += "Developed by onix-systems.com"
    return text_str


def get_is_photo(data):
    photo_id = None
    status = 0
    if 'photo' in data['message'] and (data['message']['photo']):
        photo_id = data['message']['photo'][-1]['file_id']

    if 'document' in data['message'] and (data['message']['document']):
        if data['message']['document']['mime_type'] in ['image/jpeg', 'image/png', 'image/pjpeg']:
            photo_id = data['message']['document']['file_id']
        else:
            status = 1

    return photo_id, status


def get_json(method_name, *args, **kwargs):
    return make_request('get', method_name, *args, **kwargs)


def post_json(method_name, *args, **kwargs):
    return make_request('post', method_name, *args, **kwargs)


def make_request(method, method_name, *args, **kwargs):
    token = config.get('TOKEN')
    response = getattr(requests, method)(
        'https://api.telegram.org/bot%s/%s' % (token, method_name),
        *args, **kwargs
    )
    if response.status_code > 200:
        raise DownloadError(response)
    return response.json()


def download_file(app, photo_id, dst_path):
    photo = get_json('getFile', params={"file_id": photo_id})
    app.logger.info(photo)
    file_path = photo['result']['file_path']

    file_name = os.path.basename(file_path)
    file_name = str(time.time()) + '_' + file_name
    token = config.get('TOKEN')

    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (token, file_path))
    dst_file_path = os.path.join(dst_path, file_name)
    with open(dst_file_path, 'wb') as f:
        f.write(response.content)
    app.logger.info(u"Downloaded file to {}".format(dst_file_path))

    return dst_file_path
