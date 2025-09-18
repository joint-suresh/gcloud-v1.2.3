import Pyro4
name_server = Pyro4.locateNS()
calc_uri = name_server.lookup("ex2.calculator")
# Get the RMI object
calc_rmi = Pyro4.Proxy(calc_uri)
num1 = 10
num2 = 12
print("Two Numbers are: {}, {}".format(num1, num2))
print(f"Add: {calc_rmi.add(num1, num2)}")
print(f"Subtract: {calc_rmi.sub(num1, num2)}")
print(f"Multiply: {calc_rmi.mul(num1, num2)}")