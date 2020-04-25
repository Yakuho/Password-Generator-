class GeneratorCreator:
    """
    #### 示例用法一：
    g1 = GeneratorCreator('3', '0123456789')    -> 拿到长度为3，密令字符组成为0123456789的密令生成对象
    for i in g1.generator():
        print(i)
    执行结果:
    >> 000
    >> 001
    >> 002
    >> ...
    >> 998
    >> 999

    #### 示例用法二：
    g1 = GeneratorCreator('3-4', '0123456789')    -> 拿到长度为3位到4位，密令字符组成为0123456789的密令生成对象
    for i in g1.generator():
        print(i)
    执行结果:
    >> 000
    >> 001
    >> 002
    >> ...
    >> 998
    >> 999
    >> 0000
    >> 0001
    >> ...
    >> 9999

    #### 示例用法三：
    g1 = GeneratorCreator('3-4', '0123456789')    -> 拿到长度为3位到4位，密令字符组成为0123456789的密令生成对象
    tasks = g1.task_distribution(3)     -> 将总遍历任务分割为3个子任务
    print(tasks)
    for i in g1.generator(tasks[0]):        -> 拿到的 tasks[0] 为 (0, 3666)
        print(i)
    执行结果：
    >> [(0, 3666), (3667, 7332), (7333, 10998)]
    >> 000
    >> 001
    >> ...
    >> 0001
    >> 0002
    >> ...
    >> 3666
    """
    def __init__(self, amount_range: str, sign_set: str):
        """
        初始化密令生成器
        :param amount_range: 密令长度区间：例如 6-8 或者 6
        :param sign_range: 密令字符的符号集：例如 0123456789abcde.....ABCDE.....!@#$!...
        """
        if len(amount_range) > 1:
            self.s, self.e = amount_range.split('-')            # 拿到遍历长度
            self.s, self.e = int(self.s), int(self.e)
        else:
            self.s, self.e = int(amount_range), int(amount_range)
        self.sign = {i: sign_set[i] for i in range(len(sign_set))}
        # 生成密令字符的字典 用于进制数相加后，根据数值拿到最终字符串
        # 例如{0: '0', 1: '1', ... , 10: 'a', 11: 'b', ...., 20: '@'}
        self.n = len(sign_set)    # 密令字符的字典的长度
        self.array = []     # 密令字符的量化值->例如000000 = [0, 0, 0, 0, 0, 0]

    def generator(self, offset=None):
        """
        密令的生成过程
        :return: 密令生成器对象，可以直接遍历
        """
        # 如果传入偏移区间 则按偏移区间遍历
        if offset:
            x, y = offset
            x = self.transform(x)
            y = self.transform(y)
        # 否则从头开始遍历
        else:
            x = [0] * self.s
            y = [self.n - 1] * self.e
        self.array = x
        while 1:
            # 密令字符的量化值转化为密令
            string = ''.join([self.sign[i] for i in self.array])
            yield string
            if self.array == y:
                break
            # self.increase()密令字符的量化值自增1
            # 溢出则扩充长度n+1
            if not self.increase():
                self.array = [0] * (len(self.array) + 1)

    def task_distribution(self, user):
        """
        传入分发的任务数 返回遍历区间
        :param user: 分割的任务数
        :return:
        """
        # 计算最后一条密令的十进制量化值
        total = 0
        for i in range(self.s, self.e + 1):
            total += self.n**i - 1
        # 遍历次数平均分割
        t = round(total/user)
        tasks = []
        # 分发遍历任务
        for i in range(user):
            #     因为根据平均分割后，可能会出现小数部分，t为四舍五入拿到的整数值，若不对右区间进行处理，会造成右区间为total±▲x
            #     区间规则：<1.若左区间为0开始，则为0，否则等于上一个区间的右区间+1><2.若有区间为最后一个区间，则右区间为遍历总数>
            tasks.append((0 if i == 0 else i*t+1, total if i == user-1 else (i+1)*t))
        return tasks

    def transform(self, x):
        """
        通过传入参数x，转化为self.n进制的最小长度的self.n进制数。
        :param x: 十进制数
        :return: self.n进制数列表 例如[13, 11, 0, 1, 2]
        """
        if x == 0:
            # 如果是0开始 则默认为000000->位数为起始区间决定
            x = [0] * self.s
        else:
            t = 0
            # 算出x含有几位数
            for i in range(self.s, self.e + 1):
                if self.n**i > x:
                    t = i
                    break
            # 初始化x
            x2 = list()
            for i in range(t-1, -1, -1):
                # 计算各个数位的权重，例如3217873 在13进制中，长度为6的数中，13**5的权重为8，13**4的权重为8......
                weight = int(x/self.n**i)
                x -= weight*self.n**i
                x2.append(weight)
            else:
                x = x2
        return x

    def increase(self, index=-1):
        """
        self.n进制数增加
        :param index: 默认从右数起的第一位加一，遇到进位就递归传入index=index-1  ( |index-1| <= 目前密令的最大长度)
        :return: 不溢出则返回True,溢出则返回False
        """
        temp = self.array[index]
        if temp + 1 < self.n:
            self.array[index] = temp + 1
            return True
        else:
            self.array[index] = 0
            if abs(index - 1) <= len(self.array):
                return self.increase(index-1)
            else:
                return False
