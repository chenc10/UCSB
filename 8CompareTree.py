import subprocess
from decimal import *
import math

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

def read_file(TreeNodeList, FileName):
    fread = open(FileName,'r')
    Database = fread.readlines()
    fread.close()
    TmpValue = 0
    i = 0
    while i < len(Database):
        CurrentLine = Database[i].split(' ')
        CurrentNode = TreeNodeList.setdefault(int(CurrentLine[0],10),TreeNode(int(CurrentLine[0],10)))
        CurrentNode.Type = int(CurrentLine[1],10)
        CurrentNode.NumOfNodes = int(CurrentLine[2],10)
        if TmpValue < CurrentNode.NumOfNodes:
            TreeRoot = CurrentNode
            TmpValue = CurrentNode.NumOfNodes

        i = i + 1
        SaveChildrens = Database[i][0:len(Database[i])-2].split(' ')
        if SaveChildrens <> ['']:
            for m in range(len(SaveChildrens)):
                C = TreeNodeList.setdefault(int(SaveChildrens[m],10),TreeNode(int(SaveChildrens[m],10)))
                CurrentNode.TCList.append(C)
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
    if Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) < Decimal('0.9') or Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) > Decimal('1.1'):
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
    while len(Stack1):
        CTreeNode1 = Stack1.pop(0)
        CTreeNode2 = Stack2.pop(0)
        if Level <> CTreeNode1[1]:
            print Level,"again"
            Level = CTreeNode1[1]
        print CTreeNode1[1]
        if not compare_node(CTreeNode1[0], CTreeNode2[0]):
            return [0, CTreeNode1[1]]
        else:
            for CNode1 in CTreeNode1[0].TCList:
                Stack1.append([CNode1,CTreeNode1[1]+1])
            for CNode2 in CTreeNode2[0].TCList:
                Stack2.append([CNode2,CTreeNode2[1]+1])
    return [1, -1]

if __name__ == "__main__":
    TreeRoot1 = read_file(TreeNodeList1,'TreeRoot1.dat')
    TreeRoot2 = read_file(TreeNodeList2,'TreeRoot2.dat')
    result = compare_tree(TreeRoot1, TreeRoot2)
    print 'success'
    print result

    



