class graph:
    def __init__(self,rFile):
        self.D = {}
        self.MessageWeight = {}
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