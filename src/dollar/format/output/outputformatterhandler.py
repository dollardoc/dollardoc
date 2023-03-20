from dollar.format.output.outputformatter import OutputFormatterMarkdown


class OutputFormatterHandler:
    formatter = OutputFormatterMarkdown()

    @classmethod
    def get_formatter(cls):
        return cls.formatter
