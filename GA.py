import math 
import random
import time


POP_size = 100
nb_iteration = 975
mutation_prob = 0.01
Max_fitness = 250000
elitism_ratio = 0.1 
count = 0 

coordinates = { 
    1: (565, 575), 2: (25, 185), 3: (345, 750), 4: (945, 685), 5: (845, 655),
    6: (880, 660), 7: (25, 230), 8: (525, 1000), 9: (580, 1175), 10: (650, 1130),
    11: (1605, 620), 12: (1220, 580), 13: (1465, 200), 14: (1530, 5), 15: (845, 
680),
    16: (725, 370), 17: (145, 665), 18: (415, 635), 19: (510, 875), 20: (560, 365),
    21: (300, 465), 22: (520, 585), 23: (480, 415), 24: (835, 625), 25: (975, 580),
    26: (1215, 245), 27: (1320, 315), 28: (1250, 400), 29: (660, 180), 30: (410, 
250),
    31: (420, 555), 32: (575, 665), 33: (1150, 1160), 34: (700, 580), 35: (685, 
595),
    36: (685, 610), 37: (770, 610), 38: (795, 645), 39: (720, 635), 40: (760, 650),
    41: (475, 960), 42: (95, 260), 43: (875, 920), 44: (700, 500), 45: (555, 815),
    46: (830, 485), 47: (1170, 65), 48: (830, 610), 49: (605, 625), 50: (595, 360),
    51: (1340, 725), 52: (1740, 245)
}

nb_city = len(coordinates) #52

def distance_xy (X,Y) :
    return math.sqrt( (X[0]-Y[0])**2 + (X[1]-Y[1])**2 )

def total(path): #path=individual
    total = 0
    for i in range (len(path) - 1) :
        total+=distance_xy(coordinates[path[i]], coordinates[path[i + 1]])
    total += distance_xy(coordinates[path[-1]], coordinates[path[0]])  #from the last (-1) to the first (0)
    
    return total

def random_pop(): 
    population = []
    base_route = list(range(2, nb_city + 1)) #From 2 to 52
    for _ in range(POP_size):
        random.shuffle(base_route)
        population.append([1] + base_route + [1])
    return population 

def fitness(path):
    global count # Possible to call from outside, not only locally
    count += 1 #because of max calculations
    return 1 / total(path)

def roulette_wheel_selec(population, fitnesses):
    total_fitness = sum(fitnesses)
    pick = random.uniform(0, total_fitness)
    current = 0
    for ind, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return ind

def tournament_selec(population, fitnesses, k=3): # k is a parameter 
    selected = random.sample(list(zip(population, fitnesses)), k) #select k-element randomly without repetition
    return max(selected, key=lambda x: x[1])[0]

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(1, size - 1), 2))
    child = [None] * size
    child[start:end] = parent1[start:end] #copy the [start, end] of the parent to the child
    idx = 0 
    for value in parent2:
        if value not in child : 
            while child[idx] != None: # until we find an empty slot for the number we selected
                idx += 1 
            child[idx] = value
    child[-1] = 1
    return child

def swap_mutation(path):
    if random.random() < mutation_prob:  
        start, end = sorted(random.sample(range(1,len(path)-1), 2))
        path[start:end] = reversed(path[start:end])  # reverse the selected part
    return path



# GA
def genetic_algorithm():
    population = random_pop()
    elite_num = int(elitism_ratio * POP_size) # Keep them in the next gen
    for i in range(nb_iteration):
        fitness_tab = [fitness(individual) for individual in population] 
        if count >= Max_fitness:
            break
        print(f"generation number {i} with best distance: { 
1/max(fitness_tab):.2f}")
        sorted_population = sorted(zip(population, fitness_tab), key=lambda x: 
x[1], reverse=True) #From best to worst
        new_pop = [ind[0] for ind in sorted_population[:elite_num]] #selecting elite 
        while len(new_pop) < POP_size:
            if(1/max(fitness_tab) > 13000) : #13000 is a parameter to change  between the two selection methods chosen
                parent1 = tournament_selec(population, fitness_tab) #Best of them
                parent2 = tournament_selec(population, fitness_tab)
            else :
                parent1 = roulette_wheel_selec(population, fitness_tab) #More explorer
                parent2 = roulette_wheel_selec(population, fitness_tab)
            
            while parent1 == parent2 : #To be sure we don't creat similar childrens
                parent2 = tournament_selec(population, fitness_tab)
                
            child1 = swap_mutation(ordered_crossover(parent1, parent2))
            child2 = swap_mutation(ordered_crossover(parent2, parent1))
            
            while child1 == child2 :
                child2 = swap_mutation(ordered_crossover(parent2, parent1))
                
            new_pop.append(child1)
            if len(new_pop) < POP_size:
                new_pop.append(child2) #completing the population
        population = new_pop
    best_route = max(population, key=fitness)
    
    return best_route


#execution
start = time.time()
best_route = genetic_algorithm()
end = time.time()
print(f"\n execution time: {end - start:.0f} sec")
print("best route:", best_route)
print(f"\n best distance: {total(best_route):.2f}")