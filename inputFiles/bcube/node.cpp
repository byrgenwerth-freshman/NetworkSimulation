#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include "node.h"

using namespace std;

nodeClass::nodeClass()
{ 
    identity=0;
    pathcost=999;
    length=0;
    prev=0;
    tag='v';
}

void nodeClass:: reset()
{
    identity=0;
    pathcost=999;
    length=0;
    prev=0;
    tag='v';
}

//accessors or getters
int nodeClass::getidentity()const
{
    return identity;
}

int nodeClass::getpathcost()const
{
    return pathcost;
}

int nodeClass::getlength()const
{
    return length;
}

int nodeClass::getprev()const
{
    return prev;
}

char nodeClass::gettag()const
{
    return tag;
}

//modifiers or setters
void nodeClass::setidentity(int newidentity)
{
    identity=newidentity;
}

void nodeClass::setpathcost(int newpathcost)
{
    pathcost=newpathcost;
}

void nodeClass::setlength(int newlength)
{
    length=newlength;
}

void nodeClass::setprev(int newprev)
{
    prev=newprev;
}

void nodeClass::settag(char newtag)
{
    tag=newtag;
}

ostream & operator<<(ostream & out,
        const nodeClass &right)
{
    out << setw(10) << right.identity 
        << setw(10) << right.pathcost
        << setw(10) << right.prev
        << setw(10) << right.tag 
        << setw(10) << right.length;
    return out;
}
