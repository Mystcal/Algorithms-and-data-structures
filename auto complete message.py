#%%
# MaxHeap
class MaxHeap:
    def __init__(self,size = 26) -> None:
        """
        # from pg 33, 34( FIT 2004 course notes)

        Constructor for MaxHeap
        Time Complexity: O( Log L )
        space Complexity: O( L )
        """
        # to store data
        self.array = [None]*(size+1)
        # to serve
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
        res = self.index[1]
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
            if self.array[self.index[parent]][1] < self.array[self.index[element]][1]:
                self.swap(parent,element)
                element = parent
                parent = element // 2
            elif self.array[self.index[parent]][1] == self.array[self.index[element]][1] and self.index[parent] > self.index[element]:
                self.swap(parent,element)
                element = parent
                parent = element // 2
            else:
                break

    def update(self,vtx):
        self.array[vtx][1] += 1
        self.rise(self.array[vtx][2])

# Node for Trie
class Node: 
    def __init__(self, size = 26) -> None:
        """
        Node using in CatsTrie
        complexity: O(1)
        """
        # connection
        self.link = [None] * size
        # for last node, auto complete
        self.terminal = 0 
        self.data = None
        # for collecting preferences
        self.preferences = MaxHeap()

# CatsTrie 
class CatsTrie:
    def __init__(self,sentences:list) -> None:
        self.root = Node()
        """
        initialize the words into the Trie
        Complexity = O( MN )
        """
        for i in sentences:             # complexity = O( N )
            self.insert_recursive(i)    # complexity = O( M )

    # insert function for Cats Trie
    def insert_recursive(self,key):
        """
        insert function to insert Node into the CatsTrie
        Complexity = O(X)
        """
        current = self.root
        if len(key) == 0:
            return 
        else:
            return self.insert_recAux(current,key,0)

    def insert_recAux(self,current, key,i):
        if i == len(key):                   # reached last key
            current.terminal += 1           # update terminal
            current.data = key              # store key
        else:
            index = ord(key[i]) - 97        # a = 0, b = 1
            # if path exist                 
            if current.link[index] != None:             # a --> link[0]
                current.preferences.update(index+1)     # (update heap) a --> prefer.array[1]
                current = current.link[index]           # go to next node
                i += 1
                self.insert_recAux(current,key,i)

            # if no path
            else:
                current.link[index] = Node()            # create node a --> link[0]
                current.preferences.insert(index+1,1)   # (insert to heap) a --> prefer.array[1]
                current = current.link[index]           # go to next node
                i += 1
                self.insert_recAux(current,key,i)
        
    def autoComplete(self,key):
        """
        function use for auto complete the prompt
        complexity = O( Y )
        """
        current = self.root
        return self.search_aux(current,key,0)
        
    def search_aux(self,current,key,i):
        # reached the prompt
        if i == len(key):
            # if input is a sentence
            if current.terminal != 0:           
                if current.preferences.length == 0:
                    return current.data         # return key
                elif current.terminal >= current.preferences.array[current.preferences.serve()][1]:
                    return current.data         # return key
                else:
                    current = current.link[current.preferences.serve()-1]
                    # go to next character
                    i += 1
                    return self.search_aux(current,key,i)
            # if input is not terminal
            else:
                # then go next
                current = current.link[current.preferences.serve()-1]
                i += 1
                return self.search_aux(current,key,i)
        
        # havent reach prompt
        elif i < len(key):
            index = ord(key[i]) - 97        # a = 0
            # if path not exist
            if current.link[index] == None:
                return 
            # if there is path
            else:
                # update current
                current = current.link[index]
                # go to next character
                i += 1
                return self.search_aux(current,key,i)
        # after prompt
        else:
            # if is terminal and >= than go next
            if current.terminal != 0:
                if current.preferences.length == 0: 
                    return current.data

                elif current.terminal >= current.preferences.array[current.preferences.serve()][1]:
                    return current.data
                else:
                    current = current.link[current.preferences.serve()-1]
                    # go to next character
                    i += 1
                    return self.search_aux(current,key,i)
            # if is not terminal, go to next prefer / is terminal but < prefer
            else:
                # get prefernce
                current = current.link[current.preferences.serve()-1]
                # go to next character
                i += 1
                return self.search_aux(current,key,i)