from RPCObjects import *


"""
This file handles the routing of the API requests
It receives the processed request, and calls the
appropriate function and returns the response. Specific
methods declarations not related to handling and routing
the request SHOULD NOT be included here, but rather in a
module that is imported and initialized

The router takes advantage of the Python's reflective
property, which basically allows it to know some meta-data
about itself such as what functions are available and where
they are. This allows us to iterate through the variables and
methods available in the scope based on a string that we recieve
from the user. In this case, it's passed in from the request
"""

# Function Imports
from APIExamples import Info
from celery_tasks import CeleryTasks

class Router():

    # Define references to other classes, this
    #   makes them visible to the API
    # Declaring them as members of the class
    #   makes these persist across different requests
    def __init__(self):
        self.info = Info()
        self.tasks = CeleryTasks()


    # Handle a request
    def run(self, request):
        assert isinstance(request, JsonRpcRequest)

        # Find the requested attribute/function

        # Provide a starting scope
        obj = self
        # Get the method
        method = str(request.method)
        # Get the "steps" to get there, i.e. what traversal to do
        steps = method.split('.')

        # Iterate through the scope to find the final object
        for step in steps:
            # Replace our current scope with the object specified in the request
            obj = getattr(obj, step, None)
            # Make sure that the object/scope exists
            if obj is None:
                # Throw and error if it does not exist
                raise JsonRpcMethodNotFound("Could not find '%s'" % request.method)

        # Execute the function and return the response
        return obj(**request.params)