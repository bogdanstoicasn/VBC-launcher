import os
import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Score variables
score = 0
intermediate_score = 0
lives = 10
boss_spawned = False

# Variables for storing key states
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load spaceship image
script_dir = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(script_dir, "..", "..", "images", "asteroids images")

# Load spaceship image
ship_image_path = os.path.join(images_path, "spaceship.png")
ship_image = pygame.image.load(ship_image_path)
ship_rect = ship_image.get_rect()
ship_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
ship_speed = 7

# Alien
alien_image_path = os.path.join(images_path, "extraterestru.png")
alien_image = pygame.image.load(alien_image_path)
alien_rect = alien_image.get_rect()
alien_speed = 1
aliens = []

# Class for Aliens
class Alien:
    def __init__(self, rect):
        self.rect = rect

# Alien bullet
alien_bullet_image = pygame.Surface((10, 20))
alien_bullet_image.fill(GREEN)
alien_bullet_speed = 4
alien_bullets = []

# Boss bullets
boss_bullets = []

# Function to display aliens
def draw_aliens():
    for alien in aliens:
        screen.blit(alien_image, alien.rect)

# Function for spawning aliens
def generate_alien():
    global aliens
    if random.randint(1, 100) <= 100:
        alien_rect = pygame.Rect(0, 0, alien_image.get_width(), alien_image.get_height())
        alien_rect.midtop = (random.randint(0, WIDTH), 0)
        alien = Alien(alien_rect)
        return alien

class BossBullet:
    def __init__(self, rect, life=2):
        self.rect = rect
        self.life = life
# Add class for Boss
class Boss:
    def __init__(self, rect, image_path, max_lives=20):
        self.rect = rect
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (rect.width, rect.height))
        self.max_lives = max_lives
        self.lives = max_lives
        
    def move(self):
        # Left-right movement
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            # Change direction if it hits the screen edge
            self.speed = -self.speed
        self.rect.x += self.speed

    def shoot(self):
        global boss_bullets
        # Generate boss bullets from beneath it
        space_between_bullets = 20
        for i in range(3):
            boss_bullets.append(BossBullet(pygame.Rect(self.rect.centerx - 5 + i * space_between_bullets, self.rect.bottom, 10, 20)))

# Initialize boss
boss_rect = pygame.Rect(WIDTH // 2 - 50, 0, 100, 100)
boss_image_path = os.path.join(images_path, "boss.png")
boss = Boss(boss_rect, boss_image_path)
boss.speed = 2 

 

# Load background image
background_image_path = os.path.join(images_path, "background.png")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Bullet
bullet_image = pygame.Surface((10, 20))
bullet_image.fill(RED)
bullet_speed = 6
bullets = []

# Asteroid
asteroid_image_path = os.path.join(images_path, "asteroids.png")
asteroid_image = pygame.image.load(asteroid_image_path)
asteroid_speed = 2
asteroids = []

# Resize the images to be 10 times smaller
ship_image = pygame.transform.scale(ship_image, (ship_rect.width // 10, ship_rect.height // 10))
asteroid_image = pygame.transform.scale(asteroid_image, (asteroid_image.get_width() // 9, asteroid_image.get_height() // 10))
alien_image = pygame.transform.scale(alien_image, (alien_image.get_width() // 9, alien_image.get_height() // 10))

# Update the rect objects with the new image sizes
ship_rect = ship_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

# Function to generate asteroids
def generate_asteroid():
    asteroid_rect = pygame.Rect(0, 0, asteroid_image.get_width(), asteroid_image.get_height())
    asteroid_rect.midtop = (random.randint(0, WIDTH), 0)
    
    # 50% probability for double-sized asteroids
    if random.randint(1, 10) <= 5:
        asteroid_rect.size = (asteroid_rect.width * 2, asteroid_rect.height * 2)
        return Asteroid(asteroid_rect, size=2)
    else:
        return Asteroid(asteroid_rect, size=1)

# Function to display the spaceship
def draw_ship():
    screen.blit(ship_image, ship_rect)

# Function to display projectiles
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)
    for boss_bullet in boss_bullets:
        pygame.draw.rect(screen, (0, 128, 0), boss_bullet)

def update_bullets():
    for bullet in bullets:
        bullet.y -= bullet_speed
    for boss_bullet in boss_bullets:
        boss_bullet.rect.y += alien_bullet_speed
    

# Function to update alien positions
def update_aliens():
    for alien in aliens.copy():
        alien.rect.y += alien_speed

# Function to display alien projectiles
def draw_alien_bullets():
    for bullet in alien_bullets:
        pygame.draw.rect(screen, GREEN, bullet)

def update_alien_bullets():
    global alien_bullets
    for bullet in alien_bullets:
        bullet.y += alien_bullet_speed

# Function to display asteroids
def draw_asteroids():
    for asteroid in asteroids:
        if asteroid.size == 2:
            # Scalarea imaginii pentru asteroizii de dimensiune dublă
            scaled_image = pygame.transform.scale(asteroid_image, (asteroid.rect.width, asteroid.rect.height))
            screen.blit(scaled_image, asteroid.rect)
        else:
            screen.blit(asteroid_image, asteroid.rect)

# Function to update asteroid positions
def update_asteroids():
    for asteroid in asteroids.copy():
        asteroid.rect.y += asteroid_speed

# Function to handle events
def handle_events():
    global left_pressed, right_pressed, up_pressed, down_pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_UP:
                up_pressed = True
            elif event.key == pygame.K_DOWN:
                down_pressed = True
            elif event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(ship_rect.centerx - 5, ship_rect.top, 10, 20))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
            elif event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_UP:
                up_pressed = False
            elif event.key == pygame.K_DOWN:
                down_pressed = False

# Function for handling collisions
def check_collisions():
    global score, lives, boss_spawned

    for bullet in bullets.copy():
        for asteroid in asteroids.copy():
            if bullet.colliderect(asteroid.rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                if asteroid.size == 2:
                    # When a size 2 asteroid is destroyed, generate 2 size 1 asteroids
                    score += 2
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid(pygame.Rect(asteroid.rect.x, asteroid.rect.y, asteroid.rect.width // 2, asteroid.rect.height // 2), size=1))
                    asteroids.append(Asteroid(pygame.Rect(asteroid.rect.x + asteroid.rect.width // 2, asteroid.rect.y, asteroid.rect.width // 2, asteroid.rect.height // 2), size=1))
                else:
                    score += 1
                    asteroids.remove(asteroid)

    for asteroid in asteroids.copy():
        if ship_rect.colliderect(asteroid.rect):
            asteroids.remove(asteroid)
            if asteroid.size == 2:
                # When colliding with a size 2 asteroid, lose 2 lives
                lives -= 2
            else:
                lives -= 1
            if lives <= 0:
                game_over()

        # Check if the asteroid has gone off the screen on the bottom
        if asteroid.rect.y > HEIGHT:
            asteroids.remove(asteroid)
            if asteroid.size == 2:
                # If a size 2 asteroid goes off the screen, lose 2 lives
                lives -= 2
            else:
                lives -= 1
            if lives <= 0:
                game_over()
    # Check collisions between alien bullets and the spaceship
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.colliderect(ship_rect):
            alien_bullets.remove(alien_bullet)
            lives -= 1
            if lives <= 0:
                game_over()

    # Check collisions between red bullets and aliens
    for bullet in bullets.copy():
        for alien in aliens.copy():
            if bullet.colliderect(alien.rect):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1

    # Check collisions between spaceship and aliens
    for alien in aliens.copy():
        if ship_rect.colliderect(alien.rect):
            aliens.remove(alien)
            lives -= 2
            if lives <= 0:
                game_over()
        if alien.rect.y > HEIGHT:
            aliens.remove(alien)
            lives -= 2
            if lives <= 0:
                game_over()

    # Check if alien bullets go off the screen
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.y > HEIGHT:
            alien_bullets.remove(alien_bullet)
            
    # Check collisions between red and green bullets
    for bullet in bullets.copy():
        for alien_bullet in alien_bullets.copy():
            if bullet.colliderect(alien_bullet):
                bullets.remove(bullet)
                alien_bullets.remove(alien_bullet)
    # Check collisions between spaceship bullets and boss bullets
    for bullet in bullets.copy():
        for boss_bullet in boss_bullets.copy():
            if bullet.colliderect(boss_bullet.rect):
                bullets.remove(bullet)
                boss_bullet.life -= 1
                if boss_bullet.life <= 0:
                    boss_bullets.remove(boss_bullet)


    # Check collisions with the boss
    for bullet in bullets.copy():
        if bullet.colliderect(boss.rect):
            bullets.remove(bullet)
            boss.lives -= 4
            if boss.lives <= 0:
                global intermediate_score
                intermediate_score = 0
                boss.lives = boss.max_lives  # Reset lives on boss respawn
                score += 10  # Add points for defeating the boss

    # Check collisions between boss bullets and spaceship
    for boss_bullet in boss_bullets.copy():
        if boss_bullet.rect.colliderect(ship_rect):
            boss_bullets.remove(boss_bullet)
            lives -= 1
            if lives <= 0:
                game_over()


# Function for displaying the game over screen
def game_over():
    global score, lives

    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    retry_text = font.render("Press Enter to Play Again", True, (0, 0, 0))

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
    screen.blit(retry_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

    pygame.display.flip()

    waiting_for_retry = True
    while waiting_for_retry:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Reset game state
                global left_pressed, right_pressed, up_pressed, down_pressed
                score = 0
                lives = 5
                global asteroids
                asteroids = []
                global aliens
                aliens = []
                global alien_bullets
                alien_bullets = []
                left_pressed = False
                right_pressed = False
                up_pressed = False
                down_pressed = False
                waiting_for_retry = False
                # Reset boss state
                global boss_spawned
                boss_spawned = False
                global boss_bullets
                boss_bullets = []
                global intermediate_score
                intermediate_score = 0
                global copiescore
                copiescore = 0



# Set the font for text
font = pygame.font.Font(None, 36)

# Main loop
frame_count = 59
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

class Asteroid:
    def __init__(self, rect, size=1):
        self.rect = rect
        self.size = size  # 1 for normal, 2 for double
        self.alive = True

while True:
    handle_events()
    frame_count += 1

    # Move the spaceship based on pressed keys
    if left_pressed:
        ship_rect.x -= ship_speed
        if ship_rect.right < 0:
            ship_rect.left = WIDTH
    if right_pressed:
        ship_rect.x += ship_speed
        if ship_rect.left > WIDTH:
            ship_rect.right = 0
    if up_pressed:
        ship_rect.y -= ship_speed
        if ship_rect.top < 0:
            ship_rect.top = 0
    if down_pressed:
        ship_rect.y += ship_speed
        if ship_rect.bottom > HEIGHT:
            ship_rect.bottom = HEIGHT
    if not boss_spawned:
    # Generate asteroids
        if frame_count % 60 == 0 and random.randint(1, 100) <= 60:
            asteroids.append(generate_asteroid())

    # Generate aliens
        if frame_count % 120 == 0 and random.randint(1, 100) <= 50:
            aliens.append(generate_alien())
    
        if frame_count % 120 == 0 and random.randint(1, 100) <= 50:
            for new_alien in aliens:
            # Generate alien bullets for each alien
                alien_bullets.append(pygame.Rect(new_alien.rect.centerx - 5, new_alien.rect.bottom, 10, 20))

    # Update position and check collisions for aliens
    update_aliens()
    
    # Update position and check collisions for alien bullets
    update_alien_bullets()

    # Update position and check collisionsi
    update_asteroids()
    update_bullets()
    copiescore = score
    check_collisions()
    if(intermediate_score <= 10):
        if not boss_spawned:
            intermediate_score += score - copiescore
        else:
            boss_spawned = False


    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Afisare imagine de fundal
    draw_ship()
    draw_bullets()
    draw_asteroids()
    # Draw aliens and alien bullets
    draw_aliens()
    draw_alien_bullets()

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    intermediate_score_text = font.render(f"Intermediate Score: {intermediate_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 10 + score_text.get_height()))
    screen.blit(intermediate_score_text, (10, 10 + score_text.get_height() + lives_text.get_height()))

    # Spawn boss at intermediate score >= 10
    if intermediate_score >= 10 and not boss_spawned:
        boss_spawned = True
    if boss_spawned:
        boss.move()
        if frame_count % 60 == 0 and random.randint(1, 100) <= 50:
            boss.shoot()
        screen.blit(boss.image, boss.rect)

    # Update the screen
    pygame.display.flip()

    # Control FPS
    clock.tick(60)

pygame.quit()
sys.exit()
