#!flask/bin/python
import json
import uuid
import urllib.request

import werkzeug
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


def write_log(json_data):
    log_file = open('dialog_log.json', 'a')
    json.dump(json_data + '\n', log_file)
    log_file.close()


class UploadAudio(Resource):
    def post(self):
        request_id = str(uuid.uuid1())

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('dialog')
        args = parser.parse_args()

        audio_file = args['file']
        audio_file.save('audio/' + request_id + '.mp3')

        dialog = args['dialog']
        write_log(dialog)


class SaveVoxLog(Resource):
    def post(self):
        request_id = str(uuid.uuid1())
        json_data = request.get_json(force=True)
        urllib.request.urlretrieve(json_data['audio_url'], 'audio/' + request_id + '.mp3')

        try:
            json_data['audio_url'] = 'audio/' + request_id + '.mp3'
        except KeyError:
            json_data['audio_url'] = 'did not receive this parameter'

        json_data['request_id'] = request_id
        write_log(json_data)

        return {"response": "success"}


api.add_resource(UploadAudio, '/save_file_and_text')
api.add_resource(SaveVoxLog, '/save_vox_log')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1519, debug=False)