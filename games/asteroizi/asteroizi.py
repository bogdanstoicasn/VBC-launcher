import os
import sys
import pygame
import random

# Initializare Pygame
pygame.init()

# Variabile pentru scor
score = 0
lives = 10

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
GREEN = (0, 255, 0)

# Setarea caii pentru imagini relativ la directorul scriptului
script_dir = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(script_dir, "..", "..", "images", "asteroids images")

# Încarcă imaginea navei spațiale
ship_image_path = os.path.join(images_path, "spaceship.png")
ship_image = pygame.image.load(ship_image_path)
ship_rect = ship_image.get_rect()
ship_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
ship_speed = 7

# Extraterestru
alien_image_path = os.path.join(images_path, "extraterestru.png")
alien_image = pygame.image.load(alien_image_path)
alien_rect = alien_image.get_rect()
alien_speed = 1
aliens = []

# Clasa pentru extratereștri
class Alien:
    def __init__(self, rect):
        self.rect = rect

# Proiectil extraterestru
alien_bullet_image = pygame.Surface((10, 20))
alien_bullet_image.fill(GREEN)
alien_bullet_speed = 4
alien_bullets = []

# Funcție pentru afișarea extratereștrilor
def draw_aliens():
    for alien in aliens:
        screen.blit(alien_image, alien.rect)

# Funcție pentru generarea extratereștrilor
def generate_alien():
    global aliens
    if random.randint(1, 100) <= 100:
        alien_rect = pygame.Rect(0, 0, alien_image.get_width(), alien_image.get_height())
        alien_rect.midtop = (random.randint(0, WIDTH), 0)
        alien = Alien(alien_rect)
        return alien
 

# Încarcă imaginea de fundal
background_image_path = os.path.join(images_path, "background.png")
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Proiectil
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

# Funcție pentru generarea asteroizilor
def generate_asteroid():
    asteroid_rect = pygame.Rect(0, 0, asteroid_image.get_width(), asteroid_image.get_height())
    asteroid_rect.midtop = (random.randint(0, WIDTH), 0)
    
    # Probabilitate de 10% pentru asteroizii de dimensiune dublă
    if random.randint(1, 10) <= 5:
        asteroid_rect.size = (asteroid_rect.width * 2, asteroid_rect.height * 2)
        return Asteroid(asteroid_rect, size=2)
    else:
        return Asteroid(asteroid_rect, size=1)

# Funcție pentru afișarea navei spațiale
def draw_ship():
    screen.blit(ship_image, ship_rect)

# Funcție pentru afișarea proiectilelor
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

def update_bullets():
    for bullet in bullets:
        bullet.y -= bullet_speed

# Funcție pentru actualizarea pozițiilor extratereștrilor
def update_aliens():
    for alien in aliens.copy():
        alien.rect.y += alien_speed

# Funcție pentru afișarea proiectilelor extratereștrilor
def draw_alien_bullets():
    for bullet in alien_bullets:
        pygame.draw.rect(screen, GREEN, bullet)

def update_alien_bullets():
    global alien_bullets
    for bullet in alien_bullets:
        bullet.y += alien_bullet_speed

# Funcție pentru afișarea asteroizilor
def draw_asteroids():
    for asteroid in asteroids:
        if asteroid.size == 2:
            # Scalarea imaginii pentru asteroizii de dimensiune dublă
            scaled_image = pygame.transform.scale(asteroid_image, (asteroid.rect.width, asteroid.rect.height))
            screen.blit(scaled_image, asteroid.rect)
        else:
            screen.blit(asteroid_image, asteroid.rect)

# Funcție pentru actualizarea pozițiilor asteroizilor
def update_asteroids():
    for asteroid in asteroids.copy():
        asteroid.rect.y += asteroid_speed

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

# Funcție pentru gestionarea coliziunilor
def check_collisions():
    global score, lives

    for bullet in bullets.copy():
        for asteroid in asteroids.copy():
            if bullet.colliderect(asteroid.rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                if asteroid.size == 2:
                    # La spargerea unui asteroid de tip 2, genera 2 asteroizi de tip 1
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
                # La impactul cu un asteroid de tip 2, pierzi 2 vieti
                lives -= 2
            else:
                lives -= 1
            if lives <= 0:
                game_over()

        # Verifică dacă asteroidul a ieșit din ecran pe partea de jos
        if asteroid.rect.y > HEIGHT:
            asteroids.remove(asteroid)
            if asteroid.size == 2:
                # Dacă asteroidul de tip 2 iese din ecran, pierzi 2 vieti
                lives -= 2
            else:
                lives -= 1
            if lives <= 0:
                game_over()
    # Verificare coliziuni între bullet-ul extratereștrilor și nava spațială
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.colliderect(ship_rect):
            alien_bullets.remove(alien_bullet)
            lives -= 1
            if lives <= 0:
                game_over()

    # Verificare coliziuni între bullet-ul roșu și extratereștri
    for bullet in bullets.copy():
        for alien in aliens.copy():
            if bullet.colliderect(alien.rect):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1

    # Verificare coliziuni între nava spațială și extratereștri
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

    # Verificare dacă bullet-ul extratereștrilor iese din ecran
    for alien_bullet in alien_bullets.copy():
        if alien_bullet.y > HEIGHT:
            alien_bullets.remove(alien_bullet)
            
    # Verificare coliziuni între bullet-urile roșii și bullet-urile verzi
    for bullet in bullets.copy():
        for alien_bullet in alien_bullets.copy():
            if bullet.colliderect(alien_bullet):
                bullets.remove(bullet)
                alien_bullets.remove(alien_bullet)

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
                global aliens
                aliens = []
                global alien_bullets
                alien_bullets = []
                left_pressed = False
                right_pressed = False
                up_pressed = False
                down_pressed = False
                waiting_for_retry = False


# Setează fontul pentru text
font = pygame.font.Font(None, 36)

# Loop principal
frame_count = 59
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

class Asteroid:
    def __init__(self, rect, size=1):
        self.rect = rect
        self.size = size  # 1 pentru normal, 2 pentru dublă
        self.alive = True

while True:
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
    if frame_count % 60 == 0 and random.randint(1, 100) <= 60:
        asteroids.append(generate_asteroid())

    # Generare extratereștri
    if frame_count % 120 == 0 and random.randint(1, 100) <= 50:
        aliens.append(generate_alien())
    
    if frame_count % 120 == 0 and random.randint(1, 100) <= 50:
        for new_alien in aliens:
            # Generare proiectil extraterestru pentru fiecare extraterestru
            alien_bullets.append(pygame.Rect(new_alien.rect.centerx - 5, new_alien.rect.bottom, 10, 20))

    # Actualizare poziție și verificare coliziuni pentru extratereștri
    update_aliens()
    
     # Actualizare poziție și verificare coliziuni pentru proiectile extratereștri
    update_alien_bullets()

    # Actualizare poziție și verificare coliziuni
    update_asteroids()
    update_bullets()
    check_collisions()

    # Desenare pe ecran
    screen.blit(background_image, (0, 0))  # Afisare imagine de fundal
    draw_ship()
    draw_bullets()
    draw_asteroids()
    # Desenare extratereștri și proiectile extratereștri
    draw_aliens()
    draw_alien_bullets()

    # Afisare scor
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 10 + score_text.get_height()))

    # Actualizare ecran
    pygame.display.flip()

    # Control FPS
    clock.tick(60)

pygame.quit()
sys.exit()
