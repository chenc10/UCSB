from munkres import Munkres
import subprocess
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
        self.NumOfNodes = 0 
        self.BelowLevel = -1

def myprint(TreeNodeList,graphnum):
    filename = 'TreeGraph'+str(graphnum)+'.dot'
    file_object = open(filename,'w')
    file_object.write('digraph G{ \n')
    i = 1
    NumList = dict()
    for ele1,ele2 in TreeNodeList.items():
        file_object.write('\tnode'+ '%d' %i + '[label = "%d"]' %ele1 +';\n')
        NumList[ele1] = i
        i += 1
    file_object.write('\n')
    for ele1,ele2 in TreeNodeList.items():
        for f in ele2.TCList:
            file_object.write('\tnode%d' %NumList[ele1] + ' -> ' + 'node%d' %NumList[f.SeqNum] +'\n')
    file_object.write('}')
    file_object.close()
    subprocess.Popen('dot -Tjpg -o '+ 'TreeGraph'+str(graphnum)+'.jpg ' + filename,shell = True)

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
	CurrentNode.TCList = sorted(CurrentNode.TCList, reverse=True, key = lambda child: child.NumOfNodes)
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
    print "enter compare_node",TreeNode1.SeqNum, TreeNode2.SeqNum
    Vector1 = []
    Vector2 = []
    if TreeNode1.Type <> TreeNode2.Type:
	print "return 0, TreeNode1.Type <> TreeNode2.Type"
        return 0
    if Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) < Decimal('0.8') or Decimal(TreeNode1.NumOfNodes)/Decimal(TreeNode2.NumOfNodes) > Decimal('1.2'):
	#print ""
	#print "Their seqnum:",TreeNode1.SeqNum,TreeNode2.SeqNum #print "NumOfNodes diff exceed"
	print "Return 0, TreeNode1.NumOfNodes",TreeNode1.NumOfNodes
	print "Return 0, TreeNode2.NumOfNodes",TreeNode2.NumOfNodes
        return 0
    if len(TreeNode1.TCList) <> len(TreeNode2.TCList):
        if len(TreeNode1.TCList) > len(TreeNode2.TCList):
            for i in range(len(TreeNode1.TCList) - len(TreeNode2.TCList)):
        	TreeNode2.TCList.append(TreeNode(-1))
        else:
            for i in range(len(TreeNode2.TCList) - len(TreeNode1.TCList)):
        	TreeNode1.TCList.append(TreeNode(-1))		
        #print "Num in CList diff"
        #print "their seqnum",TreeNode1.SeqNum, TreeNode2.SeqNum
    if not len(TreeNode1.TCList) and not len(TreeNode2.TCList):
	print "TreeNode1 and TreeNode2 no child"
        return 1
    for CNode in TreeNode1.TCList:
        Vector1.append(CNode.NumOfNodes)
    for CNode in TreeNode2.TCList:
        Vector2.append(CNode.NumOfNodes)
    print "vector1",Vector1
    print "vector2",Vector2
    if cosine_similarity(Vector1, Vector2) < 0.8:
	print "cosine_similarity less than 0.7"
        return 0
    return 1


def compare_tree(TreeRoot1, TreeRoot2):
    Stack1 = [[TreeRoot1,0]]
    Stack2 = [[TreeRoot2,0]]
    Level = 0
    TotalNumOfNodes1 = TreeRoot1.NumOfNodes
    TotalNumOfNodes2 = TreeRoot2.NumOfNodes
    DiffNumOfNodes1 = 0
    DiffNumOfNodes2 = 0
    while len(Stack1) and len(Stack2):
	# it should be kept that the node poped is corresponded
        CTreeNode1 = Stack1.pop(0)
        CTreeNode2 = Stack2.pop(0)
        if Level <> CTreeNode1[1]:
            #print Level,"again"
            Level = CTreeNode1[1]
	    #print "level changed",Level
        if not compare_node(CTreeNode1[0], CTreeNode2[0]):
	    print "not compare_node, here is the DiffNumOfNodes",CTreeNode1[0].SeqNum, CTreeNode2[0].SeqNum, CTreeNode1[0].NumOfNodes, CTreeNode2[0].NumOfNodes
	    DiffNumOfNodes1 = DiffNumOfNodes1 + CTreeNode1[0].NumOfNodes
	    DiffNumOfNodes2 = DiffNumOfNodes2 + CTreeNode2[0].NumOfNodes
        else:
            for CNode1 in CTreeNode1[0].TCList:
                Stack1.append([CNode1,CTreeNode1[1]+1])
            for CNode2 in CTreeNode2[0].TCList:
                Stack2.append([CNode2,CTreeNode2[1]+1])
    SimilarNumOfNodes1 = TotalNumOfNodes1 - DiffNumOfNodes1
    SimilarNumOfNodes2 = TotalNumOfNodes2 - DiffNumOfNodes2
    if SimilarNumOfNodes1 < 0 or SimilarNumOfNodes2 < 0:
	print "Error! SimilarNumOfNodes < 0! Exit"
	exit(1)
    print "TotalNumOfNodes1",TotalNumOfNodes1,"SimilarNumOfNodes1",SimilarNumOfNodes1
    print "TotalNumOfNodes2",TotalNumOfNodes2,"SimilarNumOfNodes2",SimilarNumOfNodes2
    #if Level < 5:
	    #return 0
    result= min(Decimal(SimilarNumOfNodes1)/Decimal(TotalNumOfNodes1) ,Decimal(SimilarNumOfNodes2)/Decimal(TotalNumOfNodes2))
    result = result / Decimal(math.sqrt(min(TotalNumOfNodes1, TotalNumOfNodes2)))
    return result

def func_similarity(func1, func2):
    global TreeNodeList1
    global TreeNodeList2
    TreeNodeList1=dict()
    TreeNodeList2=dict()
    TreeRoot1 = read_file(TreeNodeList1,func1)
    TreeRoot2 = read_file(TreeNodeList2,func2)
    print " "
    print "func1, func2",func1, func2
    #myprint(TreeNodeList1,1)
    #myprint(TreeNodeList2,2)
    if TreeRoot1.BelowLevel > TreeRoot2.BelowLevel:
        TotalLevel = TreeRoot1.BelowLevel
    else:
        TotalLevel = TreeRoot2.BelowLevel
    TotalLevel = TotalLevel - 1 #validity needed checking
    if TotalLevel == 0:
	return Decimal(0)
    return compare_tree(TreeRoot1, TreeRoot2)

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
    Folder1 = "./"+str(Folder1)
    Folder2 = "./"+str(Folder2)
    print ""
    print "two software:",Folder1,Folder2
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
    CostMatrix = []
    for Ele1 in Database1:
        A = []
	B = []
        for Ele2 in Database2:
	    fResult = func_similarity(Ele1,Ele2)
	    #print "result",fResult
	    if fResult > 0:
		print "		",Ele2,"not zero"
            A.append(fResult)
	    B.append((-1)*A[-1])
	print "    ",Ele1,"loop finished"
        Matrix.append(A)
	CostMatrix.append(B)
    print_matrix(Matrix)
    m = Munkres()
    IndexPairs = m.compute(CostMatrix)
    TotalValue = 0
    for x,y in IndexPairs:
	TotalValue = TotalValue + Matrix[x][y]
    #note that here the first para is the test software, and the second para is a function in the database
    TotalValue = float(TotalValue) / float(len(Matrix))
    print "size",len(Matrix),"*",len(Matrix[0])
    print 'success'
    print "result"," %.6f" %TotalValue
    print "" 
