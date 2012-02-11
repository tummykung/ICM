class graph:
    def __init__(self,rFile):
        self.D = {}
        self.notConspSend = -.5
        self.notConspRec = -.8
        self.conspSend = 1
        self.conspRec = .5
        self.MessageWeight = {1:0,\
                              2:0,\
                              3:0,\
                              4:0,\
                              5:0,\
                              6:0,\
                              7:1,\
                              8:0,\
                              9:0,\
                              10:0,\
                              11:1,\
                              12:0,\
                              13:1,\
                              14:0,\
                              15:0}
        f = open(rFile, 'r')
        for line in f.readlines():
            Nums = line.split()
            Node1 = int(Nums[0])
            Node2 = int(Nums[1])
            if not self.D.has_key((Node1,Node2)):
                    self.D[(Node1,Node2)] = []
            for i in Nums[2:]:
                self.D[(Node1,Node2)] += [int(i)]
        f.close()

    def weightConspirator(self, node, known = 1):
        for i in range(1,83):
            for j in self.D[(node,i)]:
                self.MessageWeight[j]+= known * self.conspSend
            for j in self.D[(i,node)]:
                self.MessageWeight[j]+= known * self.conspRecieve

    def weightNotConspirator(self, node, known = 1):
        for i in range(1,83):
            for j in self.D[(node,i)]:
                self.MessageWeight[j]+= known * self.notConspSend
            for j in self.D[(i,node)]:
                self.MessageWeight[j]+= known * self.notConspRecieve
        
