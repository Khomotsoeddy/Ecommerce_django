import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "Ae9wF2mN53z_C_rBbzOjVHKM6seYI1U3vfsGLKrvgbHEY8wo3cgvpKJFRXqKW5HLbTq8saF64u67U5bV"
        self.client_secret = "EOos-QlR_DW_99-WS4SGoA0eyzz3id1n8xEibVeWYhktz54Sba0RLmbhcgKDnJqA-5PEBinOxoDDVNHX"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)