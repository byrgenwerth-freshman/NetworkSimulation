#pragma once;

#include <fstream>
#include <iostream>
#include <string>
using namespace std;

class nodeClass
{
public:
    nodeClass();  

    void reset();

    //accessors or getters
    int getidentity()const;

    int getpathcost()const;
    
    int getlength()const;
    
    int getprev()const;
    
    char gettag()const;
    
    //modifiers or setters
    void setidentity(int newidentity);

    void setpathcost(int newpathcost);
    
    void setlength(int newlength);
   
    void setprev(int newprev);
    
    void settag(char newtag);

    friend ostream & operator<<(ostream & out,
        const nodeClass &right);
    
private:
    int identity, pathcost, length, prev;
    char tag;
};