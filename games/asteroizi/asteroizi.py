import os
import sys
import pygame
import random

# Initializare Pygame
pygame.init()

# Variabile pentru scor
score = 0
lives = 5

# Variabile pentru stocarea stării tastelor
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

# Setări ale ecranului
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")

# Culori
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Setarea caii pentru imagini relativ la directorul scriptului
script_dir = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(script_dir, "..", "..", "images", "asteroids images")

# Încarcă imaginea navei spațiale
ship_image_path = os.path.join(images_path, "spaceship.png")  
ship_image = pygame.image.load(ship_image_path)
ship_rect = ship_image.get_rect()
ship_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
ship_speed = 7

# Proiectil
bullet_image = pygame.Surface((10, 20))
bullet_image.fill(RED)
bullet_speed = 6
bullets = []

# Asteroid

asteroid_image_path = os.path.join(images_path, "asteroids.png")
asteroid_image = pygame.image.load(asteroid_image_path)
asteroid_rect = asteroid_image.get_rect()
asteroid_speed = 3
asteroids = []

# Resize the images to be 10 times smaller
ship_image = pygame.transform.scale(ship_image, (ship_rect.width // 10, ship_rect.height // 10))
asteroid_image = pygame.transform.scale(asteroid_image, (asteroid_rect.width // 9, asteroid_rect.height // 10))

# Update the rect objects with the new image sizes
ship_rect = ship_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
asteroid_rect = asteroid_image.get_rect()



# Funcție pentru afișarea navei spațiale
def draw_ship():
    screen.blit(ship_image, ship_rect)

# Funcție pentru afișarea proiectilelor
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

# Funcție pentru afișarea asteroizilor
def draw_asteroids():
    for asteroid in asteroids:
        screen.blit(asteroid_image, asteroid)

# Funcție pentru actualizarea poziției proiectilelor
def update_bullets():
    for bullet in bullets:
        bullet.y -= bullet_speed


# Funcție pentru actualizarea poziției asteroizilor
def update_asteroids():
    for asteroid in asteroids:
        asteroid.y += asteroid_speed

# Funcție pentru gestionarea evenimentelor
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

# Funcție pentru afișarea ecranului de game over
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
                # Resetează starea jocului
                global left_pressed, right_pressed, up_pressed, down_pressed
                score = 0
                lives = 5
                global asteroids
                asteroids = []
                left_pressed = False
                right_pressed = False
                up_pressed = False
                down_pressed = False
                waiting_for_retry = False


# Funcție pentru gestionarea coliziunilor
def check_collisions():
    global score, lives

    for bullet in bullets:
        for asteroid in asteroids:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                score += 1

    for asteroid in asteroids:
        if ship_rect.colliderect(asteroid):
            asteroids.remove(asteroid)
            lives -= 1
            if lives == 0:
                game_over()

        # Verifică dacă asteroidul a ieșit din ecran pe partea de jos
        if asteroid.y > HEIGHT:
            asteroids.remove(asteroid)
            lives -= 1
            if lives == 0:
                game_over()

# Setează fontul pentru text
font = pygame.font.Font(None, 36)



# Loop principal
frame_count = 59
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

clock = pygame.time.Clock()
while True:
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    handle_events()
    frame_count += 1

    # Deplasare nava în funcție de tastele apăsate
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

    # Generare asteroizi
    if frame_count % 60 == 0 and random.randint(1, 100) <= 75:
        asteroid_rect = asteroid_image.get_rect()
        asteroid_rect.midtop = (random.randint(0, WIDTH), 0)
        asteroids.append(asteroid_rect)

    # Actualizare poziție și verificare coliziuni
    update_asteroids()
    update_bullets()
    check_collisions()

    # Desenare pe ecran
    screen.fill(WHITE)
    draw_ship()
    draw_bullets()
    draw_asteroids()

    # Afisare scor
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 10 + score_text.get_height()))

    # Actualizare ecran
    pygame.display.flip()

    # Control FPS
    clock.tick(60)

    # Clear ecran pentru a preveni urmele
    screen.fill(WHITE)

pygame.quit()
sys.exit()
