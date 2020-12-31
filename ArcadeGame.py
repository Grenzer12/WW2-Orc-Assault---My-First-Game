import pygame

pygame.init()
wn = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

running = True
while running:
    for every_event in pygame.event.get():
        if every_event.type == pygame.QUIT:
            running = False
    pygame.display.update()
