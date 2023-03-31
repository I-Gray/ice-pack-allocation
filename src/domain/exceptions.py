

class PostCodeNotFoundException(Exception):
    def __init__(self, postcode: str):
        self.postcode = postcode
