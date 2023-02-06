import numpy as np
import matplotlib.pyplot as plt

# equation for the integral of the square root of 1-x^2 dx
def equation(b,a=0):
    return 0.5*(np.arcsin(b)+0.5*(np.sin(2*np.arcsin(b)))) - 0.5*(np.arcsin(a)+0.5*(np.sin(2*np.arcsin(a))))

def area_slice(x):
    return np.pi/(x*2)

slices = 6
area = area_slice(slices)

# create an array of values from 0 to 1 with 10000 points
d = np.linspace(0,1,100)

# calculate the output of the equation for each value in the array
output = equation(d)

# calculate the difference between the output and pi/8
difference = np.abs(output-(area))

#print the output value for the smallest difference
print(d[np.argmin(difference)])

#plot a unit circle and the area of the slice
plt.plot(np.cos(np.linspace(0,2*np.pi,100)),np.sin(np.linspace(0,2*np.pi,100)))


#plot a vertical line at the value of the smallest difference and mirror it over the y axis and make it red and dashed
plt.plot([d[np.argmin(difference)],d[np.argmin(difference)]],[-1,1],color='r',linestyle='--')

#add the value of d to the plot as a double
plt.text(d[np.argmin(difference)],0.5,'d = %s' %d[np.argmin(difference)],color='r')

#plot a grid over the plot and place a origin at the center
plt.grid()
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')

#change the screen to be square
plt.axis('square')
plt.show()












