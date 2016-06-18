from copy import deepcopy

class Letter(object):
    letterNum=0
    
    def __init__(self, ch='', params=[]):
            Letter.letterNum+=1
         
            self._ch=ch                 # Type string
            
            self._params=[]         # Type list of tuples <paramName, paramVal> with initial value None 
            for param in params:
                if type(param)==tuple:
                    self._params.append(param)
                else:
                    self._params.append((param, None))

#     def __copy__(self):
#         newone = type(self)()
#         newone._ch=self._ch
#         newone._params=self._params
#         Letter.letterNum+=1
#         return newone

    def myCopy(self):
        newParams = []
        for param in self._params:
            newParams.append((param[0],param[1]))
        newone = type(self)()
        newone._ch=self._ch
        newone._params=newParams
        newone._type=self._type
        return newone
    
    def __del__(self):
        Letter.letterNum-=1    
        
    def get(self):
        return self._ch
    
    def __repr__(self):
        res = self.get()
        if self._params==[]:
            res += '[]'
        else:
            res += '['
            for param in self._params:
                #val = param[1] if (param[1]!=None) else 'None'
                if param[0] != 'scd' and  param[0] !='dcd' and  param[0] !='rcd':
                    res += str(param[0]) + '=' + str(param[1]) + ","
            res = res[:-1]
            res += ']'
        return res
    
    def __eq__(self, other):
        if type(other)!=type(self):
            return False
        
        if other.matchFullLetter(self):
            return True
                
        return False
    
    def getParam(self, name): 
        if name==None or self._params==[]:
            return None
        for pair in self._params:
            if pair[0]==name:
                return pair[1]
       
    def setParam(self, name, val): 
        if name==None or self._params==[]:
            return None
        for paramIndex in range(len(self._params)):
            param = self._params[paramIndex]
            if param[0] == name:
                self._params[paramIndex] = (name,val)
        return None
    
    def getParamName(self, index):
        return self._params[index][0];
    
    def getParamVal(self, index):
        return self._params[index][1];
    
    def getParamList(self):
        return self._params
    
    def hasParam(self, other_name):
        for param in self._params:
            if param[0]==other_name:
                return True
        return False

    def matchLetter(self, letter):
        if letter.get()==self.get() and self.matchTerminalLetterParams(letter):
            return True
        return False
    
    def matchFullLetter(self, letter):
        if letter.get()==self.get() and self.matchFullyLetterParams(letter):
                return True
        return False
        
#     def matchPartialLetter(self, letter):
#         if letter.get()==self.get() and self.matchLetterParams(letter):
#                 return True
#         return False
    
    def matchTerminalLetterParams(self, obs):
        for (name, val) in self._params:
            if val!=None:
                if obs.getParam(name)!=val and obs.getParam(name)!=None:
                    #print "name1", name
                    return False
        return True    
    
#     def matchLetterParams(self, obs):
#         for (name, val) in self._params:
#             if val!=None:
#                 if obs.getParam(name)!=val:
#                     #print "name2", name
#                     return False
#         return True 
    
    def matchFullyLetterParams(self, obs):
        for (name, val) in self._params:
            if obs.getParam(name)!=val:
                #print "name2", name
                return False
        return True   
    
class Sigma(Letter):
    _type='Sigma'

