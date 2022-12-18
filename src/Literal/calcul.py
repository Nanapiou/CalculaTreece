import sympy as sp
sp.init_printing(use_latex=True)


class equation:

    def __init__(self, equation):
        self.equation = equation
        self.x = sp.symbols(['x'])


    def __str__(self):
        return f'{self.x[0]} = {self.solution[0]}'

    def solution(self):
        self.expr = sp.parse_expr(self.equation)
        self.solution = sp.solve(self.expr, self.x)
        return self.solution


if __name__ == '__main__':
    equation1 = equation('2*(x+1) +2')
    print(equation1.solution())
    print(equation1)



