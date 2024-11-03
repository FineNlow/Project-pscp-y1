import pygame
import random
import time
import sys
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KITCATS")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (139, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 139)
YELLOW = (139, 139, 0)
DARK_GREEN = (0, 32, 0)
BORDER_GREEN = (0, 255, 0)
DARK_GRAY = (20, 20, 20)

# game elements
BACKGROUND = pygame.image.load("./assets/img/level/Background/Hard.png")
DIFFICULTY = pygame.image.load("./assets/img/level/Difficulty/DIFFICULTY _ Hard.png")
COUNT_ZONE = pygame.image.load("./assets/img/level/User zone/Rectangle 9946.png")
PROBLEM_BOX = pygame.image.load("./assets/img/level/User zone/Ploblem rec.png")
PROBLEM_DISPLAY = pygame.image.load("./assets/img/level/User zone/Ploblem quiz.png")
ANS_RED = pygame.image.load("./assets/img/level/Answer btn/red.png")
ANS_BLUE = pygame.image.load("./assets/img/level/Answer btn/blue.png")
ANS_GREEN = pygame.image.load("./assets/img/level/Answer btn/green.png")
ANS_YELLOW = pygame.image.load("./assets/img/level/Answer btn/yellow.png")

# Load Pixelify Sans font
font_path = "./assets/font/PixelifySans-Regular.ttf"
pixel_font = pygame.font.Font(font_path, 24)
pixel_font_large = pygame.font.Font(font_path, 36)
pixel_font_large = pygame.font.Font(None, 36)

# Game variables
remains_target = 5  # Total questions to solve to win
problem_limit = 10  # Maximum problems allowed before losing
default_timer = 30  # Default timer for each question in seconds
timer = default_timer
current_time = time.time()
operations = ['+', '-', '*', '/']
remains_done = 0  # Counter for questions answered correctly
problem_count = 0  # Counter for total problems generated
problems = []  # List to store problem data including position
current_problem = None  # Currently selected problem

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
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        op = random.choice(operations)
        if op == '/':
            num2 = random.randint(1, 9)
            answer = num1 // num2
        else:
            answer = eval(f"{num1} {op} {num2}")
        return f"{num1} {op} {num2}", answer
    
    def generate_choices(self):
        choices = [self.answer]
        while len(choices) < 4:
            wrong = self.answer + random.randint(-10, 10)
            if wrong not in choices and wrong != self.answer:
                choices.append(wrong)
        random.shuffle(choices)
        return choices
    
    def get_remaining_time(self):
        elapsed = time.time() - self.start_time
        return max(0, int(self.timer - elapsed))

def create_gradient(size, start_color, end_color):
    """Create a vertical gradient surface"""
    surface = pygame.Surface(size)
    for y in range(size[1]):
        factor = y / size[1]
        color = [start + (end - start) * factor 
                for start, end in zip(start_color, end_color)]
        pygame.draw.line(surface, color, (0, y), (size[0], y))
    return surface

def draw_scanlines(surface):
    """Draw scanline effect"""
    for y in range(0, surface.get_height(), 2):
        pygame.draw.line(surface, (0, 0, 0, 64), 
                       (0, y), (surface.get_width(), y), 1)

def add_problem():
    """Add a new problem at a random position"""
    if problem_count < problem_limit:  # Check against total problem count
        # Generate random position within the main surface
        margin = 150  # Increased margin to accommodate problem boxes
        x = random.randint(margin, int(WIDTH * 0.6) - margin)
        y = random.randint(margin, int(HEIGHT * 0.7) - margin)
        
        # Create new problem with incrementing number
        problem = Problem(len(problems) + 1, x, y)
        problems.append(problem)

def draw_info_panel():
    info_surface = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.8))
    info_surface.fill(DARK_GRAY)
    
    # Draw count zone background for status
    count_zone_scaled = pygame.transform.scale(COUNT_ZONE, (info_surface.get_width() - 20, 60))
    info_surface.blit(count_zone_scaled, (10, 10))
    
    # Draw status text
    remains_text = pixel_font.render("remains:", True, GREEN)
    remains_value = pixel_font.render(f"{remains_done} / {remains_target}", True, GREEN)
    info_surface.blit(remains_text, (20, 20))
    info_surface.blit(remains_value, (remains_text.get_width() + 30, 20))
    
    problem_text = pixel_font.render("problem limit:", True, RED)
    problem_value = pixel_font.render(f"{problem_count} / {problem_limit}", True, RED)
    info_surface.blit(problem_text, (20, 40))
    info_surface.blit(problem_value, (problem_text.get_width() + 30, 40))
    
    if current_problem:
        # Draw problem header
        problem_header_scaled = pygame.transform.scale(PROBLEM_BOX, 
                                                     (info_surface.get_width() - 20, 40))
        info_surface.blit(problem_header_scaled, (10, 80))
        header_text = pixel_font.render(f"PROBLEM: N{current_problem.number}", True, (255, 215, 0))
        info_surface.blit(header_text, (20, 90))
        
        # Draw timer 
        pygame.draw.circle(info_surface, WHITE, 
                         (info_surface.get_width() - 35, 100), 15, 1)
        timer_text = pixel_font.render(str(current_problem.get_remaining_time()), True, WHITE)
        timer_rect = timer_text.get_rect(center=(info_surface.get_width() - 35, 100))
        info_surface.blit(timer_text, timer_rect)
        
        # Draw problem display
        problem_display_scaled = pygame.transform.scale(PROBLEM_DISPLAY, 
                                                      (info_surface.get_width() - 20, 80))
        info_surface.blit(problem_display_scaled, (10, 130))
        
        # Draw question with = ?
        question_text = pixel_font_large.render(current_problem.question, True, GREEN)
        text_rect = question_text.get_rect(center=(info_surface.get_width()//2, 170))
        info_surface.blit(question_text, text_rect)
        
        # Draw answer buttons
        button_images = [ANS_RED, ANS_BLUE, ANS_YELLOW, ANS_GREEN]
        button_height = 40
        button_spacing = 10
        button_y = 220
        
        for i, (choice, img) in enumerate(zip(current_problem.choices, button_images)):
            button_rect = pygame.Rect(10, 
                                    button_y + i * (button_height + button_spacing),
                                    info_surface.get_width() - 20, 
                                    button_height)
            # Scale and draw button background image
            button_scaled = pygame.transform.scale(img, (button_rect.width, button_rect.height))
            info_surface.blit(button_scaled, button_rect)
            
            # Draw the choice number
            choice_text = pixel_font.render(str(choice), True, WHITE)
            text_rect = choice_text.get_rect(center=button_rect.center)
            info_surface.blit(choice_text, text_rect)
    
    return info_surface

def draw_problem_box(surface, problem):
    # Box dimensions
    box_width = 200
    box_height = 80
    box_x = problem.x - box_width // 2
    box_y = problem.y - box_height // 2
    
    # Scale and draw problem box background
    problem_box_scaled = pygame.transform.scale(PROBLEM_BOX, (box_width, box_height))
    surface.blit(problem_box_scaled, (box_x, box_y))
    
    # Draw problem text
    header_text = pixel_font.render(f"PROBLEM: N{problem.number}", True, (255, 215, 0))
    surface.blit(header_text, (box_x + 5, box_y + 5))
    
    # Draw timer
    pygame.draw.circle(surface, WHITE, 
                      (box_x + box_width - 15, box_y + 15), 10, 1)
    timer_text = pixel_font.render(str(problem.get_remaining_time()), True, WHITE)
    timer_rect = timer_text.get_rect(center=(box_x + box_width - 15, box_y + 15))
    surface.blit(timer_text, timer_rect)
    
    # Draw question
    question_text = pixel_font_large.render(f"{problem.question} = ?", True, GREEN)
    text_rect = question_text.get_rect(center=(box_x + box_width//2, 
                                             box_y + box_height//2 + 10))
    surface.blit(question_text, text_rect)


def update_display():
    # Draw background
    screen.blit(BACKGROUND, (0, 0))
    
    # Draw difficulty
    difficulty_scaled = pygame.transform.scale(DIFFICULTY, (200, 40))
    screen.blit(difficulty_scaled, (20, 20))
    
    # Draw main game area
    main_surface = pygame.Surface((WIDTH * 0.6, HEIGHT * 0.8))
    # Use background image for gradient effect
    main_bg = pygame.transform.scale(BACKGROUND, main_surface.get_size())
    main_surface.blit(main_bg, (0, 0))
    
    # Add scanlines
    draw_scanlines(main_surface)
    
    # Draw problems if any
    for problem in problems:
        draw_problem_box(main_surface, problem)
    
    # Draw border
    pygame.draw.rect(main_surface, BORDER_GREEN, main_surface.get_rect(), 2)
    
    # Position main surface and info panel
    screen.blit(main_surface, (50, 50))
    info_panel = draw_info_panel()
    screen.blit(info_panel, (WIDTH - info_panel.get_width() - 50, 50))
    
    # Draw bottom pixel pattern
    pixel_height = 20
    for x in range(0, WIDTH, 4):
        for y in range(HEIGHT - pixel_height, HEIGHT, 4):
            if (x + y) % 8 == 0:
                pygame.draw.rect(screen, BORDER_GREEN, (x, y, 2, 2))
    
    pygame.display.flip()

def draw_problem_box(surface, problem):
    # Box dimensions
    box_width = 200
    box_height = 80
    box_x = problem.x - box_width // 2
    box_y = problem.y - box_height // 2
    
    # Scale and draw problem box background
    problem_box_scaled = pygame.transform.scale(PROBLEM_BOX, (box_width, box_height))
    surface.blit(problem_box_scaled, (box_x, box_y))
    
    # Draw problem text
    header_text = pixel_font.render(f"PROBLEM: N{problem.number}", True, (255, 215, 0))
    surface.blit(header_text, (box_x + 5, box_y + 5))
    
    # Draw timer
    pygame.draw.circle(surface, WHITE, 
                      (box_x + box_width - 15, box_y + 15), 10, 1)
    timer_text = pixel_font.render(str(problem.get_remaining_time()), True, WHITE)
    timer_rect = timer_text.get_rect(center=(box_x + box_width - 15, box_y + 15))
    surface.blit(timer_text, timer_rect)
    
    # Draw question
    question_text = pixel_font_large.render(problem.question, True, GREEN)
    text_rect = question_text.get_rect(center=(box_x + box_width//2, 
                                             box_y + box_height//2 + 10))
    surface.blit(question_text, text_rect)

# Add initial problems
for _ in range(3):
    add_problem()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(BACKGROUND, (0, 0))
    
    # Create and draw main game area
    main_surface = pygame.Surface((WIDTH * 0.6, HEIGHT * 0.8))
    gradient = create_gradient(main_surface.get_size(), DARK_GREEN, (0, 64, 0))
    main_surface.blit(gradient, (0, 0))
    draw_scanlines(main_surface)
    
    # Draw and check problems
    for problem in problems[:]:
        draw_problem_box(main_surface, problem)
        
        # Check if problem timer expired
        if problem.get_remaining_time() <= 0 and not problem.is_expired:
            problem.is_expired = True
            problem_count += 1  # Increment problem count for expired problems
            problems.remove(problem)
            if problem_count < problem_limit:
                add_problem()
    
    # Check for game over condition
    if problem_count >= problem_limit:
        running = False
        print("Game Over - Problem limit reached!")
    
    # Draw borders
    pygame.draw.rect(main_surface, BORDER_GREEN, main_surface.get_rect(), 2)
    
    # Draw information panel
    info_surface = draw_info_panel()
    
    # Position surfaces on screen
    screen.blit(main_surface, (50, 50))
    screen.blit(info_surface, (WIDTH - info_surface.get_width() - 50, 50))
    
    # Draw bottom pixel pattern
    pixel_height = 20
    for x in range(0, WIDTH, 4):
        for y in range(HEIGHT - pixel_height, HEIGHT, 4):
            if (x + y) % 8 == 0:
                pygame.draw.rect(screen, BORDER_GREEN, (x, y, 2, 2))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Convert mouse position to main surface coordinates
            main_x = mouse_x - 50
            main_y = mouse_y - 50
            
            # Check if a problem was clicked
            for problem in problems:
                # Calculate click area for the problem box
                box_width = 200
                box_height = 80
                box_x = problem.x - box_width // 2
                box_y = problem.y - box_height // 2
                box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
                
                # Check if click is within the box
                if box_x <= main_x <= box_x + box_width and box_y <= main_y <= box_y + box_height:
                    current_problem = problem
                    break
            
            # Check if an answer button was clicked
            if current_problem and not current_problem.is_expired:
                info_x = WIDTH - info_surface.get_width() - 50
                info_y = 50
                button_y = info_y + 200  # Starting y position of answer buttons
                
                for i in range(4):
                    button_rect = pygame.Rect(
                        info_x + 10,
                        button_y + i * 50,
                        info_surface.get_width() - 20,
                        40
                    )
                    
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        if current_problem.choices[i] == current_problem.answer:
                            remains_done += 1
                            problems.remove(current_problem)
                            current_problem = None
                            if remains_done == remains_target:
                                running = False
                                print("You won!")
                            elif len(problems) < remains_target:
                                add_problem()
                        else:
                            current_problem.timer *= 0.5
                            current_problem.start_time = time.time()
                        break
    
    pygame.display.flip()
    clock.tick(144)

pygame.quit()
sys.exit()