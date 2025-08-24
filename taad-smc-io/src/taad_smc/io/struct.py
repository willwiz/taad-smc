import traceback


class Error:
    msg: str
    trace: traceback.StackSummary

    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.trace = traceback.extract_stack()
