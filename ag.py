import struct
from typing import Tuple
import numpy as np

from random import random

#f(y) = y + |sin(32y)|, 0 <= y <= pi

# Chromosome size in bits
L = 4*8 

# Bounds for fitness function
lower_bound = 0
upper_bound = np.pi

# Probabilites for crossover and mutation
pc = 0.7
pm = 0.001

def get_bits(num):
    return bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)

def get_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]


def crossover(bits_p1:str, bits_p2:str, p:float) -> Tuple[str, str]:
    """
    Selects one random locus to crossover between two bits.
    """
    if p < pc:
        locus = int(random()*L)
        f1 = bits_p1[:locus] + bits_p2[locus:]
        f2 = bits_p2[:locus] + bits_p1[locus:]
        return f1, f2
    else:
        return bits_p1, bits_p2

def mutation(bits:str, p:float) -> str:
    """
    Selects random locus to mutate a chromosome
    """

    if p < pm:
        locus = int(random()*L)
        bits_l = list(bits)
        bits_l[locus] = '0' if bits_l[locus] == '1' else '1'
        return ''.join(bits_l)
    else:
        return bits

def fitness(bits:str) -> float:
    """
    Receives a chromosome, converts it to float value and applies the respective function:
    f(y) = y + |sin(32y)|, 0 <= y <= pi
    
    If y is out of bounds the fitness will return 0.
    """

    y = float(get_float(bits))
    if np.isnan(y):
        return 0
    if y < lower_bound or y > upper_bound:
        return 0
    fy = y + abs(np.sin(32*y))
    return fy

def selection(generation: list) -> tuple:
    return 0

if __name__ == '__main__':
    
    for n in range(10, 100, 20):
    #n = 60
        print(n)
        t = []
        generations = 600

        first_generation = [get_bits((random()*(upper_bound - lower_bound)+lower_bound)) for _ in range(n)]
        prev_generation = first_generation

        for i in range(generations):
            
            next_generation = []

            values = [get_float(val) for val in prev_generation]
            fitness_values = [fitness(bits) for bits in prev_generation]
            total_fit = sum(fitness_values)
            average_fit = total_fit/len(fitness_values)
            fitness_probabilty = [fit_val/total_fit for fit_val in fitness_values]
            
            while len(next_generation) < n:
                f1 = prev_generation[np.random.choice(n, p=fitness_probabilty)]
                f2 = prev_generation[np.random.choice(n, p=fitness_probabilty)]
                f1_crs, f2_crs = crossover(f1, f2, np.random.uniform(low = 0.0, high=1.0))
                f1_mut = mutation(f1_crs, np.random.uniform(low = 0.0, high=1.0))
                f2_mut = mutation(f2_crs, np.random.uniform(low = 0.0, high=1.0))
                next_generation.append(f1_mut)
                next_generation.append(f2_mut)
            
            if n %2 == 1:
                next_generation.pop(np.random.randint(0, n))

            t.append(np.column_stack([i, np.reshape(values, (1, n)), np.reshape(fitness_values, (1, n)), average_fit]))
            
            prev_generation = next_generation

#print(t)
        np.savetxt(f'logs/run-n{n}-g{generations}.log', np.vstack(t))
#print(mutation(get_bits(math.pi)))