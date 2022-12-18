"""
The main entry
"""
import pygame
from src.Graphique.app import App

pygame.init()

# Window size
WIDTH = 410
HEIGHT = 610

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Define the font
gui_font = pygame.font.Font(None, 30)

# Create the app
app = App(screen)
app.run()  # Launch a loop

# Quit pygame
pygame.quit()
