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
from optparse import OptionParser
import subprocess
ALLNodeList = dict()#dictionary for saving the existence of nodes
TreeRootList = dict()
class TreeRoot:
    "'Tree inside node'"
    def __init__(self,Addr,type):
        #the usage of type can be extended
        self.IfLoop = 0
        self.TCList = []
        self.Addr = Addr
        self.TreeRootType = type
        self.TreeRootListSeqNum = len(TreeRootList)
        TreeRootList[self.TreeRootListSeqNum] = self
        if not type:
            self.NumOfNodes = 1
        else:
            self.NumOfNodes = 0
    def Tadd_CList(self,TreeRoot):
        #AbstractionMethod express whether this abstraction contains a loop
        self.TCList.append(TreeRoot)
        self.NumOfNodes = self.NumOfNodes + TreeRoot.NumOfNodes
class Node:
    "'node for the graph'"
    def __init__(self,Addr,type = 0):
        #type==0: this node is initial actual node;
        #type==1: this node is an abstracted node after abstractionmethod1
        #type==2: this node is an abstracted node after abstractionmethod2
        #type==3: this node is a replicated node after abstractionmethod3
        self.Addr = Addr
        self.FList = []
        self.CList = []
        self.IsVisited = 0#it is a sign showing whether this node has been visited or not
        self.TreeRoot = TreeRoot(Addr,type)
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
    
def check_abs1_type(Node):
    if len(Node.CList) == 0:
        return -3 # we cannot use abs1
    if len(Node.CList) == 1:
        if len(Node.CList[0].FList) <> 1:
            return -3
        if Node.CList[0].FList[0] <> Node:
            print 'error'
        return -2
    sign = 1
    for cnode in Node.CList:
        if len(cnode.FList) <> 1:
            sign = 0
            break
        if len(cnode.CList) <> 1:
            sign = 0
            break
    if sign == 1:
        for cnode in Node.CList:
            if cnode == Node.CList[0]:
                continue
            if cnode.CList[0] <> Node.CList[0].CList[0]:
                sign = 0
                break
    if sign == 1:
        return -1
    for i in range(len(Node.CList)):
        sign = 1
        for cnode in Node.CList:
            if cnode == Node.CList[i]:
                continue
            if len(cnode.FList) <> 1:
                sign = 0
                break
            if len(cnode.CList) <> 1:
                sign = 0
                break
        if  sign == 1:
            for cnode in Node.CList:
                if cnode == Node.CList[i]:
                    continue
                if cnode.CList[0] <> Node.CList[i]:
                    sign = 0
                    break
        if sign == 1:
            return i
    return -3

def myprint(graphnum):
    # this function is for helping debuging, it can display the current CFG graph in abstraction process
    # a different graphnum should be set each time using this function
    filename = 'GDB'+str(graphnum)+'.dot'
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
    subprocess.Popen('dot -Tjpg -o '+ 'GDB'+str(graphnum)+'.jpg ' + filename,shell = True)
    
if __name__ == "__main__":

######################################################################################################################################
#   ReadDataFromFile: get data from GDB.txt
#
    Parser = OptionParser()
    Parser.add_option("-r", "--read", dest="readfilename",help="read CFG data from READFILE", metavar ="READFILE")
    ##Parser.add_option("-w", "--write", dest="writefilename", help="write abstracted tree data to WRITEFILE", metavar = "WRITEFILE")
    (options, args) = Parser.parse_args()
    #print options.readfilename
    #options.readfilename = "sub_401D7E"
    ReadFileName = options.readfilename + ".txt"
    TreeFileName = options.readfilename + "_Tree.dat"
    TreeDotName = options.readfilename + "_TreeDot.dot"
    TreeGraphName = options.readfilename + "_TreeGraph.jpg"
    ##TreeFileName = options.writefilename + ".dat"
    ##TreeGraphName = options.writefilename + ".dot"
    ##for readfilename itself, we needn't add ".txt" after it
    fread = open(ReadFileName,'r')
    Database = fread.readlines()
    fread.close()
    i = 0
    ReturnNode = []
    while i < len(Database):#we should make address * 10
        if not ALLNodeList.has_key(int(Database[i],16)):
            ALLNodeList[int(Database[i],16)] = Node(int(Database[i],16))
        CurrentNode = ALLNodeList[int(Database[i],16)]
        i = i + 1
        SaveFathers = Database[i][1:len(Database[i])-3].split(' ')
        if SaveFathers <> ['']:
            for m in range(len(SaveFathers)):
                if not ALLNodeList.has_key(int(SaveFathers[m],16)):
                    ALLNodeList[int(SaveFathers[m],16)] = Node(int(SaveFathers[m],16))
                F = ALLNodeList[int(SaveFathers[m],16)]
                CurrentNode.add_FList(F)
        else:
            FirstNode = CurrentNode
        i = i + 1
        SaveChildrens = Database[i][1:len(Database[i])-3].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                if not ALLNodeList.has_key(int(SaveChildrens[m],16)):
                    ALLNodeList[int(SaveChildrens[m],16)] = Node(int(SaveChildrens[m],16))
                C = ALLNodeList[int(SaveChildrens[m],16)]
                CurrentNode.add_CList(C)
        else:
            ReturnNode.append(CurrentNode)
        i = i + 1
        
    print 'finished reading'
######################################################################################################################################
#   PreOperationMethod2
#
    if len(ReturnNode) > 1:
        print "pre-operation method 2 is being used\n"
        RepNode = Node(ReturnNode[0].Addr + 1)
        RepNode.FList = ReturnNode
        for node in ReturnNode:
            node.CList = [RepNode]
        ALLNodeList[RepNode.Addr] = RepNode
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
                if check_abs1_type(node) == -3:
                    continue
                elif check_abs1_type(node) == -2:
                    IsSimplable = 1
                    RepNode = Node(node.Addr,1)
                    RepNode.FList = node.FList
                    RepNode.CList = node.CList[0].CList
                    RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                    RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot)
                    if FirstNode == node:
                        FirstNode = RepNode
                    for fnode in node.FList:
                        fnode.CList.remove(node)
                        fnode.CList.append(RepNode)
                    for cnode in node.CList[0].CList:
                        cnode.FList.remove(node.CList[0])
                        cnode.FList.append(RepNode)
                    del ALLNodeList[node.Addr]
                    del ALLNodeList[node.CList[0].Addr]
                    ALLNodeList[RepNode.Addr] = RepNode
                    break
                    
                elif check_abs1_type(node) == -1:
                    IsSimplable = 1
                    #create
                    NextNode = node.CList[0].CList[0]
                    RepNode = Node(node.Addr,1)
                    RepNode.FList = node.FList
                    RepNode.CList = [NextNode]
                    RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                    if FirstNode == node:
                        FirstNode = RepNode
                    for cnode in node.CList:
                        RepNode.TreeRoot.Tadd_CList(cnode.TreeRoot)
                    #set
                    for fnode in node.FList:
                        fnode.CList.remove(node)
                        fnode.CList.append(RepNode)
                    for cnode in node.CList:
                        NextNode.FList.remove(cnode)
                    NextNode.FList.append(RepNode)
                    #delete
                    del ALLNodeList[node.Addr]
                    for cnode in node.CList:
                        del ALLNodeList[cnode.Addr]
                    ALLNodeList[RepNode.Addr] = RepNode
                    break
                    
                else:
                    IsSimplable = 1
                    NextNode = node.CList[check_abs1_type(node)]
                    RepNode = Node(node.Addr,1)
                    RepNode.FList = node.FList
                    RepNode.CList = [NextNode]
                    RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                    if FirstNode == RepNode:
                        FirstNode = RepNode
                    for cnode in node.CList:
                        if cnode == NextNode:
                            continue
                        RepNode.TreeRoot.Tadd_CList(cnode.TreeRoot)
                    
                    for fnode in node.FList:
                        fnode.CList.remove(node)
                        fnode.CList.append(RepNode)
                    for cnode in node.CList:
                        if cnode == NextNode:
                            continue
                        NextNode.FList.remove(cnode)
                    NextNode.FList.remove(node)
                    NextNode.FList.append(RepNode)
                    del ALLNodeList[node.Addr]
                    for cnode in node.CList:
                        if cnode == NextNode:
                            continue
                        del ALLNodeList[cnode.Addr]
                    ALLNodeList[RepNode.Addr] = RepNode
                    break
        # above: DO WHILE CFG has been changed, using abstraction method 1 to abstract CFG

    ######################################################################################################################################
    #   AbstractMethod2:
    #
        # 0: a node is not in the stack and has not been visited; 1: a node is in the stack but has not been visited
        # 2: a node is not in the stack but is currently being visited; 3: a node is not in the stack but has already been visited 
        MyStack = Stack()
        for t,node in ALLNodeList.items():
            node.IsVisited = 0 #reset sign
        CurrentNode = FirstNode
        MyStack.Push(CurrentNode)
        while MyStack.IsEmpty() <> True and IsSimplable == 0:
            CurrentNode = MyStack.Pop()
            CurrentNode.IsVisited = 2
            IfFinished = 1 # 1 represents that this branch has been finished visiting
            if len(CurrentNode.CList) <> 0:  #if this node is not an endpoint of current visiting branch
                for node in CurrentNode.CList:
                    
                    if node.IsVisited == 2:##HERE can we make a traversal? In order to reduce entropy. 2 First! maybe not important
                        # we find a loop and then we should begin to abstract this loop into a single node
                        RepNode = Node(node.Addr,2)
                        
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
                                RepNode.TreeRoot.Tadd_CList(snode.TreeRoot)
                                del ALLNodeList[snode.Addr]
                        if FirstNode == node:
                            print 'FirstNode is changed in loop'
                            FirstNode = RepNode
                        ALLNodeList[RepNode.Addr] = RepNode
                        IsSimplable = 1
                        break
                    
                    elif node.IsVisited == 0:
                        node.IsVisited = 1
                        MyStack.Push(node)
                        IfFinished = 0 # we shall mark that current branch can be extended

                    elif node.IsVisited == 1:
                        #we need to update the position of node in the stack.
                        if MyStack.Array.index(node) != len(MyStack.Array) - 1:
                            MyStack.Array.remove(node)
                            MyStack.Array.append(node)
                        IfFinished = 0
            # when current branch is finished, we have to create new branch or choose to stop        
            if IfFinished == 1 and IsSimplable == 0:# Change 1 #If current branch has been finished
                if MyStack.IsEmpty():
                    node = FirstNode
                    node.IsVisited = 3 # we search from root
                else:#we begin to mark those nodes that should be marked as 3
                    node = MyStack.Array[-1]
		    tmp927 = 0
		    for fnode in node.FList:
			if fnode.IsVisited == 2:
			    tmp927 = tmp927+1
		    if tmp927 <> 1:
			print "another error"

		    for fnode in node.FList:
                        if fnode.IsVisited == 2:
                            node = fnode
                            break
                #while node.CList <> []:# we keep search from this node,this search is to change state 2 to 3
                    #### here is where error comes from. I should change it to muti-branches cases correspondedly
		TmpStack=Stack()
		TmpStack.Push(node)
		while TmpStack.IsEmpty() <> True:
		    tmpnode = TmpStack.Pop()
		    for cnode in tmpnode.CList:
		    	if cnode.IsVisited == 2:
		            cnode.IsVisited = 3
			    TmpStack.Push(cnode)

        for t,node in ALLNodeList.items():
            node.IsVisited = 0 #reset sign
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
        FirstNode.IsVisited = 1
        CurrentNode = FirstNode
        MyStack.Push(CurrentNode)
        IsSimplable = 0
        while MyStack.IsEmpty() <> True and IsSimplable == 0:
            CurrentNode = MyStack.Pop()
            if len(CurrentNode.CList) <> 0:  #if this node is an endpoint of current visiting branch
                for node in CurrentNode.CList:
                    if node.IsVisited == 1:
                        if len(node.CList) == 0:
                            continue
                        # we find a case where a replication is needed
                        # we replicate the initial node into two different nodes in subquent addresses
                        # we should avoid Addr conflict here by check if the address to use already exist
                        RepNodeAddrOffset = 1
                        while ALLNodeList.has_key(node.Addr + RepNodeAddrOffset):
                            RepNodeAddrOffset = RepNodeAddrOffset + 1
                        if RepNodeAddrOffset > 16:
                            print 'error RepNodeAddrOffset'
                        RepNode1 = Node(node.Addr + RepNodeAddrOffset,3) # it's difficult to assign a new address to the created node, since there is another same address, so we simply + 1
                        RepNode1.TreeRoot.Tadd_CList(node.TreeRoot)
                        node.FList.remove(CurrentNode)
                        CurrentNode.CList.remove(node)

                        RepNode1.FList = [CurrentNode] # we set proper father
                        CurrentNode.CList.append(RepNode1)
                        
                        #note that here CList in RepNode should be created differently
                        for cnode in node.CList:
                            RepNode1.CList.append(cnode)
                        for cnode in node.CList:
                            cnode.FList.append(RepNode1)
                        ALLNodeList[RepNode1.Addr] = RepNode1

##                        graphnum = graphnum + 1
##                        print 'graphnum:',graphnum
##                        myprint(graphnum)
                        
                        while ALLNodeList.has_key(node.Addr + RepNodeAddrOffset):
                            RepNodeAddrOffset = RepNodeAddrOffset + 1
                        if RepNodeAddrOffset > 16:
                            print 'error RepNodeAddrOffset'
                        RepNode2 = Node(node.Addr + RepNodeAddrOffset, 3)
                        RepNode2.TreeRoot.Tadd_CList(node.TreeRoot)
                        for fnode in node.FList:
                            RepNode2.FList.append(fnode)
                            fnode.CList.remove(node)
                            fnode.CList.append(RepNode2)
                        for cnode in node.CList:
                            RepNode2.CList.append(cnode)
                            cnode.FList.remove(node)
                            cnode.FList.append(RepNode2)
                        del ALLNodeList[node.Addr]
                        ALLNodeList[RepNode2.Addr] = RepNode2

                        IsSimplable = 1# to show that abstraction method 3 comes into force
                        break
                    else:
                        node.IsVisited = 1
                        MyStack.Push(node)
                        
        for a,node in ALLNodeList.items():
            node.IsVisited = 0
    ######################################################################################################################################
    #   AbstractMethod1:
    #
        if IsSimplable == 1:
            for a,node in ALLNodeList.items():
                for fnode in node.FList:
                    if fnode.CList.count(node) <> 1:
                        print 'before error'
                for cnode in node.CList:
                    if cnode.FList.count(node) <> 1:
                        print 'before error2'
            while IsSimplable == 1:
                IsSimplable = 0
                for t,node in ALLNodeList.items():
                    if check_abs1_type(node) == -3:
                        continue
                    elif check_abs1_type(node) == -2:
                        IsSimplable = 1
                        RepNode = Node(node.Addr,1)
                        RepNode.FList = node.FList
                        RepNode.CList = node.CList[0].CList
                        RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                        RepNode.TreeRoot.Tadd_CList(node.CList[0].TreeRoot)
                        if FirstNode == node:
                            FirstNode = RepNode
                        for fnode in node.FList:
                            fnode.CList.remove(node)
                            fnode.CList.append(RepNode)
                        for cnode in node.CList[0].CList:
                            cnode.FList.remove(node.CList[0])
                            cnode.FList.append(RepNode)
                        del ALLNodeList[node.Addr]
                        del ALLNodeList[node.CList[0].Addr]
                        ALLNodeList[RepNode.Addr] = RepNode
                        break
                        
                    elif check_abs1_type(node) == -1:
                        IsSimplable = 1
                        #create
                        NextNode = node.CList[0].CList[0]
                        RepNode = Node(node.Addr,1)
                        RepNode.FList = node.FList
                        RepNode.CList = [NextNode]
                        RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                        if FirstNode == node:
                            FirstNode = RepNode
                        for cnode in node.CList:
                            RepNode.TreeRoot.Tadd_CList(cnode.TreeRoot)
                        #set
                        for fnode in node.FList:
                            fnode.CList.remove(node)
                            fnode.CList.append(RepNode)
                        for cnode in node.CList:
                            NextNode.FList.remove(cnode)
                        NextNode.FList.append(RepNode)
                        #delete
                        del ALLNodeList[node.Addr]
                        for cnode in node.CList:
                            del ALLNodeList[cnode.Addr]
                        ALLNodeList[RepNode.Addr] = RepNode
                        break
                        
                    else:
                        IsSimplable = 1
                        NextNode = node.CList[check_abs1_type(node)]
                        RepNode = Node(node.Addr,1)
                        RepNode.FList = node.FList
                        RepNode.CList = [NextNode]
                        RepNode.TreeRoot.Tadd_CList(node.TreeRoot)
                        if FirstNode == node:
                            FirstNode = RepNode
                        for cnode in node.CList:
                            if cnode == NextNode:
                                continue
                            RepNode.TreeRoot.Tadd_CList(cnode.TreeRoot)
                        
                        for fnode in node.FList:
                            fnode.CList.remove(node)
                            fnode.CList.append(RepNode)
                        for cnode in node.CList:
                            if cnode == NextNode:
                                continue
                            NextNode.FList.remove(cnode)
                        NextNode.FList.remove(node)
                        NextNode.FList.append(RepNode)
                        del ALLNodeList[node.Addr]
                        for cnode in node.CList:
                            if cnode == NextNode:
                                continue
                            del ALLNodeList[cnode.Addr]
                        ALLNodeList[RepNode.Addr] = RepNode
                        break
            # above: DO WHILE CFG has been changed, using abstraction method 1 to abstract CFG
            IsSimplable = 1
######################################################################################################################################

File_TreeRoot = open(TreeFileName, 'w')
for i in range(len(TreeRootList)):
    File_TreeRoot.write('%d' %i + ' %d' %TreeRootList[i].TreeRootType + ' %d' %TreeRootList[i].NumOfNodes + '\n\t')
    for c in TreeRootList[i].TCList:
        File_TreeRoot.write('%d ' %(c.TreeRootListSeqNum))
    File_TreeRoot.write('\n')
File_TreeRoot.close()

file_object = open(TreeDotName,'w')
file_object.write('digraph G{ \n')
for i in range(len(TreeRootList)):
    file_object.write('\tTNode' + '%d' %i + '[label = "%X"]' %TreeRootList[i].Addr + ';\n')
file_object.write('\n')
for i in range(len(TreeRootList)):
    for c in TreeRootList[i].TCList:
        file_object.write('\tTNode%d' %i + ' -> ' + 'TNode%d' %(c.TreeRootListSeqNum) +'\n')
file_object.write('}')
file_object.close()
subprocess.Popen('dot -Tjpg -o '+ TreeGraphName +' ' + TreeDotName,shell = True)
print 'success!'
print ''
    


