import pygame, sys
from PIL import Image

pygame.init()
width, height = 1440, 1024
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

#Icon & Name's bar
pygame.display.set_caption("KITCATS")
icons = pygame.image.load("./assets/menu/geometry.png")
pygame.display.set_icon(icons)

#Game menu element image
background = pygame.image.load("./assets/menu/cat-background (2).png") #Menu's background image
gamename = pygame.image.load("./assets/menu/name.png") #Game's name image
start_button = pygame.image.load("./assets/menu/start.png") #Start button
quit_button = pygame.image.load("./assets/menu/quit.png") #Quit button

#start & quit button size
start_button = pygame.transform.scale(start_button, (200, 70))
quit_button = pygame.transform.scale(quit_button, (200, 70))

#Adjust background image
def update_background(size):
    return pygame.transform.scale(background, size)

#Adjust game's name image
def game_name(size):
    return pygame.transform.scale(gamename, size)

#Other button
close_tab = pygame.image.load("./assets/yes no btn/x.png")
def closed(size):
    return pygame.transform.scale(close_tab, size)

close_tab = closed((width*0.04, height*0.06))
close_tab_pos = (width // (height-(height*9.5)) + close_tab.get_width() // width, height // height**0.8)

#Check button click
def check_button_click(image, x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = image.get_rect(topleft=(x, y))

    if rect.collidepoint(mouse):
        if click[0] == 1:
            return True
    return False

#Clock for FPS control
clock = pygame.time.Clock()

current_screen = "menu"

#Main Game Loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        background = update_background((width, height))
        screen.blit(background, (0,0))

        #Game menu screen's element
        gamename_pos = (width // 2 - gamename.get_width() // 2, height // 8)
        gamename = game_name((width*0.63, height*0.26))
        start_button_pos = (width // 2 - start_button.get_width() // 2, height // 2 - 50)
        quit_button_pos = (width // 2 - quit_button.get_width() // 2, height // 2 + 40)

        #Game's name image
        screen.blit(gamename, gamename_pos)

        if current_screen == "menu":
            #Start button
            screen.blit(start_button, start_button_pos)
            if check_button_click(start_button, *start_button_pos):
                current_screen = "level"

            #Quit button
            screen.blit(quit_button, quit_button_pos)
            if check_button_click(quit_button, *quit_button_pos):
                current_screen = "confirm"

        #Quit comfirm window
        elif current_screen == "confirm":
            screen.fill((0,0,0))
            confirm_page = pygame.image.load("./assets/menu/confirm.png")

            #Adjust confirm window
            def confirm_quit(size):
                return pygame.transform.scale(confirm_page, size)

            #confirm window
            confirm_page = confirm_quit((600, 450))
            confirm_rect = confirm_page.get_rect(center=(width // 2, height // 2))
            screen.blit(confirm_page, confirm_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png") #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - confirm_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png") #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - confirm_page.get_width() // 3.6, height // height + (height*0.52))
            screen.blit(yes_confirm, yes_confirm_pos)
            screen.blit(not_confirm, not_confirm_pos)

            #Click confirm button
            if check_button_click(yes_confirm, *yes_confirm_pos):
                pygame.quit()
                sys.exit()

            #Click back to menu
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = "menu"

        #Select level window
        elif current_screen == "level":
            screen.fill((0,0,0))
            levelground = pygame.image.load("./assets/cat-backgound resource/cat-background (9).png")

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(levelground, size)

            levelground = update_background((width, height))
            screen.blit(levelground, (0,0))

            select_level = pygame.image.load("./assets/select_level/select text.png")
            
            #Adjust select level text image
            def level_selected(size):
                return pygame.transform.scale(select_level, size)

            select_level_pos = (width // 2 - gamename.get_width() // 2.5, height // height + (height*0.05))
            select_level = level_selected((width*0.5, height*0.2))
            screen.blit(select_level, select_level_pos)

            #child play button
            level_child = pygame.image.load("./assets/select_level/click child.png")
            level_child= pygame.transform.scale(level_child, (170, 220))
            level_child_pos = (width // 15 - levelground.get_width() // 50, height // height + (height*0.3))

            #easy mode button
            level_easy = pygame.image.load("./assets/select_level/click easy.png")
            level_easy= pygame.transform.scale(level_easy, (170, 220))
            level_easy_pos = (width // 3.4 - levelground.get_width() // 300, height // height + (height*0.3))

            #medium mode button
            level_medium = pygame.image.load("./assets/select_level/click medium.png")
            level_medium= pygame.transform.scale(level_medium, (170, 220))
            level_medium_pos = (width // 1.87 - levelground.get_width() // 550, height // height + (height*0.3))

            #hard mode button
            level_hard = pygame.image.load("./assets/select_level/click hard.png")
            level_hard= pygame.transform.scale(level_hard, (170, 220))
            level_hard_pos = (width // 1.3 - levelground.get_width() // 700, height // height + (height*0.3))

            #level selected button
            screen.blit(level_child, level_child_pos)
            screen.blit(level_easy, level_easy_pos)
            screen.blit(level_medium, level_medium_pos)
            screen.blit(level_hard, level_hard_pos)
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "back menu"

            #Click select child play mode
            if check_button_click(level_child, *level_child_pos):
                current_screen = "child play"

            #Click select easy mode
            if check_button_click(level_easy, *level_easy_pos):
                current_screen = "easy mode"

            #Chick select medium mode
            if check_button_click(level_medium, *level_medium_pos):
                current_screen = "medium mode"

            #Click select hard mode
            if check_button_click(level_hard, *level_hard_pos):
                current_screen = "hard mode"

        elif current_screen == "back menu":
            screen.fill((0,0,0))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png")

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png") #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png") #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - quit_level_page.get_width() // 3.6, height // height + (height*0.52))

            #Click confirm button
            screen.blit(yes_confirm, yes_confirm_pos)
            if check_button_click(yes_confirm, *yes_confirm_pos):
                current_screen = "menu"

            screen.blit(not_confirm, not_confirm_pos)
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = "level"

        #Child play mode window
        elif current_screen == "child play":
            screen.fill((0,0,0))
            childground = pygame.image.load("./assets/child play/Child Play.jpg")

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(childground, size)

            childground = update_background((width, height))
            screen.blit(childground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "child play"

        #Easy mode window
        elif current_screen == "easy mode":
            screen.fill((0,0,0))
            easyground = pygame.image.load("./assets/easy mode/Easy.gif")

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(easyground, size)

            easyground = update_background((width, height))
            screen.blit(easyground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "easy mode"

        #Medium mode window
        elif current_screen == "medium mode":
            screen.fill((0,0,0))
            mediumground = pygame.image.load("./assets/medium mode/Medium.jpg")

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(mediumground, size)

            mediumground = update_background((width, height))
            screen.blit(mediumground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "medium mode"

        #Hard mode window
        elif current_screen == "hard mode":
            screen.fill((0,0,0))
            hardground = pygame.image.load("./assets/hard mode/Hard.jpg")

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(hardground, size)

            hardground = update_background((width, height))
            screen.blit(hardground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "hard mode"

        elif current_screen == "quit level":
            screen.fill((0,0,0))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png")

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png") #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png") #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - quit_level_page.get_width() // 3.6, height // height + (height*0.52))

            #Click confirm button
            screen.blit(yes_confirm, yes_confirm_pos)
            if check_button_click(yes_confirm, *yes_confirm_pos):
                current_screen = "level"

            #Click back to menu
            screen.blit(not_confirm, not_confirm_pos)
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = period_screen

        pygame.display.flip()
        clock.tick(60) #FPS fixed
