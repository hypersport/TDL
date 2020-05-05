from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from wtforms.widgets import Input
from .models import Users
from flask_login import current_user


class CancelInput(Input):
    """
    Renders a cancel button.

    The field's label is used as the text of the cancel button instead of the
    data on the field.
    """
    input_type = 'button'

    def __call__(self, field, **kwargs):
        kwargs.setdefault('value', field.label.text)
        return super(CancelInput, self).__call__(field, **kwargs)


class CancelField(BooleanField):
    """
    Represents an ``<input type="button">``.  This allows checking if a given
    cancel button has been pressed.
    """
    widget = CancelInput()


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
    is_administrator = BooleanField('是否设为管理员')
    submit = SubmitField('添加')
    cancel = CancelField('取消')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')


class ToDoForm(FlaskForm):
    todo_content = TextAreaField('ToDo内容')
    cancel = SubmitField('取消')
    submit = SubmitField('确认')


class ResetInfoForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能由字母，数字，小数点和下划线组成')])
    old_password = PasswordField('旧密码', validators=[DataRequired(message='密码不能为空')])
    password = PasswordField('新密码', validators=[DataRequired(message='密码不能为空'), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('修改信息')
    cancel = CancelField('取消')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('密码不正确')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
