from NT import NT
from Sigma import Sigma

class Rule(object):
    '''
    classdocs
    '''
    ruleAmount=0

    def __init__(self, A, alpha=[], order=[], paramConst=[], prob=0.1, pid=False):
        '''
        Constructor
        '''
        self._A=A           #this item is either of type Sigma or NT
        self._alpha=alpha   #this is a list of NTs and Sigmas
        self._order=order   #each item in this list is (i,j) which means the ith child must come before the jth chikd
                                #both i and j are of type int
        self._paramConst=paramConst   #each item in this list is (i,iname,j,jname) which means that the parameter iname of the ith child
                                        #Alternatively, (i, iname, val) means that the iname of the ith child should have the value val
                                        #must be equal to the parameter jname of the jth child (i or j equals -1 means that its the root)
        self._probability = prob

        if pid:
            self._pid = pid
        else:    
            Rule.ruleAmount+=1
            self._pid=Rule.ruleAmount
                                                            
    def myCopy(self):
        newAlpha = []
        for letter in self._alpha:
            newAlpha.append(letter.myCopy())
        newone = type(self)(self._A.myCopy(), newAlpha, self._order, self._paramConst, self._probability, self._pid)
        return newone
                                    
    def __repr__(self):
        res = self._A.get() + " -> "
        for child in self._alpha:
            res += child.get() + " "       
        res += "| [ "
        for cons in self._order:
            res += self.constraintWithLetters(cons)
        res += "]\n"
        res += "\t" + self.parameterConstraints()      
        return res
    
    def getPriorProbability(self):
        return self._probability
    
    def constraintWithLetters(self, cons):
        left = self._alpha[cons[0]].get()
        right = self._alpha[cons[1]].get()
        return "(" + left + "," + right + ") "
        
    def parameterConstraints(self):
        if self._paramConst==None:
            return "[]"
        res="[ "
        for cons in self._paramConst:
            if len(cons)==4:
                if cons[0]==-1:
                    res+= self._A.get() + "." + cons[1] + "=" +  self._alpha[cons[2]].get() + "." + (cons[3]) + " "
                elif cons[2]==-1:
                    res+= self._alpha[cons[0]].get() + "." + cons[1] + "=" +  self._A.get() + "." + (cons[3]) + " "
                else:
                    res+= self._alpha[cons[0]].get() + "." + cons[1] + "=" +  self._alpha[cons[2]].get() + "." + (cons[3]) + " "
            else:
                if cons[0]==-1:
                    res+= self._A.get() + "." + cons[1] + "=" + cons[2] + " "
                else:
                    res+= self._alpha[cons[0]].get() + "." + cons[1] + "=" + cons[2] + " "
        res+= "]"
        return res

    def getParamCons(self):
        return self._paramConst
        
    # Return all leftmost childs of the rule    
    def leftMostChilds(self, byIndex=False):
        res = []
        i=0
        
        if self._alpha == None:
            return []
        
        for ch in self._alpha:            
            if not self.hasConstraint(i):
                if byIndex:
                    res.append(i)
                else:
                    res.append(ch)
            i+=1
                
        return res;
    # If letter is a lefmost child of this rule's alpha, returns its possible indices in alpha. Otherwise, return false
    def isALeftmostChild(self, letter, withParams=False):
        if type(self._alpha) != type([]):
            return False
        
        if type(letter)!=NT and type(letter)!=Sigma:
            return False
        
        res = []
        for (constituent, i) in self.leftMostChildsWithNums():
            if withParams:
                if letter.matchLetter(constituent):
                    res.append(i)
            else:
                if letter._ch==constituent._ch:
                    res.append(i)
            i+=1
            
        return res
    
    # Return tuples of leftmost childs with their index
    def leftMostChildsWithNums(self):
        res = []
        i=0
        
        if self._alpha == None:
            return []

        for ch in self._alpha:            
            if not self.hasConstraint(i):
                res.append((ch,i))
            i+=1
                
        return res;
    
    # Return all right childs of the rule
    def rightChilds(self, byIndex=False):
        right = self._alpha[:] if not byIndex else list(range(len(self._alpha)))
        for ch in self.leftMostChilds(byIndex):
            right.remove(ch)
        return right
    
    # service function for leftmostChilds
    def hasConstraint(self, index):
        for cons in self._order:
            if cons[1] == index:
                return True;
        return False;
    
    #return a list of all order constraints limiting this child
    def allChildConstraints(self, index):
        res = []
        for cons in self._order:
            if cons[1] == index:
                res.append(cons[0])
        return res
           
    #return the first index of child in alpha (children's list), or throws an error if there is no such child
    def getChildIndex(self, child):
        return self._alpha.index(child)
    
#     def __eq__(self, other):
#         if other == ():
#             return False
#         if self._A != other._A:
#             return False
#         if self._alpha != other._alpha:
#             return False
#         if self._order != other._order: 
#             return False
#         if self._paramConst != other._paramConst:
#             return False
#         
#         return True
        
        