# FIT2004 ASSIGNMENT 1
# STUDENT ID: 32637888
#%%
# Question 1
# Adjacency List
class Adj_list:
    """
    This class initialise the roads into an Adjacecy list.
    Then The lst_Edge class stores the vertices connected and the time needed between the vertices

    Precondition: list cannot be None
    Postcondition: output the list contain lst_Vertex , lst_Vertex.edge contain lst_Edge or empty list

    Input:
        passengers: [2]
        roads: [(2,3,4,1),(1,2,3,4)]
    Return:
        [lst_Vertex(1),
        lst_Vertex(2),
        lst_Vertex(3)]

        lst_Vertex(1).edges = [lst_Edge(1,2,3,4)]
        lst_Vertex(2).edges = [lst_Edge(2,3,4,1)]
        lst_Vertex(3).edges = []
        lst_Vertex(2).passenger = True

    Time complexity: 
        Best: O( R + L + P )
        Worst: O( R + L + P )

    Space complexity: 
        Input: O( R )
        Aux: O( L+R )

    """
    def __init__(self,road,passengers):
        # find the largest vertex
        # time complexity: O(R)
        temp = road[0][1]
        for i in range(len(road)):
            if temp < road[i][1]:
                temp = road[i][1]

        for i in range(len(road)):
            if temp < road[i][0]:
                temp = road[i][0]
        
        # initialise the array
        self.vertices = [None] * (temp + 1)
        # input vertex included
        # time complexity : O( L )
        # space complexity: O( L )
        for i in range(len(self.vertices)):
            self.vertices[i] = lst_Vertex(i)
        # input the connection between edges
        # space complexity: O( R )
        # time complexity : O( R )
        for i in road:
            self.add_edge(i[0],i[1],i[2],i[3])
        # update the vertex that has passengers
        # time complexity: O( P )
        for i in passengers:
            self.vertices[i].passenger = True
        
    def __str__ (self):
        return_str = ""
        for vertex in self.vertices:
            path = ""
            for i in vertex.edges :
                path = path +  str(i) + "," 
            return_str += "Vertex " + str(vertex) + " " + "[" + path[:-1] + "]" + "\n"
        return return_str

    def add_edge(self, u, v, x, y):
        self.vertices[u].edges += [lst_Edge(u,v,x,y)]  

# Class Vertex
class lst_Vertex:
    """
    this class stores data for each vertex

    Time complexity: 
        Best: O( 1 )
        Worst: O( 1 )

    Space complexity: 
        Input: O( 1 )
        Aux: O( 1 )

    """
    def __init__( self, id):
        self.id = id
        # list of edges
        self.edges = []
        # distance
        self.distance = 0
        # for traversal
        self.discovered = False
        # check is the vertex visited
        self.visited = False
        # backtracking / where i was from
        self.previous = None
        # note there is passenger at that vertex
        self.passenger = False
        self.toll = False   # check if there is passenger in the car

    def __str__(self) -> str:
        return_str = str(self.id)
        return return_str

# Class Edge
class lst_Edge:
    """
    this class stores data for each road

    Time complexity: 
        Best: O( 1 )
        Worst: O( 1 )
    Space complexity: 
        Input: O( 1 )
        Aux: O( 1 )

    """
    def __init__( self, start, end, one, carpool):
        # starting vertex
        self.start = start
        # end vertex
        self.end = end
        # time needed for no passenger fetched lane
        self.one = one
        # time needed for passenger fetched lane
        self.carpool = carpool

    def __str__(self):
        return_str = (self.start,self.end,self.one,self.carpool)
        return str(return_str)

# MinHeap
class MinHeap:
    def __init__(self,size) -> None:
        """
        # from pg 33, 34( FIT 2004 course notes)

        Constructor for MinHeap
        Time Complexity: O( Log L )
        space Complexity: O( L )
        """
        self.array = [None]*(size+1)
        self.index = [None]
        self.length = 0

    def __str__(self) -> str:
        return str(self.index)

    def insert(self,vertex,distance):
        if vertex in self.index:
            print("Error: duplicate vertex detected, vertex " + vertex + " exist !")
            return
        self.length += 1
        self.array[vertex] = [vertex,distance,self.length]
        self.index.append(vertex)
        self.rise(self.length)

    def serve(self):
        """
        Removes and returns the smallest number in the minheap's array
        time complexity: O(Log V), where V is the number of elemnts in minheap's array
        """
        self.swap(1,self.length)
        self.length -= 1
        self.sink(1)
        res = self.index.pop()
        self.array[res] = None
        return res
    
    def swap(self,x,y):
        """
        swap two number's position in the minheap array
        Time Complexity: O(1)
        """
        self.array[self.index[x]][2], self.array[self.index[y]][2] = y, x
        self.index[x],self.index[y] = self.index[y],self.index[x]

    def rise(self, element):
        """
        Adjust the position of the number accordingly with the other number, if parent's number is bigger, swap parent number with current number
        Time complexity: O(Log V), where V is the number of elements in minheap's array
        """
        parent = element // 2
        while parent >= 1:
            if self.array[self.index[parent]][1] > self.array[self.index[element]][1]:
                self.swap(parent,element)
                element = parent
                parent = element // 2
            else:
                break

    def sink(self,element):
        """
        Adjusts the position of the number accordingly with the other number. If parent number is smaller, swap parent number with the current number
        Time Complexity: O(Log V), where V is the number of elements in minheap's array
        """
        child = 2*element
        while child <= self.length:
            if child < self.length and self.array[self.index[child+1]][1] < self.array[self.index[child]][1]:
                child += 1
            if self.array[self.index[element]][1] > self.array[self.index[child]][1]:
                self.swap(element, child)
                element = child
                child = 2*element
            else: 
                break

    def update(self,vtx,w):
        if self.array[vtx][1] > w:
            self.array[vtx][1] = w
            self.rise(self.array[vtx][2])

# Dijkstra
def Dijkstra(source, destination, map1:Adj_list, map2:Adj_list):
    """
    # Idea from FIT 2004 lecture 5 
    
    This function find the fastst path from the source to the destination

    Precondition: map1 and map2 list cannot be None or empty, source and destination must be in map1 or map2
    Postcondition: discovered( minHeap) must be empty

    Input:
        roads = [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
                (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20)]
        start = 0
        end = 4
        passengers = [2, 1]
        map1 = Adj_list(roads)
        map2 = Adj_list(roads)

    Return:
        [0, 3, 2, 0, 3, 4]
        
    Time complexity: 
        Best: O( R logL )
        Worst: O( R logL )

    Space complexity: 
        Input: O( L+R )
        Aux: O( L )

    """
    path = []                                   # for tracing the path from the dextination
    res = []                                    # for the path from the source
    dist = 0                                    # distance for the source
    discovered = MinHeap(len(map1.vertices))     # discovered a queue
    discovered.insert(source, dist)              # append(key, data)

    while discovered.length > 0:
        # serve from
        u = discovered.serve()  
        # Serve: O(log L)
        # means I have visit u
        if map2.vertices[u].toll == True:
            map2.vertices[u].visited = True
        else:
            map1.vertices[u].visited = True         
        # reached destination
        if u == destination:            
            break
        # fetched a person
        if map2.vertices[u].toll == True:
            # perform edge relaxation on all adjacent vertices
            for edge in map2.vertices[u].edges:
            # O(R)
                v = edge.end
                # previous cumilated distance (map2 -> map2)
                start_distance = map2.vertices[u].distance
                if map2.vertices[v].discovered == False:   # means distance is sill infinity
                    map2.vertices[v].toll = True
                    map2.vertices[v].distance = start_distance + edge.carpool
                    if discovered.array[v] != None:        # if is in heap, update
                        discovered.update(v,map2.vertices[v].distance)
                    else: 
                        discovered.insert(v,map2.vertices[v].distance)
                    map2.vertices[v].discovered = True     # means I have discovered v, adding it to queue
                    map2.vertices[v].previous = u  
                # it is in Heap, but not yet finalise
                elif map2.vertices[v].visited == False:
                    if map2.vertices[v].distance > start_distance + edge.carpool:
                        #update distance
                        map2.vertices[v].distance = start_distance + edge.carpool
                        map2.vertices[v].previous = u
                        # update vertex v in heap with distance v.distance (smaller); perform upheap
                        discovered.update(v, map1.vertices[v].distance)
        # there is a passenger
        elif map1.vertices[u].passenger == True:
            map2.vertices[u].discovered = True
            map2.vertices[u].toll = True
            map2.vertices[u].visited = True
            # perform edge relaxation on all adjacent vertices
            for edge in map2.vertices[u].edges:
            # O(R)
                v = edge.end
                # previous cumilated distance (map1 -> map2)
                start_distance = map1.vertices[u].distance
                if map2.vertices[v].discovered == False:   # means distance is sill infinity
                    if map1.vertices[v].discovered == True: # if is in heap, update
                        if map1.vertices[v].distance > start_distance + edge.carpool:
                            map2.vertices[v].toll = True
                            map2.vertices[v].distance = start_distance + edge.carpool
                            discovered.update(v,map2.vertices[v].distance)
                            map2.vertices[v].discovered = True     # means I have discovered v, adding it to queue
                            map2.vertices[v].previous = u
                    else:   # if not in heap, insert
                        map2.vertices[v].toll = True
                        map2.vertices[v].distance = start_distance + edge.carpool
                        discovered.insert(v,map2.vertices[v].distance)
                        map2.vertices[v].discovered = True     # means I have discovered v, adding it to queue
                        map2.vertices[v].previous = u

                # it is in Heap, but not yet finalise
                elif map2.vertices[v].visited == False:
                    if map2.vertices[v].distance > start_distance + edge.carpool:
                        #update distance
                        map2.vertices[v].distance = start_distance + edge.carpool
                        map2.vertices[v].previous = u
                        # update vertex v in heap with distance v.distance (smaller); perform upheap
                        discovered.update(v, map1.vertices[v].distance)
        else:        
            if map1.vertices[u].edges == None:
                continue
            # perform edge relaxation on all adjacent vertices
            for edge in map1.vertices[u].edges:

            # O(V)
                v = edge.end
                start_distance = map1.vertices[edge.start].distance
                if map1.vertices[v].discovered == False:   # means distance is sill infinity
                    if map2.vertices[v].toll == True:
                        if map2.vertices[v].distance > start_distance + edge.one:
                            map2.vertices[v].toll = False
                            map1.vertices[v].distance = start_distance + edge.one
                            discovered.update(v,map1.vertices[v].distance)
                            map1.vertices[v].discovered = True
                            map1.vertices[v].previous = u
                    else:        
                        map1.vertices[v].distance = start_distance + edge.one
                        discovered.insert(v,map1.vertices[v].distance)
                        map1.vertices[v].discovered = True     # means I have discovered v, adding it to queue
                        map1.vertices[v].previous = u

                # it is in Heap, but not yet finalise
                if map1.vertices[v].visited == False:
                    if map2.vertices[v].toll == True:
                        if map2.vertices[v].distance > start_distance + edge.one:
                            map2.vertices[v].toll = False
                            map1.vertices[v].distance = start_distance + edge.one
                            discovered.update(v,map1.vertices[v].distance)
                            map1.vertices[v].discovered = True
                            map1.vertices.previous = u
                            map2.vertices[v].toll = False
                    else:
                        if map1.vertices[v].distance > start_distance + edge.one:
                        #update distance
                            map1.vertices[v].distance = start_distance + edge.one
                            map1.vertices[v].previous = u
                            # update vertex v in heap with distance v.distance (smaller); perform upheap
                            discovered.update(v, map1.vertices[v].distance)

    # backtrack 
    path += [ destination ]
    # time complexity: O( R)
    # space complexity: O( R)
    while map2.vertices[path[-1]].toll == True and map2.vertices[path[-1]].previous != None:
        path += [ map2.vertices[path[-1]].previous ]
    while map1.vertices[path[-1]].previous != None:
        path += [ map1.vertices[path[-1]].previous ]

    # reverse the path (path gives the trace from destination to source)
    # time complexity: O( R)
    # space complexity: O( R)
    for _ in range(len(path)):
        res += [path.pop()]

    return res

# optimalRoute
def optimalRoute(start, end, passengers:list, roads:list):
    """
    This function find the fastst path from the source to the destination

    Precondition: length of roads must be larger than 0, start and end must be in roads, passengers must be in roads

    Input:
        roads = [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
                (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20)]
        start = 0
        end = 4
        passengers = [2, 1]

    Return:
        [0, 3, 2, 0, 3, 4]
        
    Time complexity: 
        Best: O( R logL )
        Worst: O( R logL )
    Space complexity: 
        Input: O( R )
        Aux: O( L + R )

    """
    # Time complexity: O( R + logL )
    # space complexity Aux: O( L+R )
    x = Adj_list(roads,passengers)
    y = Adj_list(roads,passengers)
    # Time complexity: O( R logL )
    # space complexity Aux: O( 1 )
    return Dijkstra( start, end, x, y)



# Question 2
# Node class for every position
class Node:
    """
    time complexity: O( 1)
    space complexity: O( 1)
    """
    def __init__(self, prob, x, y) -> None:
        self.id = (x,y)                     # id 
        self.prob = prob                    # probability
        self.prev = None                    # previous node
        self.sum = 0                        # minimum sum from the start

    def __str__(self) -> str:
        res = self.sum
        return res

# function to arrange the "occupancy_probability" for selection use
def arrange(occupancy_probability: list):
    """
    this function initialize the array with Nodes for each position

    Precondition: list cannot be None
    Postcondition: output the nested list contain Node

    Input:
        occupancy_probability = [[31, 54, 94, 34, 12],
                                [26, 25, 24, 16, 87],
                                [39, 74, 50, 13, 82],
                                [42, 20, 81, 21, 52],
                                [30, 43, 19, 5, 47],
                                [37, 59, 70, 28, 15],
                                [ 2, 16, 14, 57, 49],
                                [22, 38, 9, 19, 99]]

    Return:
        [[Node(0,0), Node(0,1), Node(0,2), Node(0,3), Node(0,4)],
        [Node(1,0), ...],
        ...
        ...
        [Node(7,0), Node(7,1), Node(7,2), Node(7,3), Node(7,4)]]
        
    Time complexity: 
        Best: O( MN )
        Worst: O( MN )

    Space complexity: 
        Input: O( MN )
        Aux: O( MN )

    """
    # initialize array
    # space complexity: O(N)
    office = [None]* len(occupancy_probability)
    width = len(occupancy_probability[0])
    # initialise array column
    for i in range(len(office)): 
        # space complexity: O(M)
        office[i] = [None]*width
    # total space complexity: O( NM)
    # initialise array row
    for i in range(len(office)):
        # O(N)
        for j in range(width):
            # O(M)
            office[i][j] = Node(occupancy_probability[i][j],i,j)
    # input the occupancy probability for each position
    for i in range(width):
        office[0][i].sum = office[0][i].prob
    return office

# function for traverse the whole graph to find minimum probability and path used
def selection(office = list):
    """
    this function gives the minimum sum and the path of the minimum sum. 

    Precondition: office input cannot be None or empty
    Postcondition: len(res) == 0, len(return_res) == N, previous of every location is not None

    Input:
        arrange(occupancy_probability = [[31, 54, 94, 34, 12],
                                        [26, 25, 24, 16, 87],
                                        [39, 74, 50, 13, 82],
                                        [42, 20, 81, 21, 52],
                                        [30, 43, 19, 5, 47],
                                        [37, 59, 70, 28, 15],
                                        [ 2, 16, 14, 57, 49],
                                        [22, 38, 9, 19, 99]])

    Return:
        [118, [(0, 4), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 2), (7, 2)]]
        
    Time complexity: 
        Best: O( MN )
        Worst: O( MN )
    Space complexity: 
        Input: O( MN )
        Aux: O( N)

    """
    res = []        # for trace from the last location
    return_res = [] # revert the res so that the path starts from the first row
    # traverse the whole graph for the shortest path
    for i in range(len(office)-1):
        # time complexity: O( m)
        for j in range(len(office[0])):
            # time complexity: O( n)
            office[i+1][j].sum = office[i+1][j].prob + office[i][j].sum 
            office[i+1][j].prev = office[i][j].id
            # if the position is at most left,  can only move up and up right
            if j == 0 and (j+1) <= len(office[0])-1 :
                # if the up right is smaller than the up, update the prev and the sum
                if office[i+1][j].sum > office[i+1][j].prob + office[i][j+1].sum:
                    office[i+1][j].sum = office[i+1][j].prob + office[i][j+1].sum
                    office[i+1][j].prev = office[i][j+1].id
            # if the position is at most right, can only move up and up left
            elif j == ( len(office[0])-1 ) and ( j-1 ) >= 0:
                # if up left is smaller than the up, update the prev and the sum
                if office[i+1][j].sum > office[i+1][j].prob + office[i][j-1].sum:
                    office[i+1][j].sum = office[i+1][j].prob + office[i][j-1].sum
                    office[i+1][j].prev = office[i][j-1].id
            # else if the position is between the most right and most left,
            else:
                # check if there is left and right
                if ( j-1 ) >= 0 and (j+1) <= len(office[0])-1:
                    # if up left is smaller than the up, update the prev and the sum
                    if office[i+1][j].sum > office[i+1][j].prob + office[i][j-1].sum:
                        office[i+1][j].sum = office[i+1][j].prob + office[i][j-1].sum
                        office[i+1][j].prev = office[i][j-1].id
                    # if the up right is smaller than the up, update the prev and the sum
                    if office[i+1][j].sum > office[i+1][j].prob + office[i][j+1].sum:
                        office[i+1][j].sum = office[i+1][j].prob + office[i][j+1].sum
                        office[i+1][j].prev = office[i][j+1].id

    # find the end location of the shortest path
    min = office[-1][0].sum
    end = office[-1][0].id
    for i in range(len(office[-1])-1):
        if office[-1][i+1].sum < min:
            min = office[-1][i+1].sum
            end = office[-1][i+1].id
    
    res.append(end)
    # backtracking
    # time complexity: O( N)
    # space complexity Aux: O( N)
    while office[res[-1][0]][res[-1][1]].prev != None :
        res.append( office[res[-1][0]][res[-1][1]].prev )
    # time complexity: O( N)
    # space complexity Aux: O( N)
    while len(res) != 0:
        return_res.append(res.pop())
    return [min,return_res]
        
# function for ans
def select_sections(lst= list):
    """
    this function modify the input by using funciton arrange 
    and input the result for function selection

    Precondition: lst cannot be empty or None

    Input:
    occupancy_probability = [[31, 54, 94, 34, 12],
                            [26, 25, 24, 16, 87],
                            [39, 74, 50, 13, 82],
                            [42, 20, 81, 21, 52],
                            [30, 43, 19, 5, 47],
                            [37, 59, 70, 28, 15],
                            [ 2, 16, 14, 57, 49],
                            [22, 38, 9, 19, 99]]

    Return:
        [118, [(0, 4), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 2), (7, 2)]]
        
    Time complexity: 
        Best: O( MN )
        Worst: O( MN )
    Space complexity: 
        Input: O( MN )
        Aux: O( MN)
    """
    # time complexity: O( MN )
    # space complexity Aux: O( MN )
    office = arrange(lst)
    # time complexity : O( MN )
    # space complexity Aux: O( 1)
    return selection(office)
