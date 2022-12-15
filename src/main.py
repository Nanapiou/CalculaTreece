"""
The main entry
"""
import pygame
from src.app import App

pygame.init()
screen = pygame.display.set_mode((800, 600))
app = App(screen)
app.run()
pygame.quit()
