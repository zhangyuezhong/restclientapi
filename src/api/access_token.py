import time
class AccessToken:
    def __init__(self, token, expire_at):
        self.token = token
        self.expire_at = expire_at

    def get_token(self):
        return self.token
    
    def is_expired(self):
        return time.time() >= self.expire_at

    def __str__(self):
        return f"Token: {self.token}\nExpire At: {self.expire_at}"
