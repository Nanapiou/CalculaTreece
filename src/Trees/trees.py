"""
Just trees
"""
from typing import List, Dict, Generator
from turtle import Turtle, done


class RootedTree:
    """
    Represent a rooted tree, is used as a "branch" too
    """

    def __init__(self, value: any):
        self.value = value
        try:
            self.branches: List[RootedTree] = list()
        except AttributeError:  # For derivation, imagine a getter...
            pass

    def __repr__(self):
        return str(self.deepdict())

    def __iter__(self):
        # Can be related to a postfix iteration
        yield self.value
        for br in self.branches:
            yield from br

    def iter_branches(self) -> Generator:
        """
        Iterate over the branches

        :return:
        """
        yield self
        for e in self.branches:
            yield e
            yield from e.iter_branches()

    def deepdict(self) -> Dict[str, Dict]:
        """
        Create a dict representing the tree, doesn't work for cyclic trees

        :return:
        """
        dic = dict()
        for e in self.branches:
            dic[e.value] = e.deepdict()
        return dic

    def add_branches(self, *branches):
        """
        Add some branches to the tree (which is a branch itself)

        :param branches: Branches too add (*args)
        :type branches: RootedTree
        :return: self
        """
        for e in branches:
            if isinstance(e, RootedTree):
                self.branches.append(e)
            else:
                self.branches.append(RootedTree(e))
        return self

    def get_branches_at_height(self, height: int):
        """
        Return a list containing each branches at the provided height

        :param height: The height. What else?
        :return: List[RootedTree]
        """
        if height == 1:
            return [self]
        branches: List[RootedTree] = list()
        for e in self.branches:
            branches += e.get_branches_at_height(height - 1)
        return branches

    def is_leaf(self) -> bool:
        """
        Return whether the tree/branch is alone at the top (/bottom, you know point of vue...) of the tree.

        :return:
        """
        return not self.branches

    @property
    def height(self) -> int:
        """
        Returns the height of the tree.

        :return: The height of the tree.
        """
        if self.is_leaf():
            return 1
        else:
            return 1 + max([child.height for child in self.branches])

    @property
    def size(self):
        """
        The size of the tree

        :return:
        """
        return sum(1 for _ in self.__iter__())

    def leafs_count(self):
        """
        The leaf count

        :return:
        """
        return sum(1 for e in self.__iter__() if e.is_leaf())

    # TODO Maybe use smt else than trtl
    def draw(self, trtl: Turtle, radius: int = 20) -> Turtle:
        """
        Draw the tree with the turtle module

        :param trtl: The turtle to use, required
        :param radius: The radius of each value
        :return: The turtle used
        """
        self._draw_getup(trtl, -radius)
        if hasattr(self.value, '__call__'):
            # It's a function, draw the name
            trtl.write(self.value.__name__, align='center', font=('', radius, ''))
        else:
            trtl.write(self.value, align='center', font=('', radius, ''))
        trtl.circle(radius)

        # A strange working, ik...
        largest = 0
        for i in range(1, self.height + 1):
            ln = len(self.get_branches_at_height(i))
            if ln > largest:
                largest = ln
        length = largest * 3 * radius - 2 * radius

        x, y = trtl.pos()
        branches_count = len(self.branches)
        height = 50
        if branches_count % 2 == 0:
            for i in range(branches_count // 2):
                trtl.goto(x - branches_count // 2 * length + i * length + length // 2, y - height)
                self.branches[i].draw(trtl)
                self._draw_getup(trtl, radius)
                trtl.goto(x, y)
            for j in range(branches_count // 2, branches_count):
                trtl.goto(x + (j - branches_count // 2 + 1) * length - length // 2, y - height)
                self.branches[j].draw(trtl)
                self._draw_getup(trtl, radius)
                trtl.goto(x, y)
        else:
            for i in range(branches_count // 2):
                trtl.goto(x - (branches_count // 2 + i) * length, y - height)
                self.branches[i].draw(trtl)
                self._draw_getup(trtl, radius)
                trtl.goto(x, y)
            # Mid one
            trtl.goto(x, y - height)
            self.branches[branches_count // 2].draw(trtl)
            trtl.goto(x, y)
            for j in range(branches_count // 2 + 1, branches_count):
                trtl.goto(x + (j - branches_count // 2) * length, y - height)
                self.branches[j].draw(trtl)
                self._draw_getup(trtl, radius)
                trtl.goto(x, y)
        return trtl

    @staticmethod
    def _draw_getup(trtl: Turtle, radius: int):
        """
        Just used in the draw method, so we can get upt easily without code duplication

        :param trtl:
        :param radius:
        :return:
        """
        trtl.penup()
        trtl.setheading(90)
        trtl.forward(radius * 2)
        trtl.setheading(0)
        trtl.pendown()


class BinaryTree(RootedTree):
    """
    Derivation of RootedTree.
    It's a RootedTree that can have from 0 to 2 subbranches per branches, not more.

    **branches** prop becomes a getter, so it becomes readonly
    """

    def __init__(self, value: any):
        super().__init__(value)

        # Only two pieces, you know 'binary' ?
        self.left = None
        self.right = None

    def __iter__(self):
        # Prevent None to break it all
        return self.prefix_iter()

    @property
    def branches(self):
        """
        **Read only**

        Branches of the tree, in a clean version

        :return:
        """
        return [e for e in (self.left, self.right) if e is not None]

    # Prefer set_branches
    def add_branches(self, b1, b2=None):
        """
        Add branches, considering the maximum of 2

        Raise an Exception if exceeded

        :param b1: The 1st branch to add
        :type b1: BinaryTree | any
        :param b2: The 2nd branch to add
        :type b2: BinaryTree | None | any
        :return: self
        """
        match len(self.branches):
            case 0:
                self.set_branches(b1, b2)
            case 1:
                if b2 is not None:
                    raise Exception('Too many branches')
                self.set_branches(self.left, b1)
            case 2:
                raise Exception('Too many branches')
        return self

    def set_branches(self, b1, b2=None):
        """
        Set the branches of the tree

        :param b1:
        :param b2:
        :return:
        """
        if not isinstance(b1, BinaryTree):
            b1 = BinaryTree(b1)
        if not isinstance(b2, BinaryTree) and b2 is not None:
            b2 = BinaryTree(b2)
        self.left, self.right = b1, b2
        return self

    def prefix_iter(self) -> Generator[any, None, None]:
        """
        A prefix iteration of the tree.
        See https://fr.wikipedia.org/wiki/Arbre_binaire#Parcours_pr%C3%A9fixe (sadly, french doc)

        :return:
        """
        yield self.value
        if self.left is not None:
            yield from self.left.prefix_iter()
        if self.right is not None:
            yield from self.right.prefix_iter()

    def postfix_iter(self) -> Generator[any, None, None]:
        """
        A postfix iteration of the tree.
        See https://fr.wikipedia.org/wiki/Arbre_binaire#Parcours_postfixe_ou_suffixe (sadly, french doc)

        :return:
        """
        if self.left is not None:
            yield from self.left.postfix_iter()
        if self.right is not None:
            yield from self.right.postfix_iter()
        yield self.value

    def infix_iter(self) -> Generator[any, None, None]:
        """
        An infix iteration of the tree.
        See https://fr.wikipedia.org/wiki/Arbre_binaire#Parcours_infixe (sadly, french doc)

        :return:
        """
        if self.left is not None:
            yield from self.left.infix_iter()
        yield self.value
        if self.right is not None:
            yield from self.right.infix_iter()

    # TODO Use another algorithm (lighter)
    def width_iter(self) -> Generator[any, None, None]:
        """
        A width iteration of the tree (height by height)
        See https://fr.wikipedia.org/wiki/Arbre_binaire#Parcours_en_largeur (sadly, french doc)

        :return:
        """
        for i in range(1, self.height + 1):
            yield from (br.value for br in self.get_branches_at_height(i))


if __name__ == '__main__':
    branch = BinaryTree('*').set_branches(BinaryTree('-').set_branches(12, 2), BinaryTree('/').set_branches(30, 3))
    b = branch
    print(branch == b, b is branch)
    # t = Turtle()
    #     # t.penup()
    #     # t.goto(0, 350)
    #     # branch.draw(t)
    #     # done()
