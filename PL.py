import Tree
import NT
import Sigma
 
#import math
#import itertools
#from copy import deepcopy
 
#This class represents a plan library
class PL(object):
    '''
    classdocs
    '''
    plNum=0
 
    def __init__(self, sigma, NT, R, P):
        '''
        Constructor
        '''
        self._Sigma = sigma     # list of Sigmas
        self._NT = NT           # list of NTs
        self._R = R             # subset of NT
        self._P = P             # list of rules
        PL.plNum+=1
        #self._ruleProb = prob
    
 
        
    def __del__(self):
        PL.plNum-=1   
    
    def getRuleProbNotUniform(self, rule):
        if rule==() or rule==[]:
            return self._getRuleProb()
        amountOfMatchingRules = 0.0
        for rule in self._P:
            if rule._A.get() == rule._A.get():
                amountOfMatchingRules += 1
        if amountOfMatchingRules == 0:
            return 0
        else:
            return rule.getPriorProbability()/amountOfMatchingRules
 
    def isGoalLetter(self, letter):
        for goal in self._R:
#            print goal.get()
            #print letter.get()
            if goal.get() == letter.get():
                #print "here2"
                return True
        return False
 
    def getRuleProb(self, startsWith=[]):
        if startsWith==[]:
            return 1.0/len(self._P)
        amountOfMatchingRules = 0.0
        for rule in self._P:
            if rule._A.get() == startsWith.get():
                amountOfMatchingRules += 1
        if amountOfMatchingRules == 0:
            return 0.0
        else:
            return 1.0/amountOfMatchingRules
        
    
    def __repr__(self):
        res = "Plan Library: \nSigma=" + self._Sigma.__repr__() + "\nNT=" + self._NT.__repr__() + "\nR=" + self._R.__repr__() + "\nRules="
        for rule in self._P:
            res += "\t" + rule.__repr__() + "\n"
        return res
    
    def getGoals(self):
        return self._R
    
    def getRootProb(self):
        return 1.0/len(self._R)
    
# This function returns the set of generating trees whose foot is obs and root is root of the new tree
    def generatingSetForObs(self, treesBeforeSubstitute, observation):
        #treesBeforeSubstitute = self.generatingSet([root])
        treesAfterSubstitute = []
        for tree in treesBeforeSubstitute:
 
 
            footWithIndex = tree.isLeftMostTree(byIndex=True)
            #If this tree has a foot (must be true here, if false, it's a bug!) and if this foot matches the observation 
            if footWithIndex and footWithIndex[0].sameParameters(observation, '-1') :
                newCopy = tree    #myCopy - Removed 
                if newCopy.substitute(observation, footWithIndex[1]):
                    treesAfterSubstitute.append(newCopy)
        return treesAfterSubstitute
    
   # This function returns the set of generating trees whose foot is replaced by fragment and root is root of the new tree
    def generatingSetForFragment(self, fragment):
        generatingSet = []
        for rule in self._P:
            for (childLetter, index) in rule.leftMostChildsWithNums():
                if childLetter.get() == fragment.getRoot().get():
                    generatingSet += self.createTreesUpwards(rule, index, fragment)   
        return generatingSet 
            
    def createTreesUpwards(self, rule, index, specialChild, recursion=0):
        newSpecialChild = specialChild #deepcopy
        #If this is the last iteration, make empty descendants for all other children
        if rule._A in self._R:
            substitutionSuccessful = self.createFlatTreeForRule(rule, index, newSpecialChild)
            if substitutionSuccessful:
                return [self.createFlatTreeForRule(rule, index, newSpecialChild)]
            else:
                return []
        
        #If you need to go one level higher to get to a goal
        else:
            #make sure you're not entering an infinite loop by bounding the depth of the trees
            if recursion >= 3:
                return []
            else:
                recursion += 1
            
            possibleTrees = []
            for parentRule in self._P:
                #print "000"
                #print "parentRule=",parentRule
                for (letter, higherIndex) in parentRule.leftMostChildsWithNums():
                    if letter.get() == rule._A.get():
                        #print "111"
                        #print parentRule
                        treeForChild = self.createFlatTreeForRule(rule, index, newSpecialChild) #deepcopy
                        if treeForChild != []:
                            #print "222"
                            #print treeForChild
                            possibleTrees.extend(self.createTreesUpwards(parentRule, higherIndex, treeForChild, recursion))  

        #print "possibleTrees=", possibleTrees                
        return possibleTrees                     
   
    def createFlatTreeForRule(self, rule, index, specialChild):
        newSpecialChild = specialChild.myCopy()  #deepcopy
        alpha = []
        for childIndex in range(len(rule._alpha)):
            child=rule._alpha[childIndex] 
            if child._type == 'Sigma':
                alpha.append(Tree.Tree("Basic", child.myCopy(), (), [], self))
            else:
                # DEBUG: if here with a bug, you should consider that there might be a problem with the rules of the extended child"
                alpha.append(Tree.Tree("Complex", child.myCopy(), [], [], self))
                        
        newTree =  Tree.Tree("Complex", rule._A.myCopy(), rule, alpha, self)
        successInSubstitution = newTree.substituteNode(newSpecialChild, str(index))
        return newTree if successInSubstitution else []
         
    def generatingSet(self, generatingFrom):
        #res is a set of all leftmost trees deriving from this PL which start with a root from R or NT
        res=[] 
        for goal in generatingFrom:
            for rule in self._P:
                if goal.matchLetter(rule._A):
                    for tree in self.createTrees(rule):
                        if tree.isLeftMostTree():
                            res.append(tree)
 
 
 
                        else:
                            print "Not leftmost:"
                            print tree
                            print tree._rule
        return res                    
            
    def createTrees(self, rule, recursive=0):
        #if rule has only one child 
        if 1 == len(rule._alpha):
            if rule._alpha[0]._type=='Sigma':
                child = Tree.Tree("Basic", rule._alpha[0].myCopy(), (), [], self)
                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [child], self)
                return [root]
#             else:
#                 print "rule._alpha[0]=",rule._alpha[0] 
#                 possibleChildrenTrees = self.generatingSetForObs([rule._alpha[0]])
#                 print "rule._alpha[0].GS:=",possibleChildrenTrees 
#                 possibleTrees = []
#                 for subTree in possibleChildrenTrees:
#                     root = Tree.Tree("Complex", rule._A, rule, [subTree], self)
#                     possibleTrees.append(root)
#                 return possibleTrees
                #return []
        
        #else, need to create all possible outcomes from tree
        trees=[]
        leftMostChilds = rule.leftMostChilds(byIndex=True)
        for childIndex in leftMostChilds:#range(len(rule._alpha)):
            #if childIndex in leftMostChilds:
            if type(rule._alpha[childIndex])==NT.NT:
                #collect all possible derivations of this child to childTrees
                for childRule in self._P:
                    childRecursion = recursive
                    #Make sure you're not entering a possibly infinite loop (Left recursion bounding)
                    if childRule._A.get() == rule._A.get():
                        if childRecursion <= 3:
                            childRecursion += 1
                        else:
                            return trees
                        
                    if rule._alpha[childIndex].get() == childRule._A.get():
                        #to create the tree, other children should be basic tree nodes
                        otherChildren=self.otherChildrenTrees(rule, childIndex)
                        if otherChildren == []:
                            for tree in self.createTrees(childRule, childRecursion+1):
                                root = Tree.Tree("Complex", rule._A.myCopy(), rule, [tree], self)
                                trees.append(root)  
                        #for each possible combination of children:
                        else:
                            for singleOtherChildrenExp in otherChildren:
                                #add all current leftmostTrees to the list, under trees:
                                for tree in self.createTrees(childRule, childRecursion+1):
                                    allChildren=[]
                                    for childInSOC in singleOtherChildrenExp:
                                        allChildren.append(childInSOC.myCopy())
                                    allChildren.insert(childIndex,tree)
                                    root = Tree.Tree("Complex", rule._A.myCopy(), rule, allChildren, self)
                                    trees.append(root)  
        return trees
     
    def otherChildrenTrees(self, rule, specialChild):
        res=[]
        i = 0;
        for child in rule._alpha:
            if i != specialChild:
                listOfPossibleTrees = self.childWithPossibleRules(child)
                if res==[]:
                    res=listOfPossibleTrees
                else:
                    completeRes = []
                    for singleExp in res:
                        for newTree in listOfPossibleTrees:
                            newExp = singleExp  #myCopy - Removed
                            newExp.extend(newTree)
                            completeRes.append(newExp)   
                    res = completeRes  
            i += 1      
        return res    
 
    def childWithPossibleRules(self, child):
        res=[]
        if type(child)==Sigma.Sigma:
            res.append([Tree.Tree("Basic", child.myCopy(), (), PL=self)])
        else:
            childRules = []            
            for rule in self._P:    #Collect all possible rules this child might be
                if rule._A.get() == child.get():
                    childRules.append(rule)    
            res.append([Tree.Tree("Complex", child.myCopy(), childRules, PL=self)])
        return res 
 
#######################################################################################################
#                        Buttom-Up Functions
#######################################################################################################
    def createTreeForRule(self, rule):
        children=[]
        for child in rule._alpha:
            if child._type=='Sigma':
                children.append(Tree.Tree("Basic", child, (), [], self))
            else:
                # DEBUG: if here with a bug, you should consider that there might be a problem with the rules of the extended child"
                children.append(Tree.Tree("Complex", child, [], [], self))
        
        return  Tree.Tree("Complex", rule._A, rule, children, self)
    
    def createFragments(self, generatedFrom):
        if type(generatedFrom)!=NT.NT and type(generatedFrom)!=Sigma.Sigma:
            print type(generatedFrom)
            return None
        
        fragments = []
        for rule in self._P:
            #print "rule=", rule
            possibleRule = rule.isALeftmostChild(generatedFrom, False)
            if possibleRule:
                treeForRule = self.createTreeForRule(rule)
                for indexOfGeneretedInTree in possibleRule:
                    newFragment = treeForRule.myCopy()
                    newFragment.substitute(generatedFrom, str(indexOfGeneretedInTree))
                    fragments.append((newFragment, str(indexOfGeneretedInTree)))
        
        return fragments                       
                
                 
#    def createPFFG(self):
#        PFFG=[]
#        gl=self.generatingSet()
#        for tree in gl:
#            s = tree.treeToList()
#            foot = tree.isLeftMostTree()
#            footIndex = s.index(foot)
#            s.remove(foot)
#             
#            #make constraints list according to list without the foot
#            
#            # Order Constraints
#            # simply don't add this constraint to the new list of constraints
#            if len(s) < 2:
#                order = []
#            #else
#            order = []
#            tempOrder = tree.treeConstraints()
#            for cons in tempOrder:
#                if cons[0] == footIndex or cons[1] == footIndex:
#                    continue
#                cons0 = (cons[0]-1 if cons[0] > footIndex else cons[0])
#                cons1 = (cons[1]-1 if cons[1] > footIndex else cons[1])
#                order.append((cons0, cons1))
#            
#            
#            # Parameter Constraints
#            paramCons = []
#            tempParams = tree.treeParamConstraints()
#            for cons in tempParams:
#                cons0 = (cons[0]-1 if cons[0] > footIndex else (cons[0] if cons[0] < footIndex else -2))
#                cons2 = (cons[2]-1 if cons[2] > footIndex else (cons[2] if cons[2] < footIndex else -2))
#                paramCons.append((cons0, cons[1], cons2, cons[3]))
#                                
#            #create the new rule for the PFFG
#            newRule = Rule.Y_Rule(foot, tree._root, s, order, paramCons, tree.getProbability())
#            PFFG.append(newRule)
#            
#        return PFFG