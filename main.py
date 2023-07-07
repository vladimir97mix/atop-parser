from os.path import join, dirname, relpath
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, url_for
import json

import atop_parse

UPLOAD_FOLDER = join(dirname(relpath(__file__)), 'uploads')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

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
    if not os.path.exists("uploads/{0}.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_c.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_mem.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_mem_c.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_dsk.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_dsk.txt".format(filename)) \
            or not os.path.exists("uploads/{0}_dsk_c.txt".format(filename)):
        atop_parse.compile_file_to_txt(filename)
    json_dump_cpu = atop_parse.parse_cpu(filename)
    json_dump_mem = atop_parse.parse_mem(filename)
    json_dump_dsk = atop_parse.parse_dsk(filename)
    waf_nginx_cpu = json.dumps(json_dump_cpu[8])
    waf_nginx_mem = json.dumps(json_dump_mem[8])
    waf_nginx_dsk = json.dumps(json_dump_dsk[8])
    general_cpu_sys = json.dumps(json_dump_cpu[10])
    general_cpu_user = json.dumps(json_dump_cpu[11])
    general_mem_total = json.dumps(json_dump_mem[10])
    general_mem_free = json.dumps(json_dump_mem[11])

    return render_template("chart.html", json_dump_cpu=json_dump_cpu, json_dump_mem=json_dump_mem,
                           waf_nginx_cpu=waf_nginx_cpu, waf_nginx_mem=waf_nginx_mem, json_dump_dsk=json_dump_dsk,
                           waf_nginx_dsk=waf_nginx_dsk, general_cpu_sys=general_cpu_sys,
                           general_cpu_user=general_cpu_user, general_mem_total=general_mem_total,
                           general_mem_free=general_mem_free)


if __name__ == '__main__':
    app.run(debug=True, port=5050, host='0.0.0.0')
