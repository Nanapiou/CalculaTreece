"""
The main entry
"""
import pygame
from src.Graphique.app import App

pygame.init()
screen = pygame.display.set_mode((425, 520))
gui_font = pygame.font.Font(None, 30)
app = App(screen)
app.run()
pygame.quit()
