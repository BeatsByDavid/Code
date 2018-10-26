from RPCObjects import *

# Function Imports
from APIExamples import info

class Router():

    def __init__(self):
        self.info = info()
        pass

    def run(self, request):
        assert isinstance(request, JsonRpcRequest)

        # Find the requested attribute/function
        obj = self
        method = str(request.method)
        assert isinstance(method, str)
        steps = method.split('.')

        for step in steps:
            obj = getattr(obj, step, None)
            if obj is None:
                raise JsonRpcError("No Method Found!")

        return obj(request.params)