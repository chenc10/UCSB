#Pre-operation method 2:
#if there are more than two "return" node in a graph, we add a virtual final "return" node.

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
    if len(ReturnNode) > 1:
        RepNode = Node(ReturnNode[0].Addr + 1)
        RepNode.FList = ReturnNode
        for node in ReturnNode:
            node.CList = [RepNode]

        

    
