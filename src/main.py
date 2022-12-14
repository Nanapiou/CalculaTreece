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


fenetre = Calculator(800, 600, "CalculaTreece")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
