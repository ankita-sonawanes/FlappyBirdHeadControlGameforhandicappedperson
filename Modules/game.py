import pygame
import random
from Modules.head_control import HeadController

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((288, 512))
        self.clock = pygame.time.Clock()

        # Load game assets
        self.bird = pygame.image.load('assets/newbird.png').convert_alpha()
        self.background = pygame.image.load('assets/newbackground.png').convert_alpha()
        self.pipe_top = pygame.image.load('assets/pipe1.png').convert_alpha()
        self.pipe_bottom = pygame.image.load('assets/pipe2.png').convert_alpha()

        # Initial bird position (center of the screen)
        self.bird_y = self.screen.get_height() // 2  # Bird starts in the middle
        self.bird_movement = 0

        # Pipe settings
        self.pipe_gap = 200  # Increased gap between top and bottom pipes (200 pixels)
        self.pipe_velocity = 3  # Speed at which pipes move
        self.pipe_list = []  # To store pipe positions
        self.spawn_pipe()  # Spawn initial pipes

        self.head_controller = HeadController()
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 30)

        self.game_over = False
        self.start_ticks = pygame.time.get_ticks()  # Track the game start time

    def spawn_pipe(self):
        # Randomize pipe height for variation
        pipe_height = random.randint(150, 300)
        pipe_top_y = pipe_height - self.pipe_top.get_height()
        pipe_bottom_y = pipe_height + self.pipe_gap
        pipe_x = self.screen.get_width()  # Start pipe off-screen

        self.pipe_list.append([pipe_x, pipe_top_y, pipe_bottom_y])

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe[0] -= self.pipe_velocity

        # Remove pipes that go off-screen and spawn new pipes
        if self.pipe_list[0][0] < -self.pipe_top.get_width():
            self.pipe_list.pop(0)
            self.spawn_pipe()

    def check_collision(self):
        # Delay collision detection for 2 seconds after the game starts
        if (pygame.time.get_ticks() - self.start_ticks) < 2000:
            return False

        bird_rect = pygame.Rect(50, self.bird_y, self.bird.get_width(), self.bird.get_height())
        print(f"Bird Rect: {bird_rect}")  # Debug the bird's position

        for pipe in self.pipe_list:
            pipe_top_rect = pygame.Rect(pipe[0], pipe[1], self.pipe_top.get_width(), self.pipe_top.get_height())
            pipe_bottom_rect = pygame.Rect(pipe[0], pipe[2], self.pipe_bottom.get_width(), self.pipe_bottom.get_height())
            print(f"Pipe Top Rect: {pipe_top_rect}, Pipe Bottom Rect: {pipe_bottom_rect}")  # Debug pipe positions

            if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
                print("Collision with pipe detected!")  # Debug when a collision is detected
                return True

        # Check collision with the top or bottom of the screen
        if self.bird_y <= 0 or self.bird_y >= self.screen.get_height() - self.bird.get_height():
            print("Collision with top/bottom of screen detected!")  # Debug boundary collision
            return True

        return False

    def update_score(self):
        for pipe in self.pipe_list:
            if 45 <= pipe[0] < 50:  # Adjust this range to make score update smoother
                self.score += 1

    def display_game_over(self):
        text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(text, (100, 256))

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def run_game(self):
        while True:
            self.screen.blit(self.background, (0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if not self.game_over:
                # Get head movement
                movement_direction = self.head_controller.get_head_movement()

                # Control the bird based on head movement
                if movement_direction == 'up':
                    self.bird_movement = -5  # Move bird up
                elif movement_direction == 'down':
                    self.bird_movement = 5  # Move bird down
                else:
                    self.bird_movement = 1  # Natural falling movement

                # Update bird position
                self.bird_y += self.bird_movement

                # Move pipes
                self.move_pipes()

                # Check for collisions
                if self.check_collision():
                    self.game_over = True

                # Update score
                self.update_score()

            # Draw bird and pipes
            self.screen.blit(self.bird, (50, self.bird_y))
            for pipe in self.pipe_list:
                self.screen.blit(self.pipe_top, (pipe[0], pipe[1]))
                self.screen.blit(self.pipe_bottom, (pipe[0], pipe[2]))

            # Display score
            self.display_score()

            # If game over, display game over message
            if self.game_over:
                self.display_game_over()

            # Update display
            pygame.display.update()
            self.clock.tick(30)

        self.head_controller.release()

# For testing purposes
if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run_game()
