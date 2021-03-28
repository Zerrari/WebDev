from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators
from wtforms.validators import DataRequired
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


## DataBase

## 初始化数据库的设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@127.0.0.1:3306/WebData'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

## 创建表单，继承自FlaskForm
class LoginForm(FlaskForm):
    username = StringField("Username")
    passwd = PasswordField()

##生成对应路径的app，route为出发函数的URL
@app.route('/home')

##<>内的为变量，会作为关键字传递给函数
@app.route('/home/<name>')

def index(form=None):

    ##创建没有csrf令牌保护的表单
    form = FlaskForm(csrf_enabled=False)

    ##通过视图函数生成模版文件
    return render_template('home.html',form=form)

@app.route('/products')
def products():
    return render_template('products.html')



@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    return render_template('login.html',form=form)
            
@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the file']
        f.save('/var/files/upload_files.txt')


with app.test_request_context('/home',method='POST'):
    assert request.path == '/home' 
    assert request.method == 'POST'
