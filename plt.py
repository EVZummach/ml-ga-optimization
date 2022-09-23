import numpy as np
import matplotlib.pyplot as plt

val = np.loadtxt('run.log')
n = 32

generation = val[:, 0]
y = val[:, 1:n+1]
fy = val[:, n+1:2*n+1]
average = val[:, -1]

t = np.arange(0.0, np.pi, 0.001)
fun = t + abs(np.sin(32*t))

#plt.plot(t, fun)
#plt.scatter(y, fy, color='red')
plt.savefig('Function.png')

plt.plot(generation, average)
plt.savefig('Fitness.png')

#print(y)
#print(fy)