""""
prototype of equation calculation with the module sympy
"""

import sympy as sp

sp.init_printing(use_latex=True)


class Equation:
    """
    Classe permettant de résoudre une équation donnée sous forme de chaîne de caractères.
    """

    def __init__(self, equation: str):
        """
        Initialise l'équation à résoudre et la variable symbolique 'x' comme inconnue.

        Params:
        equation (str): L'équation à résoudre, sous forme de chaîne de caractères.
        """
        self.equation = equation
        self.x = sp.Symbol('x')

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne de caractères de l'équation et de la variable symbolique 'x'.
        """
        return f'{self.equation} , {self.x}'

    def __modify(self) -> str:
        """
        Modifie l'équation en retranchant la seconde partie de la première.

        Returns:
        str: L'équation modifiée, sous forme de chaîne de caractères.
        """
        array = self.equation.split('=')

        if len(array) != 2:
            raise SyntaxError('Invalid equation')

        part1, part2 = array[0], array[1]
        part1 = part1 + '-(' + part2 + ')'

        return part1.strip()

    def solution(self) -> list:
        """
        Résout l'équation en utilisant la fonction 'solve' de la bibliothèque 'sp'.

        Returns:
        list: La solution de l'équation, sous forme de liste.
        """
        equation = self.__modify()

        return sp.solve(equation, self.x)


if __name__ == '__main__':
    equation1 = Equation('2*(x+1) +2 = 2')
    print(equation1)
    print(equation1.solution())
