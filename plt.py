import os
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, np.pi, 0.001)
fun = t + abs(np.sin(32*t))

if __name__ == '__main__':

    for file in os.listdir('logs'):
        val = np.loadtxt(f'logs/{file}')
        _, n, g = file.split('-')
        n = int(n[1:])
        g = int(g.split('.')[0][1:])

        generation = val[:, 0]
        y = val[:, 1:n+1]
        fy = val[:, n+1:2*n+1]
        average = val[:, -1]

        plt.plot(generation, average, label=f'n: {n}')
    
    plt.legend()    
    plt.savefig('images/Fitness.png')

#print(y)
#print(fy)