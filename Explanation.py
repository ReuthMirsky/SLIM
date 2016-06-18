'''
Created on Mar 7, 2013

@author: Reuth
'''
#import defs.Tree

class Explanation(object):
    '''
    classdocs
    '''
    expsNum=0

    def __init__(self, trees=[]):
        '''
        Constructor
        '''
        self._trees = []    # A list of the current trees
        self._pendingSets = []  # A list of each tree's pending set
        for tree in self._trees:
            self._pendingSets.append(tree.getFrontier(True))
        self._probRoots = 1.0
        self._probChoices = 1.0
        self._age = 0
        self._probability = -1.0
        Explanation.expsNum+=1
        
    def myCopy(self):
        newone = type(self)()
        for tree in self._trees:
            newone._trees.append(tree.myCopy())
        #newone._pendingSets=myCopy(self._pendingSets)
        newone._probRoots = self._probRoots
        newone._probchoices=self._probChoices
        newone._age = self._age
        newone._probability = self._probability
        return newone
        
    def __del__(self):
        Explanation.expsNum-=1

    # Try to print the tree nicely
    def __repr__(self):
        if self._trees == []:
            return "Empty Explanation"
        res = "Explanation ("
        res += str(self.getExpProbability())
        res += "):\n"
        treeNums = []
        for tree in self._trees:
            treeNums.append(tree.getID())
            res += tree.reprWithParams(depth="\t")
            res += "\tfrontier: \n"
            res += "\t"+str(tree.getFrontier(withIndices=True))
            res += "\n"
        res+="Trees:"
        res+=str(treeNums)
        res+="\n"
        
        # self.printExpProbability()
        return res
    
    def __eq__(self, other):
        if len(self._trees)!=len(other._trees):
            return False
        else:
            for i in range(len(self._trees)):
                if self._trees[i]!=other._trees[i]:
                    return False
        return True
    
    def printInMCSAForm(self):
        print "<?xml version=\"1.0\"?>"
        res = "<ROOT probName=\"Oracle.xml\" answer=\"***\">\n"
        pos=1
        for tree in self._trees:
            treeRepr=tree.reprForMCSA("\t",pos)
            res += treeRepr[0]
            pos=treeRepr[1]
        res += "</ROOT>"
        print res
    
    def printExpProbability(self):
        print "roots=",self._probRoots
        print "probChoices=",self._probChoices
        psIndex=0
        for PS in self._pendingSets:
            if len(PS)!=0:
                print "ps at ",psIndex,"=",len(PS)
            psIndex+=1
        
    def getTrees(self):
        return self._trees
    
    def getTree(self, index=0):
        if len(self._trees)<index:
            return self._trees[-1]
        else:
            return self._trees[index] 
        
    def setTree(self, newTree, index=-1):
        if len(self._trees)<index or -1==index:
            self._trees.append(newTree)
            self._pendingSets.append(newTree.getFrontier(True))
        else:
            self._trees[index]=newTree
            
    def backpatchPS(self, tAddition):
        for PS in self._pendingSets:
            PS.append(tAddition)
            
    def getTreeIDs(self):
        treeNums = []
        for tree in self._trees:
            treeNums.append(tree.getID())
        return treeNums
    
    def removeTree(self, index):
        if not (len(self._trees)<index or -1==index):
            self._trees.pop(index)
                
    def updateLocalProbChoices(self, tree):
        self._probChoices *= tree.getProbability()
        
    def updateLocalProbRoots(self, newRootProbability):
        self._probRoots *= newRootProbability
        
    def setExpProbability(self, prob):
        self._probability = prob    
    
    def getExpProbability(self):
        if self._probability != -1:
            return self._probability
        else:
            res = 1.0
            res *= self._probRoots
            res *= self._probChoices
            for PS in self._pendingSets:
                if len(PS)!=0:
                    res *= 1.0/len(PS)
            return res
    
    def getFrontierSize(self):
        res = 0
        for tree in self._trees:
            res += len(tree.getFrontier(False))
        return res
 
    def getAvgTreeSize(self):
        res = 0.0
        amoutOfTrees=0
        for tree in self._trees:
            res += tree.getDepth()
            amoutOfTrees+=1
        return res / len(self._trees) 
    
    def getSize(self):
        return len(self.getTrees())
    
    def incrementAge(self):
        self._age += 1
        
    def resetAge(self):
        self._age = 0
        
    def getAge(self):
        return self._age