import math

while True:
   # x = float(input("\n\nx component? "))
    #y = float(input("y component? "))

    #mag = math.sqrt(x**2 + y**2)
    #theta = math.atan(y / x)

    #print("\nmagnitude = " + str(mag) + "\ndirection angle = " + str(theta) + " degrees")
    mag = float(input("\n\nMagnitude? "))
    theta = math.radians(float(input("Directional angle in degrees? ")))
    
    components = [0,0]

    components[0] = math.cos(theta) * mag
    components[1] = math.sin(theta) * mag

    print("\n" + str(components))