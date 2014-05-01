#this is for reading the graph from the "GDB.txt" file into the memory, it is a base for a easier debugging
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
        #CurrentNode = ALLNodeList.setdefault(eval(Database[i]),Node(eval(Database[i])))
        CurrentNode = ALLNodeList.setdefault(int(Database[i],16),Node(int(Database[i],16)))
        i = i + 1
        SaveFathers = Database[i][0:len(Database[i])-2].split(' ')
        if SaveFathers <> ['']:
            for m in range(len(SaveFathers)):
                #F = ALLNodeList.setdefault(eval(SaveFathers[m]),Node(eval(SaveFathers[m])))
                F = ALLNodeList.setdefault(int(SaveFathers[m],16),Node(int(SaveFathers[m],16)))
                CurrentNode.add_FList(F)
        else:
            FirstNode = CurrentNode
        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                #C = ALLNodeList.setdefault(eval(SaveChildrens[m]),Node(eval(SaveChildrens[m])))
                C = ALLNodeList.setdefault(int(SaveChildrens[m],16),Node(int(SaveChildrens[m],16)))
                CurrentNode.add_CList(C)
        i = i + 1
