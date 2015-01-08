This is a brief introduction of my work.
* For better understanding of my work, I divide the whole program into several independent part as flow:

	1GetDataFromIDA.py
		read data from IDA results into a txt file

	2ReadDataFromFile.py
		read data from txt file into memory

 	3PreOperationMethod.py
		exert pre-operation method 

	4AbstractionMethod1.py
		using abstraction method 1 to simplify the graph

 	5AbstractionMethod2.py
		using abstraction method 2 to simplify the graph

 	6AbstractionMethod3.py
		using abstraction method 3 to simplify the graph


    	ABOVE is for debugging and reading seperately. And each file can be executed independently.
 

 	7WholeAbstractionCode.py
		this is an integrated code from the last 6 independent files and it can finish all the abstraction work.

    	I've finished the inner construction inside each node. About the detailed instruction, please refer to the report named "Intro_CFG_Matching_Method.pdf".
	
	8CompareTree.py
		this code is for comparing the two trees inside the final nodes after abstraction. We can achieve exact matching currently.


* Let me use a real example of file to illustrate the result of abstraction:

	The initial cfg graph is in the file "Before_CFGGraph.jpg"

	The tree inside the final node after abstraction is represented by the file "After_TreeGraph.jpg". And the construction of this tree can show the process of abstraction and we can use it for comparing it with another CFG.

	Every CFG is abstracted into such a tree in the database. And we can judge whether two initial CFGs are similar by comparing their trees with 8CompareTree.py.

* If you want to have a try:
	
	First, run 1GetDataFromIDA.py under IDA->python_command, and a file named "GDB.txt" would be generated. Every three lines in "GDB.txt" mean the address of a node, the addresses of its fathers and the addresses of its children, respectively. 
	Second, run 7WholeAbstractionCode.py under the same folder. It will automatically read the 'GDB.txt' file and give useful results.

* What's the next:

	We need to decide to what extend shall we tolerate the difference between two trees when judging them as "similar". I'm reading papers to better understand the mechanism polymorphism.
	
_____________2014_11_5____________
The test results is terrible.... I have found some problem in the comparing method( 8
