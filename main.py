import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, url_for
import json
from atop_parse import *


UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('chart', name=filename))
    return render_template("upload_file.html")


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    filename = request.args.get('name')
    # compile_file_to_txt(filename)
    json_dump = parse_cpu(filename)
    java_cpu = json.dumps(json_dump[0])
    mongo_cpu = json.dumps(json_dump[1])
    correlator_cpu = json.dumps(json_dump[2])
    wafd_cpu = json.dumps(json_dump[3])
    wafgowaf_cpu = json.dumps(json_dump[4])
    celery_cpu = json.dumps(json_dump[5])
    rabbitmq_cpu = json.dumps(json_dump[6])
    freshclam_cpu = json.dumps(json_dump[7])
    waf_nginx_cpu = json.dumps(json_dump[8])
    waf_sync_cpu = json.dumps(json_dump[9])

    return render_template("chart.html", java_cpu=java_cpu, mongo_cpu=mongo_cpu, correlator_cpu=correlator_cpu, wafd_cpu=wafd_cpu, wafgowaf_cpu=wafgowaf_cpu, celery_cpu=celery_cpu, rabbitmq_cpu=rabbitmq_cpu, freshclam_cpu=freshclam_cpu, waf_nginx_cpu=waf_nginx_cpu, waf_sync_cpu=waf_sync_cpu)


if __name__ == '__main__':
    app.run(debug=True, port=5050)
