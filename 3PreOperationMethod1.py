#Pre-operation method 1:
#To those nodes who have more than 2 children, we will split each of them into several nodes, all of which having two children

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

    for t,node in ALLNodeList.items():
        # here we assume that there is only a node that has more than two children in a function
        if len(node.CList) > 2:
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
                ALLNodeList[RepNode] = RepNode
                node = RepNode
            break
        

    
