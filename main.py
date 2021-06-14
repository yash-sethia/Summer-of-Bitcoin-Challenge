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

# Reading CSV into a list
def parse_mempool_csv():
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])


def get_fee(obj):
    return obj.give_fee()



# Linear search that returns the transaction with given txid
def search(tList, id):
    for b in tList:
        if b.txid == id:
            return b

# Recursive function that adds the parents of the given block (parents list) via a Deapth First Search Algorithm
def addParents(tList, ans, parents):
    global limit
    for p in parents:
        if p in ans:
            continue
        else:
            ob = search(tList, p)
            if(addBlock(tList, ob, ans) == False):
                return False
    return True


# A recursive funtion to add the blocks and it's parents (via DFS)
def addBlock(tList, obj, ans):
    global limit
    if obj.weight <= limit:
        if obj.parents[0] == '':
            ans.append(obj.txid)
            limit -= obj.weight
            return True
        else:
            for p in obj.parents:
                if (addParents(tList, ans, obj.parents) == False):
                    return False
            return True
    else:
        return False


if __name__ == '__main__':
    # Declaring limit as global variable
    global limit

    # Reading data from the CSV file
    l = parse_mempool_csv()

    #sorting the list to make sure transactions with highest fee are processed first (Greedy approach)
    l.sort(key = get_fee, reverse=True)

    #ans => list that contains the transaction ids selected for the block
    ans = []
    limit = 4000000
    for obj in l:
        #if limit the weighr we can add is 0, break from the loop
        if(limit == 0):
            break;
        # Because DFS might cause limit to be zero before adding all the ancestors of a transactions, we need to store the previous limit for backtracking
        cont = limit
        if(addBlock(l, obj, ans) == False):
            limit = cont

    # For cross checking the totalf weight and fee of block
    # totalw = 0
    # totalf = 0
    # for b in ans:
    #     ob = search(l, b)
    #     totalf += ob.fee
    #     totalw += ob.weight
    # print(totalw)
    # print(totalf)

    # Writing output in block.txt as mentioned in the question
    with open('block.txt', mode="w") as outfile:
        for block in ans:
            outfile.write('%s\n' % block)

