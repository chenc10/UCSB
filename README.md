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



* Let me use a real example of file to illustrate the result of abstraction:

	The initial cfg graph is in the file "Before_CFGGraph.jpg"

	The tree inside the final node after abstraction is represented by the file "After_TreeGraph.jpg". And the construction of this tree can show the process of abstraction and we can use it for comparing it with another CFG.

* If you want to have a try:
	
	First, run 1GetDataFromIDA.py under IDA->python_command, and a file named "GDB.txt" would be generated. Every three lines in "GDB.txt" mean the address of a node, the addresses of its fathers and the addresses of its children, respectively. 
	Second, run 8WholeAbstractionCode.py under the same folder. It will automatically read the 'GDB.txt' file and give useful results.

* What's the next:

	Since the inner construction of nodes has been finished, it's easy to do experiments and give evaluation to our thoery.

	It's very possible that some problems be met when more experiments are done.

