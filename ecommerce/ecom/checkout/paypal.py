import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AacRQ_0o8FhW8X0sj4lAh74XBPIu10Ypr6UzTuZLggo6Mo7Q11l5WE7-xZdjB0HLFdgdXCKBpewVhvUF"
        self.client_secret = "EB4T_Su22BAp8u-EWIaSjrVh0jaL9pbdQH51emoEbMg8tOTwQvaZziCYkXDgHfF55yPsd6570rKHclgx"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)