from tkinter import *
import random

# Game constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#6599D8"
FOOD_COLOR = "#FCF18C"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake coordinates
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create snake squares on canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # Randomly place food
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction, score
    
    x, y = snake.coordinates[0]

    # Move head based on direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add new head position
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if food eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        # Remove tail if no food eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    
    # Prevent 180-degree turns
    if (new_direction == 'left' and direction != 'right') or \
       (new_direction == 'right' and direction != 'left') or \
       (new_direction == 'up' and direction != 'down') or \
       (new_direction == 'down' and direction != 'up'):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    
    # Wall collision
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    
    # Self collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                      font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,
                      font=('consolas', 30), text=f"Final Score: {score}", fill="white")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 150,
                      font=('consolas', 20), text="Press any key to restart", fill="white")

def restart_game(event=None):
    global snake, food, direction, score
    
    canvas.delete(ALL)
    score = 0
    direction = 'right'
    label.config(text=f"Score: {score}")
    
    snake = Snake()
    food = Food()
    next_turn(snake, food)

# Initialize game window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Score label
score = 0
direction = 'right'
label = Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

# Game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center window on screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Key bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Key>', restart_game)  # Restart on any key press after game over

# Start game
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()