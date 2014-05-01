#extracting graph from the results of IDA, and then save that graph in a txt file ¡°GDB.txt" in the form of an adjacency list
#this is for the convenience of debugging, we needn't execute the program in IDA any more
from idaapi import *
import subprocess
from idautils import *
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
    iseffective = 1
    ea = PrevFunction(ScreenEA())
    CurrentNode = Node(ea)
    ALLNodeList[ea] = CurrentNode
    for head in Heads(NextNotTail(ea), FindFuncEnd(ea)):
        if isCode(GetFlags(head)):
            if not iseffective:
                for RefBackTo in CodeRefsTo(head,0):
                    iseffective = 1
                if iseffective:
                    CreateNode = ALLNodeList.setdefault(head,Node(head))
                    CurrentNode = CreateNode		
            else:
                isreftoexist = 0
                for RefBackTo in CodeRefsTo(head,0):
                    isreftoexist = 1
                if isreftoexist:  
                    CreateNode = ALLNodeList.setdefault(head,Node(head))
                    if CurrentNode == CreateNode:
                        continue
                    CurrentNode.add_CList(CreateNode)
                    CreateNode.add_FList(CurrentNode)
                    CurrentNode = CreateNode
                else:
                    if GetMnem(head) == 'retn':
                        iseffective = 0
                        continue
                    if GetMnem(head) <> 'jmp':
                        if GetMnem(head)[0] == 'j':
                            CurrentNode1 = ALLNodeList.setdefault(NextNotTail(head),Node(NextNotTail(head)))
                            for f in CodeRefsFrom(head,0):
                                break
                            CurrentNode2 = ALLNodeList.setdefault(f,Node(f))
                            CurrentNode1.add_FList(CurrentNode)
                            CurrentNode2.add_FList(CurrentNode)
                            CurrentNode.add_CList(CurrentNode1)
                            CurrentNode.add_CList(CurrentNode2)
                            CurrentNode = CurrentNode1
                    else:
                        for f in CodeRefsFrom(head,0):
                            CurrentNode2 = ALLNodeList.setdefault(f,Node(f))
                            CurrentNode2.add_FList(CurrentNode)
                            CurrentNode.add_CList(CurrentNode2)
                        iseffective = 0



                
print len(ALLNodeList.items())
for ele1,ele2 in ALLNodeList.items():
    ele2.FList = list(set(ele2.FList))
    ele2.CList = list(set(ele2.CList))
sorted = ALLNodeList.items()
sorted.sort()

# be noted that we make a shift(by *16), in order to prepare for replication(where we need to distinguish those created from replication)
record = open("GDB.txt",'w')
for ele1,ele2 in sorted:
    ele1 = ele1 * 16
    record.write("%d\n\t"%ele1)
    for f in ele2.FList:
        ad = f.Addr
        ad = ad * 16
        record.write("%d "%ad)
    record.write("\n\t")
    for c in ele2.CList:
        ad = c.Addr
        ad = ad * 16
        record.write("%d "%ad)
    record.write("\n")
record.close()

fname = GetFunctionName(ea)
filename = fname + '.dot'
file_object = open(filename,'w')
file_object.write('digraph G{ \n')
i = 1
NumList = dict()
for ele1,ele2 in sorted:
    file_object.write('\tnode'+ '%d' %i + '[label = "%X"]' %ele1 +';\n')
    NumList[ele1] = i
    i += 1
file_object.write('\n')
for ele1,ele2 in sorted:
    for f in ele2.CList:
        file_object.write('\tnode%d' %NumList[ele1] + ' -> ' + 'node%d' %NumList[f.Addr] +'\n')
file_object.write('}')
file_object.close()
subprocess.Popen('xdot '+filename,shell = True) 
subprocess.Popen('dot -Tpdf -o '+fname +'.pdf ' + filename,shell = True)     

