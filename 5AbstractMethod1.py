#function description:
#function input:
#   GDB.txt: a txt file which saves the data of the graph in a certain format
#function output:
#   GDB.dot: a dot file to save the simplified graph after using abstraction method 1
#   GDB.pdf: a pdf file to display the simplified graph
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

if __name__ == "__main__":
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
        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                C = ALLNodeList.setdefault(eval(SaveChildrens[m]),Node(eval(SaveChildrens[m])))
                CurrentNode.add_CList(C)
        i = i + 1

IsSimplable = 1
while IsSimplable:
    IsSimplable = 0
    for t,node in ALLNodeList.items():
        if len(node.CList) == 2:
            if len(node.CList[0].CList) == 1 and len(node.CList[1].CList) == 1 and len(node.CList[0].FList) == 1 and len(node.CList[1].FList) == 1:
                if node.CList[0].CList[0] == node.CList[1].CList[0]:
                    RepNode = Node(node.Addr)# a newly created node to replace the model detected
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
                    RepNode = Node(node.Addr)# a newly created node to replace the model detected
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
                    RepNode = Node(node.Addr)# a newly created node to replace the model detected
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
            RepNode = Node(node.Addr)
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
subprocess.Popen('dot -Tpdf -o '+ 'GDB.pdf ' + filename,shell = True)     




