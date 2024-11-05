import pygame
import random
import time
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Game")

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

# Font settings
font = pygame.font.Font(None, 36)
pixel_font = pygame.font.Font(None, 24)  # Smaller font for pixel-style text

# Game variables
remains_target = 5  # Total questions to solve to win
problem_limit = 10  # Maximum problems allowed before losing
default_timer = 30  # Default timer for each question in seconds
timer = default_timer
current_time = time.time()
operations = ['+', '-', '*', '/']
remains_done = 0  # Counter for questions answered correctly
problem_count = 0  # Counter for total problems generated

# Problem tracking
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
        self.is_expired = False  # Track if problem expired
        
    def generate_question(self):
        """Generate a random math question and its answer"""
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
        """Generate answer choices including the correct answer"""
        choices = [self.answer]
        while len(choices) < 4:
            wrong = self.answer + random.randint(-10, 10)
            if wrong not in choices and wrong != self.answer:
                choices.append(wrong)
        random.shuffle(choices)
        return choices
    
    def get_remaining_time(self):
        """Get remaining time for this problem"""
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

def draw_problem_box(surface, problem):
    """Draw the problem box with timer in top right"""
    # Box dimensions
    box_width = 200
    box_height = 80
    box_x = problem.x - box_width // 2
    box_y = problem.y - box_height // 2
    
    # Draw main box
    pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, box_height), 2)
    
    # Draw problem header
    header_height = 25
    pygame.draw.rect(surface, DARK_GRAY, (box_x, box_y, box_width, header_height))
    pygame.draw.rect(surface, GREEN, (box_x, box_y, box_width, header_height), 2)
    
    # Draw problem number in header
    header_text = pixel_font.render(f"PROBLEM: N{problem.number}", True, (255, 215, 0))
    surface.blit(header_text, (box_x + 5, box_y + 5))
    
    # Draw timer circle in top right of header
    timer_circle_x = box_x + box_width - 15
    timer_circle_y = box_y + header_height//2
    pygame.draw.circle(surface, DARK_GRAY, (timer_circle_x, timer_circle_y), 10)
    pygame.draw.circle(surface, WHITE, (timer_circle_x, timer_circle_y), 10, 1)
    
    # Draw timer text
    timer_text = pixel_font.render(str(problem.get_remaining_time()), True, WHITE)
    timer_rect = timer_text.get_rect(center=(timer_circle_x, timer_circle_y))
    surface.blit(timer_text, timer_rect)
    
    # Draw problem text
    problem_text = font.render(problem.question, True, GREEN)
    text_rect = problem_text.get_rect(center=(box_x + box_width//2, box_y + header_height + (box_height - header_height)//2))
    surface.blit(problem_text, text_rect)

def draw_info_panel():
    """Draw the right-side information panel"""
    info_surface = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.8))
    info_surface.fill(DARK_GRAY)
    
    # Draw status information
    difficulty_text = font.render("DIFFICULTY: EASY", True, GREEN)
    remains_text = font.render(f"remains: {remains_done}/{remains_target}", True, GREEN)
    limit_text = font.render(f"problem limit: {problem_count}/{problem_limit}", True, RED)
    
    info_surface.blit(difficulty_text, (10, 10))
    info_surface.blit(remains_text, (10, 50))
    info_surface.blit(limit_text, (10, 80))
    
    # Draw current problem if selected
    if current_problem:
        # Problem header
        problem_label = font.render(f"PROBLEM: N{current_problem.number}", True, (255, 215, 0))
        info_surface.blit(problem_label, (10, 140))
        
        # Problem display box
        pygame.draw.rect(info_surface, (40, 40, 40), 
                        (10, 180, info_surface.get_width() - 20, 80))
        problem_text = font.render(f"{current_problem.question} = ?", True, GREEN)
        text_rect = problem_text.get_rect(center=(info_surface.get_width() // 2, 220))
        info_surface.blit(problem_text, text_rect)
        
        # Answer buttons
        button_colors = [RED, BLUE, YELLOW, (0, 139, 0)]
        button_height = 40
        button_margin = 10
        button_y = 300
        
        for i, choice in enumerate(current_problem.choices):
            button_rect = pygame.Rect(10, 
                                    button_y + i * (button_height + button_margin),
                                    info_surface.get_width() - 20, 
                                    button_height)
            pygame.draw.rect(info_surface, button_colors[i], button_rect)
            
            text = font.render(f"ANS #{i+1}: {choice}", True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            info_surface.blit(text, text_rect)
    
    return info_surface

# Add initial problems
for _ in range(3):
    add_problem()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
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
            
            # Check if a problem circle was clicked
            for problem in problems:
                distance = ((problem.x - main_x) ** 2 + (problem.y - main_y) ** 2) ** 0.5
                if distance < 15:  # Circle radius
                    current_problem = problem
                    break
            
            # Check if an answer button was clicked
            if current_problem and not current_problem.is_expired:
                info_x = WIDTH - info_surface.get_width() - 50
                info_y = 50
                button_y = info_y + 300
                
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
    clock.tick(200)

pygame.quit()
sys.exit()