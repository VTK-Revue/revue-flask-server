import time

import os
import random
from flask import request, jsonify, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

from revue import app
from revue.internal.views import internal_site


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@internal_site.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['upload']
    if file and allowed_file(file.filename):
        filename = secure_filename("{}-{}-{}".format(int(time.time()), random.randint(0, 9999), file.filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            "uploaded": 1,
            "fileName": filename,
            "url": url_for('.uploaded_file', filename=filename)
        })
    return jsonify({
        "uploaded": 0,
        "error": {
            "message": "An error occurred"
        }
    })


@internal_site.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
