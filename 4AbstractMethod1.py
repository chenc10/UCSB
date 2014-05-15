#function description:
#function input:
#   GDB.txt: a txt file which saves the data of the graph in a certain format
#function output:
#   GDB.dot: a dot file to save the simplified graph after using abstraction method 1
#   GDB.jpg: a jpg file to display the simplified graph
#related methods:
#   abstraction method 1: we can use it to simplify a diamond as well as two subsquent nodes
#function mechanism: we keep doing simplification until nothing can be changed by method 1
import subprocess
ALLNodeList = dict()#dictionary for saving the existence of nodes
class Node:
    "'node for the graph'"
    def __init__(self,Addr):
        self.Addr = Addr
        self.FList = []
        self.CList = []       
    def add_FList(self,Node):
        self.FList.append(Node)
    def add_CList(self,Node):
        self.CList.append(Node)
        
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
    
    #case 0:
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

    #case +:
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

        
if __name__ == "__main__":
    fread = open("GDB.txt",'r')
    Database = fread.readlines()
    fread.close()
    i = 0
    ReturnNode = []
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
        else:
            ReturnNode.append(CurrentNode)
        i = i + 1

    IsSimplable = 1
    while IsSimplable:
        IsSimplable = 0
        for t,node in ALLNodeList.items():
            if check_abs1_type(node) == -3:
                continue
            elif check_abs1_type(node) == -2:
                #print '-2'
                IsSimplable = 1
                RepNode = Node(node.Addr)
                RepNode.FList = node.FList
                RepNode.CList = node.CList[0].CList
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
                #print '-1'
                IsSimplable = 1
                #create
                NextNode = node.CList[0].CList[0]
                RepNode = Node(node.Addr)
                RepNode.FList = node.FList
                RepNode.CList = [NextNode]
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
                #print hex(node.Addr),check_abs1_type(node)
                IsSimplable = 1
                NextNode = node.CList[check_abs1_type(node)]
                RepNode = Node(node.Addr)
                RepNode.FList = node.FList
                RepNode.CList = [NextNode]
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
                
    print ALLNodeList.items()
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
    subprocess.Popen('dot -Tjpg -o '+ 'GDB.jpg ' + filename,shell = True)     




