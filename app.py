# -*- coding: utf-8 -*-

import os
from flask import Flask, request, \
    redirect, url_for, render_template, \
    send_from_directory, abort
from werkzeug import secure_filename
from time import time

SEP = os.sep
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = CURRENT_DIRNAME + SEP + 'uploads'
ALLOWED_EXTENSIONS = {'zip', 'png', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload():
    # replace windows or mac
    cmd_str = CURRENT_DIRNAME + (str.replace('/bin/%s/img2webp -lossy ', '/', SEP) % 'mac')
    if request.method == 'POST':
        upload_files = request.files.getlist('file[]')
        # create new dir
        time_stamp = str(int(time()))
        # mac
        files_dir = CURRENT_DIRNAME + SEP + 'uploads' + SEP + time_stamp
        print('files_dir====>' + files_dir)
        os.mkdir(files_dir)

        # single convert
        if len(upload_files) == 1:
            file = upload_files[0]
            file_out_path = files_dir + SEP + file.filename.split('.')[0] + '.webp'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(files_dir, filename))
                abspath = files_dir + SEP + filename
                cmd_str += abspath + ' '
            cmd_str += '-o ' + file_out_path
            print(cmd_str)
            os.system(cmd_str)
        else:
            # out path
            file_name_out = '%s.webp' % time_stamp
            file_out_path = CURRENT_DIRNAME + SEP + 'static' + SEP + file_name_out
            file_paths = []
            for file in upload_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(files_dir, filename))
                    abspath = files_dir + SEP + filename
                    cmd_str += abspath + ' '
                    file_paths.append(abspath)
            cmd_str += '-o ' + file_out_path
            print(cmd_str)
            os.system(cmd_str)
            # for abspath in file_paths:
            #     os.remove(abspath)
            file_url = url_for('show', name=file_name_out)
            print(file_url)
            return render_template('upload.html') + '<br><img src=' + file_url + '>'
    return render_template('upload.html')

@app.route('/show/<name>')
def show(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port='5001',
        debug=True
    )
