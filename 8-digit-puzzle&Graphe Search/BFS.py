import time


# 交换一个字符串中的两个字符，用于解决交换空格
def switchchar(str, p1, p2):
    left = p1
    right = p2
    if (p1 > p2):
        left = p2
        right = p1
    elif (p1 == p2):
        return str
    lstr = ""
    rstr = ""
    mstr = ""
    if (left == 0):
        lstr = ""
    else:
        lstr = str[:left]
    if right == len(str) - 1:
        rstr = ""
    else:
        rstr = str[right + 1:]
    if ((right - left) == 1):
        mstr = ""
    else:
        mstr = str[left + 1: right]
    return lstr + str[right] + mstr + str[left] + rstr


# 用对象表示状态点
class StateNode:
    rank = -2
    mother_rank = -2
    # 初始化即执行
    def __init__(self, value, dstvalue, step):
        self.value = value
        self.index = value.find("*")
        self.assess = 0
        self.dstvalue = dstvalue
        if (self.index < 0):
            print(self.tostring() + " error")
            raise RuntimeError
        for i in range(len(value)):
            if (value[i] == dstvalue[i]):
                self.assess += 1
        self.step = step
        # self.rank = 0  # index用于记录每个结点的编号，
        # self.mother_rank = 0 # mother_rank用于记录其亲结点的编号

    # 显示一下当前结点
    def tostring(self):
        return "Node:{0} assess={1} step={4}\n     {2}\n     {3}\n".format(self.value[:3], self.assess, self.value[3:6],
                                                                           self.value[6:], self.step)

    def left(self):
        if (self.index % 3 != 0):
            return StateNode(switchchar(self.value, self.index - 1, self.index), self.dstvalue, self.step + 1)

    def right(self):
        if (self.index % 3 != 2):
            return StateNode(switchchar(self.value, self.index + 1, self.index), self.dstvalue, self.step + 1)

    def up(self):
        if (self.index > 2):
            return StateNode(switchchar(self.value, self.index - 3, self.index), self.dstvalue, self.step + 1)

    def down(self):
        if (self.index < 6):
            return StateNode(switchchar(self.value, self.index + 3, self.index), self.dstvalue, self.step + 1)


def bfs(startval, endval):
    rank = 0  # rank从0开始，初始节点的index为0，其mother_index为-1
    startNode = StateNode(startval, endval, 0)
    startNode.rank = 0
    startNode.mother_rank = -1
    openlist = [startNode]  # OpenList，用于存储
    closelist = []  # CloseList，用于存储
    AllNode.append(startNode)  # 首先包含初始结点
    while True:
        # rank += 1  # rank先自增一次 发现似乎不用，产生新结点时候再自增更好控
        # assess值用于表示当前结点中有多少个数码在正确的位置上
        openlist = sorted(openlist, key=lambda node: node.assess)  # 根据access值来排序，让更有希望的先出来，能显著提高速度
        curNode = openlist.pop()
        if (curNode == None):
            print("End")
            return

        print(curNode.tostring())

        # 如果所有九个数码都在正确位置上，说明找到，可结束
        if (curNode.assess == 9):
            print("Found,end!")
            return curNode

        # 否则就以此为父结点衍生出其子结点
        leftNode = curNode.left()
        rightNode = curNode.right()
        upNode = curNode.up()
        downNode = curNode.down()
        # 对于所有新产生的结点，不在openlist且不在closelist里面的即先插入openlist
        if (leftNode != None):
            exist = False
            for node in openlist:
                if (leftNode.value == node.value):
                    exist = True
                    break
            for node in closelist:
                if (leftNode.value == node.value):
                    exist = True
                    break
            if (not exist):
                rank += 1
                leftNode.rank = rank
                leftNode.mother_rank = curNode.rank
                openlist.append(leftNode)
                AllNode.append(leftNode)
        if (rightNode != None):
            exist = False
            for node in openlist:
                if (rightNode.value == node.value):
                    exist = True
                    break
            for node in closelist:
                if (rightNode.value == node.value):
                    exist = True
                    break
            if (not exist):
                rank += 1
                rightNode.rank = rank
                rightNode.mother_rank = curNode.rank
                openlist.append(rightNode)
                AllNode.append(rightNode)
        if (upNode != None):
            exist = False
            for node in openlist:
                if (upNode.value == node.value):
                    exist = True
                    break
            for node in closelist:
                if (upNode.value == node.value):
                    exist = True
                    break
            if (not exist):
                rank += 1
                upNode.rank = rank
                upNode.mother_rank = curNode.rank
                openlist.append(upNode)
                AllNode.append(upNode)
        if (downNode != None):
            exist = False
            for node in openlist:
                if (downNode.value == node.value):
                    exist = True
                    break
            for node in closelist:
                if (downNode.value == node.value):
                    exist = True
                    break
            if (not exist):
                rank += 1
                downNode.rank = rank
                downNode.mother_rank = curNode.rank
                openlist.append(downNode)
                AllNode.append(downNode)
        # 若不存在新生结点那么把这个结点放入closelist
        closelist.append(curNode)


#用于打印结果,使用递归方法
def print_rank(curnode:StateNode):
    if(curnode.rank != 0):
        # 如果当前结点不是根结点，递归到上一层
        rank = curnode.mother_rank
        s = int(rank)
        print_rank(AllNode[s])
    # 然后直接打印即可
    print(curnode.value[:3], "\n", curnode.value[3:6], "\n", curnode.value[6:])
    return

if __name__ == '__main__':
    DistNode = StateNode("12345678*", "*12345678", 0)
    AllNode = []  # 记录所有结点
    time_start = time.time()
    start = "1234*5678"
    dist = "1234567*8"
    DistNode = bfs(start, dist)
    print("begin", start)
    print("dist", dist)
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    # 接下来打印步骤,不属于求解，故不计入时间
    # CurNode = DistNode.value
    # print(CurNode)
    # print(CurNode[:3], "\n", CurNode[3:6], "\n", CurNode[6:])
    print_rank(DistNode)
    # print(DistNode.mother_rank)
