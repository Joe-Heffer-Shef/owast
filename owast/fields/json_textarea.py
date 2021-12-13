import json

from wtforms import TextAreaField


class JsonTextAreaField(TextAreaField):
    def process_formdata(self, valuelist: list):
        if valuelist:
            self.data = json.loads(valuelist[0])