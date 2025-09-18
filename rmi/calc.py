import Pyro4
@Pyro4.expose
class Calculator:
    def add(self, num1, num2):
        return num1 + num2
    def sub(self, num1, num2):
        return num1 - num2
    def mul(self, num1, num2):
        return num1 * num2
    def div(self, num1, num2):
        try:
            return num1 / num2
        except:
            return "Cant Divide by Zero..."
