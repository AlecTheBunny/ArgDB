from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from werkzeug import secure_filename
from flask.ext.restful import Api
from flask.ext.restful import Resource
from flask.ext.restful import fields
import datetime
import pymongo
from bson.objectid import ObjectId
import gridfs
from cStringIO import StringIO

#
class StorageFiles(Resource):
    def __init__(self):
        super(StorageFiles, self).__init__()
        # self._upload_folder = '/tmp/storage'
        self.mongo = pymongo.MongoClient('127.0.0.1',27017)
        self.db = self.mongo['storage']
        self.fs = gridfs.GridFS(self.db,'files')

    def Time(self):
        date1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.now().strftime('.%f')[:4]
        date = date1 + date2
        return date

    #
    def __allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['txt', 'conf', 'ini', 'cf', 'yml', 'xml', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json', 'gz', 'rar','unzip', 'tgz'])
        return '.' in filename and filename.split('.',1)[1] in ALLOWED_EXTENSIONS
    #
    def get(self):
        filename = request.values['filename']
        files_id = request.values['files_id']
        #
        files = self.fs.get(ObjectId(files_id))
        data = files.read()

        headers = {}
        headers['Content-Type'] = 'application/octet-stream; charset=utf-8'
        headers['Content-Disposition'] = 'attachment; filename=' + filename

        return make_response(data,200,headers)
    #
    def post(self):
        begin_time = self.Time()
        # files = request.files['files']
        files_meta = request.files.getlist('files')
        #
        uri = []
        for meta in files_meta:
            filename = meta.filename
            if filename and self.__allowed_file(filename):
                filename = secure_filename(filename)
                # files.save(os.path.join(self._upload_folder,filename))
                data = StringIO(meta.read()).getvalue()
                files_id = self.fs.put(data=data,filename=filename)
                uri.append(fields.url_for(endpoint='StorageFiles',files_id=files_id,filename=filename))
            else:
                return make_response(jsonify({'error':'The format is not correct'}),403)
        #
        runtime = {'begin_time': begin_time, 'end_time': self.Time()}
        res = {}
        res['status'] = 'ok'
        res['runtime'] = runtime
        res['uri'] = uri
        #
        return make_response(jsonify(res),200)
    #
    def put(self):
        pass
    #
    def delete(self):
        begin_time = self.Time()
        files_id = request.values['files_id']

        self.fs.delete(ObjectId(files_id))
        # os.remove(self._upload_folder + '/' + filename)
        runtime = {'begin_time': begin_time, 'end_time': self.Time()}
        res = {}
        res['status'] = 'ok'
        res['runtime'] = runtime
        return make_response(jsonify(res), 200)
#
app = Flask(__name__)

api = Api(app=app)
api.add_resource(StorageFiles,'/storage',endpoint='StorageFiles')

#
if __name__ == '__main__':
    app.run(port=8000,debug=True)