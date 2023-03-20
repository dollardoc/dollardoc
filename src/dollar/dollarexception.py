from dollar.dollarcontext import DollarContext


class DollarException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message


class DollarExecutionException(DollarException):

    def __init__(self, message: str, dollar_context: DollarContext):
        super().__init__(
                "\n" + dollar_context.get_file() + " on line " + str(dollar_context.get_line()) + ": " + message)
        self.dollar_context = dollar_context

    def get_dollar_context(self):
        return self.dollar_context
