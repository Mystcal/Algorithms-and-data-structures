#%%
# Adjacency List
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
