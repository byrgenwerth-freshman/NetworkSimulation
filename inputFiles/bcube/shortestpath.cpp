#include <iomanip>
#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include "node.h"
using namespace std;

const int LINKS = 64;

int *arrayptr; 
int graph[LINKS][3];
int originalgraph[LINKS][3];
int K, currentk, NODES;
int FLAG=0;

int readgraph(int matrix[][3], istream& fin);

void printgraph(int matrix[][3], int items);

void initializenodes(nodeClass matrix[], int nodes, int source);

int pickcheapest(nodeClass matrix[], int nodes);

bool complete(nodeClass matrix[], int nodes);

void printpath(nodeClass matrix[], int start, int end, ofstream& fout);

void shortestpath(nodeClass matrix[], int graph[][3], int source, int links, int nodes);

void resetnodes(nodeClass matrix[], int nodes);

bool deletecheapest(int matrix[][3], int path[], int totallinks, ofstream& fout);

int main(int argc, char *argv[])
{
	
        if(argc != 4)
	{
	  cerr << "This requires 3 arguments." << endl;
	  cerr << "Source, Sink, Number of Paths" << endl;
	  exit(2);
	}

        ifstream fin; //fin is to read in the graph
	ofstream fout, ferr; 

	int links;
	nodeClass *paths;
	//int deleted[LINKS];

	int a, source, sink, nodes;
	source = atoi(argv[1]);
	sink = atoi(argv[2]);
	K = atoi(argv[3]);

	//Change this to the topology file
	fin.open("bcube.txt"); // open input file

	if(fin.fail()) //alert user if input file could not be opened
	{
		cerr << "Couldn't open file 'bcube.txt'/n";
		exit(1);
	}

	fin >> nodes;

	NODES=nodes;

	paths=new nodeClass[nodes];

	links=readgraph(graph, fin);

	//store original graph configuration used to reset graph
	for(int m=0; m<LINKS; m++)
	{
		for(int n=0; n<3; n++)
		{
			originalgraph[m][n]=graph[m][n];
		}
	}

       	a=source;
       	if(source==0)
       	{
       		return 0;
       	}

       	//open output streams to document results
       	fout.open("kshortestpaths.txt", ios::app);
       	ferr.open("kerrors.txt", ios::app);

       	//printgraph(graph, links);

       	for(currentk = 1; currentk <= K; currentk++)
       	{
	        resetnodes(paths, nodes);

	        FLAG=0;  //reset error flag

       		initializenodes(paths, nodes, source);

       		shortestpath(paths, graph, source, links, nodes);

       		if(FLAG>0)
       		{
       			ferr<<"For source "<<source<<" and sink "<<sink<<", could only find "<<FLAG-1<<" paths instead of "<<K<<"."<<endl;
       			break;  //break out of otherwise infinite for loop
       		}

       		printpath(paths, a, sink, fout);

       		deletecheapest(graph, arrayptr, links, fout);

       		//printgraph(graph, links);

       	}//end of for loop

       	//reset graph for new k pair
       	for(int m=0; m<LINKS; m++)
       	{
       		for(int n=0; n<3; n++)
       		{
       			graph[m][n]=originalgraph[m][n];
       		}
       	}
       	ferr.close();
       	fin.close();
	resetnodes(paths, nodes);
       	fout.close();

	delete[] arrayptr;  //avoids memory leak after printpath is called
	delete [] paths;
	return 0;

	/*cout << endl << "The node data is:" << endl << endl;

	cout << setw(10) << "identity"  
	<< setw(10) << "pathcost" 
	<< setw(10) << "previous"
	<< setw(10) << "tag" 
	<< setw(10) << "length" << endl;

	for(i=0; i<nodes; i++)
	{
	cout << paths[i] << endl;
	}*/
}

int readgraph(int matrix[][3], istream& fin)
{
	int i;
	i=0;
	char tmp;
	while (i < LINKS && !fin.eof())
	{  
		fin >> matrix[i][0]     //1st side of edge
		>> tmp
			>> matrix[i][1]     //2nd side of edge
		>> matrix[i][2];    //edge cost
		i++;  
	}
	return i;  //i will be returned as the number of links
}

void printgraph(int matrix[][3], int items)
{
	int i;  //i is index of row, j is index of column
	//cout << "The graph is: " << endl;
	for(i=0; i<items-1; i++)  //write as many rows as recorded by filling function
	{
	  //        cout << matrix[i][0]
	  //	<< "-"
	  //		<< matrix[i][1]
	  //	<< "  "
	  //		<< matrix[i][2]
	  //	<< endl;
	}
	return;
}

void initializenodes(nodeClass matrix[], int nodes, int source)
{
	int i,j;
	j=0;
	for(i=0; i<nodes; i++)
	{
		j++;
		matrix[i].setidentity(j);  //numbers the nodes
		if(j==source)
		{
			matrix[i].settag('a');  
			matrix[i].setpathcost(0);   //forces pickcheapest to pick source first
			matrix[i].setprev(1);   //necessary to get path length to work right
		}
	}
}

int pickcheapest(nodeClass matrix[], int nodes)
{
	int i, j, m, min;
	min=999;
	j=0;
	for(i=0; i<nodes; i++)
	{   //search through array of nodes
		if(matrix[i].gettag()=='a')
		{   //only look at adjacent nodes
			if(matrix[i].getpathcost()<min)
			{
				j=matrix[i].getidentity();      //j is the identity of cheapest node
				min=matrix[i].getpathcost();    //save current min
			}
		} 
	}

		j--;                    //decrement j for use as index
		if(j<0)
		{
			FLAG=currentk;
			return 1;
		}
		matrix[j].settag('s');  //make the cheapest node member of the shortest path
		m=matrix[j].getprev();  //get identity of previous node
		m--;                    //decrement m for use as index
		if(m<0)
		{
			FLAG=currentk;
			return 1;
		}
		m=matrix[m].getlength();//store in m the length of path up to previous node
		m++;                    //increment m to account for node just added to length
		matrix[j].setlength(m); //set length of node just chosen to m
		j++;                    //increment j for use as identity
	return j;
}

bool complete(nodeClass matrix[], int nodes)
{
	int i;
	for(i=0; i<nodes; i++)
	{
		if(matrix[i].gettag()!='s') 
			return false;   //if there are any nodes with tag v or a, shortest path not complete
	}
	return true;    //if all nodes have s, the shortest path is complete
}

void printpath(nodeClass matrix[], int start, int end, ofstream& fout)
{
	end--;      //decrement to use as index
	int i, j, nodes; 
	nodes=matrix[end].getlength();  //number of nodes to get to last node in path
	end++;                          //increment to use as identity

	arrayptr = new int[nodes+1];      //array to store path in souce to sink order

	fout << start << " " << end << " " << currentk << " "
		<< matrix[end-1].getpathcost() << " | ";

	arrayptr[0]=nodes;
	arrayptr[nodes]=end;  //place sink in last location of array

	for(i=1; i<nodes; i++)
	{
		j=arrayptr[(nodes+1)-i];    //previous node identity
		j--;        //decrement to use as index
		arrayptr[nodes-i]=matrix[j].getprev();   
	}
	for(i=1; i<(nodes+1); i++)
	{
		fout << arrayptr[i] << " ";
	}  
	fout << "| " << nodes <<endl;
}


void shortestpath(nodeClass matrix[], int graph[][3], int source, int links, int nodes)
{
	int i, j, adjacent, counter;
	counter=0;
	while(!complete(matrix, nodes))    //continue until every node is included in tree
	{
		if(counter>NODES)
		{
			FLAG=currentk;
			return;
		}
		source=pickcheapest(matrix, nodes);    //find the adjacent with the cheapest path cost


		//the for loop updates all adjacent nodes of the new source changing their pathcosts, previous nodes, and tags
		for(i=0; i<links; i++)
		{
			if(source==graph[i][0]) //checks if edge is attached to source
			{
				adjacent=graph[i][1];
				adjacent--;         
				source--; 
				if(adjacent >= 0 && source >= 0)
				{
					if(matrix[adjacent].getpathcost()>      //check if pathcost of adjacent can be improved by going
						matrix[source].getpathcost()+graph[i][2])  //through the source-adjacent edge 
					{
						matrix[adjacent].setpathcost(matrix[source].getpathcost()+graph[i][2]);
						matrix[adjacent].settag('a');       //node has been visited, so set as adjacent
						j=source;
						j++;             //identity of source
						matrix[adjacent].setprev(j);    //updates adjacent node's predecessor to source
					} 
				}	
				source++;
			}
			if(source==graph[i][1]) //checks other if other side of edge is connected to the source
			{                       //this whole block replicates the above block of code
				adjacent=graph[i][0];       
				adjacent--;        
				source--;
				if(adjacent >= 0 && source >= 0)
				{
					if(matrix[adjacent].getpathcost()>      
						matrix[source].getpathcost()+graph[i][2])
					{
						matrix[adjacent].setpathcost(matrix[source].getpathcost()+graph[i][2]);
						matrix[adjacent].settag('a');
						j=source;
						j++;
						matrix[adjacent].setprev(j);
					}
				}	
				source++; 
			}
		} 
		//cout << endl << "The node data is:" << endl << endl;

		//cout << setw(10) << "identity"  
		//	<< setw(10) << "pathcost" 
		//	<< setw(10) << "previous"
		//	<< setw(10) << "tag" 
		//	<< setw(10) << "length" << endl;

		for(i=0; i<nodes; i++)
		{
		  //	cout << matrix[i] << endl;
		}

		if(complete(matrix, nodes))
		  //	cout<<"done"<<endl;

		counter++;	
	}
	//cout<<"shortest path function looped " <<counter<<" times"<<endl;
}

void resetnodes(nodeClass matrix[], int nodes)
{
	int i;
	for(i=0; i<nodes; i++)
		matrix[i].reset();
}

bool deletecheapest(int matrix[][3], int path[], int totallinks, ofstream& fout)
{
	int i, leftcurrent, rightcurrent, leftmin, rightmin, cheapestlink;
	int pathlinks = path[0]; //number of links in path
	cheapestlink=999;

	leftmin=rightmin=leftcurrent=rightcurrent=0;

	for(int j=1; j<pathlinks; j++)
	{
		leftcurrent=path[j];
		rightcurrent=path[j+1];
		for(i=0; i<totallinks; i++)
		{
			//if path propagates forward
			if(leftcurrent==matrix[i][0]) 
			{
				if(rightcurrent==matrix[i][1])  //if right & left nodes match path link
				{
					if(matrix[i][2]<cheapestlink)
					{
						cheapestlink=matrix[i][2]; //save cheapest link cost
						leftmin=leftcurrent;  //save left node of cheapest link
						rightmin=rightcurrent;  //save right node of cheapest link
					}
				}
			}
			if(rightcurrent==matrix[i][1]) 
			{                       
				if(leftcurrent==matrix[i][0]) //if right & left nodes match path link
				{
					if(matrix[i][2]<cheapestlink)
					{
						cheapestlink=matrix[i][2]; //save cheapest link cost
						leftmin=leftcurrent;  //save left node of cheapest link
						rightmin=rightcurrent;  //save right node of cheapest link
					}
				}   
			}

			//if path propagates backwards
			if(leftcurrent==matrix[i][1]) 
			{
				if(rightcurrent==matrix[i][0])  //if right & left nodes match path link
				{
					if(matrix[i][2]<cheapestlink)
					{
						cheapestlink=matrix[i][2]; //save cheapest link cost
						leftmin=leftcurrent;  //save left node of cheapest link
						rightmin=rightcurrent;  //save right node of cheapest link
					}
				}
			}
			if(rightcurrent==matrix[i][0]) 
			{                       
				if(leftcurrent==matrix[i][1]) //if right & left nodes match path link
				{
					if(matrix[i][2]<cheapestlink)
					{
						cheapestlink=matrix[i][2]; //save cheapest link cost
						leftmin=leftcurrent;  //save left node of cheapest link
						rightmin=rightcurrent;  //save right node of cheapest link
					}
				}   
			}
		}//end of link search for loop
	}//end of path traversal for loop

	//now delete the cheapest link
	for(i=0; i<totallinks; i++)
	{
		//if path propagates forward
		if(leftmin==matrix[i][0]) 
		{
			if(rightmin==matrix[i][1])  //if right & left nodes match path link
			{
				matrix[i][0]=matrix[i][1]=0;
			}
		}

		if(rightmin==matrix[i][1]) 
		{                       
			if(leftmin==matrix[i][0]) //if right & left nodes match path link
			{
				matrix[i][0]=matrix[i][1]=0;
			}   
		}
		
		//if path propagates backward
		if(leftmin==matrix[i][1]) 
		{
			if(rightmin==matrix[i][0])  //if right & left nodes match path link
			{
				matrix[i][0]=matrix[i][1]=0;
			}
		}

		if(rightmin==matrix[i][0]) 
		{                       
			if(leftmin==matrix[i][1]) //if right & left nodes match path link
			{
				matrix[i][0]=matrix[i][1]=0;
			}   
		}
	} 

	//	fout << "cheapest link cost of: " <<cheapestlink<< " left node: " <<leftmin
	//	<< " right node: " <<rightmin <<endl;

	return false;
}
