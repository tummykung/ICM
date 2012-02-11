class graph:
    def __init__(self,rFile):
        self.D = {}
        self.notConspSend = -.5
        self.notConspRec = -.8
        self.conspSend = 1
        self.conspRec = .5
        self.topicCount = [0]*16
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
        f = open(rFile, 'r')
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

    def weightConspirator(self, node, known = 1):
        for i in range(83):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    self.topicWeight[j]+= known * self.conspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    self.topicWeight[j]+= known * self.conspRec

    def numSent(self, node, topic):
        count = 0
        for i in range(83):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    if j == topic: count+=1
        return count
        
    def numRec(self, node, topic):
        count = 0
        for i in range(83):
            if self.D.has_key((i, node)):
                for j in self.D[(i, node)]:
                    if j == topic: count+=1
        return count

    def weightNotConspirator(self, node, known = 1):
        for i in range(83):
            if self.D.has_key((node,i)):
                for j in self.D[(node,i)]:
                    self.topicWeight[j]+= known * self.notConspSend
            if self.D.has_key((i,node)):
                for j in self.D[(i,node)]:
                    self.topicWeight[j]+= known * self.notConspRec