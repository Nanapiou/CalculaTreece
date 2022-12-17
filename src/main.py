"""
The main entry
"""
import pygame
from src.app import App

pygame.init()
screen = pygame.display.set_mode((415, 515))
gui_font = pygame.font.Font(None, 30)
app = App(screen)
app.run()
pygame.quit()
