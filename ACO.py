# -*- coding: utf-8 -*-
import random

class Shop:
    def __init__(self, name):
        self.name = name
        self.roads = []
        self.coordinates = []
    
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    
    def add_road(self, road):
        if road not in self.roads:
            self.roads.append(road)

class Road:
    def __init__(self, connected_shops, cost, pheromone=0):
        self.connected_shops = connected_shops
        self.cost = cost
        self.pheromone = pheromone
        
    def set_pheromone(self, pheromone):
        self.pheromone = pheromone
        
    def evaporate_pheromone(self, rho):
        # update the pheromone of the road
        self.pheromone = (1-rho) * self.pheromone
        
    def deposit_pheromone(self, ants):
        # 1. search for ants that uses the road
        for ant in ants:
            if self in ant.path:
                # 2. deposit pheromone using the inveresely proportionate relationship between path length and deposited pheromone
                self.pheromone += 1 / ant.get_path_length() 
                
class Ant:
    def __init__(self):
        self.shops = []     # Shops that the ant passes through, in sequence
        self.path = []       # Roads the ant uses, in sequence 
        
    # Find path from origin to destination
    def get_path(self, origin, destination, alpha, intermediate_shops):
        # 1. append origin to the self.shops
        self.shops.append(origin)
        # 2. if the last shop is not destination, search for the next shop to go
        while (self.shops[-1] != destination) or (all(shop in self.shops for shop in intermediate_shops) == False):
        #for i in range(20):
            current_shop = self.shops[-1]
            current_roads = []
            probabilities = []
            pheromone_sum = 0
            selectedProbability = random.random()
            currentCumulatedProbability = 0
            
            # Remove road that was just used 
            for i in range(len(current_shop.roads)):
                if len(self.path) != 0:
                    if (current_shop.roads[i] != self.path[-1]) or (len(current_shop.roads) == 1):     # if road was not just used, or if it is the only possible road 
                        current_roads.append(current_shop.roads[i])
                else:
                    current_roads.append(current_shop.roads[i])
                
            # Get total pheromone of roads connected to a shop
            for i in range(len(current_roads)):
                pheromone_sum += (current_roads[i].pheromone ** alpha)

            # Calculate probabilities of each road connected to the shop 
            for i in range(len(current_roads)):
                p = ((current_roads[i].pheromone ** alpha) / pheromone_sum)
                probabilities.append(p)

            # Select road and append to path list 
            for choice, prob in zip(current_roads, probabilities):
                currentCumulatedProbability += prob
                if selectedProbability < currentCumulatedProbability:
                    road_chosen = choice
                    self.path.append(road_chosen)
                    break

            #print(str(self.path[-1].connected_shops[0].name) + ' ' + str(self.path[-1].connected_shops[1].name))
            
            # Add Shop to the list of shops based on road
            if (road_chosen.connected_shops[0] == self.shops[-1]):
                self.shops.append(road_chosen.connected_shops[1])
            else: 
                self.shops.append(road_chosen.connected_shops[0])
                
        # 3. after getting to the destination, remove the loop within the path, i.e. if there are repeated shops in self.shops, remove the shops and the roads in between the repetition
        self.remove_loopy_paths()
            
        print()
        for i in range(len(self.shops)):
            if (i+1 < len(self.shops)):
                print(self.shops[i].name, end=" -> ")
            else:
                print(self.shops[i].name)
        
    # Removes Loopy Paths in shops and path lists
    def remove_loopy_paths(self):
        while (len(set(self.shops)) != len(self.shops)):   # Repeat process until shops list only contain unique shops
            temp = []
            n = len(self.shops)
            
            for i in range(n):         # used to find the index of similar pairs 
                for j in range(n):
                    if (self.shops[i] == self.shops[j]) and (i < j):
                        if (len(temp) > 0):            # if a duplicate has already been found
                            if (j > temp[-1]):         # if another duplicate is found after the first one 
                                temp = []
                                temp.extend([i,j])     # extend temp list with index of duplicates
                        else:
                            temp.extend([i,j])
                
                if (len(temp) > 0):     # if duplicate found, break out of for loop and address it first
                    break
            
            #print(temp)
            del self.shops[temp[0]: temp[1]]      # remove loopy path
            del self.path[temp[0]: temp[1]]
                
    # Calculate path length of each ant 
    def get_path_length(self):
        # Calculate path length based on self.path
        path_length = 0
        for road in self.path:
            path_length += road.cost
        return path_length
        
    # Clear all paths and shops 
    def reset(self):
        self.path = []
        self.shops = []
       
# Calculate the percentage of the most dominant path 
def get_percentage_of_dominant_path(ants):
    percentage = 0
    frequency = 0
    paths = []
    n = len(ants)
    
    for ant in ants:      # Append all paths into a list
        paths.append(ant.path)
        
    for i in range(len(paths)-1):        # Calculate frequency of most dominant path
        count = 1
        for j in range(i+1, len(paths)):
            if paths[i] == paths[j]:
                count += 1
                if (frequency < count):
                    frequency = count

    percentage = frequency / n
    return percentage

# Return path with most frequency as solution
def get_solution(ants):
    solution_index = 0
    solution = []
    final_paths = []
    temp = []
    n = len(ants)
    
    for ant in ants:     # Append all paths into final_paths list
        final_paths.append(ant.path)
        
    for i in range(n):   # Fill up temp with values from 0 to n
        temp.append(i)
    
    for i in range(n):   # If paths are same, they will have same value in temp 
        for j in range(n):
            if final_paths[i] == final_paths[j] and i < j:
                temp[j] = temp[i]
            
    print(temp)
    solution_index = max(set(temp), key = temp.count)    # get the index of values with highest frequency
    solution.append(final_paths[solution_index])         # list of roads used 
    solution.append(ants[solution_index].shops)         # list of cities 
    solution.append(ants[solution_index].get_path_length())    # path length
    return solution

if __name__ == "__main__":
    location_list = [ # [x,y,name]
      [12, 0, 'Main Entrance'],
      [7, 1, "Ben's Cafe"],
      [12, 4, "South Atrium 1"],
      [17, 4, "Papa Cheah Pharmacy"],
      [6, 7, "Uncle Marcus"],
      [12, 10, "Ming's Iceland"],
      [22, 10, "Toilet 1"],
      [4, 13, 'West Escalator 1'],
      [7, 13, 'West Atrium 1'],
      [18, 13, 'East Atrium 1'],
      [20, 13, 'East Escalator 1'],
      [6, 19, "Ching's Fashion"],
      [12, 21, "North Atrium 1"],
      [18, 21, "Richardson"],
      [12, 24, "Exit"],
      # Level 2
      [6, 5, "Manesh Banana Leaf"],
      [21, 4, "Lucas Fun Time"],
      [12, 7, "South Atrium 2"],
      [2, 10, "Toilet 2"],
      [4, 13, "West Escalator 2"],
      [6, 13, "West Atrium 2"],
      [18, 13, "East Atrium 2"],
      [20, 13, "East Escalator 2"],
      [12, 15, "Alex Swag Wear"],
      [12, 17, "North Atrium 2"],
      [3, 19, "Chee's Electronics"],
      [15, 20, "Elizabeth's Hair Care"]
    ]
    
    step_cost = [
      ['Main Entrance', "Ben's Cafe", 30], ['Main Entrance', "South Atrium 1", 35],
      ['Main Entrance', "Papa Cheah Pharmacy", 45], ["Ben's Cafe", "Papa Cheah Pharmacy", 65],
      ["Ben's Cafe", "South Atrium 1", 55], ["Papa Cheah Pharmacy", "South Atrium 1", 40],
      
      ["South Atrium 1", "Uncle Marcus", 30], ["South Atrium 1", "Ming's Iceland", 15],
      ["South Atrium 1", "Toilet 1", 65], ["South Atrium 1", 'West Atrium 1', 55],
      ["South Atrium 1", 'East Atrium 1', 60], ["Uncle Marcus", "West Atrium 1", 45],
      ["East Atrium 1", "Toilet 1", 35],
      
      ["West Atrium 1", "West Escalator 1", 15], ["East Atrium 1", "East Escalator 1", 10],
      
      ["West Atrium 1", "Ching's Fashion", 45], ["West Atrium 1", "North Atrium 1", 55],
      ["Ching's Fashion", "North Atrium 1", 30], ["North Atrium 1", "Exit", 25],
      ["North Atrium 1", "Richardson", 40], ["Richardson", "Exit", 45],
      ["North Atrium 1", "East Atrium 1", 60],
      
      # Connection ----------------------------
      ["West Escalator 1", "West Escalator 2", 5], ["East Escalator 1", "East Escalator 2", 5], 
      
      # Level 2 - Currently not connected to lvl 1
      ["West Escalator 2", "West Atrium 2", 10], ["East Escalator 2", "East Atrium 2", 10],
      
      ["Manesh Banana Leaf", "South Atrium 2", 40], ["Manesh Banana Leaf", "Toilet 2", 45],
      ["Manesh Banana Leaf", "West Atrium 2", 40], ["Toilet 2", "West Atrium 2", 35],
      ["Toilet 2", "South Atrium 2", 65], ["South Atrium 2", "West Atrium 2", 60],
      
      ["South Atrium 2", "East Atrium 2", 60], ["South Atrium 2", "Lucas Fun Time", 60],
      ["Lucas Fun Time", "East Atrium 2", 60],
      
      ["East Atrium 2", "North Atrium 2", 50],
      
      ["North Atrium 2", "Alex Swag Wear", 10],
      
      ["North Atrium 2", "Elizabeth's Hair Care", 30],
      
      ["North Atrium 2", "West Atrium 2", 50], ["North Atrium 2", "Chee's Electronics", 55],
      ["West Atrium 2", "Chee's Electronics", 45]
    ]
    
    shops = {} # Create dictionary
    for coord1, coord2, name in location_list:
        shops[name] = Shop(name)     # Create Shop objects and place in dictionary
        shops[name].set_coordinates([coord1, coord2])
        
    roads = []
    for shop1, shop2, cost in step_cost:
        road = Road([shops[shop1], shops[shop2]], cost) # Create Road objects
        shops[shop1].add_road(road)
        shops[shop2].add_road(road)                    # Add road between cities to City object
        roads.append(road)
        
    # Define origin and destination shops 
    origin = shops["Main Entrance"]
    destination = shops["Toilet 1"]
    intermediate_shops = [shops["North Atrium 1"]]
    
    # Parameters Initilization
    n_ant = 10
    alpha = 1
    rho = 0.1
    final_paths = []
    solution = []
    # 1.0 Pheromone Initialization
    initial_pheromone = 0.01
    for road in roads:
        road.set_pheromone(initial_pheromone)
    # 2.0 Ants Initialization
    ants = [Ant() for _ in range(n_ant)]      

    # termination threshold
    iteration = 0
    max_iteration = 200
    percentage_of_dominant_path = 0
    min_percentage = 0.9

    # Enter while loop
    while (iteration < max_iteration and percentage_of_dominant_path < min_percentage): # termination conditions
        # loop through all the ants to identify the path of each ant
        for ant in ants:
            # reset the path of the ant
            ant.reset()
            # identify the path of the ant
            ant.get_path(origin, destination, alpha, intermediate_shops)
        # calculate percentage of dominant paths
        percentage_of_dominant_path = get_percentage_of_dominant_path(ants)
        # loop through all roads
        for road in roads:
            # evaporate the pheromone on the road
            road.evaporate_pheromone(rho)
            # deposit the pheromone
            road.deposit_pheromone(ants)
        # increase iteration count
        iteration += 1
      
    # after exiting the loop, return the most occurred path as the solution
    solution = get_solution(ants)
    print('iter', iteration)
    
    print('Solution: ')
    for i in range(len(solution[1])):
            if (i+1 < len(solution[1])):
                print(solution[1][i].name, end=" -> ")
            else:
                print(solution[1][i].name)

    print('Path Cost:', solution[2])
    
