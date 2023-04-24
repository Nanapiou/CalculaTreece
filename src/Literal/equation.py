"""
Module to solve an equation
"""
from math import sqrt
from turtle import Turtle, done

from src.Trees.trees import BinaryTree
from src.Trees.calculator import calculate_tree


class Equation:
    """
    params:
    x (str): The unknown of the equation

    methods:
        resolve(left: BinaryTree, right: BinaryTree = 0) -> list: Resolve the equation
        level_1(left: BinaryTree, right: BinaryTree) -> list: Solve the equation if it is simple ('+' or '-' or '*' or '/')
        level_2(left: BinaryTree, right: BinaryTree) -> list: Solve the equation if type ax² + bx+ c = 0

    result (list): solution(s) of the equation
    """

    def __init__(self, x):
        self.unknown = x

    def eval_level(self, left: BinaryTree, right: BinaryTree) -> int:
        level = 0
        for side in [left, right]:
            for branch in side.iter_branches():
                if branch.value == '**' or branch.value == '^' and branch.right.value == 2:
                    level = 1
                elif not (isinstance(branch.value, (int, float)) or branch.value in ['+', '-', '*', '/', self.unknown]):
                    level = 2
        return level

    def resolve(self, left: BinaryTree, right: BinaryTree = BinaryTree(0)) -> list:

        """
        Resolve the equation

        params:
        left (BinaryTree): The left part of the equation
        right (BinaryTree): The right part of the equation

        result (list): solution(s) of the equation
        """
        assert self.__verif(left, right), 'Tree is empty'

        level = self.eval_level(left, right)
        # print(f'level: {level}')

        match level:
            case 0:
                result = self.level_1(left, right)
            case 1:
                result = self.level_2(left, right)
            case 2:
                pass

        return result

    def level_1(self, left: BinaryTree, right: BinaryTree) -> list:
        """
        Solve the equation if it is simple ('+' or '-' or '*' or '/')
        """

        all_x = 0
        # for division
        multi = []

        for side in [left, right]:
            for branch in side.iter_branches():
                if branch.value == self.unknown:
                    all_x += 1 if side == left else -1
                    branch.value = 0

                elif branch.value == '*':
                    if branch.left.value == self.unknown:
                        all_x += branch.right.value if side == left else -branch.right.value
                        branch.left.value = 0
                    elif branch.right.value == self.unknown:
                        all_x += branch.left.value if side == left else -branch.left.value
                        branch.right.value = 0

                elif branch.value == '/':
                    if branch.left.value == self.unknown:
                        multi.append(branch.right.value)
                        all_x += 1 if side == left else -1
                        branch.left.value = 0
                    elif branch.right.value == self.unknown:
                        all_x += 1 if side == left else -1
                        branch.right.value = 1

        if all_x == 0:
            raise SyntaxError(f'No {self.unknown} in the equation or {self.unknown} cancels out')

        solutions = []
        # calculate the result
        result_left = -calculate_tree(left)
        result_right = calculate_tree(right)
        result = result_right + result_left

        for i in multi:
            result *= i


        # verify if is unknown is negative
        if all_x < 0:
            result = -result
            all_x = -all_x

        result /= all_x

        # add the result to the list
        solutions.append(result)

        return solutions

    def level_2(self, left: BinaryTree, right: BinaryTree) -> list:
        """
        Solve the equation if type ax² + bx+ c = 0
        """
        a = 0  # x²
        b = 0  # x

        # for division
        multi = []

        for side in [left, right]:
            for branch in side.iter_branches():

                if branch.value == '-':

                    if branch.left.value == self.unknown:
                        b += 1 if side == left else -1
                        branch.left.value = 0
                    elif branch.right.value == self.unknown:
                        b += -1 if side == left else 1
                        branch.right.value = 0

                elif branch.value == self.unknown:
                    b += 1 if side == left else -1
                    branch.value = 0

                elif (branch.right == '**' or branch.right == '^') and branch.right.value == 2:
                    a += 1 if side == left else -1
                    branch.left.value = 0

                elif branch.value == '*':
                    if branch.right.value == '**' and branch.right.right.value == 2:
                        a += branch.left.value if side == left else -branch.left.value
                        branch.right.left.value = 0

                    elif branch.left.value == self.unknown:
                        b += branch.right.value if side == left else -branch.right.value
                        branch.left.value = 0
                    elif branch.right.value == self.unknown:
                        b += branch.left.value if side == left else -branch.left.value
                        branch.right.value = 0

                elif branch.value == '/':
                    if branch.left.value == self.unknown:
                        multi.append(branch.right.value)
                    elif branch.right.value == self.unknown:
                        b += 1 if side == left else -1
                        branch.right.value = 1

        # calculate the result
        result_left = -calculate_tree(left)
        result_right = calculate_tree(right)
        c = result_right + result_left

        print(f'a: {a}, b: {b}, c: {c}')

        if a == 0:
            raise SyntaxError('The equation is not a quadratic equation')

        for i in multi:
            c *= i

        delta = b ** 2 - 4 * a * c

        print(f'delta: {delta}')

        solutions = []

        if delta < 0:
            pass

        elif delta == 0:
            solutions.append(-b / (2 * a))

        else:
            solutions.append((-b + sqrt(delta)) / (2 * a))
            solutions.append((-b - sqrt(delta)) / (2 * a))

        print(f'solutions: {solutions} ')

        return solutions

    def __find_x(self, arbre: BinaryTree, v: int = 1) -> list:
        """
        Find the unknown variable in the equation
        """
        k = 1
        for i in arbre.iter_branches():
            if not i.is_leaf() and i.left.value == self.unknown or i.right.value == self.unknown:
                if k == v:
                    return i
                k += 1

    def __replace(self, arbre: BinaryTree, x, y):
        """
        Replace the value of the unknown variable by the value given (0)
        """
        for i in arbre.iter_branches():
            if i.value == x:
                i.value = y

    def __verif(self, left: BinaryTree, right: BinaryTree) -> bool:
        """
        Check if the equation is simple

        :param arbre: The equation
        :return: basic verification
        """
        return not (left is None or right is None)


if __name__ == '__main__':
    eq = Equation('x')

    assert eq.resolve(
        BinaryTree('+').set_branches(BinaryTree('+').set_branches('x', 'x'), BinaryTree('+').set_branches('x', 5)),
        BinaryTree('-').set_branches('x', BinaryTree('+').set_branches(5, 2))) == [-6.0], 'Error with - and +'
    print('(+ and -) test passed')

    assert eq.resolve(BinaryTree('+').set_branches(BinaryTree('*').set_branches(2, 'x'), 5),
                      BinaryTree('+').set_branches(BinaryTree('*').set_branches(4, 'x'), 3)) == [1.0], 'Error with *'
    print('* test passed')

    assert eq.resolve(
        BinaryTree('+').set_branches(BinaryTree('/').set_branches('x', 4), BinaryTree('-').set_branches(3, 6)),
        BinaryTree('+').set_branches(BinaryTree('*').set_branches('x', 2), 1)) == [-2.285714286], 'Error with / (x/n)' #not working

    assert eq.resolve(
        BinaryTree('+').set_branches(BinaryTree('/').set_branches(4, 'x'), BinaryTree('-').set_branches('x', 1)),
        BinaryTree('+').set_branches('x', 3)) == [0.0], 'Error with / (n/x)'
    print('/ test passed')

    branch = BinaryTree('+').set_branches(BinaryTree('*').set_branches('x', 2), 1)
    t = Turtle()
    t.penup()
    t.goto(0, 350)
    branch.draw(t)
    done()

    tree = BinaryTree('-').set_branches(BinaryTree('*').set_branches(2, BinaryTree('**').set_branches('x', 2)),
                                        BinaryTree('-').set_branches(BinaryTree('-').set_branches(0, 'x'), 6))

    assert eq.resolve(tree, BinaryTree('-').set_branches(0, 0)) == [1.356107225224513, -1.106107225224513], 'Error with ax² + bx + c'
    print('** test passed')

    print('---------------------------------------------------------------')
    print('All tests passed')
