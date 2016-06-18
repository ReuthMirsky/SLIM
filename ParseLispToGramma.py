'''
Created on 21  2014

@author: Owner
'''
import sys
import time
from Rule import Rule
from Sigma import Sigma
from NT import NT
from PL import PL
from Algorithm import ExplainAndCompute, ExplainAndComputePHATT
from Explanation import Explanation
import random


location = "Owner"

currentLetter = 0
Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Letters2 = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
currentNumber = 1#{letter: 1 for letter in Letters2.split(" ")}
AllNTs = []     #List of strings
AllRules = ""
AllRulesAsList = []

def runAlgorithm(stringObs):
    global AllRulesAsList
    Sigmas = []
    NTs = []
    Goals = []
    Observations = []
    for i in range(100):
        Sigmas.append(Sigma("A"+str(i+1)))
    
    for nt in AllNTs:
        if nt[0]=="*":
            Goals.append(NT(nt[1:]))
            NTs.append(NT(nt[1:]))
        else:
            NTs.append(NT(nt))
    
    #For 1 goal
    realGoal = Goals[int(stringObs[0][1:-1])]
    #For 2 goals
    #realGoals = [Goals[int(stringObs[0][1:])], Goals[int(stringObs[1][:-1])]]
    print "real goal=", realGoal
    for obs in stringObs[1:]:
        if len(obs)>1:
            if obs[len(obs)-1]=='\n':
                obs = obs[:-1]
            Observations.append(Sigma(obs))
            print "obs=", obs
#         if not realObs:# and obs[len(obs)-1]==")":
#             realObs=True
            
    newPL = PL(Sigmas, NTs, Goals, AllRulesAsList)
    #print "here1"
    exps = ExplainAndComputePHATT(newPL, Observations)
   
    if len(exps)==0:
        print "No Explnanations"    
    print "\n\n"    
    explanations = 0   
    noFrontier = []
    goalsPusrued = {}
    
    exps.sort(key=Explanation.getExpProbability)
    firstflag = True
    totalExps = len(exps)
    print "Total exps=", totalExps
#     print exps

    
    ######## Code to create goldStandard #####################
#     filee = open("C:\\Users\\Owner\\Desktop\\goldStandard-2-3-3-2-2-full-20\\"+sys.argv[2]+".xml", 'a+')
#     print "Total exps=", totalExps
#     dictionaryToPickFrom = {}
#     singleExps=[]
#     i=0
#     for exp in exps:
#         if exp.getSize()==2 and exp.getFrontierSize()==0:
#             #print "here"
#             singleExps.append(exp)
#             dictionaryToPickFrom[i]=exp.getExpProbability()
#             i+=1 
#     
#     print "remaining exps:", len(singleExps)
#     print dictionaryToPickFrom
#     chosenExp=singleExps[WeightedPick(dictionaryToPickFrom)]
#     print chosenExp  
#     filee.write("<?xml version=\"1.0\"?>\n")
#     filee.write("<Explanation>\n")
#     for tree in chosenExp.getTrees():
#         filee.write(tree.asXML())
#     filee.write("</Explanation>\n")
#     filee.close()
#     return
#                  

    ######## Code to probe #####################
    for exp in exps:
     while not len(exps)==0:
         exp = exps.pop()
   
         if firstflag:
             print "-------------\n First Exp\n-----------------"
             firstflag = False
           
         if exp.getFrontierSize()==0:
             print "-------------\n Exp with Empty Frontier\n-----------------"
              
         print exp
         for tree in exp.getTrees():
             root = tree.getRoot().get()
             if goalsPusrued.has_key(root):
                 goalsPusrued[root] += exp.getExpProbability()
             else:
                 goalsPusrued[root] = exp.getExpProbability()
                  



    ######## Code to print resulted exps  #####################  
#      print goalsPusrued
#      sumOfProb = sum(goalsPusrued.values())
#      goalsNormPursued = {key : val/sumOfProb for key ,val in goalsPusrued.items()}
#          
#      print goalsNormPursued
#      print "Total exps=", totalExps
     
#      myfile3 = open('C:\\Users\\'+location+'\\Desktop\\test2\\goals.csv', 'a+')
#      goalSum=0
#      goals = ['B28', 'B56', 'B84', 'B112', 'B140']
#      goals.reverse()
#      best = goalsNormPursued.keys()[0]
#     for item in goals:
#         if item in goalsNormPursued.keys() and goalsNormPursued[item]>goalsNormPursued[best]:
#             best = item
#             
#     for item in goals:
#         if item in goalsNormPursued.keys() and item == best:
#             myfile3.write("1\n")
#             goalSum+=goalsNormPursued[item]
#         else:
#             myfile3.write("0\n")
#     myfile3.write("\n\n\n\n")
#     myfile3.close()

def WeightedPick(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    for k, w in d.iteritems():
        s += w
        if r < s: return k
    return k

def printDomainFile(path='C:\\Users\\Owner\\Dropbox (BGU)\\Reuth\\Online Plan Recognition\\Doplar\\Results2016\\domain'+str(sys.argv[2])+'.txt'):
    global AllNTs
    global AllRules
    file = open(path, "w+")
    file.write("Sigmas\n")
    for i in range(100):
        file.write("A"+str(i+1)+" []\n")
    
    file.write("\n")
    file.write("NTs\n")
    for nt in AllNTs:
        file.write(nt+" []\n")
    
    file.write("\nRules\n")
    file.write(AllRules)
    
    file.close()
    
def printObservations(observations):
    file = open("C:\\Users\\Owner\\Dropbox (BGU)\\Reuth\\Online Plan Recognition\\Doplar\\sampleObs.txt", "w+")
    for obs in observations:
        file.write(obs)
        file.write("[]\n")
    
    file.close()
    
def addRule(ruleToPrint):
    global AllRules
    global AllRulesAsList
    
    toPrint = "\n"
    toPrint += str(ruleToPrint._A) #ruleToPrint._A.get()[1:]
    toPrint += " -> "
    for child in ruleToPrint._alpha:
        if child.get()[0]=="A":
            toPrint += (str(child)+" ") # str(int(child.get()[1:])+99) + " "
        elif child.get()[0]=="B":
            toPrint += (str(child)+" ") #child.get()[1:] + " "
    toPrint += str(ruleToPrint._order)
    toPrint += "\n[]\n\n"
    AllRules += toPrint
    AllRulesAsList.append(ruleToPrint)

def generateNextLetter(definedLetter=False):
    global currentLetter
    global Letters
    global currentNumber
    
    if not definedLetter:
        letterToReturn = Letters2.split(" ")[currentLetter]
    else:
        letterToReturn = definedLetter
        
    numberToReturn = currentNumber
    currentNumber += 1
    

#     if not definedLetter:
#         letterToReturn = Letters2.split(" ")[currentLetter]
#         if currentNumber < 100:
#             numberToReturn = currentNumber[letterToReturn]
#             currentNumber[letterToReturn] += 1
#         else:
#             currentLetter += 1
#     else:
#         letterToReturn = definedLetter
#         
#     numberToReturn = currentNumber[letterToReturn]
#     currentNumber[letterToReturn] += 1
    
    return letterToReturn+str(numberToReturn)

def getDelimiters(line):
    indices = []
    openBrackets = 0
    changed = False
    
    for i in range(len(line)):
        if line[i]=="(":
            openBrackets += 1
            changed = True
        elif line[i]==")":
            openBrackets -= 1
        
        if openBrackets==0 and changed:
            indices.append(i)
            changed = False
            
    return indices 

def parseWholeFile(currentLine):
    global currentLetter
    global Letters2
    global currentNumber
    global AllNTs
    
    currentLine = currentLine[1:-1]
    delimiters = getDelimiters(currentLine)
    del1 = delimiters[0]-2
    del2 = delimiters[1]+1
    i=1
    while True:
        currentLetter = 1
        currentNumber = 1#{letter: 1 for letter in Letters2.split(" ")}
        singleProblem = currentLine[del1+2:del2]
#        print singleProblem
        
        probDels = getDelimiters(singleProblem)[0]
        recipeLibrary = singleProblem[:probDels]
        observations = singleProblem[probDels+4:-1]
        
        if i==int(sys.argv[2]):
            parseRecipeLibrary(recipeLibrary)
#             if 7==int(sys.argv[2]):
#                 printDomainFile('C:\\Users\\Owner\\Desktop\\Domain7.txt')
            #Home
            #log = str('C:\Users\Owner\Dropbox (BGU)\Reuth\Online Plan Recognition\Domains\VirtualLabs-Recipe+Logs\Logs\\'+sys.argv[1]+".log")
            #sys.stdout = open('C:\Users\Owner\Dropbox (BGU)\Reuth\Online Plan Recognition\Probing\Doplar\One Goal\MPE-Cut6\\'+str(sys.argv[2])+'.txt', 'w+')
            sys.stdout = open('C:\\Users\\Owner\\Desktop\\test2\\'+str(sys.argv[2])+'.txt', 'w+')
            #Office
            #log = str('C:\Users\dekelr\Dropbox (BGU)\Reuth\Online Plan Recognition\Domains\VirtualLabs-Recipe+Logs\Logs\\'+sys.argv[1]+".log")
            #sys.stdout = open('C:\Users\dekelr\Dropbox (BGU)\Reuth\Online Plan Recognition\Doplar\Results2016\\'+str(sys.argv[2])+'.txt', 'w+')
            #sys.stdout = open('C:\\Users\\dekelr\\Desktop\\test\\'+str(sys.argv[2])+'.txt', 'w+')
        
            #printObservations(observations.split(" "))
            start = time.clock()
            runAlgorithm(observations.split(" "))
            elapsed = (time.clock() - start)
            print elapsed
            AllNTs = []
            AllRules = []
              
#         if i==2:
#             break  
        i+=1
        del1=del2+1
        if i==len(delimiters)+1:
            break
        elif i==len(delimiters):
            del2=len(delimiters)-1
        else:        
            del2=delimiters[i]+1
        if i==len(delimiters):
            break

def parseOrder(order):
    pairs = "["+order.replace(".", ",")+"]"
    pairs = pairs.replace(") (", "),(")
    order = eval(pairs)
    return order

def parseOrRecipe(line):
    global AllNTs
    line = line[3:-1].strip()
    newRules = []
    newNT = generateNextLetter()
    AllNTs.append(newNT)
    
    if line[1:-1].count("(")==0:
        sigmas = line.split()
        for sigma in sigmas:
            newRules.append(Rule(NT(newNT), [Sigma(sigma)]))
       
    else: 
        rules = []   
        delims = getDelimiters(line)
        i=1
        del1 = 0
        del2 = delims[0]+2 if len(delims) >=2 else len(line)
        while True:
            i+=1
            if len(line[del1:del2])<2:
                if i==len(delims)+1:
                    break
            resultOfAnd = parseAndRecipe(line[del1:del2])
            alpha = NT(resultOfAnd[0])
            newRules.append(Rule(NT(newNT), [alpha]))
            
            del1=del2
            if i==len(delims)+1:
                break
            if i==len(delims):
                del2=len(line)
            else:        
                del2=delims[i]+2
                
    for rule in newRules:
        addRule(rule)
                    
    return (newNT, newRules) 
            
def parseAndRecipe(recipe):
    global AllNTs
    recipe = recipe.strip()[1:-1]
    recipeDelimiters = getDelimiters(recipe)
#     print recipeDelimiters

#     for x in range(len(recipeDelimiters)):
#         print recipe[recipeDelimiters[x]]
    alphaLetters = []
    fullOrder=False
    i=0
    del1 = 0
    del2 = recipeDelimiters[0]+2 if len(recipeDelimiters) >= 2 else len(recipe)
    while True:
        i+=1
        currentPiece = recipe[del1:del2].strip()
        #print "current:", currentPiece
        if currentPiece=="":
            del1=del2
            if i<len(recipeDelimiters):
                del2=recipeDelimiters[i]
            else:
                break
            continue
        elif currentPiece[1]=="(":
            order = parseOrder(currentPiece[1:-1])
        elif currentPiece[0]=="N":
            order = []
            resultOfOr = parseOrRecipe(currentPiece[4:])
            alphaLetters.append(NT(resultOfOr[0]))
            #print "here:", currentPiece[:2]
        elif currentPiece[0]=="O" or currentPiece[1]=="O": #OR
                        #(Place in sentence, (NT, rules)) 
            resultOfOr = parseOrRecipe(currentPiece)
            alphaLetters.append(NT(resultOfOr[0]))
        elif currentPiece[0]=="F":
            fullOrder=True
            resultOfOr = parseOrRecipe(currentPiece[8:].strip())
            alphaLetters.append(NT(resultOfOr[0]))
                      
        del1=del2
        if i==len(recipeDelimiters)+1:
            break
        elif i==len(recipeDelimiters):
            del2=len(recipe)
        else:        
            del2=recipeDelimiters[i]+2
        if fullOrder:
            order = []
            for num in range(len(alphaLetters)-1):
                order.append((num,num+1))        
    letter = generateNextLetter()
    AllNTs.append(letter)
    newRule = Rule(NT(letter), alphaLetters, order)
    addRule(newRule)
    return (letter, newRule)
    
def parseRecipeLibrary(currentLine):
    currentLine = currentLine[1:].strip()
     
    delimiters = getDelimiters(currentLine[:-1])
    i=0
    recipes = []
    recipes.append(currentLine[:delimiters[0]+1])
    while i<len(delimiters)-1:
        recipes.append(currentLine[delimiters[i]+4:delimiters[i+1]+1])
        i+=1
    
    recipes.append(currentLine[delimiters[i]+4:])
#     print "r1:", recipe1
#     print "r2:", recipe2
#     print "r3:", recipe3
#     print "r4:", recipe4
#     print "r5:", recipe5
    
    for i in range(len(recipes)):
        result = parseAndRecipe(recipes[i])
        AllNTs.remove(result[0])
        AllNTs.append("*"+str(result[0])) 
#         addRule(result[1]) 
#     
#     addRule(parseAndRecipe(recipe2)[1])
#     addRule(parseAndRecipe(recipe3)[1])
#     addRule(parseAndRecipe(recipe4)[1])
#     addRule(parseAndRecipe(recipe5)[1])
#
     
#    printDomainFile()
    
    #print parseAndRecipe(recipe2)
    #print parseAndRecipe(recipe3)
    #print parseAndRecipe(recipe4)
    #print parseAndRecipe(recipe5)
#      
#     #End case - reached a line with no ()
#     if currentLine.count('(')==0:
#         if currentLine[0] == 'N':
#             i = 3
#         elif currentLine[0] == 'O':
#             rulesToMake = currentLine.split(" ")[1:]
#             print rulesToMake
#         else:
#             i = 3
#     else:
#         
#      

#import profile

# def main():
#     profile.run('myMain()')

def main():
    grammarPath = str(sys.argv[1])
    grammarFile = open(grammarPath)
    grammarAsLine = grammarFile.read()
    
    parseWholeFile(grammarAsLine)
    
if __name__ == '__main__': main()    