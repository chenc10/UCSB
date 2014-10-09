import os
from decimal import Decimal
import math
from optparse import OptionParser
TreeNodeList1 = dict()
TreeNodeList2 = dict()
class TreeNode:
    "'Tree inside node'"
    def __init__(self, SeqNum):
        #the usage of type can be extended
        self.TCList = []
        self.Type = -1
        self.SeqNum = SeqNum
        self.NumOfNodes = -1
        self.BelowLevel = -1

def read_file(TreeNodeList, FileName):
    fread = open(FileName,'r')
    Database = fread.readlines()
    fread.close()
    TmpValue = 0
    i = 0
    while i < len(Database):
        CurrentLine = Database[i][0:len(Database[i])-2].split(' ')
        CurrentNode = TreeNodeList.setdefault(int(CurrentLine[0],10),TreeNode(int(CurrentLine[0],10)))
        CurrentNode.Type = int(CurrentLine[1],10)
        CurrentNode.NumOfNodes = int(CurrentLine[2],10)
        CurrentNode.BelowLevel = int(CurrentLine[3],10)
        if TmpValue < CurrentNode.NumOfNodes:
            TreeRoot = CurrentNode
            TmpValue = CurrentNode.NumOfNodes
        i = i + 1
        SaveChildrens = Database[i][1:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                C = TreeNodeList.setdefault(int(SaveChildrens[m],10),TreeNode(int(SaveChildrens[m],10)))
                CurrentNode.TCList.append(C)
	CurrentNode.TCList = sorted(CurrentNode.TCList, key = lambda child: child.NumOfNodes)
        i = i + 1
    
    return TreeRoot

def cosine_similarity(Vector1, Vector2):
    Numerator = 0.0
    Denominator1 = 0
    Denominator2 = 0
    for i in range(len(Vector1)):
        Numerator = Numerator + Vector1[i]*Vector2[i]
        Denominator1 = Denominator1 + Vector1[i]*Vector1[i]
        Denominator2 = Denominator2 + Vector2[i]*Vector2[i]
    Denominator = math.sqrt(Denominator1) * math.sqrt(Denominator2)
    return Numerator/Denominator

def compare_node(TreeNode1, TreeNode2):
    Vector1 = []
    Vector2 = []
    if TreeNode1.Type <> TreeNode2.Type:
        return 0
    if Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) < Decimal('0.5') or Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) > Decimal('2'):
        return 0
    if len(TreeNode1.TCList) <> len(TreeNode2.TCList):
        return 0
    if not len(TreeNode1.TCList):
        return 1
    for CNode in TreeNode1.TCList:
        Vector1.append(CNode.NumOfNodes)
    for CNode in TreeNode2.TCList:
        Vector2.append(CNode.NumOfNodes)
    if cosine_similarity(Vector1, Vector2) < 0.9:
        return 0
    return 1


def compare_tree(TreeRoot1, TreeRoot2):
    Stack1 = [[TreeRoot1,0]]
    Stack2 = [[TreeRoot2,0]]
    Level = 0
    while len(Stack1) and len(Stack2):
        CTreeNode1 = Stack1.pop(0)
        CTreeNode2 = Stack2.pop(0)
        if Level <> CTreeNode1[1]:
            #print Level,"again"
            Level = CTreeNode1[1]
        if not compare_node(CTreeNode1[0], CTreeNode2[0]):
            return Level
        else:
            for CNode1 in CTreeNode1[0].TCList:
                Stack1.append([CNode1,CTreeNode1[1]+1])
            for CNode2 in CTreeNode2[0].TCList:
                Stack2.append([CNode2,CTreeNode2[1]+1])
    return Level

def func_similarity(func1, func2):
    global TreeNodeList1
    global TreeNodeList2
    TreeRoot1 = read_file(TreeNodeList1,func1)
    TreeRoot2 = read_file(TreeNodeList2,func2)
    if TreeRoot1.BelowLevel > TreeRoot2.BelowLevel:
        TotalLevel = TreeRoot1.BelowLevel
    else:
        TotalLevel = TreeRoot2.BelowLevel
    result = compare_tree(TreeRoot1, TreeRoot2)
    #print Decimal(result)/Decimal(TotalLevel)
    return Decimal(result)/Decimal(TotalLevel)

def print_matrix(Matrix):
    for index1 in range(len(Matrix)):
	for index2 in range(len(Matrix[0])):
	    print ' %.4f  ' % Matrix[index1][index2],
	print ""
    
if __name__ == "__main__":
    Parser = OptionParser()
    Parser.add_option("-1",dest="Folder1")
    Parser.add_option("-2",dest="Folder2")
    (options, args) = Parser.parse_args()
    Folder1 = options.Folder1
    Folder2 = options.Folder2
    Folder1 = "./"+Folder1
    Folder2 = "./"+Folder2
    FileList1 = os.listdir(Folder1)
    FileList2 = os.listdir(Folder2)
    Database1 = []
    Database2 = []
    for Ele in FileList1:
        if Ele[-4:] == ".dat":
            Database1.append(Folder1+"/"+Ele)
    for Ele in FileList2:
        if Ele[-4:] == ".dat":
            Database2.append(Folder2+"/"+Ele)
    Matrix = []
    for Ele1 in Database1:
        A = []
        for Ele2 in Database2:
	    if func_similarity(Ele1,Ele2) <> 0:
		print Ele1,Ele2
            A.append(func_similarity(Ele1,Ele2))
        Matrix.append(A)
    print_matrix(Matrix)
    print "size",len(Matrix),"*",len(Matrix[0])
    print 'success' 
     
     
     
     
     
     
     
     
