class Adj_list:
    def __init__(self, connect:list, max_in:list, max_out:list, origin, target: list):
        x = 0
        """
        Adjacency list for vertex connection
        Complexity = O( C + D )
        """
        # initialize array
        # complexity = O(D)
        for i in range(len(connect)):
            if x < max(connect[i][0],connect[i][1]):
                x = max(connect[i][0],connect[i][1])
        self.vertices = [None] * (x+2)
        # vertex class for each data centre
        for i in range(len(self.vertices)):
            self.vertices[i] = lst_Vertex(i)
        # input and output for each data centre EXCEPT SUPER TERMINAL NODE
        for i in range(len(self.vertices)-1):
            self.vertices[i].output = min(max_in[i],max_out[i])
            self.vertices[i].input = max_in[i]
        # connection of the data centre
        # complexity = O(C)
        for i in connect:
            self.add_edge(i[0],i[1],min(i[2],self.vertices[i[0]].output,self.vertices[i[1]].output))

        # output of Source == MaxOut
        self.vertices[origin].output = max_out[origin]
        # target output == MaxIn
        for i in target:
            self.vertices[i].output = max_in[i]

        # initialize the super terminal
        self.vertices[x+1].input = max_out[origin]
        self.vertices[x+1].output = max_out[origin]
        # edge from target to super terminal (  x+1 )
        for i in target:
            self.add_edge(i,x+1,self.vertices[i].output)

    def __str__ (self):
        return_str = ""
        for vertex in self.vertices:
            path = ""
            for i in vertex.edges:
                path = path + str(i) + ","
            return_str = return_str + "Vertex " + str(vertex) + " " + "["+ path[:-1] +"]" + str(vertex.input)+"/"+str(vertex.output) +"\n"
        return return_str
    
    def add_edge(self, u, v, w):
        """
        add edges between the vertices
        complexity = O(1)
        """
        vtx = self.vertices[u]
        vtx.edges += [lst_Edge(u,v,w)]

    def modify_edge(self,u,v,w):
        """
        modify the weight of the edges
        Complexity = O(C)
        """
        for x in range(len(self.vertices[u].edges)):
            if self.vertices[u].edges[x].end == v:
                # if connection is full, remove edge  OR    if node is fully occupied, remove edge
                if self.vertices[u].edges[x].connection <= w or self.vertices[v].output == 0:
                    self.vertices[u].edges.pop(x)
                else:
                    self.vertices[u].edges[x].connection -= w
                
                break

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
        # max output of data for a data center to send 
        self.output = 0
        self.input = 0
        # to store the bottleneck
        self.temp = 0
        # backtracking / where i was from
        self.previous = None

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
    def __init__( self, start, end, connect):
        # starting vertex
        self.start = start
        # end vertex
        self.end = end
        self.connection = connect

    def __str__(self):
        return_str = (self.start,self.end,self.connection)
        return str(return_str)
    
# BFS Breath First Search
def bfs(graph:Adj_list,source):
    """
    Breath First Search from source to terminal node
    total time complexity = O( C + D )
    """                
    graph.vertices[source].temp = graph.vertices[source].output     # initialize flow from source
    path = []           # list to store backtrack
    res = []            # path from source to destination
    visit = [None] * len(graph.vertices)    # initialize array for record if visited
    discovered = [None] * len(graph.vertices)   # initialize array for record if discovered
    queue = []                     # discovered a queue
    queue.append(source)
    discovered[source] = True
    destination = ( len(graph.vertices)-1 )
    if graph.vertices[source].output == 0:      # if there is no flow from source, no path
        return False
    
    while len(queue) > 0:
        # serve from 
        u = queue.pop(0)           # pop(0) same as serve
        visit[u] = True
        if u == destination:        # destination found, break the loop
            break
        # time complexity: O(C)
        for edge in graph.vertices[u].edges:    # find the connected edges 
            v = edge.end

            if discovered[v] == None:   # if is not discovered
                
                if v is destination and graph.vertices[destination].input != 0: # if thats the destination and have space for input

                    queue.append(v)
                    discovered[v] = True            # means I have discovered v, adding it to queue
                    graph.vertices[v].previous = u

                    if graph.vertices[u].temp < edge.connection:      # amoount of data that can be transfered
                        if graph.vertices[u].temp < graph.vertices[v].input: # (IN < connect)  < OUT  ==> use IN
                            graph.vertices[v].temp = graph.vertices[u].temp
                        else:                                                   # (IN < connect)  > OUT  ==> use OUT
                            graph.vertices[v].temp = graph.vertices[v].input
                    else:                                                       
                        if edge.connection < graph.vertices[v].input:          # (IN >= connect)  < OUT  ==> use connect
                            graph.vertices[v].temp = edge.connection 
                        else:
                            graph.vertices[v].temp = graph.vertices[v].input   # (IN >= connect)  > OUT  ==> use OUT
                    break
                elif v is destination and graph.vertices[destination].input == 0:   # if is destination but space for input fully occupied, no path
                    return False
                else:                                                  # if is not the destination node
                    if graph.vertices[v].output != 0:       # if that node pass by is not fully occupied
                        queue.append(v)
                        discovered[v] = True            # means I have discovered v, adding it to queue
                        graph.vertices[v].previous = u
                        if graph.vertices[u].temp < edge.connection:      # amount of data that can be transfered
                            if graph.vertices[u].temp < graph.vertices[v].output: # (IN < connect)  < OUT  ==> use IN
                                graph.vertices[v].temp = graph.vertices[u].temp
                            else:                                                   # (IN < connect)  > OUT  ==> use OUT
                                graph.vertices[v].temp = graph.vertices[v].output
                        else:                                                       
                            if edge.connection < graph.vertices[v].output:          # (IN >= connect)  < OUT  ==> use connect
                                graph.vertices[v].temp = edge.connection 
                            else:
                                graph.vertices[v].temp = graph.vertices[v].output   # (IN >= connect)  > OUT  ==> use OUT

    if graph.vertices[destination].previous is None:        # backtrack the path
        return False
    path += [destination]
    # time complexity = O(D)
    while graph.vertices[path[-1]].previous is not None:
        path += [graph.vertices[path[-1]].previous]
    for _ in range(len(path)):                              # reverse the backtrack result to correct order
        res += [path.pop()]
    if res[0] != source:                                    # if the first of the result is not the source
        return False
    for i in res:                                           # if is not visited, return false
        if visit[i] is None:
            return False

    internet_band = graph.vertices[destination].temp        # store the maximum data that can be sent for the path

    return [res,internet_band]

def maxThroughput(connections: list, maxIN: list, maxOut: list, source, target:list):
    """
    Calculate the maximum flow from the source to the targets
    
    Complexity = O( D * C^2 )
    """
    # initialize flow
    flow = 0
    # initialize the residual network
    NetworkFlow = Adj_list(connections,maxIN,maxOut,source,target)
    if NetworkFlow.vertices[source].output == 0:
        return flow
        # complexity = O( C + D )
    have_flow = bfs(NetworkFlow,source)
    while have_flow:        # if there is a path
        # complexity= O( C )
        #take the path
        path = have_flow[0]
        # Bottleneck
        bottle_value = have_flow[1]

        #augment the flow equal to the residual capacity
        flow += bottle_value
        # updating the residual network
        # complexity: O( D )
        # for path before destination
        for i in path[:-1]:                                 
            if NetworkFlow.vertices[i].output > bottle_value:       #   if bottleneck smaller than output
                NetworkFlow.vertices[i].output -= bottle_value          #   output - bottleneck ==> output residual decrease   
                NetworkFlow.vertices[i].input -= bottle_value           #   input - bottleneck  ==> input residual decrease
            else:                                                   # if bottleneck larger or equal to output
                NetworkFlow.vertices[i].output = 0                      #   ouput fully occupied
                NetworkFlow.vertices[i].input = 0                       #   input fully occupied
        # for destination
        if NetworkFlow.vertices[path[-1]].input > bottle_value:     #   if bottleneck smaller than input
            NetworkFlow.vertices[path[-1]].input -= bottle_value        #   input - bottleneck  ==> input residual decrease
            NetworkFlow.vertices[path[-1]].output -= bottle_value       #   output - bottleneck ==> output residual decrease
        else:                                                       #   if bottleneck larger or equal to input
            NetworkFlow.vertices[path[-1]].input = 0                    #   input fully occupied
            NetworkFlow.vertices[path[-1]].output = 0                   #   ouput fully occupied
        # update the values in edge
        # complexity = O( D )
        for j in range(len(path)-1):
            # complexity = O( C)
            NetworkFlow.modify_edge(path[j],path[j+1],bottle_value)
        # complexity= O(C + D)
        have_flow = bfs(NetworkFlow,source)

    return flow
