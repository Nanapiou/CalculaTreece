import pygame
from app import App


screen = pygame.display.set_mode((800, 600))
app = App(screen)
app.run()
pygame.quit()
