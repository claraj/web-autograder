import json
from json import JSONEncoder
from dataclasses import asdict

class TestItemEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return asdict(obj)
        except:
            return JSONEncoder.default(self, obj)
        # 
        # if hasattr(obj, 'JSONRepr'):
        #     return obj.JSONRepr()
        #
        # return JSONEncoder.default(self, obj)
