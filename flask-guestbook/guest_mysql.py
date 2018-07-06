# -*-coding:utf-8-*-


import MySQLdb
from datetime import datetime
from flask import Flask, request, render_template, redirect, escape, Markup,flash

application = Flask(__name__)
MYSQL_HOST = "200.200.200.230"
MYSQL_PORT = 3307
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "z123456"
DB_NAME = "lingtest"

def get_conn():
    conn = MySQLdb.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        passwd=MYSQL_PASSWORD,
        db=DB_NAME,
        charset='utf8',
        use_unicode=True)
    return conn

def save_data(name, comment, create_at):
    """
    save data from form submitted
    """
    conn = get_conn()
    cur = conn.cursor()
    if len(comment) > 5 and len(comment) < 500:
        value = [name, comment, create_at]
        cur.execute("insert into guestbook values(%s, %s, %s)", value)
        conn.commit()

def load_data():
    """
    load saved data
    """
    conn = get_conn()
    cur = conn.cursor()
    query = "SELECT * from guestbook"
    cur.execute(query)
    greeting_list = cur.fetchall()
    conn.close()
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
    #load_data()
