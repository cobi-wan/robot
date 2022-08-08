import uuid
from datetime import datetime

class Request:
    def __init__(self, destination, linked=None):
        self.requestID = uuid.uuid4()
        self.requestTime = datetime.now()
        self.destination = destination      # Should be a node
        self.ETA = None
        self.active = True
        self.next = linked                  # Should be another request
        self.assignedBot = None