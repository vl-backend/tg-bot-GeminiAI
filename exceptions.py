class InsufficientBalanceError(Exception):
    def __init__(self, detail="Insufficient balance. Sending messages is not allowed."):
        super().__init__(detail)
        self.detail = detail


class UserBlockedError(Exception):
    def __init__(self, detail="You are blocked. Sending messages is not allowed."):
        super().__init__(detail)
        self.detail = detail


class InvalidDataError(Exception):
    def __init__(self, detail="Invalid data provided."):
        super().__init__(detail)
        self.detail = detail
