#Function description:
#
#Function input:
#   GDB.txt: a txt file which saves the data of the graph in a certain format
#
#Function output:
#   GDB.dot: a dot file to save the simplified graph after using abstraction method 3
#   GDB.pdf: a pdf file to display the simplified graph
#
#Related methods:
#   abstraction method 3: we do replication when a replication is needed
#                           and we only replicate a node at a time
#
#Meaning of the number of the state -- IsVisited: 
#   0: a node that has not been visited;
#   1: a node that has already been visited


import subprocess
ALLNodeList = dict()#dictionary for saving the existence of nodes
class Node:
    "'node for the graph'"
    def __init__(self,Addr):
        self.Addr = Addr
        self.FList = []
        self.CList = []
        self.IsVisited = 0#it is a sign showing whether this node has been visited or not
    def add_FList(self,Node):
        self.FList.append(Node)
    def add_CList(self,Node):
        self.CList.append(Node)
class Stack:
    "'Stack for DFS'"
    def __init__(self):
        self.Array = []
    def IsEmpty(self):
        return len(self.Array) == 0
    def Push(self,node):
        self.Array.append(node)
    def Pop(self):
        return self.Array.pop()
    
if __name__ == "__main__":

    # This first part is for reading the data from the disk into the memory
    fread = open("GDB.txt",'r')
    Database = fread.readlines()
    fread.close()
    i = 0
    while i < len(Database):
        CurrentNode = ALLNodeList.setdefault(eval(Database[i]),Node(eval(Database[i])))
        i = i + 1
        SaveFathers = Database[i][0:len(Database[i])-2].split(' ')
        if SaveFathers <> ['']:
            for m in range(len(SaveFathers)):
                F = ALLNodeList.setdefault(eval(SaveFathers[m]),Node(eval(SaveFathers[m])))
                CurrentNode.add_FList(F)
        else:
            FirstNode = CurrentNode
        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                C = ALLNodeList.setdefault(eval(SaveChildrens[m]),Node(eval(SaveChildrens[m])))
                CurrentNode.add_CList(C)
        i = i + 1
    # The code above is for reading the data from the disk to the memory
    
    # 0: a node is not in the stack and has not been visited; 1: a node is in the stack but has not been visited
    # 2: a node is not in the stack but is currently being visited; 3: a node is not in the stack but has already been visited 

    MyStack = Stack()
    CurrentNode = FirstNode
    MyStack.Push(CurrentNode)
    IsSimplable = 0
    while MyStack.IsEmpty() <> True and IsSimplable == 0:
        CurrentNode = MyStack.Pop()
        CurrentNode.IsVisited = 1
        if len(CurrentNode.CList) <> 0:  #if this node is an endpoint of current visiting branch
            for node in CurrentNode.CList:
                if node.IsVisited == 1:
                    # we find a case where a replication is needed
                    RepNode = Node(node.Addr + 1) # it's difficult to assign a new address to the created node, since there is another same address, so we simply + 1
                    
                    node.FList.remove(CurrentNode)
                    CurrentNode.CList.remove(node)
                    
                    RepNode.FList = [CurrentNode] # we set proper father
                    CurrentNode.CList.append(RepNode)
                    
                    RepNode.CList = node.CList
                    for cnode in node.CList:
                        cnode.FList.append(RepNode)
                    
                    ALLNodeList.setdefault(RepNode.Addr,RepNode)
                    IsSimplable = 1
                    break
                else:
                    MyStack.Push(node)

                    
# The following part is for output rightly
filename = 'GDB.dot'

file_object = open(filename,'w')
file_object.write('digraph G{ \n')
i = 1
NumList = dict()
for ele1,ele2 in ALLNodeList.items():
    file_object.write('\tnode'+ '%d' %i + '[label = "%X"]' %ele1 +';\n')
    NumList[ele1] = i
    i += 1
file_object.write('\n')
for ele1,ele2 in ALLNodeList.items():
    for f in ele2.CList:
        file_object.write('\tnode%d' %NumList[ele1] + ' -> ' + 'node%d' %NumList[f.Addr] +'\n')
file_object.write('}')
file_object.close()
subprocess.Popen('xdot '+filename,shell = True) 
subprocess.Popen('dot -Tpdf -o '+ 'GDB.pdf ' + filename,shell = True)     





