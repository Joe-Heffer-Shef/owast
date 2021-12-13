from bson import ObjectId
from wtforms import HiddenField


class ObjectIdStringField(HiddenField):
    """
    String field for BSON object identifier.

    https://docs.mongodb.com/manual/reference/method/ObjectId/
    """

    def process_formdata(self, valuelist: list):
        if valuelist:
            self.data = ObjectId(valuelist[0])