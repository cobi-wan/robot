import uuid
from datetime import datetime

class Request:
    def __init__(self, reqStation):
        self.requestID = uuid.uuid4()
        self.requestTime = datetime.now()
        self.requestingStation = reqStation
        self.destination = None
        self.ETA = None