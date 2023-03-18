from dollar.format.output.outputformatter import OutputFormatterMarkdown


class OutputFormatterHandler:
    formatter = OutputFormatterMarkdown()

    @classmethod
    def getformatter(cls):
        return cls.formatter
