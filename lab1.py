from collections import deque


w = [15,32,60,80,43,120,77,6,93,35,37]
v = [20, 40, 50, 36, 26, 64, 54, 18, 46, 28, 25]
max_w = 420


def knapsackDFS(max_w,w,v) :
    stack = [(0,0,0,[])]
    n= len(w)
    best_value = 0 
    best_stack = [] #the optimal combination of items



    while stack :
        index,current_w,current_v,path = stack.pop() 

        if n==index : #We arrived at a leaf node
            if current_v > best_value :
                best_value = current_v 
                best_stack = path
            continue #skip the rest of code 
             
        stack.append((index+1,current_w,current_v,path))

        if current_w + w[index] <= max_w :
            stack.append((index+1,current_w + w[index],current_v + v[index],path + [index]))

    print(best_value,best_stack) 


def knapsackBFS(max_w,w,v):
    queue = deque([(0,0,0,[])])
    n=len(w)    
    best_value = 0
    best_enqueue = []
    while queue :
        index , current_w,current_v,path = queue.popleft()  
        if n==index :
            if current_v > best_value :
                best_value = current_v 
                best_stack = path
            continue
             
        queue.append((index+1,current_w,current_v,path))

        if current_w + w[index] <= max_w :
            queue.append((index+1,current_w + w[index],current_v + v[index],path + [index]))
    print(best_value,best_stack)

knapsackDFS(420,w,v) 
knapsackBFS(420,w,v)