"""
The main entry
"""
import pygame
from src.Graphique.app import App

# Window size
WIDTH = 425
HEIGHT = 520

# Init pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define the font
gui_font = pygame.font.Font(None, 30)

# Create the app
app = App(screen)
app.run()

# Quit pygame
pygame.quit()
