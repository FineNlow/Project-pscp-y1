import pygame, sys
from PIL import Image

#game screen .. 100%
pygame.init()
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))

#icon & name's bar ... 100%
pygame.display.set_caption("KITCATS")
icons = pygame.image.load("./assets/menu/cat-logo.png").convert_alpha()
pygame.display.set_icon(icons)

#Game menu element image ... 99%
background = screen.fill((226, 179, 209))
gamename = pygame.image.load("./assets/menu/name.png").convert_alpha() #Game's name image

setting_button = pygame.image.load("./assets/setting/setting.png").convert_alpha()
start_button = pygame.image.load("./assets/menu/start.png").convert_alpha() #Start button
quit_button = pygame.image.load("./assets/menu/quit.png").convert_alpha() #Quit button

close_tab = pygame.image.load("./assets/yes no btn/x.png").convert_alpha()
close_tab = pygame.transform.scale(close_tab, (45,45))
close_tab_pos = (width // (height-(height*9.5)) + close_tab.get_width() // width, height // height**0.8)

mute_set = pygame.image.load("./assets/setting/mute.png").convert_alpha()
mute_set = pygame.transform.scale(mute_set, (100, 100))
nosound, nosong = True, True

#convert gif to show frame by frame ... 20%
def gifgen(gif_path, scale_factor):
    im = Image.open(gif_path)
    frames = []
    
    while True:
        frame = im.copy().convert("RGBA")
        frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
        # Scale the frame
        frame = pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
        frames.append(frame)

        try:
            im.seek(len(frames))  # Move to the next frame
        except EOFError:
            break

    return frames

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
frame_index = 0
frame_duration = 100

frame_timer = 0
frame_delay = 100

current_screen = "menu"

#Main Game Loop
running = True
while running:
    screen.fill((226, 179, 209))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        screen.fill((226, 179, 209))

        #Game menu ... 40% (add gif)
        if current_screen == "menu":
            scale_factor = 2
            frames = gifgen('./assets/menu/background.gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                screen.blit(frame,  (0,0))

            #Game menu screen's element
            gamename_pos = (width // 2.8 - gamename.get_width() // 2, height // 20)
            gamename = pygame.transform.scale(gamename, (690, 195))
            start_button_pos = (width // 5 - start_button.get_width() // 3, height // 2 - height/15)
            start_button = pygame.transform.scale(start_button, (255, 115))
            quit_button_pos = (width // 5 - quit_button.get_width() // 3, height // 2 + height/8)
            quit_button = pygame.transform.scale(quit_button, (255, 115))

            #Game's name image
            screen.blit(gamename, gamename_pos)

            scale_factor = height/500 + 2
            frames = gifgen('./assets/menu/cat-gif-menu.gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                screen.blit(frame, (width*0.4 - 200,height - 490))

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
            screen.fill((226, 179, 209))
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
            screen.fill((226, 179, 209))

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (width // 50 - width // 400, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)
    
            select_level = pygame.image.load("./assets/select_level/select text.png").convert_alpha()
            
            #Adjust select level text image
            def level_selected(size):
                return pygame.transform.scale(select_level, size)

            select_level = level_selected((width*0.6, height*0.15))
            select_level_pos = (50, height // height + (height*0.07))
            screen.blit(select_level, select_level_pos)

            #easy mode button
            level_easy = pygame.image.load("./assets/select_level/click easy.png").convert_alpha()
            level_easy= pygame.transform.scale(level_easy, (350, 400))
            level_easy_pos = (50, height // height + (height*0.25))

            #normal mode button
            level_normal = pygame.image.load("./assets/select_level/click normal.png").convert_alpha()
            level_normal= pygame.transform.scale(level_normal, (170, 220))
            level_normal_pos = (width // 1.87 - width // 550, height // height + (height*0.3))

            #hard mode button
            level_hard = pygame.image.load("./assets/select_level/click hard.png").convert_alpha()
            level_hard= pygame.transform.scale(level_hard, (170, 220))
            level_hard_pos = (width // 1.3 - width // 700, height // height + (height*0.3))

            #level selected button
            screen.blit(level_easy, level_easy_pos)
            screen.blit(level_normal, level_normal_pos)
            screen.blit(level_hard, level_hard_pos)


            if check_button_click(back_button, *back_button_pos):
                current_screen = "menu"

            #Click select easy mode
            if check_button_click(level_easy, *level_easy_pos):
                current_screen = "easy mode"

            #Chick select medium mode
            if check_button_click(level_normal, *level_normal_pos):
                current_screen = "normal mode"

            #Click select hard mode
            if check_button_click(level_hard, *level_hard_pos):
                current_screen = "hard mode"

        elif current_screen == "back menu":
            screen.fill((226, 179, 209))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png").convert_alpha()

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png").convert_alpha() #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png").convert_alpha() #back to menu
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
            screen.fill((226, 179, 209))
            childground = pygame.image.load("./assets/child play/Child Play.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(childground, size)

            childground = update_background((width, height))
            screen.blit(childground, (0,0))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "quit level"
                period_screen = "child play"

        #Easy mode window
        elif current_screen == "easy mode":
            screen.fill((226, 179, 209))
            easyground = pygame.image.load("./assets/easy mode/Easy.gif").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(easyground, size)

            easyground = update_background((width, height))
            screen.blit(easyground, (0,0))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "quit level"
                period_screen = "easy mode"

        #Medium mode window
        elif current_screen == "normal mode":
            screen.fill((226, 179, 209))
            normalground = pygame.image.load("./assets/normal mode/normal.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(normalground, size)

            normalground = update_background((width, height))
            screen.blit(normalground, (0,0))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "quit level"
                period_screen = "normal mode"

        #Hard mode window
        elif current_screen == "hard mode":
            screen.fill((226, 179, 209))
            hardground = pygame.image.load("./assets/hard mode/Hard.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(hardground, size)

            hardground = update_background((width, height))
            screen.blit(hardground, (0,0))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, back_button_pos):
                current_screen = "quit level"
                period_screen = "hard mode"

        elif current_screen == "quit level":
            screen.fill((226, 179, 209))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png").convert_alpha()

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png").convert_alpha() #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png").convert_alpha() #back to menu
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
