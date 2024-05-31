import jwt

import os
import datetime




class Token:
    def __init__(self):
        self.secret_key = "secret"


    def generate(self, username):
        try:
            payload = {
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
            }

            token = jwt.encode(payload, self.secret_key, algorithm='HS256')



            return token
        except Exception as exc:


            return str(exec)