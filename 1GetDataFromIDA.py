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
sign = 0
if len(ALLNodeList.items()) < 10:
	sign = 8
sorted = ALLNodeList.items()
sorted.sort()

if sign == 7:
    fname = GetFunctionName(ea)
    filename = fname + '.txt'
    file_object = open(filename,'w')

    record = open(filename,'w')
    for ele1,ele2 in sorted:
        ele1 = ele1 * 16
        record.write("%X\n\t"%ele1)
        for f in ele2.FList:
            ad = f.Addr
            ad = ad * 16
            record.write("%X "%ad)
        record.write("\n\t")
        for c in ele2.CList:
            ad = c.Addr
            ad = ad * 16
            record.write("%X "%ad)
        record.write("\n")
    record.close()
