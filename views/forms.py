# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from .models import Users


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self, field):
        if not Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名不存在')


class AddUserForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能由字母，数字，小数点和下划线组成')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('添加')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
