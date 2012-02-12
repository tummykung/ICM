#
# Authors: Joel, Tum
# Date: 2/11/2012
# Harvey Mudd College
# ICM Problem C
#

numNodes = 83
numTopics = 15
DEBUG = 0
DEBUG2 = 1

knownConsp = ['Jean','Alex','Elsie(7)','Paul','Ulf','Yao','Harvey']
knownNotConsp = ['Darlene','Tran','Ellin','Gard','Paige','Este','Chris']

def findLast(L1,L2):
    '''Returns the index of the last element of L1 in L2
        Assumes L1 is a subset of L2'''
    indexMax = 0
    for i in L1:
        if L2.index(i) > indexMax:
            indexMax = L2.index(i)
    return indexMax

def findFirst(L1,L2):
    '''Returns the index of the firs element of L1 in L2
        Assumes L1 is a subset of L2'''
    indexMin = len(L2)
    for i in L1:
        if L2.index(i) < indexMin:
            indexMin = L2.index(i)
    return indexMin


class Names:
    def __init__(self, nameFile):
        f = open(nameFile, "r")
        self.people = []
        for line in f.readlines():
            Line = line.split()
            self.people.append(Line[1])

    def getNum(self, name):
        return self.people.index(name)

    def getName(self, num):
        return self.people[num]

    def numsToNames(self, List):
        return map(self.getName, List)

    def namesToNum(self, List):
        return map(self.getNum, List)
            

class Graph:
    def __init__(self,messageFile):
        self.fullList = []
        self.D = {}
        self.notConspSend = -0.25
        self.notConspRec = -0.50
        self.conspSend = 0.50
        self.conspRec = 0.25
        self.certaintyNotConsp = [0]*numNodes
        self.certaintyConsp = [.5]*numNodes
        self.topicCount = [0]*(numTopics+1)
        self.topicWeight = [.1,  #Not in use\
                            .1,  #1\
                            .1,  #2\
                            .1,  #3\
                            .1,  #4\
                            .1,  #5\
                            .1,  #6\
                            .95,  #7\
                            .1,  #8\
                            .1,  #9\
                            .1,  #10\
                            .95,  #11\
                            .1,  #12\
                            .95,  #13\
                            .1,  #14\
                            .1]  #15
        f = open(messageFile, 'r')
        for line in f.readlines():
            Nums = line.split()
            Node1 = int(Nums[0])
            Node2 = int(Nums[1])
            if not self.D.has_key((Node1,Node2)):
                    self.D[(Node1,Node2)] = []
            for i in Nums[2:]:
                self.D[(Node1,Node2)] += [int(i)]
                self.topicCount[int(i)]+=1
        f.close()

    def weightConspirator(self, node, certainty = 1):
        '''Changes the weights of the topics based (using a given person)
            The effect is scaled with certainty'''
        for i in range(numNodes):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    effectiveCoeff = self.notConspSend+\
                                     (self.conspSend-self.notConspSend)*certainty
                    x = 1-self.topicWeight[j]
                    #self.topicWeight[j]+= certainty * self.conspRec
                    if(DEBUG):
                        print "Send: certainty = " + str(certainty)
                        print "effectiveCoef = " + str(effectiveCoeff)
                        print " Before: topic " + str(j)+ "'s weight = " + str(self.topicWeight[j])

                    self.topicWeight[j] += min(self.topicWeight[j],x)*effectiveCoeff
                    if(DEBUG):
                        print " After: topic " + str(j)+ "'s weight = " + str(self.topicWeight[j])

                        #self.topicWeight[j]+= certainty * self.conspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    effectiveCoeff = self.notConspRec+\
                                     (self.conspRec-self.notConspRec)*certainty
                    x = 1-self.topicWeight[j]
                    if(DEBUG):
                        print "Recieve: certainty = " + str(certainty)
                        print "effectiveCoef = " + str(effectiveCoeff)
                        print " Before: topic " + str(j)+ "'s weight = " + str(self.topicWeight[j])
                    #self.topicWeight[j]+= certainty * self.conspRec
                    self.topicWeight[j] += min(self.topicWeight[j],x)*effectiveCoeff
                    if(DEBUG):
                        print " After: topic " + str(j)+ "'s weight = " + str(self.topicWeight[j])

    """def weightNotConspirator(self, node, certainty = 1):
        '''Changes the weights of the topics based (using a given person)
            The effect is scaled with certainty'''
        for i in range(numNodes):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    x = self.topicWeight[j]
                    self.topicWeight[i] -= x*self.consSend*certainty
                    #self.topicWeight[j]+= (1-certainty) * self.notConspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    self.topicWeight[j]+= (1-certainty) * self.notConspRec"""

    def numSent(self, node, topic):
        '''Returns the number of times a person sent a message pertaining
            to the specified topic'''
        count = 0
        for i in range(numNodes):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    if j == topic: count+=1
        return count
        
    def numRec(self, node, topic):
        '''Returns the number of times a person receives a message pertaining
            to the specified topic'''
        count = 0
        for i in range(numNodes):
            if self.D.has_key((i, node)):
                for j in self.D[(i, node)]:
                    if j == topic: count+=1
        return count



    def runFirstRound(self):
        '''Returns an orderd list of people from most suspicious to least'''
        for i in knownConsp:
            self.weightConspirator(i)
        for i in knownNotConsp:
            self.weightConspirator(i,0)
            
        L = map(self.scoreReport, range(numNodes))
        L.sort(key = lambda X: X[1], reverse = True)
        self.fullList = map(lambda X:X[0], L)
        return L 

    def runLaterRound(self):
        for i in knownConsp:
            self.certaintyConsp[i] = 1
        for i in knownNotConsp:
            self.certaintyConsp[i] = 0

        if(DEBUG2):
            print "last = " + str(findLast(knownConsp, self.fullList))
            print "first = " + str(findFirst(knownNotConsp, self.fullList))
        for i in self.fullList[:findLast(knownConsp, self.fullList)+1]:
            #Every possible conspirator
            if (knownNotConsp.count(i) == 0 and knownConsp.count(i) == 0):
                if(DEBUG):
                    print "Before: person " + str(i)+ "'s certainty = " + str(self.certaintyConsp[i])

                alpha = 0.7
                self.certaintyConsp[i] = self.certaintyConsp[i]*(1-alpha) + 1*alpha
                if(DEBUG):
                    print " After: person " + str(i)+ "'s certainty = " + str(self.certaintyConsp[i])                

        for i in self.fullList[findFirst(knownNotConsp, self.fullList):]:
            #Every likely non-conspirator
            if (knownNotConsp.count(i) == 0 and knownConsp.count(i) == 0):

                if(DEBUG):
                    print "Before: person " + str(i)+ "'s certainty = " + str(self.certaintyConsp[i])

                alpha = 0.1
                self.certaintyConsp[i] = self.certaintyConsp[i]*(1-alpha) + 0*alpha

                if(DEBUG):
                    print " After: person " + str(i)+ "'s certainty = " + str(self.certaintyConsp[i])


        for i in range(numNodes):
            self.weightConspirator(i, self.certaintyConsp[i])
            #self.weightNotConspirator(i, self.certaintyConsp[i])
            
        L = map(self.scoreReport, range(numNodes))
        #for i in range(numNodes):
         #   L[i].append(self.certaintyConsp[i])
        L.sort(key = lambda X: X[1], reverse = True)
        self.fullList = map(lambda X:X[0], L)
        return (L, self.topicWeight)
        
    def scoreReport(self, node):
        '''Return [node, score]'''
        score = 0.0
        for topic in range(1, numTopics + 1):
            score += self.topicWeight[topic]*(self.numRec(node, topic)+\
                                     self.numSent(node, topic)+0.0)\
                                     /self.topicCount[topic]
        return [node, score, self.certaintyConsp[node]]

def nicePrintList(L):
    print "{0:5}{1:13}{2:9}{3:7}".format("Rank".ljust(5),"Name".center(13),"Score".center(6),"Certainty".rjust(7)),'\n'
    for i in range(len(L)):
        print "{0:5}{1:13}{2:6.3f}{3:9.4f}".format(str(i).ljust(5),L[i][0],L[i][1],L[i][2])

def nicePrintTopics(L):
    print "{0:5}{1:7}".format("Topic".ljust(5),"Weight".center(7))
    for i in range(1,len(L)):
        print "{0}{1:5.4f}".format(str(i).ljust(5),L[i])
def main():
    global knownConsp
    global knownNotConsp
    names = Names('names.txt')
    graph = Graph('messages.txt')
    knownConsp = names.namesToNum(knownConsp)
    knownNotConsp = names.namesToNum(knownNotConsp)
    L = graph.runFirstRound()
    temp = 1
    topics = 0
    for i in range(5):
        if(DEBUG):
            print "-----------------------------------------------------"
            print "Round " + str(i)
            
        [L, topics] = graph.runLaterRound()
        temp = map(lambda X:[names.getName(X[0]),X[1], X[2]] , L)
        for j in range(len(temp)):
            temp[j][2] = round(temp[j][2],2)
        if(DEBUG):
            print nicePrintList(temp)
    nicePrintList(temp)
    print "--------------------------------------------------"
    nicePrintTopics(topics)
    #print map(lambda X:X[0],temp)
    print "--------------------------------------------------"
    

if __name__ == '__main__': main()
