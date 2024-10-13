import pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

background = pygame.image.load("Menu.jpg")

def update_background(size):
    return pygame.transform.scale(background, size)

pygame.display.set_caption("KITCATS")
icons = pygame.image.load("geometry.png")
pygame.display.set_icon(icons)

running = True
while running:
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        background = update_background((width, height))

    # player()
    pygame.display.update()
