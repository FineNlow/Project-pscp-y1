import pygame, sys
from PIL import Image
import time, random
import os

#game screen .. 100%
pygame.init()
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))

# Initialize pygame with pre_init to reduce sound delay
pygame.mixer.pre_init(44100, -16, 2, 512)  # Adjust buffer size if needed
#click sound
click_sound = pygame.mixer.Sound("./assets/sounds/click.wav")
click_sound.set_volume(0.2)

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

pause_button = pygame.image.load("./assets/setting/setting (1).png").convert_alpha()

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
last_click_time = 0
click_delay = 0.25

def check_button_click(image, x, y):
    global last_click_time
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = image.get_rect(topleft=(x, y))

    if rect.collidepoint(mouse):
        current_time = time.time()
        if click[0] == 1 and (current_time - last_click_time) > click_delay:
            last_click_time = current_time
            return True
    return False

pygame.mixer.init()
# Load the music file
pygame.mixer.music.load("./assets/music/music.mp3") 
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

mute_set = pygame.image.load("./assets/setting/mute.png").convert_alpha()
mute_set = pygame.transform.scale(mute_set, (100, 100))
nosound, nosong = True, True
mute_icon_displayed = False

#Clock for FPS control
clock = pygame.time.Clock()
frame_index = 0
frame_duration = 100

frame_timer = 0
frame_delay = 100
scale_factor = height/500 + 2

# Load your cursor image
cursor_image = pygame.image.load("./assets/menu/cat-cursor.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (40, 35))
cursor_width, cursor_height = cursor_image.get_size()
cursor = pygame.cursors.Cursor((cursor_width // 2, cursor_height // 2), cursor_image)
pygame.mouse.set_cursor(cursor)

custom_font1 = pygame.font.Font("./assets/font/PixelifySans-Medium.ttf", 27)
custom_font2 = pygame.font.Font("./assets/font/PixelifySans-Medium.ttf", 22)
custom_font3 = pygame.font.Font("./assets/font/PixelifySans-Medium.ttf", 18)
custom_font4 = pygame.font.Font("./assets/font/PixelifySans-Medium.ttf", 16)

current_screen = "menu"
#Main Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Play click sound on any mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            
    screen.fill((226, 179, 209))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        screen.fill((226, 179, 209))

    #Game menu ... 60% (add backgound gif)
    if current_screen == "menu":
        levelground = pygame.image.load("./assets/menu/cat-background.png")
        levelground = pygame.transform.scale(levelground,(width, height))
        screen.blit(levelground, (0,0))

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
            period_screen = "menu"
            current_screen = "confirm"

        #Setting button
        setting_button = pygame.transform.scale(setting_button, (41,38))
        setting_button_pos = (width - width*0.0625, height - height*0.96)

        screen.blit(setting_button,setting_button_pos)
        if check_button_click(setting_button, *setting_button_pos):
            current_screen = "setting menu"

    #Quit comfirm window
    elif current_screen == "confirm":
        screen.fill((226, 179, 209))
        quit_page = pygame.image.load("./assets/quit/quit level.png")

        #confirm window
        quit_page = pygame.transform.scale(quit_page, (600, 350))
        quit_page_rect = quit_page.get_rect(center=(width // 2, height // 2))
        screen.blit(quit_page, quit_page_rect)

        #Confirm button
        yes_confirm = pygame.image.load("./assets/quit/yesconfirm.png") #confirm button
        yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
        yes_confirm_pos = (300 , height // height + (height*0.55))
        not_confirm = pygame.image.load("./assets/quit/noconfirm.png") #back to menu
        not_confirm = pygame.transform.scale(not_confirm, (150, 75))
        not_confirm_pos = (560, height // height + (height*0.55))
        screen.blit(yes_confirm, yes_confirm_pos)
        screen.blit(not_confirm, not_confirm_pos)

        #Click confirm button
        if check_button_click(yes_confirm, *yes_confirm_pos):
            if period_screen == "pause":
                current_screen = "menu"
            else:
                pygame.quit()
                sys.exit()

        #Click back to menu
        if check_button_click(not_confirm, *not_confirm_pos):
            current_screen = period_screen

    #setting menu ...65% (elementครบ เหลือmute sound & song, หน้า tutorial & credits)
    if current_screen == "setting menu":
        screen.fill((226, 179, 209))
        setting_menu_tab = pygame.image.load("./assets/setting/settingtab.png").convert_alpha()

        setting_menu_tab = pygame.transform.scale(setting_menu_tab, (717, 538))
        settab_rect = setting_menu_tab.get_rect(center=(width // 2, height // 2))
        screen.blit(setting_menu_tab, settab_rect)

        scale_factor = height/500
        frames = gifgen('./assets/menu/cat-gif (1).gif', scale_factor)

        if frames:
            frame_timer += clock.get_time()
            if frame_timer >= frame_delay:
                frame_index = (frame_index + 1) % len(frames)
                frame_timer = 0

            frame = frames[frame_index]
            frame_rect = setting_menu_tab.get_rect(center=(width + (width//10), height // 2.2))
            screen.blit(frame, frame_rect)

        # Button in setting tab for mute/unmute sound
        speaker_button = pygame.image.load("./assets/setting/speaker.png").convert_alpha()
        speaker_button = pygame.transform.scale(speaker_button, (100, 100))
        speaker_button_pos = ((width // 2.2 - setting_menu_tab.get_width() // 400) - height//4, height // height + (height*0.36))
        screen.blit(speaker_button, speaker_button_pos)

        # Button in setting tab for mute/unmute music
        song_button = pygame.image.load("./assets/setting/song.png").convert_alpha()
        song_button = pygame.transform.scale(song_button, (100, 100))
        song_button_pos = (width // 2.2 - setting_menu_tab.get_width() // 400, height // height + (height*0.36))
        screen.blit(song_button, song_button_pos)

        howto_button = pygame.image.load("./assets/setting/How to.png").convert_alpha()
        howto_button = pygame.transform.scale(howto_button, (100, 100))
        howto_button_pos = ((width // 2.2 - setting_menu_tab.get_width() // 400) + height//4, height // height + (height*0.36))
        screen.blit(howto_button, howto_button_pos)

        back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
        back_button = pygame.transform.scale(back_button, (40, 30))
        back_button_pos = (20, height // height + (height*0.03))
        screen.blit(back_button, back_button_pos)

        credits_button = pygame.image.load("./assets/setting/credits.png").convert_alpha()
        credits_button = pygame.transform.scale(credits_button, (300, 85))
        credits_button_pos = (width // 2 - setting_menu_tab.get_width() // 400) - height//4.5, height // height + (height*0.6)
        screen.blit(credits_button, credits_button_pos)

        if check_button_click(speaker_button, *speaker_button_pos):
            nosound = not nosound
            # print("Sound Activated") > Sound always activated

        if not nosound:
            screen.blit(mute_set, speaker_button_pos)
            # mute in-game sound

        if check_button_click(song_button, *song_button_pos):
            nosong = not nosong
            # print("Music On") > Music always on

        if not nosong:
            pygame.mixer.music.pause() # Stop the music if muted
            screen.blit(mute_set, song_button_pos)
        else:
            pygame.mixer.music.unpause()

        if check_button_click(howto_button, *howto_button_pos):
            period_screen = "setting menu"
            current_screen = "How to play"

        if check_button_click(back_button, *back_button_pos):
            current_screen = "menu"
            scale_factor = height/500 + 2

        if check_button_click(credits_button, *credits_button_pos):
            period_screen = "setting menu"
            current_screen = "credits"

        # Load the "How to play" image
        how_to_play_image = pygame.image.load("./assets/howtoplay/HOWTOPLAY.png").convert_alpha()  # Adjust the path as needed

        # Scale the "How to play" image
        def scale_how_to_play_image(size):
            return pygame.transform.scale(how_to_play_image, size)

    #Tutorial ...10% (สอนวิธีเล่น)
    elif current_screen == "How to play":
        screen.fill((226, 179, 209))

        # Scale and display the "How to play" image
        scaled_how_to_play_image = scale_how_to_play_image((width * 0.8, height * 0.8))  # Adjust size as needed
        how_to_play_rect = scaled_how_to_play_image.get_rect(center=(width // 2, height // 2))
        screen.blit(scaled_how_to_play_image, how_to_play_rect)

        # Add the back button
        back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
        back_button = pygame.transform.scale(back_button, (40, 30))
        back_button_pos = (20, height // height + (height*0.03))
        screen.blit(back_button, back_button_pos)

        if check_button_click(back_button, *back_button_pos):
            current_screen = period_screen

    #Credits ...10% (ใส่เครดิต)
    elif current_screen == "credits":
        screen.fill((226, 179, 209))

        # Load credits image or create a credits text
        credits_image = pygame.image.load("./assets/credits/creditsname.png").convert_alpha()  # Load your credits image
        credits_image = pygame.transform.scale(credits_image, (width * 1, height * 1))  # Scale if necessary
        credits_rect = credits_image.get_rect(center=(width // 2, height // 2))
        screen.blit(credits_image, credits_rect)

        back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
        back_button = pygame.transform.scale(back_button, (40, 30))
        back_button_pos = (20, height // height + (height*0.03))
        screen.blit(back_button, back_button_pos)

        if check_button_click(back_button, *back_button_pos):
            current_screen = period_screen

    #Select level window
    elif current_screen == "level":
        screen.fill((226, 179, 209))
        levelground = pygame.image.load("./assets/menu/cat-background.png")
        levelground = pygame.transform.scale(levelground,(width, height))
        screen.blit(levelground, (0,0))

        scale_factor = height/500 + 2
        frames = gifgen('./assets/menu/cat-gif-menu.gif', scale_factor)

        if frames:
            frame_timer += clock.get_time()  # 
            if frame_timer >= frame_delay:
                frame_index = (frame_index + 1) % len(frames)
                frame_timer = 0

            frame = frames[frame_index]
            screen.blit(frame, (width*0.4 - 200,height - 490))

        back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
        back_button = pygame.transform.scale(back_button, (40, 30))
        back_button_pos = (20, height // height + (height*0.03))
        screen.blit(back_button, back_button_pos)

        select_level = pygame.image.load("./assets/select_level/select text.png").convert_alpha()
        select_level = pygame.transform.scale(select_level, (615, 115))
        select_level_pos = (50, height // height + (height*0.07))
        screen.blit(select_level, select_level_pos)

        #easy mode button
        level_easy = pygame.image.load("./assets/select_level/click easy.png").convert_alpha()
        level_easy= pygame.transform.scale(level_easy, (350, 400))
        level_easy_pos = (50, height // height + (height*0.25))

        #normal mode button
        level_normal = pygame.image.load("./assets/select_level/click normal.png").convert_alpha()
        level_normal= pygame.transform.scale(level_normal, (350, 400))
        level_normal_pos = (350, height // height + (height*0.25))

        #hard mode button
        level_hard = pygame.image.load("./assets/select_level/click hard.png").convert_alpha()
        level_hard= pygame.transform.scale(level_hard, (350, 400))
        level_hard_pos = (650, height // height + (height*0.25))

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

    #Easy mode window
    elif current_screen == "easy mode":
        def load_game_assets():
            assets = {}
            assets['background'] = pygame.image.load("./assets/easy mode/easywallpaper.png").convert_alpha()
            assets['question_back'] = pygame.image.load("./assets/easy mode/ansback.png").convert_alpha()
            assets['question_white'] = pygame.image.load("./assets/easy mode/ansbackwhite.png").convert_alpha()
            assets['wall'] = pygame.image.load("./assets/easy mode/wall.png").convert_alpha()
            assets['ansback'] = pygame.image.load("./assets/easy mode/answall.png").convert_alpha()
            assets['score_back'] = pygame.image.load("./assets/easy mode/score-background.png").convert_alpha()
            assets['problem_back'] = pygame.image.load("./assets/easy mode/Ploblem rec.png").convert_alpha()
            assets['problem_quiz'] = pygame.image.load("./assets/easy mode/Ploblem quiz.png").convert_alpha()
            assets['time_count'] = pygame.image.load("./assets/easy mode/time_count.png").convert_alpha()
            assets['ans1_back'] = pygame.image.load("./assets/easy mode/ans1_red.png").convert_alpha()
            assets['ans2_back'] = pygame.image.load("./assets/easy mode/ans2_blue.png").convert_alpha()
            assets['ans3_back'] = pygame.image.load("./assets/easy mode/ans3_yellow.png").convert_alpha()
            assets['ans4_back'] = pygame.image.load("./assets/easy mode/ans4_green.png").convert_alpha()
            assets['cat'] = pygame.image.load("./assets/easy mode/cat.png").convert_alpha()
            
            # Scale images
            assets['background'] = pygame.transform.scale(assets['background'], (width, height))
            assets['question_back'] = pygame.transform.scale(assets['question_back'], (618, 638))
            assets['question_white'] = pygame.transform.scale(assets['question_white'], (589, 606))
            assets['wall'] = pygame.transform.scale(assets['wall'], (39, 534))
            assets['ansback'] = pygame.transform.scale(assets['ansback'], (302.22, 638.25))
            assets['score_back'] = pygame.transform.scale(assets['score_back'], (256, 75.75))
            assets['problem_back'] = pygame.transform.scale(assets['problem_back'], (256.71, 168))
            assets['problem_quiz'] = pygame.transform.scale(assets['problem_quiz'], (231.82, 112.5))
            assets['time_count'] = pygame.transform.scale(assets['time_count'], (34, 33))
            assets['ans1_back'] = pygame.transform.scale(assets['ans1_back'], (244.62, 46.5))
            assets['ans2_back'] = pygame.transform.scale(assets['ans2_back'], (244.62, 46.5))
            assets['ans3_back'] = pygame.transform.scale(assets['ans3_back'], (244.62, 46.5))
            assets['ans4_back'] = pygame.transform.scale(assets['ans4_back'], (244.62, 46.5))
            assets['cat'] = pygame.transform.scale(assets['cat'], (22, 20))
            
            return assets

        #game state
        yay_screen = False
        # Game variables
        remains_target = 5
        problem_limit = 10
        default_timer = 30
        game_timer = default_timer
        start_time = time.time()
        problems = []
        current_problem = None
        remains_done = 0
        problem_count = 0
        DARK_GRAY = (20, 20, 20)
        GREEN = (0, 255, 0)
        class Problem:
            def __init__(self, number, x, y):
                self.number = number
                self.x = x
                self.y = y
                self.question, self.answer = self.generate_question()
                self.choices = self.generate_choices()
                self.timer = default_timer
                self.start_time = time.time()
                self.is_expired = False

            def generate_question(self):
                num1 = random.randint(1, 250)
                num2 = random.randint(1, 250)
                op = random.choice(['+', '-'])
                if op == '+':
                    answer = num1 + num2
                else:
                    answer = num1 - num2
                return f"{num1} {op} {num2}", answer

            def generate_choices(self):
                choices = [self.answer]
                while len(choices) < 4:
                    wrong = self.answer + random.randint(-5, 5)
                    if wrong not in choices and wrong != self.answer:
                        choices.append(wrong)
                random.shuffle(choices)
                return choices

        def reset_game_timer():
            global game_timer, start_time
            game_timer = default_timer  # รีเซ็ตเวลาให้เป็นค่าเริ่มต้น
            start_time = time.time()    # อัปเดตเวลาเริ่มต้นใหม่

        def reduce_game_timer():
            global game_timer, start_time
            remaining_time = get_remaining_game_time()
            game_timer = remaining_time * 0.91  # ลดเวลาที่เหลือโดยคูณด้วย 0.91
            start_time = time.time()            # อัปเดตเวลาเริ่มต้นใหม่

        def get_remaining_game_time():
            # คำนวณเวลา
            elapsed = time.time() - start_time
            return max(0, int(game_timer - elapsed))

        def add_problem():
            if problem_count < problem_limit:
                # Generate random position within the white question area
                margin = 100
                x = random.randint(100, 550 - margin)
                y = random.randint(100, 600 - margin)
                problem = Problem(len(problems) + 1, x, y)
                problems.append(problem)
                reset_game_timer()

        def draw_problem_box(surface, problem):
            # Draw problem boxes in the question area
            box_width = 250
            box_height = 100
            box_x = problem.x
            box_y = problem.y

            problem_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

            # Draw main box
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, box_height), 2)
            
            # Draw problem header
            header_height = 25
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, header_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, header_height), 2)

            # Draw problem text
            problem_text = custom_font4.render(f"PROBLEM: {problem.number}", True, (224, 165, 56))
            text_rect = problem_text.get_rect(topright=(box_width - 5, 5))
            problem_surface.blit(problem_text, text_rect)

            # Draw problems
            timer_text = custom_font2.render(str(problem.question), True, (0, 255, 0))
            timer_rect = timer_text.get_rect(center=(box_width//2, box_height//2))
            problem_surface.blit(timer_text, timer_rect)

            surface.blit(problem_surface, (box_x, box_y))

        def draw_game_screen(assets):
            # Draw background and UI elements
            screen.blit(assets['background'], (0, 0))
            screen.blit(assets['wall'], (649, 114))
            screen.blit(assets['ansback'], (686.22, 56.25))
            screen.blit(assets['question_back'], (36, 56))
            screen.blit(assets['question_white'], (50, 70))
            screen.blit(assets['score_back'], (709.69, 77.25))
            screen.blit(assets['problem_back'], (708.98, 187.5))
            screen.blit(assets['problem_quiz'], (721.78, 225.75))
            screen.blit(assets['time_count'], (927.98, 196.5))
            screen.blit(assets['cat'], (605, 81))
            # Draw UI text
            text_difficulty = custom_font1.render("DIFFICULTY :", True, (255, 255, 255))
            text_easy = custom_font1.render("EASY", True, (76, 255, 17))
            text_remains = custom_font3.render("remains :", True, (0, 154, 59))
            text_cnt_remains = custom_font4.render(f"{remains_done}/{remains_target}", True, (255, 255, 255))
            text_problemlimit = custom_font3.render("problem limit :", True, (220, 0, 4))
            text_cnt_problemlimit = custom_font4.render(f"{problem_count}/{problem_limit}", True, (255, 255, 255))
            text_time = custom_font4.render(str(get_remaining_game_time()), True, (224, 165, 56))
            # Draw answer buttons
            answer_buttons = [
                (assets['ans1_back'], (715.38, 391.5)),
                (assets['ans2_back'], (715.38, 456.75)),
                (assets['ans3_back'], (715.38, 522)),
                (assets['ans4_back'], (715.38, 587.25))
            ]

            for img, pos in answer_buttons:
                screen.blit(img, pos)

            # Draw current problem info if selected
            if current_problem:
                question_num = custom_font4.render(f"PROBLEM: {str(current_problem.number)}", True, (224, 165, 56))
                question_text = custom_font1.render(current_problem.question + " = ?", True, (74, 246, 38))

                for i, choice in enumerate(current_problem.choices):
                    ans_text = custom_font4.render(f"{choice}", True, (0, 0, 0))
                    y_pos = 401 + i * 65
                    screen.blit(ans_text, (826, y_pos))

                screen.blit(question_num, (725, 197))
                screen.blit(question_text, (740.33, 263.25))

            # Draw UI elements
            screen.blit(text_difficulty, (64, 22))
            screen.blit(text_easy, (225, 22))
            screen.blit(text_remains, (721.78, 92.25))
            screen.blit(text_problemlimit, (721.78, 117.75))
            screen.blit(text_cnt_remains, (908.09, 92.25))
            screen.blit(text_cnt_problemlimit, (908.09, 117.75))
            screen.blit(text_time, (937.9, 197))

        # Game initialization
        assets = load_game_assets()
        for _ in range(3):
            problem_count += 1
            add_problem()

        # Main game loop
        running = True
        clock = pygame.time.Clock()

        while running:
            if yay_screen:
                current_screen = pygame.image.load("./assets/menu/yaydid.jpg")
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check for problem clicks in question area
                    if 50 <= mouse_x <= 639 and 70 <= mouse_y <= 676:
                        for problem in problems:
                            problem_rect = pygame.Rect((problem.x- 250 // 2),(problem.y- 100 // 2),250,100)
                            if problem_rect.collidepoint(mouse_x-175, mouse_y-125):
                                current_problem = problem
                                break

                    # Check for answer button clicks
                    if current_problem:
                        button_y_positions = [391.5, 456.75, 522, 587.25]
                        for i, y_pos in enumerate(button_y_positions):
                            button_rect = pygame.Rect(715.38, y_pos, 244.62, 46.5)
                            if button_rect.collidepoint(mouse_x, mouse_y):
                                if current_problem.choices[i] == current_problem.answer:
                                    remains_done += 1
                                    problem_count -= 1
                                    problems.remove(current_problem)
                                    current_problem = None
                                    problem.start_time = time.time()
                                    if not problem_count:
                                        for _ in range(3):
                                            problem_count += 1
                                            current_time = time.time()
                                            add_problem()
                                    if remains_done == remains_target:
                                        yay_screen = True
                                        pygame.display.flip()
                                else:
                                    # Decreasing time
                                    reduce_game_timer()
                                break

            # Update problems
            for problem in problems[:]:
                if get_remaining_game_time() <= 0:
                    problem.is_expired = True
                    problem.start_time = time.time()
                    if problem_count < problem_limit:
                        current_time = time.time()
                        problem_count += 1
                        reset_game_timer()
                        add_problem()

            # Check game over condition
            if problem_count >= problem_limit:
                running = False

            # Draw game screen
            draw_game_screen(assets)

            # Draw problem boxes
            question_surface = pygame.Surface((589, 606), pygame.SRCALPHA)
            for problem in problems:
                draw_problem_box(question_surface, problem)
            screen.blit(question_surface, (50, 70))

            #Setting button
            pause_button = pygame.transform.scale(pause_button, (41,38))
            pause_button_pos = (width - width*0.0625, height - height*0.98)

            screen.blit(pause_button,pause_button_pos)
            if check_button_click(pause_button, *pause_button_pos):
                period_screen = "hard mode"
                current_screen = "pause"

            pygame.display.flip()
            clock.tick(60)

    #Medium mode window
    elif current_screen == "normal mode":
        def load_game_assets():
            assets = {}
            assets['background'] = pygame.image.load("./assets/normal mode/normal wall.png").convert_alpha()
            assets['question_back'] = pygame.image.load("./assets/easy mode/ansback.png").convert_alpha()
            assets['question_white'] = pygame.image.load("./assets/easy mode/ansbackwhite.png").convert_alpha()
            assets['wall'] = pygame.image.load("./assets/easy mode/wall.png").convert_alpha()
            assets['ansback'] = pygame.image.load("./assets/easy mode/answall.png").convert_alpha()
            assets['score_back'] = pygame.image.load("./assets/easy mode/score-background.png").convert_alpha()
            assets['problem_back'] = pygame.image.load("./assets/easy mode/Ploblem rec.png").convert_alpha()
            assets['problem_quiz'] = pygame.image.load("./assets/easy mode/Ploblem quiz.png").convert_alpha()
            assets['time_count'] = pygame.image.load("./assets/easy mode/time_count.png").convert_alpha()
            assets['ans1_back'] = pygame.image.load("./assets/easy mode/ans1_red.png").convert_alpha()
            assets['ans2_back'] = pygame.image.load("./assets/easy mode/ans2_blue.png").convert_alpha()
            assets['ans3_back'] = pygame.image.load("./assets/easy mode/ans3_yellow.png").convert_alpha()
            assets['ans4_back'] = pygame.image.load("./assets/easy mode/ans4_green.png").convert_alpha()
            assets['cat'] = pygame.image.load("./assets/easy mode/cat.png").convert_alpha()
            
            # Scale images
            assets['background'] = pygame.transform.scale(assets['background'], (width, height))
            assets['question_back'] = pygame.transform.scale(assets['question_back'], (618, 638))
            assets['question_white'] = pygame.transform.scale(assets['question_white'], (589, 606))
            assets['wall'] = pygame.transform.scale(assets['wall'], (39, 534))
            assets['ansback'] = pygame.transform.scale(assets['ansback'], (302.22, 638.25))
            assets['score_back'] = pygame.transform.scale(assets['score_back'], (256, 75.75))
            assets['problem_back'] = pygame.transform.scale(assets['problem_back'], (256.71, 168))
            assets['problem_quiz'] = pygame.transform.scale(assets['problem_quiz'], (231.82, 112.5))
            assets['time_count'] = pygame.transform.scale(assets['time_count'], (34, 33))
            assets['ans1_back'] = pygame.transform.scale(assets['ans1_back'], (244.62, 46.5))
            assets['ans2_back'] = pygame.transform.scale(assets['ans2_back'], (244.62, 46.5))
            assets['ans3_back'] = pygame.transform.scale(assets['ans3_back'], (244.62, 46.5))
            assets['ans4_back'] = pygame.transform.scale(assets['ans4_back'], (244.62, 46.5))
            assets['cat'] = pygame.transform.scale(assets['cat'], (22, 20))
            
            return assets

        # Game variables
        remains_target = 12
        problem_limit = 20
        default_timer = 60
        game_timer = default_timer
        start_time = time.time()
        problems = []
        operations = ['+', '-', '*', '/']
        current_problem = None
        remains_done = 0
        problem_count = 0
        DARK_GRAY = (20, 20, 20)
        GREEN = (0, 255, 0)

        class Problem:
            def __init__(self, number, x, y):
                self.number = number
                self.x = x
                self.y = y
                self.question, self.answer = self.generate_question()
                self.choices = self.generate_choices()
                self.timer = default_timer
                self.start_time = time.time()
                self.is_expired = False

            def generate_question(self):
                num_count = random.randint(2, 4)  # Randomly select number of terms between 2 and 4
                numbers = [random.randint(1, 100) for _ in range(num_count)]  # Generate random numbers
                ops = [random.choice(operations) for _ in range(num_count - 1)]  # Generate random operators
                
                # Randomly decide if parentheses should be added for num_count >= 3
                if num_count >= 3 and random.choice([True, False]):
                    left_paren = random.randint(0, num_count - 2)  # Position of '('
                    right_paren = random.randint(left_paren + 1, num_count - 1)  # Position of ')'
                else:
                    left_paren, right_paren = -1, -1  # No parentheses if not chosen

                # Build the equation string with optional parentheses
                question_text = ""
                for i in range(num_count):
                    if i == left_paren:
                        question_text += "("
                    question_text += str(numbers[i])
                    if i < num_count - 1:
                        question_text += f" {ops[i]} "
                    if i == right_paren:
                        question_text += ")"

                # ตรวจสอบโครงสร้างของ question_text ก่อนใช้ eval
                if not self.is_valid_expression(question_text):
                    return self.generate_question()  # Retry if structure is invalid

                # Evaluate the answer safely
                try:
                    answer = eval(question_text)
                    # Regenerate if answer has more than 5 digits
                    if len(str(int(answer))) > 5:
                        return self.generate_question()  # Retry generating question if answer is too large
                except ZeroDivisionError:
                    return self.generate_question()  # Retry generating question if division by zero occurs

                return question_text, int(answer)

            def is_valid_expression(self, expression):
                # ตรวจสอบว่ามีเครื่องหมายทางคณิตศาสตร์ตามหลัง ')' หรือไม่
                if any(op + ")" in expression for op in operations):
                    return False
                # ตรวจสอบว่า expression ไม่มี syntax ผิดพลาด
                try:
                    compile(expression, '<string>', 'eval')
                    return True
                except SyntaxError:
                    return False

            def generate_choices(self):
                choices = [self.answer]
                while len(choices) < 4:
                    wrong = self.answer + random.randint(-5, 5)
                    if wrong not in choices and wrong != self.answer:
                        choices.append(wrong)
                random.shuffle(choices)
                return choices

        def reset_game_timer():
            global game_timer, start_time
            game_timer = default_timer  # รีเซ็ตเวลาให้เป็นค่าเริ่มต้น
            start_time = time.time()    # อัปเดตเวลาเริ่มต้นใหม่

        def reduce_game_timer():
            global game_timer, start_time
            remaining_time = get_remaining_game_time()
            game_timer = remaining_time * 0.30  # ลดเวลาที่เหลือโดยคูณด้วย 0.70
            start_time = time.time()            # อัปเดตเวลาเริ่มต้นใหม่

        def get_remaining_game_time():
            # คำนวณเวลา
            elapsed = time.time() - start_time
            return max(0, int(game_timer - elapsed))

        def add_problem():
            if problem_count < problem_limit:
                # Generate random position within the white question area
                margin = 100
                x = random.randint(100, 550 - margin)
                y = random.randint(100, 600 - margin)
                problem = Problem(len(problems) + 1, x, y)
                problems.append(problem)
                reset_game_timer()

        def draw_problem_box(surface, problem):
            # Draw problem boxes in the question area
            box_width = 250
            box_height = 100
            box_x = problem.x
            box_y = problem.y

            problem_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

            # Draw main box
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, box_height), 2)
            
            # Draw problem header
            header_height = 25
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, header_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, header_height), 2)

            # Draw problem text
            problem_text = custom_font4.render(f"PROBLEM: {problem.number}", True, (224, 165, 56))
            text_rect = problem_text.get_rect(topright=(box_width - 5, 5))
            problem_surface.blit(problem_text, text_rect)

            # Draw problems
            timer_text = custom_font2.render(str(problem.question), True, (0, 255, 0))
            timer_rect = timer_text.get_rect(center=(box_width//2, box_height//2))
            problem_surface.blit(timer_text, timer_rect)

            surface.blit(problem_surface, (box_x, box_y))

        def draw_game_screen(assets):
            # Draw background and UI elements
            screen.blit(assets['background'], (0, 0))
            screen.blit(assets['wall'], (649, 114))
            screen.blit(assets['ansback'], (686.22, 56.25))
            screen.blit(assets['question_back'], (36, 56))
            screen.blit(assets['question_white'], (50, 70))
            screen.blit(assets['score_back'], (709.69, 77.25))
            screen.blit(assets['problem_back'], (708.98, 187.5))
            screen.blit(assets['problem_quiz'], (721.78, 225.75))
            screen.blit(assets['time_count'], (927.98, 196.5))
            screen.blit(assets['cat'], (605, 81))
            # Draw UI text
            text_difficulty = custom_font1.render("DIFFICULTY :", True, (255, 255, 255))
            text_easy = custom_font1.render("NORMAL", True, (243, 255, 73))
            text_remains = custom_font3.render("remains :", True, (0, 154, 59))
            text_cnt_remains = custom_font4.render(f"{remains_done}/{remains_target}", True, (255, 255, 255))
            text_problemlimit = custom_font3.render("problem limit :", True, (220, 0, 4))
            text_cnt_problemlimit = custom_font4.render(f"{problem_count}/{problem_limit}", True, (255, 255, 255))
            text_time = custom_font4.render(str(get_remaining_game_time()), True, (224, 165, 56))
            # Draw answer buttons
            answer_buttons = [
                (assets['ans1_back'], (715.38, 391.5)),
                (assets['ans2_back'], (715.38, 456.75)),
                (assets['ans3_back'], (715.38, 522)),
                (assets['ans4_back'], (715.38, 587.25))
            ]

            for img, pos in answer_buttons:
                screen.blit(img, pos)

            # Draw current problem info if selected
            if current_problem:
                question_num = custom_font4.render(f"PROBLEM: {str(current_problem.number)}", True, (224, 165, 56))
                question_text = custom_font1.render(current_problem.question + " = ?", True, (74, 246, 38))

                for i, choice in enumerate(current_problem.choices):
                    ans_text = custom_font4.render(f"{choice}", True, (0, 0, 0))
                    y_pos = 401 + i * 65
                    screen.blit(ans_text, (826, y_pos))

                screen.blit(question_num, (725, 197))
                screen.blit(question_text, (740.33, 263.25))

            # Draw UI elements
            screen.blit(text_difficulty, (64, 22))
            screen.blit(text_easy, (225, 22))
            screen.blit(text_remains, (721.78, 92.25))
            screen.blit(text_problemlimit, (721.78, 117.75))
            screen.blit(text_cnt_remains, (908.09, 92.25))
            screen.blit(text_cnt_problemlimit, (908.09, 117.75))
            screen.blit(text_time, (937.9, 197))

        # Game initialization
        assets = load_game_assets()
        for _ in range(3):
            problem_count += 1
            add_problem()

        # Main game loop
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check for problem clicks in question area
                    if 50 <= mouse_x <= 639 and 70 <= mouse_y <= 676:
                        for problem in problems:
                            problem_rect = pygame.Rect((problem.x- 250 // 2),(problem.y- 100 // 2),250,100)
                            if problem_rect.collidepoint(mouse_x-175, mouse_y-125):
                                current_problem = problem
                                break

                    # Check for answer button clicks
                    if current_problem:
                        button_y_positions = [391.5, 456.75, 522, 587.25]
                        for i, y_pos in enumerate(button_y_positions):
                            button_rect = pygame.Rect(715.38, y_pos, 244.62, 46.5)
                            if button_rect.collidepoint(mouse_x, mouse_y):
                                if current_problem.choices[i] == current_problem.answer:
                                    remains_done += 1
                                    problem_count -= 1
                                    problems.remove(current_problem)
                                    current_problem = None
                                    problem.start_time = time.time()
                                    if not problem_count:
                                        for _ in range(3):
                                            problem_count += 1
                                            add_problem()
                                    if remains_done == remains_target:
                                        running = False
                                        print("You won!")
                                else:
                                    # Decreasing time
                                    reduce_game_timer()
                                break

            # Update problems
            for problem in problems[:]:
                if get_remaining_game_time() <= 0:
                    problem.is_expired = True
                    problem.start_time = time.time()
                    if problem_count < problem_limit:
                        problem_count += 1
                        reset_game_timer()
                        add_problem()

            # Check game over condition
            if problem_count >= problem_limit:
                running = False

            # Draw game screen
            draw_game_screen(assets)

            # Draw problem boxes
            question_surface = pygame.Surface((589, 606), pygame.SRCALPHA)
            for problem in problems:
                draw_problem_box(question_surface, problem)
            screen.blit(question_surface, (50, 70))
            
            #Setting button
            pause_button = pygame.transform.scale(pause_button, (41,38))
            pause_button_pos = (width - width*0.0625, height - height*0.98)

            screen.blit(pause_button,pause_button_pos)
            if check_button_click(pause_button, *pause_button_pos):
                period_screen = "hard mode"
                current_screen = "pause"

            pygame.display.flip()
            clock.tick(60)

    #Hard mode window
    elif current_screen == "hard mode":
        def load_game_assets():
            assets = {}
            assets['background'] = pygame.image.load("./assets/hard mode/hard wall.png").convert_alpha()
            assets['question_back'] = pygame.image.load("./assets/easy mode/ansback.png").convert_alpha()
            assets['question_white'] = pygame.image.load("./assets/hard mode/hardback.png").convert_alpha()
            assets['wall'] = pygame.image.load("./assets/easy mode/wall.png").convert_alpha()
            assets['ansback'] = pygame.image.load("./assets/easy mode/answall.png").convert_alpha()
            assets['score_back'] = pygame.image.load("./assets/easy mode/score-background.png").convert_alpha()
            assets['problem_back'] = pygame.image.load("./assets/easy mode/Ploblem rec.png").convert_alpha()
            assets['problem_quiz'] = pygame.image.load("./assets/easy mode/Ploblem quiz.png").convert_alpha()
            assets['time_count'] = pygame.image.load("./assets/easy mode/time_count.png").convert_alpha()
            assets['ans1_back'] = pygame.image.load("./assets/easy mode/ans1_red.png").convert_alpha()
            assets['ans2_back'] = pygame.image.load("./assets/easy mode/ans2_blue.png").convert_alpha()
            assets['ans3_back'] = pygame.image.load("./assets/easy mode/ans3_yellow.png").convert_alpha()
            assets['ans4_back'] = pygame.image.load("./assets/easy mode/ans4_green.png").convert_alpha()
            assets['cat'] = pygame.image.load("./assets/easy mode/cat.png").convert_alpha()
            
            # Scale images
            assets['background'] = pygame.transform.scale(assets['background'], (width, height))
            assets['question_back'] = pygame.transform.scale(assets['question_back'], (618, 638))
            assets['question_white'] = pygame.transform.scale(assets['question_white'], (589, 606))
            assets['wall'] = pygame.transform.scale(assets['wall'], (39, 534))
            assets['ansback'] = pygame.transform.scale(assets['ansback'], (302.22, 638.25))
            assets['score_back'] = pygame.transform.scale(assets['score_back'], (256, 75.75))
            assets['problem_back'] = pygame.transform.scale(assets['problem_back'], (256.71, 168))
            assets['problem_quiz'] = pygame.transform.scale(assets['problem_quiz'], (231.82, 112.5))
            assets['time_count'] = pygame.transform.scale(assets['time_count'], (34, 33))
            assets['ans1_back'] = pygame.transform.scale(assets['ans1_back'], (244.62, 46.5))
            assets['ans2_back'] = pygame.transform.scale(assets['ans2_back'], (244.62, 46.5))
            assets['ans3_back'] = pygame.transform.scale(assets['ans3_back'], (244.62, 46.5))
            assets['ans4_back'] = pygame.transform.scale(assets['ans4_back'], (244.62, 46.5))
            assets['cat'] = pygame.transform.scale(assets['cat'], (22, 20))
            
            return assets

        # Game variables
        remains_target = 20
        problem_limit = 30
        default_timer = 100
        game_timer = default_timer
        start_time = time.time()
        problems = []
        operations = ['+', '-', '*', '/', '**']
        current_problem = None
        remains_done = 0
        problem_count = 0
        DARK_GRAY = (20, 20, 20)
        GREEN = (0, 255, 0)

        class Problem:
            def __init__(self, number, x, y):
                self.number = number
                self.x = x
                self.y = y
                self.question, self.answer = self.generate_question()
                self.choices = self.generate_choices()
                self.timer = default_timer
                self.start_time = time.time()
                self.is_expired = False

            def generate_question(self):
                num_count = random.randint(2, 5)  # Randomly select number of terms between 2 and 5
                numbers = [random.randint(1, 100) for _ in range(num_count)]  # Generate random numbers
                ops = [random.choice(operations) for _ in range(num_count - 1)]  # Generate random operators
                
                # Randomly decide if parentheses should be added for num_count >= 3
                if num_count >= 3 and random.choice([True, False]):
                    left_paren = random.randint(0, num_count - 2)  # Position of '('
                    right_paren = random.randint(left_paren + 1, num_count - 1)  # Position of ')'
                else:
                    left_paren, right_paren = -1, -1  # No parentheses if not chosen

                # Build the equation string with optional parentheses
                question_text = ""
                for i in range(num_count):
                    if i == left_paren:
                        question_text += "("
                    question_text += str(numbers[i])
                    if i < num_count - 1:
                        question_text += f" {ops[i]} "
                    if i == right_paren:
                        question_text += ")"

                # ตรวจสอบโครงสร้างของ question_text ก่อนใช้ eval
                if not self.is_valid_expression(question_text):
                    return self.generate_question()  # Retry if structure is invalid

                # Evaluate the answer safely
                try:
                    answer = eval(question_text)
                    # Regenerate if answer has more than 5 digits
                    if len(str(int(answer))) > 5:
                        return self.generate_question()  # Retry generating question if answer is too large
                except ZeroDivisionError:
                    return self.generate_question()  # Retry generating question if division by zero occurs

                return question_text, int(answer)

            def is_valid_expression(self, expression):
                # ตรวจสอบว่ามีเครื่องหมายทางคณิตศาสตร์ตามหลัง ')' หรือไม่
                if any(op + ")" in expression for op in operations):
                    return False
                # ตรวจสอบว่า expression ไม่มี syntax ผิดพลาด
                try:
                    compile(expression, '<string>', 'eval')
                    return True
                except SyntaxError:
                    return False

            def generate_choices(self):
                choices = [self.answer]
                while len(choices) < 4:
                    wrong = self.answer + random.randint(-5, 5)
                    if wrong not in choices and wrong != self.answer:
                        choices.append(wrong)
                random.shuffle(choices)
                return choices

        def reset_game_timer():
            global game_timer, start_time
            game_timer = default_timer  # รีเซ็ตเวลาให้เป็นค่าเริ่มต้น
            start_time = time.time()    # อัปเดตเวลาเริ่มต้นใหม่

        def reduce_game_timer():
            global game_timer, start_time
            remaining_time = get_remaining_game_time()
            game_timer = remaining_time * 0.20  # ลดเวลาที่เหลือโดยคูณด้วย 0.20
            start_time = time.time()            # อัปเดตเวลาเริ่มต้นใหม่

        def get_remaining_game_time():
            # คำนวณเวลา
            elapsed = time.time() - start_time
            return max(0, int(game_timer - elapsed))

        def add_problem():
            if problem_count < problem_limit:
                # Generate random position within the white question area
                margin = 100
                x = random.randint(100, 550 - margin)
                y = random.randint(100, 600 - margin)
                problem = Problem(len(problems) + 1, x, y)
                problems.append(problem)
                reset_game_timer()

        def draw_problem_box(surface, problem):
            # Draw problem boxes in the question area
            box_width = 250
            box_height = 100
            box_x = problem.x
            box_y = problem.y

            problem_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

            # Draw main box
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, box_height), 2)
            
            # Draw problem header
            header_height = 25
            pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, header_height))
            pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, header_height), 2)

            # Draw problem text
            problem_text = custom_font4.render(f"PROBLEM: {problem.number}", True, (224, 165, 56))
            text_rect = problem_text.get_rect(topright=(box_width - 5, 5))
            problem_surface.blit(problem_text, text_rect)

            # Draw problems
            timer_text = custom_font2.render("*-- UNKNOW --*", True, (0, 255, 0))
            timer_rect = timer_text.get_rect(center=(box_width//2, box_height//2))
            problem_surface.blit(timer_text, timer_rect)

            surface.blit(problem_surface, (box_x, box_y))

        def draw_game_screen(assets):
            # Draw background and UI elements
            screen.blit(assets['background'], (0, 0))
            screen.blit(assets['wall'], (649, 114))
            screen.blit(assets['ansback'], (686.22, 56.25))
            screen.blit(assets['question_back'], (36, 56))
            screen.blit(assets['question_white'], (50, 70))
            screen.blit(assets['score_back'], (709.69, 77.25))
            screen.blit(assets['problem_back'], (708.98, 187.5))
            screen.blit(assets['problem_quiz'], (721.78, 225.75))
            screen.blit(assets['time_count'], (927.98, 196.5))
            screen.blit(assets['cat'], (605, 81))
            # Draw UI text
            text_difficulty = custom_font1.render("DIFFICULTY :", True, (255, 255, 255))
            text_easy = custom_font1.render("HARD", True, (255, 0, 0))
            text_remains = custom_font3.render("remains :", True, (0, 154, 59))
            text_cnt_remains = custom_font4.render(f"{remains_done}/{remains_target}", True, (255, 255, 255))
            text_problemlimit = custom_font3.render("problem limit :", True, (220, 0, 4))
            text_cnt_problemlimit = custom_font4.render(f"{problem_count}/{problem_limit}", True, (255, 255, 255))
            text_time = custom_font4.render(str(get_remaining_game_time()), True, (224, 165, 56))
            # Draw answer buttons
            answer_buttons = [
                (assets['ans1_back'], (715.38, 391.5)),
                (assets['ans2_back'], (715.38, 456.75)),
                (assets['ans3_back'], (715.38, 522)),
                (assets['ans4_back'], (715.38, 587.25))
            ]

            for img, pos in answer_buttons:
                screen.blit(img, pos)

            # Draw current problem info if selected
            if current_problem:
                question_num = custom_font4.render(f"PROBLEM: {str(current_problem.number)}", True, (224, 165, 56))
                question_text = custom_font3.render(current_problem.question + " = ?", True, (74, 246, 38))

                for i, choice in enumerate(current_problem.choices):
                    ans_text = custom_font4.render(f"{choice}", True, (0, 0, 0))
                    y_pos = 401 + i * 65
                    screen.blit(ans_text, (826, y_pos))

                screen.blit(question_num, (725, 197))
                screen.blit(question_text, (740.33, 263.25))

            # Draw UI elements
            screen.blit(text_difficulty, (64, 22))
            screen.blit(text_easy, (225, 22))
            screen.blit(text_remains, (721.78, 92.25))
            screen.blit(text_problemlimit, (721.78, 117.75))
            screen.blit(text_cnt_remains, (908.09, 92.25))
            screen.blit(text_cnt_problemlimit, (908.09, 117.75))
            screen.blit(text_time, (937.9, 197))

        # Game initialization
        assets = load_game_assets()
        for _ in range(3):
            problem_count += 1
            add_problem()

        # Main game loop
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check for problem clicks in question area
                    if 50 <= mouse_x <= 639 and 70 <= mouse_y <= 676:
                        for problem in problems:
                            problem_rect = pygame.Rect((problem.x- 250 // 2),(problem.y- 100 // 2),250,100)
                            if problem_rect.collidepoint(mouse_x-175, mouse_y-125):
                                current_problem = problem
                                break

                    # Check for answer button clicks
                    if current_problem:
                        button_y_positions = [391.5, 456.75, 522, 587.25]
                        for i, y_pos in enumerate(button_y_positions):
                            button_rect = pygame.Rect(715.38, y_pos, 244.62, 46.5)
                            if button_rect.collidepoint(mouse_x, mouse_y):
                                if current_problem.choices[i] == current_problem.answer:
                                    remains_done += 1
                                    problem_count -= 1
                                    problems.remove(current_problem)
                                    current_problem = None
                                    problem.start_time = time.time()
                                    if not problem_count:
                                        for _ in range(3):
                                            problem_count += 1
                                            add_problem()
                                    if remains_done == remains_target:
                                        running = False
                                        print("You won!")
                                else:
                                    # Decreasing time
                                    reduce_game_timer()
                                break

            # Update problems
            for problem in problems[:]:
                if get_remaining_game_time() <= 0:
                    problem.is_expired = True
                    problem.start_time = time.time()
                    if problem_count < problem_limit:
                        problem_count += 1
                        reset_game_timer()
                        add_problem()

            # Check game over condition
            if problem_count >= problem_limit:
                running = False

            # Draw game screen
            draw_game_screen(assets)

            # Draw problem boxes
            question_surface = pygame.Surface((589, 606), pygame.SRCALPHA)
            for problem in problems:
                draw_problem_box(question_surface, problem)
            screen.blit(question_surface, (50, 70))
            
            #Setting button
            pause_button = pygame.transform.scale(pause_button, (41,38))
            pause_button_pos = (width - width*0.0625, height - height*0.98)

            screen.blit(pause_button,pause_button_pos)
            if check_button_click(pause_button, *pause_button_pos):
                period_screen = "hard mode"
                current_screen = "pause"

            pygame.display.flip()
            clock.tick(60)

    pygame.display.flip()
    clock.tick(60) #FPS fixed

pygame.quit()
sys.exit()
