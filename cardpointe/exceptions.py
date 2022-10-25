class ApiError(Exception):
    def __init__(self, *args, response=None):
        self.response = response
        super().__init__(*args)

    @property
    def request(self):
        return getattr(self.response, "request")
