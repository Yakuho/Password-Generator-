from common import GeneratorInit


class GeneratorCreator(GeneratorInit):
    def generator(self, offset=None):
        """
        生成纯遍历密令
        :params offset: (x, y)
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

    def generator_domain(self, position, offset=None):
        """
        生成含有特定域的遍历密令
        可以使用任务分发的方式进行遍历
        :params position: ['front', 'rear', 'all'] front->特定域在头部;rear->特定域在尾部;all->特定域在每一处遍历密令
        :params offset: (x, y) 默认为None，即从头开始遍历
        :return: 密令生成器对象，可以直接遍历
        """
        try:
            f = open('domain.txt', 'r')
            domains = [domain for domain in f.read().split('\n') if domain]
            f.close()
        except FileNotFoundError:
            print('请检查你的domain文件是否在目录内.')
            return None
        if position not in ['front', 'rear', 'all']:
            print('没有该功能.')
            return None
        for t in domains:
            for part in self.generator(offset if offset else None):
                if position == 'front':
                    yield t + part
                elif position == 'rear':
                    yield part + t
                else:
                    yield t + part
                    for t0 in range(len(part)):
                        yield part[0:t0 + 1] + t + part[t0 + 1:len(part) + 1]

    @classmethod
    def generator_file(cls, files_name: list):
        """
        读取本地的密令文件, 可直接使用类名调用
        :params files_name: 文件名集合->列表属性
        :return: 密令生成器对象，可以直接遍历
        """
        for file in files_name:
            f = open(file, 'r')
            pd = [domain for domain in f.read().split('\n') if domain]
            f.close()
            for p in pd:
                yield p

    def generator_file_and_creator(self, files_name: list, position, offset=None):
        """
        读取本地的密令文件, 并结合遍历密令，依照位置拼接密令
        :params files_name: 文件名集合->列表属性
        :params position: ['front', 'rear', 'all'] front->特定域在头部;rear->特定域在尾部;all->特定域在每一处遍历密令
        :params offset: (x, y) 默认为None，即从头开始遍历
        :return: 密令生成器对象，可以直接遍历
        """
        if position not in ['front', 'rear', 'all']:
            print('没有该功能.')
            return None
        for file in files_name:
            try:
                f = open(file, 'r')
                pd = [domain for domain in f.read().split('\n') if domain]
                f.close()
            except FileNotFoundError:
                print(f'文件名: {file} 不存在.')
                continue
            for p in pd:
                for part in self.generator(offset if offset else None):
                    if position == 'front':
                        yield p + part
                    elif position == 'rear':
                        yield part + p
                    else:
                        yield p + part
                        for t0 in range(len(part)):
                            yield part[0:t0 + 1] + p + part[t0 + 1:len(part) + 1]


if __name__ == '__main__':
    g = GeneratorCreator('2', '0123456789')
    # g2 = g.generator()
    # for i in g2:
    #     print(i)
    # g2 = g.generator_domain('all')
    # for i in g2:
    #     print(i)
    # g2 = g.generator_file(['top3000.txt'])
    # for i in g2:
    #     print(i)
    # g2 = g.generator_file_and_creator(['top3000.txt'], 'all')
    # for i in g2:
    #     print(i)
