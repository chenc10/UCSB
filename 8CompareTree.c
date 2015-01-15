#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<dirent.h>
#include<time.h>

#define BUFFER_SIZE 1000
#define THRESHOLD 0.01
#define THRESHOLD_NUM_DIFF 2

int nRows = 0, nCols = 0;
int i,j;
char * Buffer, * cBuffer;
char * sSoft1, * sSoft2;
char * sFileName1, *sFileName2;
typedef struct _TNode{
	int Type;
	int SeqNum;
	int NumOfNodes;
	int NumOfChild;
	int BLevel;
	struct	_TNode ** TNCList;
}TNode;
TNode ** AllTNList;
TNode * TRoot1, * TRoot2;
float gen_sim(struct dirent * pFile1, struct dirent * pFile2);
void gen_treenodelist(FILE * hFile, TNode ** TRoot);
void gen_diffnum(TNode * TRoot1, TNode * TRoot2, int * DiffNumOfNodes1 , int * DiffNumOfNodes2 );
int compare_node(TNode * , TNode * );
int main(int argc, char * argv[])
{
	clock_t start,end;
	start=clock();
	DIR * pFolder1, *pFolder2;
	struct dirent * pFile1, *pFile2;	
	Buffer = (char *)malloc(BUFFER_SIZE * sizeof(char));
	cBuffer = (char *)malloc(BUFFER_SIZE * sizeof(char));
	sSoft1 = (char *)malloc(100*sizeof(char));
	sSoft2 = (char *)malloc(100*sizeof(char));
	sFileName1 = (char *)malloc(100*sizeof(char));
	sFileName2 = (char *)malloc(100*sizeof(char));
	TRoot1 = (TNode *)malloc(sizeof(TNode));
	TRoot2 = (TNode *)malloc(sizeof(TNode));
	if( argc < 3 ){
		return 0;
	}else{
		strcpy(sSoft1,argv[1]);
		strcpy(sSoft2,argv[2]);
	}
	if(!strcmp(sSoft1,sSoft2))
		return 0;

	pFolder1 = opendir(sSoft1);
	pFolder2 = opendir(sSoft2);
	while( (pFile1 = readdir(pFolder1)) != NULL){	
		if( !strstr(pFile1->d_name, ".dat"))	continue;
		nRows ++;
	}
	while( (pFile2 = readdir(pFolder2)) != NULL){	
		if( !strstr(pFile2->d_name, ".dat"))	continue;
		nCols ++;
	}
	if( (float)nRows / nCols > THRESHOLD_NUM_DIFF || (float)nCols / nRows > THRESHOLD_NUM_DIFF){
		closedir(pFolder1);
		closedir(pFolder2);
		printf("	result: 0.00\n") ;
		return 0;
	}
	rewinddir(pFolder1);
	rewinddir(pFolder2);
	float ** mfSim;//matrix of float value
	mfSim = (float **)malloc( nRows * sizeof(float *));
	for(i = 0; i < nRows; i ++)
		mfSim[i] = (float *)malloc( nCols * sizeof(float));
	for(i = 0; i < nRows && (pFile1 = readdir(pFolder1));  ){
		if(strstr(pFile1->d_name, ".dat") == NULL) continue;
		for(j = 0; j < nCols && (pFile2 = readdir(pFolder2)); ){
			if(strstr(pFile2->d_name, ".dat") == NULL) continue;
			mfSim[i][j] = gen_sim(pFile1, pFile2);
			//printf("filename: 1-%s 2-%s %f\n", pFile1->d_name, pFile2->d_name, mfSim[i][j]);
			j ++;
		}
		i ++;
		rewinddir(pFolder2);
	}
	closedir(pFolder1);
	closedir(pFolder2);
	int * pFlagRow, * pFlagCol;
	int nSimGraph = 0;
	float SoftSimilarity = 0.0;
	pFlagRow = (int *)malloc(nRows * sizeof(int));
	pFlagCol = (int *)malloc(nCols * sizeof(int));
	for( i = 0; i < nRows; i ++) pFlagRow[i] = 0;
	for( j = 0; j < nCols; j ++) pFlagCol[j] = 0;
	for( i = 0; i < nRows; i ++)
		for( j = 0; j < nCols; j ++){
			if(pFlagRow[i] || pFlagCol[j])
				continue;
			if(mfSim[i][j] > THRESHOLD){
				pFlagRow[i] = 1;
				pFlagCol[j] = 1;
				nSimGraph ++;
			}
		}
	SoftSimilarity = (float)nSimGraph / (nRows + nCols);
	printf("	result: %.2f\n", SoftSimilarity);
	return 0;
	end = clock();
	float dur;
	dur = (float)(end-start)/CLOCKS_PER_SEC;
	printf("	time %f\n",dur);
	return 0;
}


float gen_sim(struct dirent * pFile1, struct dirent * pFile2)
{
	FILE * hFile1, * hFile2;
	strcpy(sFileName1, sSoft1);
	strcpy(sFileName2, sSoft2);
	strcat(sFileName1, pFile1->d_name);
	strcat(sFileName2, pFile2->d_name);
	//printf("enter gen_sim: %s %s\n",sFileName1, sFileName2);
	hFile1 = fopen(sFileName1,"r");
	hFile2 = fopen(sFileName2,"r");
	gen_treenodelist(hFile1, &(TRoot1));
	gen_treenodelist(hFile2, &(TRoot2));
	fclose(hFile1);
	fclose(hFile2);
	if(TRoot1->BLevel == 1 || TRoot2->BLevel == 1) return 0.0;
	int nTotalNumOfNodes1, nTotalNumOfNodes2;
	nTotalNumOfNodes1 = TRoot1->NumOfNodes;
	nTotalNumOfNodes2 = TRoot2->NumOfNodes;
	int DiffNumOfNodes1=0, DiffNumOfNodes2=0;
	gen_diffnum(TRoot1, TRoot2, &DiffNumOfNodes1, &DiffNumOfNodes2);
	//printf("nT1: %d, nT2: %d, DN1: %d, DN2: %d\n", nTotalNumOfNodes1, nTotalNumOfNodes2, DiffNumOfNodes1, DiffNumOfNodes2);
	float sim1 = 1 - (float)DiffNumOfNodes1/TRoot1->NumOfNodes;
	float sim2 = 1 - (float)DiffNumOfNodes2/TRoot2->NumOfNodes;

	if(sim1 > sim2) return sim2;
	return sim1;
}

void gen_diffnum(TNode * TRoot1,TNode * TRoot2, int * DiffNumOfNodes1, int * DiffNumOfNodes2){
	int I;
	if(!compare_node(TRoot1,TRoot2)){
		*DiffNumOfNodes1 += TRoot1->NumOfNodes;
		*DiffNumOfNodes2 += TRoot2->NumOfNodes;
		return;
	}
	for(I = 0; I < TRoot1->NumOfChild || I < TRoot2->NumOfChild; I ++){
		if( I >= TRoot1->NumOfChild){
			*DiffNumOfNodes2 += TRoot2->TNCList[I]->NumOfNodes;
			continue;
		}
		else if( I >= TRoot2->NumOfChild){
			*DiffNumOfNodes1 += TRoot1->TNCList[I]->NumOfNodes;
			continue;
		}
		gen_diffnum(TRoot1->TNCList[I],TRoot2->TNCList[I],DiffNumOfNodes1,DiffNumOfNodes2);
	}
}
int compare_node(TNode * TNode1, TNode * TNode2){
	float Numerator = 0.0, Denominator1 = 0.0, Denominator2 = 0.0;
	int k;
	if(TNode1->Type != TNode2->Type) return 0;
	if((float)TNode1->NumOfNodes / TNode2->NumOfNodes < 0.8 || (float)TNode2->NumOfNodes / TNode1->NumOfNodes < 0.8) return 0;
	if((TNode1->NumOfChild == 0) && (TNode2->NumOfChild == 0)) return 1;
	for( k = 0; k < TNode1->NumOfChild || k < TNode2->NumOfChild; k ++){
		if( k >= TNode1->NumOfChild){
			Denominator2 += ((float)(TNode2->TNCList[k]->NumOfNodes))*((float)(TNode2->TNCList[k]->NumOfNodes));	
			continue;
		}else if(k >= TNode2->NumOfChild){
			Denominator1 += ((float)(TNode1->TNCList[k]->NumOfNodes))*((float)(TNode1->TNCList[k]->NumOfNodes));	
			continue;
		}
		Numerator += ((float)(TNode1->TNCList[k]->NumOfNodes)) * ((float)(TNode2->TNCList[k]->NumOfNodes));	
		Denominator1 += ((float)(TNode1->TNCList[k]->NumOfNodes))*((float)(TNode1->TNCList[k]->NumOfNodes));	
		Denominator2 += ((float)(TNode2->TNCList[k]->NumOfNodes))*((float)(TNode2->TNCList[k]->NumOfNodes));	
	}
	if( Numerator*Numerator / (Denominator1 * Denominator2) > 0.8) return 1;
	return 0;
}
void gen_treenodelist(FILE * hFile, TNode ** TRoot)
{
	int k = 0, m = 0, n = 0;
	int sign = 0;
	int nTSeqNum = 0;
	int nTmpValue = 0; 
	char * tok = NULL;
	TNode * pForSwap = NULL;
	AllTNList = NULL;
	TNode * CurrentTNode = NULL;
	for( sign = 0; fgets(Buffer, BUFFER_SIZE, hFile); sign ++) 	;
	sign/=2;
	rewind(hFile);
	AllTNList = (TNode **)malloc(sign * sizeof(TNode *));
	for( sign = 1; fgets(Buffer,BUFFER_SIZE, hFile); sign ++){
		if(sign%2 == 0) continue;
		CurrentTNode = (TNode *)malloc(sizeof(TNode));	
		tok = strtok(Buffer," ");
		CurrentTNode->SeqNum = atoi(tok);
		tok = strtok(NULL," ");
		CurrentTNode->Type = atoi(tok);
		tok = strtok(NULL," ");
		CurrentTNode->NumOfNodes = atoi(tok);
		tok = strtok(NULL," ");
		CurrentTNode->BLevel = atoi(tok);
		CurrentTNode->NumOfChild = 0;
		CurrentTNode->TNCList = NULL;
		if(nTmpValue < CurrentTNode->NumOfNodes){
			nTmpValue = CurrentTNode->NumOfNodes;
			*TRoot = CurrentTNode;
		}
		AllTNList[CurrentTNode->SeqNum] = CurrentTNode;
	}
	rewind(hFile);
	for( sign = 0; fgets(Buffer, BUFFER_SIZE, hFile); sign = sign + 1){
		if(strlen(Buffer) > BUFFER_SIZE - 5 ){
			fprintf(stderr,"error! Buffer exceeded!\n");
			exit(-1);
		}
		if(sign%2 == 0) continue;
		nTSeqNum = sign/2;
		strcpy(cBuffer, Buffer);
		tok = strtok(cBuffer," ");
		while(tok && (atoi(tok) || strstr(tok,"0"))){//strlen(tok)>2 || atoi(tok))){

			AllTNList[nTSeqNum]->NumOfChild ++;
			tok = strtok(NULL," "); } AllTNList[nTSeqNum]->TNCList = (TNode **)malloc( AllTNList[nTSeqNum]->NumOfChild * sizeof(TNode *));
		for( k = 0; k < AllTNList[nTSeqNum]->NumOfChild; k ++){
			if(!k) tok = strtok(Buffer," ");
			else tok = strtok(NULL," ");
			if( !atoi(tok) && !strstr(tok,"0")){
				printf("error tok: (k)%d %s\n", k, tok);
				exit(-1);
			}
			AllTNList[nTSeqNum]->TNCList[k] = AllTNList[atoi(tok)];
		}
		if(AllTNList[nTSeqNum]->NumOfChild > 1){
			for( m = 0; m < AllTNList[nTSeqNum]->NumOfChild - 1; m ++)
				for( n = 0; n < AllTNList[nTSeqNum]->NumOfChild - 1; n ++) {
					if(AllTNList[nTSeqNum]->TNCList[n]->Type > AllTNList[nTSeqNum]->TNCList[n+1]->Type ) continue;
					if(AllTNList[nTSeqNum]->TNCList[n]->Type == AllTNList[nTSeqNum]->TNCList[n+1]->Type && AllTNList[nTSeqNum]->TNCList[n]->NumOfNodes >= AllTNList[nTSeqNum]->TNCList[n+1]->NumOfNodes) continue;
					pForSwap = AllTNList[nTSeqNum]->TNCList[n];
					AllTNList[nTSeqNum]->TNCList[n] = AllTNList[nTSeqNum]->TNCList[n+1];
					AllTNList[nTSeqNum]->TNCList[n+1] = pForSwap; 
				}
		}
	}
}
