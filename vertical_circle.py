import numpy as np

# equation for the integral of the square root of 1-x^2 dx
def equation(b,a=0):
    return 0.5*(np.arcsin(b)+0.5*(np.sin(2*np.arcsin(b)))) - 0.5*(np.arcsin(a)+0.5*(np.sin(2*np.arcsin(a))))

def area_slice(x):
    return np.pi/(x*2)

slices = 4
area = area_slice(slices)


# create an array of values from 0 to 1 with 10000 points
d = np.linspace(0,1,100)

# calculate the output of the equation for each value in the array
output = equation(d)

# calculate the difference between the output and pi/8
difference = np.abs(output-(area))

#print the output value for the smallest difference
print(d[np.argmin(difference)])

#verify the output









