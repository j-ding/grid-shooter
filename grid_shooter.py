import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Player properties
player_pos = [WIDTH // 2, HEIGHT - 50]
player_radius = 15
player_speed = 5
player_hp = 100

# Projectile properties
projectiles = []
projectile_speed = 5
shoot_cooldown = 0
shoot_delay = 10  # Delay between shots
bullet_size = 5

# Enemy properties
enemies = []
enemy_timer = 0
enemy_speed = 2
enemy_damage = 20

# Game state
running = True
shopping = False
score = 0
clock = pygame.time.Clock()
selected_upgrade = 0  # Tracks selected upgrade

# Font
font = pygame.font.Font(None, 36)

def open_shop():
    global shoot_delay, bullet_size, player_hp, score, shopping, selected_upgrade
    shop_running = True
    shop_screen = pygame.Surface((WIDTH, HEIGHT))
    shop_screen.fill(WHITE)
    
    options = [
        pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 - 50, 100, 5),
        pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 5),
        pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2 - 50, 100, 5)
    ]
    
    while shop_running:
        screen.blit(shop_screen, (0, 0))
        text = font.render("Shop - Press S to exit", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))
        
        for i, option in enumerate(options):
            color = [BLUE, GREEN, RED][i]
            pygame.draw.rect(screen, color, option)
            if i == selected_upgrade:
                pygame.draw.rect(screen, YELLOW, option, 3)  # Highlight selected option
        
        option_texts = [
            font.render("Fire Rate", True, BLACK),
            font.render("Bigger Bullets", True, BLACK),
            font.render("More HP", True, BLACK)
        ]
        
        price_texts = [
            font.render("100", True, BLACK),
            font.render("100", True, BLACK),
            font.render("100", True, BLACK)
        ]
        
        for i, option in enumerate(options):
            screen.blit(option_texts[i], (option.x + 10, option.y + 10))
            screen.blit(price_texts[i], (option.x + 35, option.y + 75))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    shop_running = False
                    shopping = False
                if event.key == pygame.K_LEFT:
                    selected_upgrade = (selected_upgrade - 1) % 3
                if event.key == pygame.K_RIGHT:
                    selected_upgrade = (selected_upgrade + 1) % 3
                if event.key == pygame.K_RETURN and score >= 100:
                    if selected_upgrade == 0:
                        shoot_delay = max(3, shoot_delay - 2)
                    elif selected_upgrade == 1:
                        bullet_size = min(10, bullet_size + 2)
                    elif selected_upgrade == 2:
                        player_hp = min(100, player_hp + 20)
                    score -= 100

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move left and right
    if keys[pygame.K_LEFT] and player_pos[0] > player_radius:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_radius:
        player_pos[0] += player_speed
    if keys[pygame.K_s]:  # Press 'S' to enter shop
        shopping = True
        open_shop()

    if not shopping:
        # Shoot bullets automatically with cooldown
        if shoot_cooldown == 0:
            projectiles.append([player_pos[0], player_pos[1]])
            shoot_cooldown = shoot_delay  # Reset cooldown
        if shoot_cooldown > 0:
            shoot_cooldown -= 1

        # Add enemies over time
        enemy_timer += 1
        if enemy_timer > 30:
            enemies.append([random.randint(0, WIDTH - 10), 0])
            enemy_timer = 0

    # Update projectiles
    for projectile in projectiles[:]:
        projectile[1] -= projectile_speed
        if projectile[1] < 0:
            projectiles.remove(projectile)

    # Update enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed

        # Collision detection
        for projectile in projectiles[:]:
            if enemy[0] <= projectile[0] <= enemy[0] + 10 and enemy[1] <= projectile[1] <= enemy[1] + 10:
                if enemy in enemies:
                    enemies.remove(enemy)
                if projectile in projectiles:
                    projectiles.remove(projectile)
                score += 10

        # Enemy reaches bottom
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            player_hp -= enemy_damage
            if player_hp <= 0:
                print("Game Over! Final Score:", score)
                running = False

    # Draw everything
    screen.fill(WHITE)

    # Draw player
    pygame.draw.circle(screen, BLUE, player_pos, player_radius)

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.circle(screen, BLUE, (projectile[0], projectile[1]), bullet_size)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 10, 10))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw HP bar
    pygame.draw.rect(screen, BLACK, (10, HEIGHT - 20, 104, 14))  # Background bar
    pygame.draw.rect(screen, GREEN, (12, HEIGHT - 18, player_hp, 10))  # HP bar
    hp_text = font.render(f"HP: {player_hp}", True, BLACK)
    screen.blit(hp_text, (120, HEIGHT - 22))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
