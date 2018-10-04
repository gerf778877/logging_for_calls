#!flask/bin/python
import uuid
import urllib.request

import werkzeug
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


def write_log(request_id, file_name, log):
    log_file = open('dialog_log.txt', 'a')
    log_file.write('request_id: ' + request_id + ';\n')
    log_file.write('file_name: ' + file_name + ';\n')
    log_file.write('log: ' + log + ';\n\n')
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
        write_log(request_id, request_id + ".mp3", dialog)


class SaveVoxLog(Resource):
    def post(self):
        request_id = str(uuid.uuid1())

        parser = reqparse.RequestParser()
        parser.add_argument('audio_url')
        parser.add_argument('dialog')
        args = parser.parse_args()

        urllib.request.urlretrieve(args['audio_url'], 'audio/' + request_id + '.mp3')

        dialog = args['dialog']
        write_log(request_id, request_id + ".mp3", dialog)

        return {"response": "success"}


api.add_resource(UploadAudio, '/save_file_and_text')
api.add_resource(SaveVoxLog, '/save_vox_log')

if __name__ == '__main__':
    app.run(debug=True)
