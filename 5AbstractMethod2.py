#Function description:
#
#Function input:
#   GDB.txt: a txt file which saves the data of the graph in a certain format
#
#Function output:
#   GDB.dot: a dot file to save the simplified graph after using abstraction method 2
#   GDB.pdf: a pdf file to display the simplified graph
#
#Related methods:
#   abstraction method 2: we can use it to simplify a loop, namely, we merge all the node inside a loop into a single node,
#                           and at the same time we don't change the basic relationship of father and children
#
#Function mechanism:
#   we abstract a loop at a time. We use a special DFS to detect a loop and then we begin to abstract it as soon as we find one
#
#Meaning of the number of the state -- IsVisited: 
#   0: a node is not in the stack and has not been visited;
#   1: a node is in the stack but has not been visited
#   2: a node is not in the stack but is currently being visited;
#   3: a node is not in the stack but has already been visited

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
        CurrentNode = ALLNodeList.setdefault(int(Database[i],16),Node(int(Database[i],16)))
        i = i + 1
        SaveFathers = Database[i][0:len(Database[i])-2].split(' ')
        if SaveFathers <> ['']:
            for m in range(len(SaveFathers)):
                F = ALLNodeList.setdefault(int(SaveFathers[m],16),Node(int(SaveFathers[m],16)))
                CurrentNode.add_FList(F)
        else:
            FirstNode = CurrentNode
        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                C = ALLNodeList.setdefault(int(SaveChildrens[m],16),Node(int(SaveChildrens[m],16)))
                CurrentNode.add_CList(C)
        i = i + 1
    # The code above is for reading the data from the disk to the memory
    
    # 0: a node is not in the stack and has not been visited; 1: a node is in the stack but has not been visited
    # 2: a node is not in the stack but is currently being visited; 3: a node is not in the stack but has already been visited 

    MyStack = Stack()
    CurrentNode = FirstNode
    MyStack.Push(CurrentNode)
    label = 1
    while MyStack.IsEmpty() <> True and label == 1:
        CurrentNode = MyStack.Pop()
        CurrentNode.IsVisited = 2
        IfFinished = 1 # 1 represents that this branch has been finished visiting
        if len(CurrentNode.CList) <> 0:  #if this node is an endpoint of current visiting branch
            for node in CurrentNode.CList:
                
                if node.IsVisited == 2:
                    # we find a loop and then we should begin to abstract this loop into a single node
                    RepNode = Node(node.Addr)

                    # This part is for ensuring that only those inside a loop can be marked with '2' and then being abstracted
                    bnode = FirstNode
                    while bnode <> node:
                        if bnode.IsVisited == 2:
                            bnode.IsVisited = 4
                        for fnode in bnode.CList:
                            if fnode.IsVisited == 2:
                                bnode = fnode

                    # This part is for judging whether a loop is detected, if true, we exert abstraction of that loop, please be noted that only one loop is abstracted at a time           
                    for t,snode in ALLNodeList.items():
                        if snode.IsVisited == 2:
                            for fnode in snode.FList:
                                if fnode.IsVisited <> 2:
                                    fnode.CList.remove(snode)
                                    if fnode.CList.count(RepNode) == 0:
                                        fnode.CList.append(RepNode)
                                        RepNode.FList.append(fnode)
                            RepNode.FList = list(set(RepNode.FList))
                            for cnode in snode.CList:
                                if cnode.IsVisited <> 2:
                                    cnode.FList.remove(snode)
                                    if cnode.FList.count(RepNode) == 0:
                                        cnode.FList.append(RepNode)
                                        RepNode.CList.append(cnode)
                            RepNode.CList = list(set(RepNode.CList))
                            del ALLNodeList[snode.Addr]
                    ALLNodeList[RepNode.Addr] = RepNode
                    label = 0
                    break
                
                elif node.IsVisited == 0:
                    node.IsVisited = 1
                    MyStack.Push(node)
                    IfFinished = 0 # we shall mark that current branch can be extended
                    
        # when current branch is finished, we have to create new branch or choose to stop        
        if IfFinished == 1:# If current branch has been finished
            if MyStack.IsEmpty():
                node = FirstNode
                node.IsVisited = 3 # we search from root
            else:#we begin to mark those nodes that should be marked as 3
                node = MyStack.Array[-1]
                for fnode in node.FList:
                    if fnode.IsVisited == 2:
                        node = fnode
                        break
                #node = node.FList[0]#curently we only consider the case where this node has only one father &&&&
            while node.CList <> []:# we keep search from this node,this search is to change state 2 to 3
                if node.CList[0].IsVisited == 2:
                    node = node.CList[0]
                    node.IsVisited = 3
                elif len(node.CList) == 2 and node.CList[1].IsVisited == 2:
                    node = node.CList[1]
                    node.IsVisited = 3
                else: 
                    break

    for t,node in ALLNodeList.items():
        node.IsVisited = 0 #reset sign



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





