import flask_wtf
import wtforms.validators


class ToolForm(flask_wtf.FlaskForm):
    code = wtforms.StringField(
        validators={wtforms.validators.InputRequired()},
        description='This could be a tool assembly ID')
    vericut_number = wtforms.IntegerField(validators={
        wtforms.validators.InputRequired(),
        wtforms.validators.NumberRange(min=1)})
    serial_number = wtforms.StringField(description="Written on machine")
    supplier = wtforms.StringField(description="Who provided this tool?")
    received = wtforms.BooleanField(
        description='Was this received from the supplier?')
