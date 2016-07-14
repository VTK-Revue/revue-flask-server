from flask import request

from revue.internal.views import upload, internal_site


@internal_site.route("/upload/ckeditor/image", methods=['POST'])
def upload_ckeditor_image():
    res = upload.upload_file(request.files['upload'])
    print(res)
    if res['uploaded'] == 1:
        return "<script>console.log(window); window.parent.CKEDITOR.tools.callFunction({},'{}');</script>".format(
            request.args.get('CKEditorFuncNum'), res['url'])
    return "error"
