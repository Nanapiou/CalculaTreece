"""
The main entry
"""
import pygame
from src.Graphique.app import App

pygame.init()

# Window size
WIDTH = 425
HEIGHT = 520

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define the font
gui_font = pygame.font.Font(None, 30)

# Create the app
app = App(screen)
app.run()

# Quit pygame
pygame.quit()
