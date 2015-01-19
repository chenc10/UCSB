#include<stdio.h>
#include<string.h>
#include<stdlib.h>
typedef struct _Node{
	int SeqNum;
	struct _Node * CNext;
	struct _Node * FNext; 
}Node;
void creat_child(Node ** , int , int );
int main( int argc, char * argv[]){
	FILE * hIFile, * hOFile;
	char * sIFile, * sOFile;
	sIFile = (char *)malloc(100*sizeof(char));
	sOFile = (char *)malloc(100*sizeof(char));
	strcpy(sIFile, argv[1]);
	strcpy(sOFile, argv[2]);
	hIFile = fopen(sIFile,"r");
	char Buffer[500];	
	char * ptr;
	int i,j;
	int ST[2] = {0};
	int nNumOfNodes = 0;
	int Sign = 0;
	for(; fgets(Buffer, 500, hIFile);){
		if( Buffer[0] == '/'){
			Sign = 1;
			break;
		}
		if( Buffer[0] != 'n' || Buffer[1] != 'o' || Buffer[2] != 'd' || Buffer[3] != 'e') continue;
		nNumOfNodes ++;
	}
	Node ** MyNodeList;
	MyNodeList = (Node **)malloc(nNumOfNodes * sizeof(Node *));
	for( i = 0; i < nNumOfNodes; i ++){
		MyNodeList[i] = (Node *)malloc(sizeof(Node));
		MyNodeList[i]->SeqNum = i;
		MyNodeList[i]->CNext = NULL;
		MyNodeList[i]->FNext = NULL;
	}
	for(; fgets(Buffer, 500, hIFile);){
		if( Buffer[0] == '/'){
			if(Sign) fprintf(stderr,"Warning! Node without edges from it!\n \tInput: %s; Output: $s\n", sIFile, sOFile);
			continue;
		}
		if( Buffer[0] == '}')
			break;
		Sign = 0;
		ST[0] = 0;
		ST[1] = 0;
		for( i = 21, j = 0; Buffer[i]; i ++){
			if( Buffer[i] > 47 && Buffer[i] < 58){
				ST[j] *= 10;
				ST[j] += Buffer[i] - 48;
			}
			else
				j = 1;
		}
		creat_child(MyNodeList, ST[0], ST[1]);
	}
	fclose(hIFile);
	hOFile = fopen(sOFile,"w");
	int nValue;
	Node * TmpNode;
	for( i = 0; i < nNumOfNodes; i ++){
		nValue = i + 10000;
		nValue *= 100;
		fprintf(hOFile, "%d\n\t", nValue);
		for(TmpNode = MyNodeList[i]->FNext; TmpNode; TmpNode = TmpNode->FNext){
			nValue = TmpNode->SeqNum; 
			nValue += 10000;
			nValue *= 100;
			fprintf(hOFile, "%d ",nValue); 
		}
		fprintf(hOFile, "\n\t");
		for(TmpNode = MyNodeList[i]->CNext; TmpNode; TmpNode = TmpNode->CNext){
			nValue = TmpNode->SeqNum; 
			nValue += 10000;
			nValue *= 100;
			fprintf(hOFile, "%d ",nValue); 
		}
		fprintf(hOFile, "\n");
	}
	fclose(hOFile);
	return 0;
}

void creat_child(Node ** MyNodeList, int a, int b){
	Node * TmpNode;
	TmpNode = MyNodeList[a];
	for(; TmpNode->CNext; TmpNode = TmpNode->CNext);
	TmpNode->CNext = (Node *)malloc(sizeof(Node));
	TmpNode->CNext->SeqNum = b;
	TmpNode->CNext->CNext = NULL;

	TmpNode = MyNodeList[b];
	for(; TmpNode->FNext; TmpNode = TmpNode->FNext);
	TmpNode->FNext = (Node *)malloc(sizeof(Node));
	TmpNode->FNext->SeqNum = a;
	TmpNode->FNext->FNext = NULL;
}
