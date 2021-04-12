import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (92, 25, 84)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 14) * SIZE
        self.y = random.randint(0, 14) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.snake_head = pygame.image.load("resources/snake_head.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        #self.parent_screen.fill(color=BACKGROUND_COLOR)
        for i in range(self.length):
            if i == 0:
                self.parent_screen.blit(self.snake_head, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        #self.play_background_music()
        self.surface = pygame.display.set_mode(size=(600, 600))
        self.surface.fill(color=BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))
   
    def display_score(self):
        font = pygame.font.SysFont('aerial', 30)
        score = font.render(f"Score: {self.snake.length - 3}", True, (255, 255, 255))
        self.surface.blit(score, (400, 10))

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound("resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            #self.play_sound("ding")
            #sound = pygame.mixer.Sound("resources/ding.mp3")
            #pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()

        # snake collision with itself
        
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                #self.play_sound("crash")
                raise "Game Over"
        

    def show_game_over(self):
        #self.surface.fill(BACKGROUND_COLOR)
        self.render_background()
        font = pygame.font.SysFont('aerial', 30)
        line_1 = font.render(f"Game Over! Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line_1, (200, 300))
        line_1 = font.render(f"Hit Enter for Replay or ESC for Exit", True, (255, 255, 255))
        self.surface.blit(line_1, (200, 360))
        pygame.display.flip()

        pygame.mixer.music.pause()
    
    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()