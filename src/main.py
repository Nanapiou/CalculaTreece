"""
The main entry
"""
import pygame
from src.app import App

pygame.init()
screen = pygame.display.set_mode((400, 500))
app = App(screen)
app.run()
pygame.quit()
