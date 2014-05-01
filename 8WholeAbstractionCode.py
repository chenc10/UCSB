#function description:
#function input:
#   GDB.txt: a txt file which saves the data of the graph in a certain format
#function output:
#   GDB.dot: a dot file to save the simplified graph after using abstraction algorithm
#   GDB.pdf: a pdf file to display the simplified graph
#Here is the algorithm about the order of pre-operation and abstraction methods:
#       begin
#         using pre-operation method 1 to modify CFG
#         using pre-operation method 2 to modify CFG
#         Do While CFG has been changed
#           Do While CFG has been changed
#               using abstraction method 1 to abstract CFG;
#           EndWhile
#           using abstraction method 2 to abstract CFG;
#           using pre-operation method 1 to modify CFG;
#         EndWhile
#         Do While CFG has been changed
#           Do While CFG has been changed
#            using abstraction method 1 to abstract CFG;
#           EndWhile
#           using abstraction method 3 to abstract CFG;
#         EndWhile
#       End   

import subprocess
ALLNodeList = dict()#dictionary for saving the existence of nodes
TreeRootList = dict()
class TreeRoot:
    "'Tree inside node'"
    def __init__(self,Addr,IsLeaf):
        self.IfLoop = 0
        self.TCList = []
        self.Addr = Addr
        if IsLeaf:
            self.NumOfNodes = 1
        else:
            self.NumOfNodes = 0
        self.TreeRootListSeqNum = len(TreeRootList)
        TreeRootList[self.TreeRootListSeqNum] = self
    def Tadd_CList(self,TreeRoot,AbstractMethod):
        print '%d ' %self.TreeRootListSeqNum 
        print '\t%d' %TreeRoot.TreeRootListSeqNum
        self.TCList.append(TreeRoot)
        if AbstractMethod:
            self.IfLoop = 1
        self.NumOfNodes = self.NumOfNodes + TreeRoot.NumOfNodes
class Node:
    "'node for the graph'"
    def __init__(self,Addr,IsLeaf = 1):
        self.Addr = Addr
        self.FList = []
        self.CList = []
        self.IsVisited = 0#it is a sign showing whether this node has been visited or not
        self.TreeRoot = TreeRoot(Addr,IsLeaf)
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

######################################################################################################################################
#   ReadDataFromFile: get data from GDB.txt
#
    fread = open("GDB.txt",'r')
    Database = fread.readlines()
    fread.close()
    i = 0
    ReturnNode = []
    while i < len(Database):#we should make address * 10
        if not ALLNodeList.has_key(int(Database[i],16)):
            ALLNodeList[int(Database[i],16)] = Node(int(Database[i],16))
        CurrentNode = ALLNodeList[int(Database[i],16)]
        #CurrentNode = ALLNodeList.setdefault(int(Database[i],16),Node(int(Database[i],16)))
        i = i + 1
        SaveFathers = Database[i][0:len(Database[i])-2].split(' ')
        if SaveFathers <> ['']:
            for m in range(len(SaveFathers)):
                if not ALLNodeList.has_key(int(SaveFathers[m],16)):
                    ALLNodeList[int(SaveFathers[m],16)] = Node(int(SaveFathers[m],16))
                F = ALLNodeList[int(SaveFathers[m],16)]
                #F = ALLNodeList.setdefault(int(SaveFathers[m],16),Node(int(SaveFathers[m],16)))
                CurrentNode.add_FList(F)
        else:
            FirstNode = CurrentNode
        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                if not ALLNodeList.has_key(int(SaveChildrens[m],16)):
                    ALLNodeList[int(SaveChildrens[m],16)] = Node(int(SaveChildrens[m],16))
                C = ALLNodeList[int(SaveChildrens[m],16)]
                #C = ALLNodeList.setdefault(int(SaveChildrens[m],16),Node(int(SaveChildrens[m],16)))
                CurrentNode.add_CList(C)
        else:
            ReturnNode.append(CurrentNode)
        i = i + 1
        
######################################################################################################################################
#   PreOperationMethod1
#
    for t,node in ALLNodeList.items():
        # here we assume that there is only a node that has more than two children in a function
        if len(node.CList) > 2:
            print "pre-operation method 1 is being used\n"
            while len(node.CList) > 2:
                RepNode = Node(node.Addr + 1)
                for cnode in node.CList:
                    if cnode == node.CList[0]:
                        continue
                    cnode.FList.remove(node)
                    cnode.FList.append(RepNode)
                    RepNode.CList.append(cnode)
                node.CList = [node.CList[0],RepNode]
                RepNode.FList = [node]
                node = RepNode
            break

######################################################################################################################################
#   PreOperationMethod2
#
    if len(ReturnNode) > 1:
        print "pre-operation method 2 is being used\n"
        RepNode = Node(ReturnNode[0].Addr + 1)
        RepNode.FList = ReturnNode
        for node in ReturnNode:
            node.CList = [RepNode]


######################################################################################################################################
# take turns to use AbstractMethod1 and AbstractMethod2
#
    IsSimplable = 1
    while IsSimplable == 1:
        
    ###################################################################
    #   AbstractMethod1:
    #
        while IsSimplable == 1:
            IsSimplable = 0
            for t,node in ALLNodeList.items():
                if len(node.CList) == 2:
                    if len(node.CList[0].CList) == 1 and len(node.CList[1].CList) == 1 and len(node.CList[0].FList) == 1 and len(node.CList[1].FList) == 1:
                        if node.CList[0].CList[0] == node.CList[1].CList[0]:
                            RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                            RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                            RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot,0)
                            RepNode.TreeRoot.Tadd_CList(node.CList[1].TreeRoot,0)
                            #print RepNode.TreeRoot.TreeRootListSeqNum+'->'+node.TreeRoot.TreeRootListSeqNum+'&'+node.CList[0].TreeRoot.TreeRootListSeqNum+'&'+node.CList[1].TreeRoot.TreeRootListSeqNum
                            del ALLNodeList[node.Addr]
                            del ALLNodeList[node.CList[0].Addr]
                            del ALLNodeList[node.CList[1].Addr]
                            for fnode in node.FList:
                                fnode.CList.remove(node)
                                fnode.CList.append(RepNode)
                            RepNode.FList = node.FList
                            NextNode = node.CList[0].CList[0]
                            RepNode.CList = [NextNode]
                            NextNode.FList.remove(node.CList[0])
                            NextNode.FList.remove(node.CList[1])
                            NextNode.FList.append(RepNode)
                            ALLNodeList[RepNode.Addr] = RepNode
                            IsSimplable = 1
                            break
                        
            for t,node in ALLNodeList.items():
                if len(node.CList) == 2:
                    if len(node.CList[0].FList) == 1 and len(node.CList[0].CList) == 1:
                        if node.CList[0].CList[0] == node.CList[1]:
                            RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                            RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                            RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot,0)
                            del ALLNodeList[node.Addr]
                            del ALLNodeList[node.CList[0].Addr]
                            for fnode in node.FList:
                                fnode.CList.remove(node)
                                fnode.CList.append(RepNode)
                            RepNode.FList = node.FList             
                            NextNode = node.CList[1]
                            RepNode.CList = [NextNode]
                            NextNode.FList.remove(node)
                            NextNode.FList.remove(node.CList[0])
                            NextNode.FList.append(RepNode)
                            ALLNodeList[RepNode.Addr] = RepNode
                            IsSimplable = 1
                            break
                        
                    if len(node.CList[1].FList) == 1 and len(node.CList[1].CList) == 1:
                        if node.CList[1].CList[0] == node.CList[0]:
                            RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                            RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                            RepNode.TreeRoot.Tadd_CList(node.CList[1].TreeRoot,0)
                            del ALLNodeList[node.Addr]
                            del ALLNodeList[node.CList[1].Addr]
                            for fnode in node.FList:
                                fnode.CList.remove(node)
                                fnode.CList.append(RepNode)
                            RepNode.FList = node.FList             
                            NextNode = node.CList[0]
                            RepNode.CList = [NextNode]
                            NextNode.FList.remove(node)
                            NextNode.FList.remove(node.CList[1])
                            NextNode.FList.append(RepNode)
                            ALLNodeList[RepNode.Addr] = RepNode
                            IsSimplable = 1
                            break
                                
            for t,node in ALLNodeList.items():
                if len(node.CList) == 1 and len(node.CList[0].FList) == 1:
                    RepNode = Node(node.Addr,0)
                    RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                    RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot,0)
                    del ALLNodeList[node.Addr]#mind the order of 'del' and 'create'
                    del ALLNodeList[node.CList[0].Addr]
                    RepNode.CList = node.CList[0].CList
                    RepNode.FList = node.FList
                    for fnode in node.FList:
                        fnode.CList.remove(node)
                        fnode.CList.append(RepNode)
                    for cnode in node.CList[0].CList:
                        cnode.FList.remove(node.CList[0])
                        cnode.FList.append(RepNode)
                    ALLNodeList[RepNode.Addr] = RepNode
                    IsSimplable = 1
                    break
        # above: DO WHILE CFG has been changed, using abstraction method 1 to abstract CFG

    ######################################################################################################################################
    #   AbstractMethod2:
    #
        # 0: a node is not in the stack and has not been visited; 1: a node is in the stack but has not been visited
        # 2: a node is not in the stack but is currently being visited; 3: a node is not in the stack but has already been visited 
        MyStack = Stack()
        CurrentNode = FirstNode
        MyStack.Push(CurrentNode)
        while MyStack.IsEmpty() <> True and IsSimplable == 0:
            CurrentNode = MyStack.Pop()
            CurrentNode.IsVisited = 2
            IfFinished = 1 # 1 represents that this branch has been finished visiting
            if len(CurrentNode.CList) <> 0:  #if this node is not an endpoint of current visiting branch
                for node in CurrentNode.CList:
                    
                    if node.IsVisited == 2:
                        # we find a loop and then we should begin to abstract this loop into a single node
                        RepNode = Node(node.Addr,0)

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
                                for cnode in snode.CList:
                                    if cnode.IsVisited <> 2:
                                        cnode.FList.remove(snode)
                                        if cnode.FList.count(RepNode) == 0:
                                            cnode.FList.append(RepNode)
                                            RepNode.CList.append(cnode)
                                RepNode.TreeRoot.Tadd_CList(snode.TreeRoot,1)
                                del ALLNodeList[snode.Addr]
                        ALLNodeList[RepNode.Addr] = RepNode
                        IsSimplable = 1
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
            
######################################################################################################################################
#   PreOperationMethod1
#
        for t,node in ALLNodeList.items():
        # here we assume that there is only a node that has more than two children in a function
            if len(node.CList) > 2:
                print "pre-operation method 1 is being used\n"
                while len(node.CList) > 2:
                    RepNode = Node(node.Addr + 1)
                    for cnode in node.CList:
                        if cnode == node.CList[0]:
                            continue
                        cnode.FList.remove(node)
                        cnode.FList.append(RepNode)
                        RepNode.CList.append(cnode)
                    node.CList = [node.CList[0],RepNode]
                    RepNode.FList = [node]
                    node = RepNode
                break
    #print ALLNodeList.items()
    # here the first half has been finished, the code above should be independent with the code below
    
######################################################################################################################################
#   take turns to use AbstractMethod1 and AbstractMethod3
#
    ######################################################################################################################################
    #   AbstractMethod3:
    #
    IsSimplable = 1
    while IsSimplable == 1:
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
                        RepNode = Node(node.Addr + 1,0) # it's difficult to assign a new address to the created node, since there is another same address, so we simply + 1
                        RepNode.TreeRoot = node.TreeRoot
                        node.FList.remove(CurrentNode)
                        CurrentNode.CList.remove(node)
                        
                        RepNode.FList = [CurrentNode] # we set proper father
                        CurrentNode.CList.append(RepNode)
                        
                        RepNode.CList = node.CList
                        for cnode in node.CList:
                            cnode.FList.append(RepNode)
                        
                        ALLNodeList.setdefault(RepNode.Addr,RepNode)
                        IsSimplable = 1# to show that abstraction method 3 comes into force
                        break
                    else:
                        MyStack.Push(node)
                        
    ######################################################################################################################################
    #   AbstractMethod1:
    #
        if IsSimplable == 1:            
            while IsSimplable == 1:
                IsSimplable = 0
                for t,node in ALLNodeList.items():
                    if len(node.CList) == 2:
                        if len(node.CList[0].CList) == 1 and len(node.CList[1].CList) == 1 and len(node.CList[0].FList) == 1 and len(node.CList[1].FList) == 1:
                            if node.CList[0].CList[0] == node.CList[1].CList[0]:
                                RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                                RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                                RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot,0)
                                RepNode.TreeRoot.Tadd_CList(node.CList[1].TreeRoot,0)
                                #print RepNode.TreeRoot.TreeRootListSeqNum+'->'+node.TreeRoot.TreeRootListSeqNum+'&'+node.CList[0].TreeRoot.TreeRootListSeqNum+'&'+node.CList[1].TreeRoot.TreeRootListSeqNum
                                del ALLNodeList[node.Addr]
                                del ALLNodeList[node.CList[0].Addr]
                                del ALLNodeList[node.CList[1].Addr]
                                for fnode in node.FList:
                                    fnode.CList.remove(node)
                                    fnode.CList.append(RepNode)
                                RepNode.FList = node.FList
                                NextNode = node.CList[0].CList[0]
                                RepNode.CList = [NextNode]
                                NextNode.FList.remove(node.CList[0])
                                NextNode.FList.remove(node.CList[1])
                                NextNode.FList.append(RepNode)
                                ALLNodeList[RepNode.Addr] = RepNode
                                IsSimplable = 1
                                break
                            
                for t,node in ALLNodeList.items():
                    if len(node.CList) == 2:
                        if len(node.CList[0].FList) == 1 and len(node.CList[0].CList) == 1:
                            if node.CList[0].CList[0] == node.CList[1]:
                                RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                                RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                                RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot,0)
                                del ALLNodeList[node.Addr]
                                del ALLNodeList[node.CList[0].Addr]
                                for fnode in node.FList:
                                    fnode.CList.remove(node)
                                    fnode.CList.append(RepNode)
                                RepNode.FList = node.FList             
                                NextNode = node.CList[1]
                                RepNode.CList = [NextNode]
                                NextNode.FList.remove(node)
                                NextNode.FList.remove(node.CList[0])
                                NextNode.FList.append(RepNode)
                                ALLNodeList[RepNode.Addr] = RepNode
                                IsSimplable = 1
                                break
                            
                        if len(node.CList[1].FList) == 1 and len(node.CList[1].CList) == 1:
                            if node.CList[1].CList[0] == node.CList[0]:
                                RepNode = Node(node.Addr,0)# a newly created node to replace the model detected
                                RepNode.TreeRoot.Tadd_CList(node.TreeRoot,0)
                                RepNode.TreeRoot.Tadd_CList(node.CList[1].TreeRoot,0)
                                del ALLNodeList[node.Addr]
                                del ALLNodeList[node.CList[1].Addr]
                                for fnode in node.FList:
                                    fnode.CList.remove(node)
                                    fnode.CList.append(RepNode)
                                RepNode.FList = node.FList             
                                NextNode = node.CList[0]
                                RepNode.CList = [NextNode]
                                NextNode.FList.remove(node)
                                NextNode.FList.remove(node.CList[1])
                                NextNode.FList.append(RepNode)
                                ALLNodeList[RepNode.Addr] = RepNode
                                IsSimplable = 1
                                break
                                    
                for t,node in ALLNodeList.items():
                    if len(node.CList) == 1 and len(node.CList[0].FList) == 1:
                        RepNode = Node(node.Addr,0)
                        RepNode.TreeRoot.Tadd_CList(RepNode.TreeRoot,0)
                        RepNode.TreeRoot.Tadd_CList(RepNode.CList[0].TreeRoot,0)
                        del ALLNodeList[node.Addr]#mind the order of 'del' and 'create'
                        del ALLNodeList[node.CList[0].Addr]
                        RepNode.CList = node.CList[0].CList
                        RepNode.FList = node.FList
                        for fnode in node.FList:
                            fnode.CList.remove(node)
                            fnode.CList.append(RepNode)
                        for cnode in node.CList[0].CList:
                            cnode.FList.remove(node.CList[0])
                            cnode.FList.append(RepNode)
                        ALLNodeList[RepNode.Addr] = RepNode
                        IsSimplable = 1
                        break
            # above: DO WHILE CFG has been changed, using abstraction method 1 to abstract CFG
            IsSimplable = 1
######################################################################################################################################

###since after abstraction usually there is only one node left, we needn't output the result
##print ALLNodeList.items()
##filename = 'GDB.dot'
##file_object = open(filename,'w')
##file_object.write('digraph G{ \n')
##i = 1
##NumList = dict()
##for ele1,ele2 in ALLNodeList.items():
##    file_object.write('\tnode'+ '%d' %i + '[label = "%X"]' %ele1 +';\n')
##    NumList[ele1] = i
##    i += 1
##file_object.write('\n')
##for ele1,ele2 in ALLNodeList.items():
##    for f in ele2.CList:
##        file_object.write('\tnode%d' %NumList[ele1] + ' -> ' + 'node%d' %NumList[f.Addr] +'\n')
##file_object.write('}')
##file_object.close()
###subprocess.Popen('xdot '+filename,shell = True) 
##subprocess.Popen('dot -Tpdf -o '+ 'GDB.pdf ' + filename,shell = True)     

TreeFileName = 'TreeGraph.dot'
file_object = open(TreeFileName,'w')
file_object.write('digraph G{ \n')
for i in range(len(TreeRootList)):
    file_object.write('\tTNode' + '%d' %i + '[label = "%X"]' %TreeRootList[i].Addr + ';\n')
file_object.write('\n')
for i in range(len(TreeRootList)):
    for c in TreeRootList[i].TCList:
        file_object.write('\tTNode%d' %i + ' -> ' + 'TNode%d' %(c.TreeRootListSeqNum) +'\n')
file_object.write('}')
file_object.close()
subprocess.Popen('dot -Tjpg -o '+ 'TreeGraph.jpg ' + 'TreeGraph.dot',shell = True)  
    


