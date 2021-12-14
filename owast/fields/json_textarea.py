import json

from wtforms import TextAreaField


class JsonTextAreaField(TextAreaField):
    DEFAULT = '{}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = kwargs.get('default', self.DEFAULT)

    def process_formdata(self, valuelist: list):
        if valuelist:
            self.data = json.loads(valuelist[0])
