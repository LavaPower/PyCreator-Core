double_car = {
    "'": "'",
    '"': '"',
    "(": ")",
    "{": "}",
    "[": "]"
}


class Analyser:
    def __init__(self, config):
        self.config = config

    def update_code(self, code):
        if len(code):
            if self.config.get("doublechar", True):
                code = double_car.get(code[-1], "")
            else:
                code = ""
        return code
