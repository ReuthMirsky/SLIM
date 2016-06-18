'''
Created on Mar 7, 2013

@author: Reuth
'''
import sys
import time
from Queue import Queue
from Sigma import Sigma
from Tree import Tree
#from copy import deepcopy 
from Explanation import Explanation

def CompleteExistingTrees(currentExp, fragment, allFragments, obs, expsTemp, numOfExps):
    treeIndexInExp = 0
    for tree in currentExp.getTrees():
        treeFrontier = tree.getFrontier(withIndices=True)
        #Try to add the current fragment as a child of an existing tree
        if treeFrontier!=[]:
            for (node, index) in treeFrontier: 
                # Try to complete the frontier if it is a terminal letter, same as currentObs
                if tree.sameParameters(fragment.getRoot(), index):
                    newCopy = tree.myCopy()
                    if newCopy.substituteNode(fragment.myCopy(), index):
                        newCopy.getNodeByFrontierIndex(index)._isComplete=True
                        Tree.openFrontiers-=1
                        newExp = currentExp.myCopy()
                        newExp.setTree(newCopy, treeIndexInExp)
                        #newExp.updateLocalProbChoices(newCopy)
                        newExp.resetAge()
                        expsTemp.append(newExp)
                        numOfExps += 1
        #Try to add the current fragment as a brother of an existing tree
        else:
            for (higherFragment, index) in allFragments[tree.getRoot().get()]:
                newHigherFragment = higherFragment.myCopy()
                resultOfSubstituteNode = newHigherFragment.substituteNode(tree.myCopy(),index)
                if not resultOfSubstituteNode:
                    continue
                #print "higherFragment=", higherFragment.reprWithParams()
                #print "index=", index
                newHigherFragment.getNodeByFrontierIndex(index)._isComplete=True
                treeFrontier = newHigherFragment.getFrontier(withIndices=True)
                #print "Tree frontier="
                #print treeFrontier
                if treeFrontier!=[]:
                    for (node, index2) in treeFrontier: 
                        #print "node is ", node.reprWithParams()
                        #print "index is", index2
                        # Try to complete the frontier if it is a terminal letter, same as currentObs
                        if newHigherFragment.sameParameters(fragment.getRoot(), index2):
                            newCopy = newHigherFragment.myCopy()
                            if newCopy.substituteNode(fragment.myCopy(), index2):
                                newCopy.getNodeByFrontierIndex(index2)._isComplete=True
                                Tree.openFrontiers-=1
                                newExp = currentExp.myCopy()
                                newExp.setTree(newCopy, treeIndexInExp)
                                #newExp.updateLocalProbChoices(newCopy)
                                newExp.resetAge()
                                #print "here2"
                                expsTemp.append(newExp)
                                numOfExps += 1
                    
                                    
        treeIndexInExp += 1    

def CreateNewFragmentInExp(currentExp, fragment, expsTemp, numOfExps):
    newExp = currentExp.myCopy()
    newExp.setTree(fragment.myCopy())
    #newExp.updateLocalProbChoices(fragment)
    newExp.resetAge()
    expsTemp.append(newExp)
    numOfExps += 1

#PL is the plan library for this run, observations is a set of sigmas that needs to be explained
def ExplainAndCompute(PL, observations, filterParams=[]):
    exps = [Explanation()]
    allFragments = {}

    TreeAvgBound = 2.0
    ProbabilityAvg = 1.0
    AgeAvg = 1.0
    FrontierAvg = 1.0

        
#     print "PL=", PL
    
    for nt in PL._NT:
        allFragments[nt.get()] = PL.createFragments(nt)
        
    for sigma in PL._Sigma:
        allFragments[sigma.get()] = PL.createFragments(sigma)
        
#     for letter in allFragments.keys():
#         print "Fragments for", letter
#         print allFragments[letter]
#         print "****************"
    
    #Loop over all observations
    myfile1 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\exps.csv', 'a+')
    myfile2 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\time.csv', 'a+')
    myfile3 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\branches.csv', 'a+')
    myfile4 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\frontiers.csv', 'a+')
    myfile1.write(sys.argv[2]+",")        
    myfile2.write(sys.argv[2]+",")
    myfile3.write(sys.argv[2]+",")
    myfile4.write(sys.argv[2]+",")
    timeBegin = time.clock()
    obsNum = 1
    
    for obs in observations:  
        Frontiers=0 
#         print "handling obs numer",obsNum  
#         print "avg. trees in exp=",TreeAvgBound
        expsTemp = []
#         treesTotal = 0
#         probabilityTotal = 0.0
#         ageTotal = 0
#         frontierTotal = 0
        numOfExps = 0.0
#         oldExpNum = 0
        #if len(exps) == 0:
        #    print "No Exps"
        #else:
        #    print "num of exps=",len(exps)
  
#         rangeList = chooseRandomAmount(range(0, exps.qsize()))
#         #print rangeList

        #Loop over all the explanations in the queue
        while not len(exps)==0:
#            oldExpNum+=1
            #print "Old exp num=", oldExpNum
            currentExp = exps.pop() 
            Frontiers+=currentExp.getFrontierSize()
            #print "current Exp", currentExp

            for (fragment, index) in allFragments[obs.get()]:
                #print "Fragment=", fragment.reprWithParams()
                #print "Index=", index
                newFragment = fragment.myCopy()
                newFragment.substitute(obs, index)
                #print "New Fragment=", newFragment.reprWithParams()
                CompleteExistingTrees(currentExp, newFragment, allFragments, obs, expsTemp, numOfExps)
                CreateNewFragmentInExp(currentExp, newFragment, expsTemp, numOfExps)
                
        exps=expsTemp
        currentTime = time.clock()
        myfile1.write(str(len(exps))+",")        
        myfile2.write(str(currentTime)+",")
        myfile3.write(str(Tree.treeNum)+",")
        myfile4.write(str(Frontiers)+",")
        print "num of fragments=", len(exps)
        obsNum+=1
    
    newExps=[]
#     for exp in exps:
#         if exp not in newExps:
#             newExps.append(ex    p)

    Frontiers=0
    exps.sort(key=Explanation.getExpProbability)            
    for i in range(101):
        newExps += CalculateTopDownExps([exps.pop()], PL)
        for exp in newExps:
            Frontiers+=exp.getFrontierSize()
        if i in [1,10,20,30,40,50,60,70,80,90,100]:
            currentTime = time.clock()
            myfile1.write(str(len(newExps))+",")        
            myfile2.write(str(currentTime)+",")
            myfile3.write(str(Tree.treeNum)+",")
            myfile4.write(str(Frontiers)+",")
            print "num of exps=", len(newExps)
    
    myfile1.write("\n")
    myfile2.write("\n")
    myfile3.write("\n")
    myfile4.write("\n")
    myfile1.close()
    myfile2.close()
    myfile3.close()
    myfile4.close()
    return exps


def CalculateTopDownExps(fragmentedExps, PL): 
    
    res = []
    currentTime = time.clock()
    print currentTime
    #Create all possible paths to Goals 
    goalsGeneratingSet = PL.generatingSet(PL._R)
    currentTime = time.clock()
    print currentTime
    
    while not len(fragmentedExps)==0:
        fragmentedExp = fragmentedExps.pop()

        #print "*********** New Fragment Explanation ****************"
        #print fragmentedExp

        #Now we activate an almost-classic PHATT, except that instead of observations, we use fragments
        topDownExps = [Explanation()]
        for fragmentObs in fragmentedExp.getTrees():
            expsTemp = []
            numOfExps = 0.0
            
            while not len(topDownExps)==0:
                currentExp = topDownExps.pop()
                #print "---------- Current Exp ------------"
                #print currentExp
                
                treeIndexInExp = 0
                
                for tree in currentExp.getTrees():                  
                    treeFrontier = tree.getFrontier(withIndices=True)
                    for (node, index) in treeFrontier: 
#                         # 1. Try to complete the frontier if it is the same letter as fragmentObs's root
#                         if tree.sameParameters(fragmentObs.getRoot(), index):
#                             newCopy = deepcopy(tree)
#                             if newCopy.substituteNode(fragmentObs, index):
#                                 newExp = deepcopy(currentExp)
#                                 newExp.setTree(newCopy, treeIndexInExp)
#                                 newExp.updateLocalProbChoices(newCopy)
#                                 newExp.resetAge()
#                                 expsTemp.append(newExp)
#                                 if newExp.getFrontierSize()==0:
#                                     print "1"
#                                     print tree.reprWithParams()
#                                     print treeFrontier
#                                     print fragmentObs.reprWithParams()
#                                 numOfExps += 1
#                                 #treesTotal += len(newExp.getTrees())
#                                 #probabilityTotal += newExp.getExpProbability()
#                                 #ageTotal += newExp.getAge()
#                                 #frontierTotal += newExp.getFrontierSize()
#                             else:
#                                 del(newCopy)
        
                        # 2. Try to complete the frontier by expanding the tree from this point
                        
                        # 2.1. First, create all trees that start in the frontier item and ends with fragmentObs
                        genSetForObs = PL.generatingSetForFragment(fragmentObs)
                         
                        # 2.2. Then, try to see if the new sub-tree can be inserted instead of the frontier item
                        for newExpandedTree in genSetForObs:
                            if tree.sameParameters(newExpandedTree.getRoot(), index):
                                newCopy = tree.myCopy()
                                newCopy.setNodeByFrontierIndex(index, newExpandedTree)
                                if newCopy.substitute(newExpandedTree.getRoot(), index):
                                    newExp = currentExp.myCopy()
                                    newExp.setTree(newCopy, treeIndexInExp)
                                    newExp.updateLocalProbChoices(newCopy)
                                    newExp.resetAge()
                                    expsTemp.append(newExp)
                                    #if newExp.getFrontierSize()==0:
                                    #    print "2"
                                    numOfExps += 1
                                    #treesTotal += len(newExp.getTrees())
                                    #probabilityTotal += newExp.getExpProbability()
                                    #ageTotal += newExp.getAge()
                                    #frontierTotal += newExp.getFrontierSize()
                                else:
                                    del(newCopy)
                    treeIndexInExp+=1
                                    
            # 3. Consider all the new plans the observation could introduce
            
            # 3.1. First, if the plan is already built until a root
            if PL.isGoalLetter(fragmentObs.getRoot()):
                newCopy = fragmentObs
                newExp = currentExp.myCopy()
                newExp.setTree(newCopy)
                #newExp.backpatchPS(deepcopy(allGeneratingSet[possTree.getRoot().get()]))
                newExp.updateLocalProbChoices(newCopy)
                newExp.updateLocalProbRoots(PL.getRootProb())
                newExp.incrementAge()
                expsTemp.append(newExp)
                numOfExps += 1
            #if not PL.isGoalLetter(fragmentObs.getRoot()):               
            else:   #might want to remove this else in domains in which a letter can be both a root and an inner letter
                # 3.2. Second, what is needed to complete this plan to the root
                genSetForFragment = PL.generatingSetForFragment(fragmentObs)
                #print "My fragmentObs=", fragmentObs.reprWithParams()
                #print "My genSet for it="
                #for item in genSetForFragment:
                #    print item.reprWithParams()
                       
                for possTree in genSetForFragment:
                    newCopy = possTree
                    newExp = currentExp.myCopy()
                    newExp.setTree(newCopy)
                                        #newExp.backpatchPS(deepcopy(allGeneratingSet[possTree.getRoot().get()]))
                    newExp.updateLocalProbChoices(newCopy)
                    newExp.updateLocalProbRoots(PL.getRootProb())
                    newExp.incrementAge()
                    expsTemp.append(newExp)
#                             if newExp.getFrontierSize()==0:
#                                 print "3"
                    numOfExps += 1
                                        #treesTotal += len(newExp.getTrees())
                                        #probabilityTotal += newExp.getExpProbability()
                                        #ageTotal += newExp.getAge()
                                        #frontierTotal += newExp.getFrontierSize()
                                
            topDownExps=expsTemp
            #print "\n\nSIZE=",len(topDownExps)
                
        if topDownExps!=[]:
            res.extend(topDownExps)
            
    return res


#########################################################################################################################
#        ORIGINAL PHATT
#########################################################################################################################

#PL is the plan library for this run, observations is a set of sigmas that needs to be explained
def ExplainAndComputePHATT(PL, observations, filterParams=[], explanations=[]):
    global location
    myfile1 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\exps.csv', 'a+')
    myfile2 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\time.csv', 'a+')
    myfile3 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\branches.csv', 'a+')
    myfile4 = open('C:\\Users\\'+"Owner"+'\\Desktop\\test2\\frontiers.csv', 'a+')
    myfile1.write(sys.argv[2]+",")        
    myfile2.write(sys.argv[2]+",")
    myfile3.write(sys.argv[2]+",")
    myfile4.write(sys.argv[2]+",")
    timeBegin = time.clock()
    exps = explanations
    exps.append(Explanation())
    goalsGeneratingSet = PL.generatingSet(PL.getGoals())
    #print goalsGeneratingSet
    allGeneratingSet = {}
    filterInNextIteration = True
    timeBegin = time.clock()
    lastNum=0
                           
    #Set Filters
    if filterParams == []:
        filterBySizeStrict = False          #Size (int>=1) or False
        filterBySizeAverage = False           #True or False
        filterByAgeStrict = False            #Age (int>=1) or False
        filterByAgeAverage = False            #True or False
        filterByProbability = False           #True or False
        filterByFrontierSize = False          #Size (int>=1) or False
        filterByFrontierAverage = False           #True or False
        filterByRandomHalf = False
    else:
        filterBySizeStrict = filterParams[0]            #Size (int>=1) or False
        filterBySizeAverage = filterParams[1]           #True or False
        filterByAgeStrict = filterParams[2]                   #Age (int>=1) or False
        filterByAgeAverage = filterParams[3]            #True or False
        filterByProbability = filterParams[4]           #True or False
        filterByFrontierSize = filterParams[5]          #Size (int>=1) or False       
        filterByFrontierAverage = filterParams[6]       #True or False
    
    TreeAvgBound = 2.0
    ProbabilityAvg = 1.0
    AgeAvg = 1.0
    FrontierAvg = 1.0
    treesInAllGenSet = 0
    
    for nt in PL._NT:
        #print "Trees for ", nt
        allGeneratingSet[nt.get()] = PL.generatingSet([nt])
        treesInAllGenSet += len(allGeneratingSet[nt.get()])
#         for tree in allGeneratingSet[nt.get()]:
#             print tree
#    for tree in goalsGeneratingSet:
#        print ("tree in GS:")
#        print (tree)

    #Loop over all observations
    print "trees in genSet = ", treesInAllGenSet
    obsNum = 1
    for obs in observations:   
        print "handling obs number",obsNum  
#        print "avg. trees in exp=",TreeAvgBound
        expsTemp = []
        treesTotal = 0
        probabilityTotal = 0.0
        ageTotal = 0
        frontierTotal = 0
        numOfExps = 0.0
        oldExpNum = 0
        
#        if len(exps)==0:
#            print "No Exps"
#        else:
#            print "num of exps=",len(exps)

        #rangeList = chooseRandomAmount(range(0, len(exps)))
        #print rangeList
        #Loop over all the explanations in the queue
        
        #Measures for upper and lower bounds
        ProbabilityMin = 1.0
        ProbabilityMax = 0.0
        TreeAmountMin = 1000
        TreeAmountMax = 0
        AgeMin= 1000
        AgeMax = 0
        FrontierMin = 1000
        FrontierMax = 0
                
        for i in range(len(exps)):
            oldExpNum+=1
            #print "Old exp num=", oldExpNum
            currentExp = exps[i]
            #print currentExp
            
            #Filter Explanations
            currentExpProb = currentExp.getExpProbability()
            currentExpSize = currentExp.getSize()
            currentExpAge = currentExp.getAge()
            currentExpFrontier = currentExp.getFrontierSize()

            #Measures for upper and lower bounds
            if currentExpProb < ProbabilityMin:
                ProbabilityMin = currentExpProb
            if currentExpProb > ProbabilityMax:
                ProbabilityMax = currentExpProb
            if currentExpSize < TreeAmountMin:
                TreeAmountMin = currentExpSize
            if currentExpSize > TreeAmountMax:
                TreeAmountMax = currentExpSize
            if currentExpAge < AgeMin:
                AgeMin = currentExpAge
            if currentExpAge > AgeMax:
                AgeMax = currentExpAge
            if currentExpFrontier < FrontierMin:
                FrontierMin = currentExpFrontier
            if currentExpFrontier > FrontierMax:
                FrontierMax = currentExpFrontier
            
            if filterInNextIteration:
                if filterBySizeStrict and currentExpSize > filterBySizeStrict:
                    #print "Filtered by size strict"
                    continue
                if filterBySizeAverage and currentExpSize > TreeAvgBound:
                    #print "Filtered by size average"
                    continue
                if filterByAgeStrict and currentExpAge > filterByAgeStrict:
                    #print "Filtered by age strict"
                    continue
                if filterByAgeAverage and currentExpAge > AgeAvg:
                    #print "Filtered by age average"
                    continue
                if filterByProbability and currentExpProb < ProbabilityAvg:
                    #print "Filtered by probability"
                    continue
                if filterByFrontierSize and currentExpFrontier > filterByFrontierSize:
                    #print "Filtered by frontier strict"
                    continue
                if filterByFrontierAverage and currentExpFrontier > FrontierAvg:
                    #print "Filtered by frontier average"
                    #print "Frontier size=", currentExpFrontier
                    continue
                #if filterByRandomHalf and obsNum!=1 and -1==rangeList[oldExpNum-1]:
                #    continue
#             else:
#                 filterInNextIteration = True
            
           
            treeIndexInExp = 0

            #Consider all the existing plans the observation could extend
            for tree in currentExp.getTrees():
                treeFrontier = tree.getFrontier(withIndices=True)
                for (node, index) in treeFrontier:
                    #if obsNum==3 and node.getRoot().get()=="place_cones":
                        #print "1.1"
                        #print "**********************************************************************"
                        #print "node=", node.reprWithParams(), ", index=", index
                        #print "\n"
                    # Try to complete the frontier if it is a terminal letter, same as currentObs
#                   if type(node.getRoot())==Sigma and tree.sameParameters(obs, index):
#                       #if obsNum==3:
#                       #   print "1.2"
#                       newCopy = tree.myCopy()
#                       if newCopy.substitute(obs, index):
#                           newCopy.getDecendant(index)._isComplete = True
#                           newCopy.setID()
#                           newExp = currentExp.myCopy()
#                           newExp.setTree(newCopy, treeIndexInExp)
#                           newExp.updateLocalProbChoices(newCopy)
#                           newExp.resetAge()
#                           expsTemp.append(newExp)
#                           numOfExps += 1
#                           treesTotal += len(newExp.getTrees())
#                           probabilityTotal += newExp.getExpProbability()
#                           ageTotal += newExp.getAge()
#                           frontierTotal += newExp.getFrontierSize()
#                       else:
#                           del(newCopy)

                    #Try to complete the frontier by expanding the tree from this point
                    #First, create all trees that start in the frontier item and ends with obs
                    if type(node.getRoot()) == Sigma:
                        genSetForObs = []
                    else:
                        genSetTrees = []
                        for subtree in allGeneratingSet[node.getRoot().get()]:
                            genSetTrees.append(subtree.myCopy())
                        genSetForObs = PL.generatingSetForObs(genSetTrees, obs)
#                     print genSetForObs
#                     print "*******", len(genSetForObs), "**********"
                    #Then, try to see if the new sub-tree can be inserted instead of the frontier item
                    for newExpandedTree in genSetForObs:
                        #if obsNum==3:
                            #print "2.1"
                        if tree.sameParameters(newExpandedTree.getRoot(), index):
                            #if obsNum==3:
                                #print "2.2"
                            newCopy = tree.myCopy()
                            newCopy.setNodeByFrontierIndex(index, newExpandedTree)
                            if newCopy.substitute(newExpandedTree.getRoot(), index):
                                newCopy.setID()
                                newExp = currentExp.myCopy()
                                Tree.openFrontiers-=1
                                newExp.setTree(newCopy, treeIndexInExp)
                                newExp.updateLocalProbChoices(newCopy)
                                newExp.resetAge()
                                expsTemp.append(newExp)
                                #print "2"
                                #print newExpandedTree
                                numOfExps += 1
                                treesTotal += len(newExp.getTrees())
                                probabilityTotal += newExp.getExpProbability()
                                ageTotal += newExp.getAge()
                                frontierTotal += newExp.getFrontierSize()
                            else:
                                print "Threw tree:", newCopy.reprWithParams()
                                print "index=", index
                                del(newCopy)
#                       else:
#                           print("tree=",tree.getNodeByFrontierIndex(index).getRoot())
#                           print("node=",newExpandedTree.getRoot())
                treeIndexInExp+=1
                            
            #Consider all the new plans the observation could introduce
            for possTree in goalsGeneratingSet:
                treeFrontier = possTree.getFrontier(withIndices=True)
                for (node, index) in treeFrontier:
                    #if obsNum==3:
                    #   print "3.1"  
                    if possTree.sameParameters(obs, index):
                        #if obsNum==3:
                        #   print "3.2"
                        newCopy = possTree.myCopy()
                        newCopy.setID()
                        if newCopy.substitute(obs, index):
                                newExp = currentExp.myCopy()
                                newExp.setTree(newCopy)
                                Tree.openFrontiers-=1
                                newExp.backpatchPS(allGeneratingSet[possTree.getRoot().get()])
                                newExp.updateLocalProbChoices(newCopy)
                                newExp.updateLocalProbRoots(PL.getRootProb())
                                newExp.incrementAge()
                                expsTemp.append(newExp)
                                numOfExps += 1
                                treesTotal += len(newExp.getTrees())
                                probabilityTotal += newExp.getExpProbability()
                                ageTotal += newExp.getAge()
                                frontierTotal += newExp.getFrontierSize()
#                                 if newCopy.getID()==2888 or newCopy.getID()==2887:
#                                     print "here, ", newCopy.getID(), possTree.getID(), node, index
                        else:
                            del(newCopy)
                        
        if expsTemp == []:
            filterInNextIteration = False
            print "Cannot Combine Observation Number", obsNum, ": ", obs 
        else:
            del[exps]
            exps=expsTemp
            
        #writeExplanations(deepcopy(exps), obsNum)
#         TreeAvgBound = treesTotal / numOfExps if 0!=numOfExps else 1000
#         ProbabilityAvg = probabilityTotal / numOfExps if 0!=numOfExps else 1.0
#         AgeAvg = ageTotal / numOfExps if 0!=numOfExps else 1.0
#         FrontierAvg = frontierTotal / numOfExps if 0!=numOfExps else 1.0
        currentTime = time.clock()
        myfile1.write(str(len(exps))+",")        
        myfile2.write(str(currentTime)+",")
        myfile3.write(str(Tree.treeNum)+",")
        myfile4.write(str(frontierTotal)+",")

        #Print Measurements:
        #print ProbabilityMin, ",", ProbabilityMax, ",", TreeAmountMin, ",", TreeAmountMax, ",", AgeMin, ",", AgeMax, ",", FrontierMin, ",", FrontierMax, numOfExps
        #print "time elapsed=", timeCurrent
#
    myfile1.write("\n")        
    myfile2.write("\n")
    myfile3.write("\n")
    myfile4.write("\n")
    myfile1.close()
    myfile2.close()    
    myfile3.close()
    myfile4.close()
    return exps