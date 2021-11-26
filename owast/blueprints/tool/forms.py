import flask_wtf
import wtforms.validators


class ToolForm(flask_wtf.FlaskForm):
    code = wtforms.StringField(validators={wtforms.validators.InputRequired()})
    vericut_number = wtforms.IntegerField(validators={
        wtforms.validators.InputRequired(),
        wtforms.validators.NumberRange(min=1)})
    serial_number = wtforms.StringField()
