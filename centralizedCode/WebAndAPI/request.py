import uuid
from datetime import datetime

class Request:
    def __init__(self, destination, linked=None, bot=None):
        if linked is None:
            self.requestID = uuid.uuid4()
        else: 
            self.requestID = linked.requestID
        self.requestTime = datetime.now()
        self.destination = destination      # Should be a node
        self.ETA = None
        self.active = True
        self.next = linked                  # Should be another request
        self.assignedBot = bot