class CalculatorTool:

    name = "calculator"

    def execute(self):

        value = 25 * 12

        return {
            "tool": self.name,
            "result": value
        }