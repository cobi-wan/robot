import uuid
from datetime import datetime

class Request:
    def __init__(self):
        self.requestID = uuid.uuid4()
        self.requestTime = datetime.now()
        self.requestingStation = None
        self.destination = None
        self.ETA = None