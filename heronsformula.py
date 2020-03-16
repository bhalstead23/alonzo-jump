import math
while True:
    a = float(input("\n\nfirst side? "))
    b = float(input("second side? "))
    c = float(input("third side? "))

    s = (a + b + c) / 2

    A = math.sqrt(s * (s - a) * (s - b) * (s - c))

    print ("\ns = " + str(s) + "\nA = " + str(A))
