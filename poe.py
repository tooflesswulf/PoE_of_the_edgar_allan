import numpy as np
import itertools
from functools import total_ordering
import math
import time

MAXNUM = 40
# a = np.array([1, 1, 10, 10, 10, 10, 19, 19])
a = np.random.randint(1, MAXNUM, 90)
a.sort()


@total_ordering
class HistNum:
    def __init__(self, v):
        self.v = v
        self.histories = [np.zeros(MAXNUM, dtype=int)]
        self.histories[0][v - 1] = 1

    # Optimization: sort `self.histories` and use binary search instead of linear
    def add_history(self, new_hist):
        for h in self.histories:
            if np.all(new_hist == h):
                return
        self.histories.append(new_hist)

    def __add__(self, ot):
        if self.v + ot.v > MAXNUM:
            return None
        new = HistNum(self.v + ot.v)
        new.histories = []
        for (h1, h2) in itertools.product(self.histories, ot.histories):
            new.add_history(h1 + h2)
        # new.histories = heapq.merge(self.histories, ot.hist)
        return new

    def __or__(self, other):
        assert self.v == other.v
        new = HistNum(self.v)
        new.histories = self.histories.copy()
        for h in other.histories:
            new.add_history(h)
        return new

    def __eq__(self, other):
        if isinstance(other, int):
            return self.v == other
        return self.v == other.v

    def __lt__(self, other):
        if isinstance(other, int):
            return self.v < other
        return self.v < other.v

    def __hash__(self):
        return hash(self.v)

    def __repr__(self):
        return str(self.v)


class HistSet(list):
    def add(self, e: HistNum):
        if e in self:
            self[self.index(e)] |= e
            return

        self.append(e)

    def union_with_history(self, s):
        for e in s:
            self.add(e)


def get_sets(a: np.ndarray, toplevel=False):
    if a.size == 1:
        return HistSet([HistNum(a[0])])

    split = a.size // 2
    if a.size > 30:
        split = math.ceil(a.size / 10)

    s2 = get_sets(a[split:])
    s1 = get_sets(a[:split])

    t = time.time()

    # res = HistSet([p + q for (p, q) in itertools.product(s1, s2) if p + q <= maxv])
    for (p, q) in itertools.product(s1, s2):
        if toplevel:
            if p.v + q.v != 40:
                continue
        if p.v + q.v <= 40:
            s1.add(p + q)
    s1.union_with_history(s2)

    dt = time.time() - t
    if dt > .05:
        print('Layer {} Merged in {}s'.format(a.size, dt))
    return s1


z = get_sets(a, True)
print(a)
print(z)

num40 = None
for el in z:
    if el == 40:
        num40 = el
        break

if num40 is None:
    print('No formation of 40 =(')
    exit(0)

# print('Solutions:')
# for hist in num40.histories:
#     ixs = np.where(hist)[0]
#     c = []
#     for i in ixs:
#         for j in range(hist[i]):
#             c.append(i + 1)
#     print(c)

print('{} solutions found'.format(len(num40.histories)))
