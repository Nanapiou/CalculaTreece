import sys, pygame
import automaton, calculator, trees, transformations

pygame.init()


class Calculator:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def text_test(self, text, font, color, x, y):
        text = font.render(text, True, color)
        self.window.blit(text, (x, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.window.fill((255, 255, 255))
            pygame.display.update()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    calc = Calculator(800, 600, 'Calculator')
    calc.run()
    calc.text_test('Hello World', pygame.font.SysFont('Arial', 20), (0, 0, 0), 0, 0)

