import base64
import os


def gen_token():
    return base64.b64encode(os.urandom(9))
