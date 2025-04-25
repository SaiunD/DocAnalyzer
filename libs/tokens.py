class TokenCounter:
    def __init__(self):
        self.total_tokens = 0

    def add_tokens(self, count):
        self.total_tokens += count

    def get_total_tokens(self):
        return self.total_tokens
