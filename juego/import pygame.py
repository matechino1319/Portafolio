import pygame
import sys

# --- 1. CONFIGURACIÓN DEL JUEGO ---
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GEOMETRY PRO - STEREO MADNESS (Réplica Exacta)")

CLOCK = pygame.time.Clock()
FPS = 60
SCROLL_SPEED = 8.4  
SPIKE_SIZE = 50 

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LEVEL_COLOR = (70, 180, 255)      
GROUND_COLOR = (100, 100, 100)    
PROGRESS_BAR_COLOR = (0, 255, 0) 

GROUND_Y = HEIGHT - 100

# --- 2. MAPA DEL NIVEL ---
# Buffer inicial de 40 bloques libres para que el jugador tenga tiempo
LEVEL_MAP = (
    [0] * 40 + [
        1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
        1, 1, 0, 0, 0, 1, 1, 1, 0, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 0, 0,
    ] + [0] * 900 + [9]
)

LEVEL_LENGTH = len(LEVEL_MAP) * SPIKE_SIZE 

# --- 3. CLASES DEL JUEGO ---
class CubePlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = SPIKE_SIZE
        self.original_image = pygame.Surface([self.size, self.size])
        self.original_image.fill(WHITE)
        pygame.draw.rect(self.original_image, BLACK, (0, 0, self.size, self.size), 3)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.velocity_y = 0
        self.gravity = 1.1
        self.jump_power = -20
        self.on_ground = True 
        self.is_dead = False
        
        self.rotation_angle = 0
        self.rotation_speed = 360 / (FPS / 2) 

    def update(self):
        if self.is_dead: 
            return
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if not self.on_ground:
            self.rotation_angle += self.rotation_speed
            self.rotation_angle %= 360 
        else:
            self.rotation_angle = round(self.rotation_angle / 90) * 90 

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.original_image, -self.rotation_angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect)


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = SPIKE_SIZE 
        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        p1 = (self.size // 2, 0)         
        p2 = (0, self.size)             
        p3 = (self.size, self.size)      
        pygame.draw.polygon(self.image, LEVEL_COLOR, [p1, p2, p3])
        pygame.draw.polygon(self.image, BLACK, [p1, p2, p3], 3)
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()
            
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 30
        self.height = SPIKE_SIZE * 2 
        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 0, 255), (0, 0, self.width, self.height), 5)
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def update(self):
        self.rect.x -= SCROLL_SPEED

# --- 4. CREADOR DE NIVELES ---
def create_level_objects(level_map, obstacles_group, portal_group):
    for i, obj_type in enumerate(level_map):
        x_pos = WIDTH + (i * SPIKE_SIZE) 
        y_pos = GROUND_Y 
        if obj_type == 1:
            obstacles_group.add(Spike(x_pos, y_pos))
        elif obj_type == 9:
            portal_group.add(Portal(x_pos, y_pos))

# --- 5. FUNCIONES ---
def check_collision(player, spikes, portal):
    if pygame.sprite.spritecollide(player, spikes, False):
        return "SPIKE"
    if pygame.sprite.spritecollide(player, portal, False):
        return "PORTAL"
    return None

def run_level_one():
    player = CubePlayer(100, GROUND_Y - SPIKE_SIZE) 
    spikes = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    create_level_objects(LEVEL_MAP, spikes, portal_group)
    
    scroll_distance = 0
    level_finished = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    player.jump()

        if not player.is_dead and not level_finished:
            scroll_distance += SCROLL_SPEED
            spikes.update()
            portal_group.update()
        
        player.update() 

        # Colisiones
        hit = check_collision(player, spikes, portal_group)
        if hit == "SPIKE" and not player.is_dead:
            print("¡GAME OVER!")
            player.is_dead = True
        if hit == "PORTAL" and not level_finished:
            print("¡VICTORIA! Nivel Completado.")
            level_finished = True
            return "VICTORY"

        # Dibujo
        SCREEN.fill(LEVEL_COLOR) 
        spikes.draw(SCREEN) 
        portal_group.draw(SCREEN)
        pygame.draw.rect(SCREEN, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        player.draw(SCREEN)

        pygame.display.flip()
        CLOCK.tick(FPS)
    
    return "QUIT"

# --- 6. MAIN LOOP ---
if __name__ == "__main__":
    current_state = "LEVEL_ONE"
    while current_state != "QUIT":
        if current_state == "LEVEL_ONE":
            current_state = run_level_one()
        elif current_state == "VICTORY":
            print("Nivel superado. El juego ha terminado.")
            break
        elif current_state == "MENU":
            print("Volviendo al menú principal...")
            break 
    pygame.quit()
    sys.exit()
