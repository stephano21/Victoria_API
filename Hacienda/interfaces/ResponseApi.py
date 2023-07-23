class ResponseApi:
    def __init__(self, message="", detail="", success=True):
        self.message = message
        self.detail = detail
        self.success = success
