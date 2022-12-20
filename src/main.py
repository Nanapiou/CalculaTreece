"""
The main entry
"""
import pygame
from src.Graphique.app import App

pygame.init()

# Window size
WIDTH = 450
HEIGHT = 670

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Create the app
app = App(screen)
app.run()  # Launch a loop

# Quit pygame
pygame.quit()
