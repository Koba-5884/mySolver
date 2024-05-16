from math import sqrt

class IntPointTri1():

    def __init__(self):

        n1 = 1 / 3

        self.P = [(n1, n1)]

        self.W = [1 / 2]

class IntPointTri3():

    def __init__(self):

        n1 = 1 / 6
        n2 = 2 / 3

        w1 = 1 / 6

        self.P = [(n1, n1), (n2, n1), (n1, n2)]

        self.W = [w1, w1, w1]

class IntPoint2x2():

    def __init__(self):

        n1 = sqrt(1 / 3)

        self.P = [( n1, n1), ( n1, -n1), 
                  (-n1, n1), (-n1, -n1)]

        self.W = [1.0, 1.0,
                  1.0, 1.0]
    
class IntPoint3x3():

    def __init__(self):

        n1 = sqrt(3 / 5)
        w1 = 8 / 9
        w2 = 5 / 9

        self.P = [( n1,  n1), (  0.0,  n1), (-n1,  n1),
                  ( n1, 0.0), (  0.0, 0.0), (-n1, 0.0),
                  ( n1, -n1), (  0.0, -n1), (-n1, -n1)]

        self.W = [w2 ** 2, w1 * w2, w2 ** 2,
                  w1 * w2, w1 ** 2, w1 * w2,
                  w2 ** 2, w1 * w2, w2 ** 2]
