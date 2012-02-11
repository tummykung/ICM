numNodes = 83
numTopics = 15

knownConsp = ['Jean','Alex','Elsie','Paul','Ulf','Yao','Harvey']
knownNotConsp = ['Darlene','Tran','Ellin','Gard','Chris','Paige','Este']
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
        self.D = {}
        self.notConspSend = -.5
        self.notConspRec = -.8
        self.conspSend = 1
        self.conspRec = .5
        self.topicCount = [0]*(numTopics+1)
        self.topicWeight = [0,  #Not in use\
                            0,  #1\
                            0,  #2\
                            0,  #3\
                            0,  #4\
                            0,  #5\
                            0,  #6\
                            1,  #7\
                            0,  #8\
                            0,  #9\
                            0,  #10\
                            1,  #11\
                            0,  #12\
                            1,  #13\
                            0,  #14\
                            0]  #15
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
                    self.topicWeight[j]+= certainty * self.conspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    self.topicWeight[j]+= certainty * self.conspRec

    def weightNotConspirator(self, node, certainty = 1):
        '''Changes the weights of the topics based (using a given person)
            The effect is scaled with certainty'''
        for i in range(numNodes):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    self.topicWeight[j]+= certainty * self.notConspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    self.topicWeight[j]+= certainty * self.notConspRec

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
            self.weightNotConspirator(i)
            
        L = map(score, range(numNodes))
        L.sort(key = lambda X: X[1])
        return map(lambda X:X[0], L)
        
        
    

def main():
    global knownConsp
    global knownNotConsp
    names = Names('names.txt')
    graph = Graph('messages.txt')
    knownConsp = names.namesToNum(knownConsp)
    knownNotConsp = names.namesToNum(knownNotConsp)
    

if __name__ == '__main__': main()
        
