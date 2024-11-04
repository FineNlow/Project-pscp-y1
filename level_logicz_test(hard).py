import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KITCATS-HARD")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (40, 40, 40)

# Font
font = pygame.font.Font(None, 36)

# Game variables
remains_target = 20  # Total questions to solve to win
problem_limit = 30  # Maximum problems allowed before losing
default_timer = 100  # Default timer for each question in seconds
timer = default_timer
current_time = time.time()
questions = []
selected_question = None
operations = ['+', '-', '*', '/','**']
remains_done = 0  # Counter for questions answered correctly
problem_count = 0  # Counter for total problems generated

# -------Logic-------



# Generate random question with 2 to 5 numbers
def generate_question():
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
    
    # Evaluate the answer safely
    try:
        answer = eval(question_text)
        # Regenerate if answer has more than 5 digits
        if len(str(int(answer))) > 5:
            return generate_question()
    except ZeroDivisionError:
        return generate_question()  # Regenerate if there's a division by zero
    return question_text, int(answer)

# Add new question to the questions list
def add_question():
    global selected_question, timer, problem_count
    if len(questions) < problem_limit:
        question_text, answer = generate_question()

        # Generate unique choices
        choices = set()
        while len(choices) < 3:
            choice = answer + random.randint(-10, 10)
            # Ensure choice is unique and not equal to the answer
            if choice != answer and choice not in choices:
                choices.add(choice)

        # Add the correct answer and shuffle choices
        choices = list(choices)
        choices.append(answer)
        random.shuffle(choices)
        
        questions.append((question_text, choices, choices.index(answer)))
        problem_count += 1  # Increment problem count
        timer = default_timer  # Reset timer to default when a new question is added



# End game with message
def end_game(message):
    print(message)
    pygame.quit()
    exit()

# Add 3 questions when game start
for _ in range(3):
    add_question()

# Main game loop
running = True
clock = pygame.time.Clock()

# -------Interface for testing-------



while running:
    screen.fill(DARK_GRAY)

    # Calculate remaining time for the current question
    elapsed_time = time.time() - current_time
    remaining_time = max(0, int(timer - elapsed_time))

    # Check timer for adding questions
    if remaining_time <= 0:
        add_question()
        current_time = time.time()

    # Display UI elements
    difficulty_text = font.render("DIFFICULTY: HARD", True, RED)
    screen.blit(difficulty_text, (20, 20))

    # Display remains done and problem count in real-time
    remains_text = font.render(f"Remains Done: {remains_done}/{remains_target}", True, YELLOW)
    problem_text = font.render(f"Problems: {problem_count}/{problem_limit}", True, RED)
    screen.blit(remains_text, (WIDTH - remains_text.get_width() - 20, 20))
    screen.blit(problem_text, (WIDTH - problem_text.get_width() - 20, 60))

    # Display questions in the left side
    for i, (question_text, _, _) in enumerate(questions):
        question_display = font.render(question_text, True, WHITE)
        screen.blit(question_display, (50, 100 + i * 40))

    # Display choices for the selected question
    if selected_question is not None:
        question_text, choices, correct_choice = questions[selected_question]
        choice_width, choice_height = 120, 50  # Width and height of choice buttons
        choice_y = HEIGHT - 200  # Y position to display choices

        # Display the choices at the center of the screen horizontally
        for i, choice in enumerate(choices):
            choice_text = font.render(str(choice), True, BLACK)
            choice_x = WIDTH // 2 - (2 * choice_width) + i * (choice_width + 10)
            pygame.draw.rect(screen, [RED, BLUE, YELLOW, GREEN][i], 
                             (choice_x, choice_y, choice_width, choice_height))
            screen.blit(choice_text, 
                        (choice_x + (choice_width - choice_text.get_width()) // 2, 
                         choice_y + (choice_height - choice_text.get_height()) // 2))

    # Display remaining time for the current question
    timer_text = font.render(f"Time: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or problem_limit == problem_count:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if a question on the left side is clicked
            for i, (question_text, _, _) in enumerate(questions):
                if 50 < mouse_x < 300 and 100 + i * 40 < mouse_y < 140 + i * 40:
                    selected_question = i
            # Check if a choice for the selected question is clicked
            if selected_question is not None:
                question_text, choices, correct_choice = questions[selected_question]
                choice_width, choice_height = 120, 50
                choice_y = HEIGHT - 200
                for i in range(4):
                    choice_x = WIDTH // 2 - (2 * choice_width) + i * (choice_width + 10)
                    if choice_x < mouse_x < choice_x + choice_width and choice_y < mouse_y < choice_y + choice_height:
                        if i == correct_choice:
                            remains_done += 1
                            problem_count -= 1
                            questions.pop(selected_question)
                            selected_question = None
                            if remains_done == remains_target:
                                end_game("1")
                            elif len(questions) < remains_target:  # Add new question if needed
                                add_question()
                                current_time = time.time()  # Reset current time
                        else:
                            # Reduce timer to 5% of the remaining time
                            current_remaining = timer - (time.time() - current_time)
                            timer = max(1, current_remaining * 0.2)  # Reduce to 80% of current remaining time
                            current_time = time.time()  # Reset timer start time
                        break



    pygame.display.flip()
    clock.tick(144)

pygame.quit()
