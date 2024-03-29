"""
Module to solve an equation
"""
from math import sqrt
from src.Trees.trees import BinaryTree
from src.Trees.calculator import calculate_tree


class Equation:
    """
    params:
    x (str): The unknown of the equation

    methods:
      resolve(left: BinaryTree, right: BinaryTree = 0) -> list Resolve the equation
      level_1(left: BinaryTree, right: BinaryTree) -> list Solve the equation if it is simple ('+' or '-' or '*' or '/')
      level_2(left: BinaryTree, right: BinaryTree) -> list Solve the equation if type ax² + bx+ c = 0

    result (list): solution(s) of the equation
    """

    def __init__(self, x):
        self.unknown = x
        self.operators = ['+', '-', '*', '/']

    def eval_level(self, left: BinaryTree, right: BinaryTree) -> int:
        """
        Evaluate the level of the equation

        :param left: The left part of the equation
        :param right: The right part of the equation
        """
        level = 0
        for side in [left, right]:
            for branch in side.iter_branches():
                if branch.value == '/' and branch.right.value == self.unknown and branch.left.value == self.unknown:
                    branch.right.value = 1
                    branch.left.value = 1
                elif branch.value == '/' and branch.left.value == self.unknown:
                    level = 2

                elif branch.value == '*' and branch.left.value == self.unknown and branch.right.value == self.unknown:
                    branch.value = '**'
                    branch.right.value = 2
                    branch.left.value = self.unknown

                elif branch.value == '*' and (
                        branch.left.value in self.operators or branch.right.value in self.operators):
                    level = 2
                elif branch.value == self.unknown and not branch.is_leaf():
                    level = 2

                elif (branch.value == '**' or branch.value == '^') and branch.right.value == 2:
                    level = 1
                elif (branch.value == '**' or branch.value == '^') and branch.right.value != 2:
                    level = 2

                elif not isinstance(branch.value, (
                        int, float)) and branch.value not in self.operators and branch.value != self.unknown:
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

        if level == 0:
            result = self.solve_level_0(left, right)
        elif level == 1:
            result = self.solve_level_1(left, right)
        else:
            result = None

        return result

    def solve_level_0(self, left: BinaryTree, right: BinaryTree) -> list:
        """
        Solve the equation if it is simple ('+' or '-' or '*' or '/')

        :param left: The left part of the equation
        :param right: The right part of the equation
        """

        all_x = 0
        # for division
        multi = []

        for side in [left, right]:
            for branch in side.iter_branches():
                match branch.value:

                    case self.unknown:
                        all_x += 1 if side is left else -1
                        branch.value = 0
                    case '*':
                        if branch.left.value == self.unknown:
                            all_x += branch.right.value if side is left else -branch.right.value
                            branch.left.value = 0
                        elif branch.right.value == self.unknown:
                            all_x += branch.left.value if side is left else -branch.left.value
                            branch.right.value = 0
                    case '/':
                        if branch.left.value == self.unknown:
                            multi.append(branch.right.value if side is left else -branch.right.value)
                            branch.right.value = 1

                        elif branch.left.value in self.operators:
                            if branch.left.value == '*' and (
                                    branch.left.left.value == self.unknown or branch.left.right.value == self.unknown):
                                multi.append(branch.right.value if side is left else -branch.left.right.value)
                                branch.right.value = 1

                    case '-':
                        if branch.right.value in self.operators:
                            if branch.right.value == '-' and branch.right.right.value == self.unknown:
                                all_x += -1 if side is left else 1
                                branch.right.right.value = 0
                            elif branch.right.value == '-' and branch.right.left.value == self.unknown:
                                all_x += -1 if side is left else 1
                                branch.right.left.value = 0

                        elif branch.left.value == self.unknown:
                            all_x += 1 if side is left else -1
                            branch.left.value = 0
                        elif branch.right.value == self.unknown:
                            all_x += -1 if side is left else 1
                            branch.right.value = 0

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

    def solve_level_1(self, left: BinaryTree, right: BinaryTree) -> list:
        """
        Solve the equation if type ax² + bx+ c = 0
        :param left: The left part of the equation
        :param right: The right part of the equation
        """
        a = 0  # x²
        b = 0  # x

        # for division
        multi = []

        for side in [left, right]:
            for branch in side.iter_branches():
                match branch.value:
                    case '-':
                        if branch.right.value in self.operators:
                            if branch.right.value == '-' and branch.right.right.value == self.unknown:
                                b += -1 if side is left else 1
                                branch.right.right.value = 0
                            elif branch.right.value == '-' and branch.right.left.value == self.unknown:
                                b += -1 if side is left else 1
                                branch.right.left.value = 0
                            elif branch.right.value == '*' and branch.right.right.value == self.unknown:
                                b += -branch.right.left.value if side is left else branch.right.left.value
                                branch.right.right.value = 0
                            elif branch.right.value == '*' and branch.right.left.value == self.unknown:
                                b += -branch.right.right.value if side is left else branch.right.right.value
                                branch.right.left.value = 0

                        elif branch.left.value == self.unknown:
                            b += 1 if side is left else -1
                            branch.left.value = 0
                        elif branch.right.value == self.unknown:
                            b += -1 if side is left else 1
                            branch.right.value = 0
                    case self.unknown:
                        b += 1 if side is left else -1
                        branch.value = 0

                    case '**' | '^':
                        if branch.right.value == 2 and branch.left.value == self.unknown:
                            a += 1 if side is left else -1
                            branch.left.value = 0
                    case '*':
                        if branch.right.value in (
                                '**',
                                '^') and branch.right.right.value == 2 and branch.right.left.value == self.unknown:
                            a += branch.left.value if side is left else -branch.left.value
                            branch.right.left.value = 0

                        elif (branch.left.value == '**'
                              and branch.left.right.value == 2
                              and branch.left.left.value == self.unknown):
                            a += branch.right.value if side is left else -branch.right.value
                            branch.left.left.value = 0

                        elif branch.right.value == self.unknown:
                            b += branch.left.value if side is left else -branch.left.value
                            branch.right.value = 0

                    case '/':
                        if branch.left.value == self.unknown:
                            multi.append(branch.right.value if side is left else -branch.right.value)

                        elif branch.left.value in self.operators:
                            if branch.left.value == '*' and (
                                    branch.left.left.value == self.unknown or branch.left.right.value == self.unknown):
                                multi.append(branch.right.value if side is left else -branch.left.right.value)
                                branch.right.value = 1

        # calculate the result
        result_left = calculate_tree(left)
        result_right = -calculate_tree(right)
        c = result_left + result_right

        # print(a, b, c)
        if a == 0:
            raise SyntaxError('The equation is not a quadratic equation')

        for i in multi:
            c *= i

        delta = b ** 2 - 4 * a * c

        solutions = []

        if delta < 0:
            pass

        elif delta == 0:
            solutions.append(-b / (2 * a))

        else:
            solutions.append((-b + sqrt(delta)) / (2 * a))
            solutions.append((-b - sqrt(delta)) / (2 * a))

        # print(solutions)

        return solutions

    def __find_x(self, arbre: BinaryTree, v: int = 1) -> list:
        """
        Find the unknown variable in the equation

        :param arbre: equation
        :param v: number of unknown variable
        :return: list of unknown variable
        """
        k = 1
        for i in arbre.iter_branches():
            if not i.is_leaf() and i.left.value == self.unknown or i.right.value == self.unknown:
                if k == v:
                    return i
                k += 1

    @staticmethod
    def __replace(arbre: BinaryTree, x, y):
        """
        Replace the value of the unknown variable by the value given (0)

        :param arbre: equation
        :param x: unknown variable
        :param y: value
        """
        for i in arbre.iter_branches():
            if i.value == x:
                i.value = y

    @staticmethod
    def __verif(left: BinaryTree, right: BinaryTree) -> bool:
        """
        Check if the equation is simple

        :param left: left side of the equation
        :param right: right side of the equation
        :return: basic verification
        """
        return not (left is None or right is None)


if __name__ == '__main__':
    """
    Unit test
    """
    from src.Trees.automaton import Automaton, infix_states
    from src.Trees.transformations import clean_list_to_infix, infix_list_to_tree

    auto = Automaton(infix_states)

    eq = Equation('x')

    assert eq.resolve(
        BinaryTree('+').set_branches(BinaryTree('+').set_branches('x', 'x'), BinaryTree('+').set_branches('x', 5)),
        BinaryTree('-').set_branches('x', BinaryTree('+').set_branches(5, 2))) == [-6.0], 'Error with - and +'
    print('(+ and -) test passed')

    assert eq.resolve(BinaryTree('+').set_branches(BinaryTree('*').set_branches(2, 'x'), 5),
                      BinaryTree('+').set_branches(BinaryTree('*').set_branches(4, 'x'), 3)) == [1.0], 'Error with *'
    print('* test passed')

    lis = auto.build("(2x)/4-4")
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    r = eq.resolve(tree, BinaryTree(0))

    assert r == [8.0], 'Error with x/n'  # n/x is not supported

    print('x/n test passed')

    lis = auto.build("x**2+x-2")
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    r = eq.resolve(tree, BinaryTree(0))

    assert r == [1, -2], 'Error with ax² + bx + c'

    assert eq.resolve(
        BinaryTree('-').set_branches(
            BinaryTree('*').set_branches(2, BinaryTree('**').set_branches('x', 2)),
            BinaryTree('-').set_branches("x", -6)
        ),
        BinaryTree(0)
    ) == [2.0,  -1.5], 'Error with ax² + bx + c'

    print('ax² + bx + c test passed')

    print('---------------------------------------------------------------')
    print('All tests passed')
