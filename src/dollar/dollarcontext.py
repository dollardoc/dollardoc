class DollarContext:

    def __init__(self, file: str, line: int, col: int):
        self.file = file
        self.line = line
        self.col = col

    def get_file(self) -> str:
        return self.file

    def get_line(self) -> int:
        return self.line

    def get_col(self) -> int:
        return self.col

    def __str__(self):
        return "DollarContext(" + ", ".join([self.file, str(self.line), str(self.col)]) + ")"


class DollarContextSpan(DollarContext):

    def __init__(self, context_start, context_end):
        super().__init__(context_start.file, context_start.line, context_start.col)
        self.context_start = context_start
        self.context_end = context_end

    def get_context_start(self) -> DollarContext:
        return self.context_start

    def get_context_end(self) -> DollarContext:
        return self.context_end

    def get_file(self) -> str:
        return self.get_context_start().get_file()

    def get_line(self) -> int:
        return self.get_context_start().get_line()

    def get_col(self) -> int:
        return self.get_context_start().get_col()

    def __str__(self):
        return "DollarContextSpan(" \
               + "\n        " + str(self.context_start) \
               + "\n        " + str(self.context_end) + ")"
