class MempoolTransaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = parents.split(';')
        # print(self)

    def give_fee(self):
        return self.fee


    def print_block(self):
        print(self.txid)
        print(self.fee)
        print(self.weight)
        print(self.parents)


global limit

def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])


def get_fee(obj):
    return obj.give_fee()

def search(blockList, id):
    for b in blockList:
        if b.txid == id:
            return b

def addParents(blockList, ans, parents):
    global limit
    for p in parents:
        if p in ans:
            continue
        else:
            ob = search(blockList, p)
            if(addBlock(blockList, ob, ans) == False):
                return False
            else:
                print(ob.txid)
    return True

def addBlock(blockList, obj, ans):
    global limit
    if obj.weight <= limit:
        if obj.parents[0] == '':
            ans.append(obj.txid)
            limit -= obj.weight
            return True
        else:
            for p in obj.parents:
                if (addParents(blockList, ans, obj.parents) == False):
                    return False
            return True
    else:
        return False


if __name__ == '__main__':
    global limit
    l = parse_mempool_csv()
    l.sort(key = get_fee, reverse=True)
    ans = []
    limit = 4000000
    for obj in l:
        if(limit == 0):
            break;
        cont = limit
        if(addBlock(l, obj, ans) == False):
            limit = cont
    # totalw = 0
    # totalf = 0
    # for b in ans:
    #     ob = search(l, b)
    #     totalf += ob.fee
    #     totalw += ob.weight
    # print(totalw)
    # print(totalf)


    with open('block.txt', mode="w") as outfile:
        for block in ans:
            outfile.write('%s\n' % block)

