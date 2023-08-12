from os.path import join, dirname, relpath
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, flash, request, redirect, url_for
import json
import atop_parse
import re


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
UPLOAD_FOLDER = join(dirname(relpath(__file__)), 'uploads/')
REGEX = re.compile(r'[\!\@\"\:\;\#\$\%\^\&\*\(\)\.\,\'\[\]\|\\\/\?\№\<\>]')

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
            folder_name = request.form.get('foldername')
            if REGEX.search(folder_name):
                flash("""В имени запрещены следующие символы: ! @ " : ; # $ % ^ & * ( ) . , ' [ ] | \ / ? № < >""")
                return redirect(request.url)
            else:
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
                if os.path.exists(upload_path):
                    flash("Данное имя занято! Введите другое имя, или найдите график в списке файлов.")
                    return redirect(request.url)
                else:
                    os.system('mkdir uploads/{0}'. format(folder_name))
                    file.save(os.path.join(upload_path, filename))
                    return redirect(url_for('chart', name=filename, fname=folder_name))

    return render_template("upload_file.html")


@app.route('/list', methods=['GET', 'POST'])
def file_list():
    dir_list = os.listdir(UPLOAD_FOLDER)

    return render_template("file_list.html", dir_list=dir_list)


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    filename = request.args.get('name')
    folder_name = request.args.get('fname')
    if filename == None:
        files = os.listdir(os.path.join('uploads', folder_name))
        for file in files:
            if not re.match(r'.*\.txt', file):
                filename = file
    atop_parse.compile_file_to_txt(filename, folder_name)
    json_dump_cpu = atop_parse.parse_cpu(filename, folder_name)
    json_dump_mem = atop_parse.parse_mem(filename, folder_name)
    json_dump_dsk = atop_parse.parse_dsk(filename, folder_name)
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


@app.route('/files', methods=['GET', 'POST'])
def files():
    pass


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, port=5000, host='127.0.0.1')
