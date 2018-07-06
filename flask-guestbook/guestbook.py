# -*- coding: utf-8 -*-


import shelve
from datetime import datetime
from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'


def save_data(name, comment, create_at):
    """
    save data from form submitted
    """
    database = shelve.open(DATA_FILE)

    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']

    greeting_list.insert(
        0, {'name': name, 'comment': comment, 'create_at': create_at})

    database['greeting_list'] = greeting_list

    database.close()


def load_data():
    """
    load saved data
    """
    database = shelve.open(DATA_FILE)
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list


@application.route('/')
def index():
    """Top page
    Use template to show the page
    """
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)


@application.route('/post', methods=['POST'])
def post():
    """Comment's target url
    """
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at = datetime.now()
    save_data(name, comment, create_at)
    return redirect('/')


@application.template_filter('nl2br')
def nl2br_filter(s):
    """ 将换行符置换为 br 标签的模板过滤器
    """
    return escape(s).replace('\n', Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')




if __name__ == '__main__':
    #在 IP 地址 127.0.0.1 的 8000 端口运行应用程序
    application.run('127.0.0.1', port=8000, debug=True)
    #save_data('test', 'test comment', datetime(2018, 6, 14, 16, 42, 0))
