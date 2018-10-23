import json
from json import JSONEncoder

class TestItemEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'JSONRepr'):
            return obj.JSONRepr()
        return JSONEncoder.default(self, obj)
