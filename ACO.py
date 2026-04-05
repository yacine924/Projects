import random
import time
import math


alpha = 1.3  # pheromon
beta = 2.0   #  heuristic
rho = 0.5    # prob evaporation rate
num_ants = 50 
num_iterations = 30
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

def distance_xy (X,Y) :
    return math.sqrt( (X[0]-Y[0])**2 + (X[1]-Y[1])**2 )

def total(path): #path=individual
    total = 0
    for i in range (len(path) - 1) :
        total+=distance_xy(coordinates[path[i]], coordinates[path[i + 1]])
    return total

#init matrixes
distance_matrix = []
for i in coordinates:
    row = []
    for j in coordinates:
        row.append(distance_xy(coordinates[i], coordinates[j]))
    distance_matrix.append(row)

#init pheromones
phero_matrix = []
for _ in coordinates:
    phero_matrix.append([10 for _ in coordinates]) # init to 10 

#Prob
def calc_prob(curr, not_visited):
    phero_not_visited = [phero_matrix[curr-1][j-1] for j in not_visited]
    heuristic_values = [1/ distance_matrix[curr-1][j-1] for j in not_visited]
    values = [(phero_not_visited[i] ** alpha) * (heuristic_values[i] ** beta) for i
in range(len(not_visited))] #Calculations : raised to the power of 
    
    total_value = sum(values)
    return [v / total_value for v in values] #List of prob of cities not_visited

def gen_solution():
    path = [1]  #node 1
    not_visited = set(coordinates.keys()) - {1} #All cities except 1
    curr = path[0] # = 1
    while not_visited:
        probabilities = calc_prob(curr, not_visited)
        next_node = random.choices(list(not_visited), weights=probabilities)[0] #choosing one node
        path.append(next_node) 
        not_visited.remove(next_node)
        curr = next_node
    path.append(1)
    return path 


#ACO
def aco_tsp():
    best_path = None
    best_dist = float('inf') # minus infinity
    for i in range(num_iterations):
        all_paths = []
        all_dist = []
        print(f"generation number {i} with best distance: { best_dist:.2f}")
        for _ in range(num_ants): #for every ant
            path = gen_solution()
            path_distance = total(path)
            all_paths.append(path)
            all_dist.append(path_distance)
            if path_distance < best_dist:
                best_path = path[:]
                best_dist = path_distance
        update_phero_matrix(all_paths, all_dist)
    return best_path, best_dist

def update_phero_matrix(paths, all_dist):
    global phero_matrix
    for i in range(len(phero_matrix)):
        for j in range(len(phero_matrix[i])):
            phero_matrix[i][j] = phero_matrix[i][j] * (1 - rho)
    for path, dist in zip(paths, all_dist):
        for i in range(len(path) - 1):
            phero_matrix[path[i]-1][path[i+1]-1]  += 1 / dist #the edge between i and i+1 (the minus 1 is because we start with 1 instead of 0)
        phero_matrix[path[-1]-1][path[0]-1]  += 1 / dist  #from the last (-1) to the first (0)



#execution 
start = time.time()
best_path, best_dist = aco_tsp()
end = time.time()
print(f"\nexecution time: {end - start:.0f} sec")
print("best route:", best_path)
print("best distance:", best_dist)


