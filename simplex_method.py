from enum import Enum
import numpy as np


class Constrains(Enum):
    LESS_THAN = 1
    GRAEATER_THAN = 2
    EQUAL = 3


class Type(Enum):
    MAX = 1
    MIN = 2


class SimplexMethod:
    def __init__(self, noOfVars, noOFConstrains):
        self.noOfVars = noOfVars
        self.noOFConstrains = noOFConstrains
        self.addedConstrains = 1
        self.matrix = np.zeros(
            (noOFConstrains + 1, noOFConstrains + noOfVars + 1))

    def convert(self, eq, constrain_type):
        if constrain_type == Constrains.GRAEATER_THAN:
            eq = [eq * -1 for eq in eq]
            return eq
        elif constrain_type == Constrains.EQUAL:
            return eq
        elif constrain_type == Constrains.LESS_THAN:
            eq = [eq * 1 for eq in eq]
            return eq

    def _add(self, eq, position, eqType="obj"):
        # get position row of matrix
        table = self.matrix[position, :]
        if eqType == "obj":
            eq = [round(float(i), 2) for i in eq.split(',')]
        if len(eq) < self.noOfVars:
            raise Exception("Invalid number of variables")

        for i in range(0, self.noOfVars):
            if eqType == "obj":
                table[i] = eq[i] * -1
            else:
                table[i] = eq[i]
        # right side value.
        table[-1] = eq[-1]
        self.matrix[position, :] = table

    def add_obj(self, eq):
        self._add(eq, 0)

    def add_constrains(self, eq, constrain_type):
        eq = [round(float(i), 2) for i in eq.split(',')]
        eq = self.convert(eq, constrain_type)
        self._add(eq, self.addedConstrains, 'constrain')
        self.addedConstrains += 1

    def check_negative_topmost_row(self):
        # get the first row of matrix
        table = self.matrix[0, :]
        m = min(table)
        if m < 0:
            return True
        return False

    def find_negative_index(self):
        neg_index = np.where(self.matrix == min(self.matrix[0, :]))
        return {
            "col": neg_index[1][0],
            "row": neg_index[0][0]
        } if len(neg_index[1]) > 0 and len(neg_index[0]) > 0 else None

    def locate_pivot(self):
        total = np.array([])
        r = self.find_negative_index()
        c = r['col']
        r = r['row']
        row = self.matrix[r, :]
        col = self.matrix[:, c]
        lastCol = self.matrix[:, -1]
        m = min(row)
        for left, right in zip(col, lastCol):
            if left > 0 and right / left > 0:
                total = np.append(total, right / left)
            else:
                total = np.append(total, 0.0)
        # find min value by excluding zero.
        index = np.where(total == min(total[total > 0]))[0][0]
        return [index, c]

    def pivot(self, row, col):
        lc = len(self.matrix[0, :])
        lr = len(self.matrix[:, 0])
        table = np.zeros((lr, lc))
        pivot = self.matrix[row, col]
        pivot_row = self.matrix[row, :]
        if pivot > 0:
            r = pivot_row / pivot
            for i in range(len(self.matrix[:, col])):
                k = self.matrix[i, :]
                c = self.matrix[i, col]
                if list(k) != list(pivot_row):
                    # subtract pivot row from each row and multiply by pivot value
                    table[i, :] = list(k - r * c)
            table[row, :] = r
            self.matrix = table

    def generate_vars(self):
        v = []
        for i in range(self.noOfVars):
            v.append('x' + str(i+1))
        return v

    def solve(self):
        while self.check_negative_topmost_row() == True:
            self.pivot(self.locate_pivot()[0], self.locate_pivot()[1])
            # print(self.matrix)

        i = 0
        var = {}
        for i in range(self.noOfVars):
            col = self.matrix[:, i]
            s = sum(col)
            m = max(col)

            if float(s) == float(m):
                location = np.where(col == m)[0][0]
                var[self.generate_vars()[i]] = self.matrix[location, -1]
            else:
                var[self.generate_vars()[i]] = 0
        var['max'] = self.matrix[0, -1]
        print(self.matrix)
        return var

    def maximize(self):
        return self.solve()

    def minimize(self):
        # multiply first row by -1
        self.matrix[0, :] = self.matrix[0, :] * -1
        return self.solve()


s = SimplexMethod(2, 3)
# s.add_obj('10, 8,0')
# s.add_constrains('3, 1, 4500', Constrains.LESS_THAN)
# s.add_constrains('2, 2, 4000', Constrains.LESS_THAN)
# s.add_constrains('1, 3, 4500', Constrains.LESS_THAN)
# print(s.matrix)
# print(s.maximize())

s.add_obj('5, 7,0')
s.add_constrains('1, 0, 10', Constrains.LESS_THAN)
s.add_constrains('1,1, 12', Constrains.EQUAL)
s.add_constrains('1, -2, 3', Constrains.GRAEATER_THAN)
print(s.matrix)
print(s.maximize())
