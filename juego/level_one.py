import pygame
import sys
import random
import os
import math
import time

# ----------------------------------------------------------------------
# --- 0. INICIALIZACIÓN DE PYGAME ---
# ----------------------------------------------------------------------

pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------------------
# --- 1. CONFIGURACIÓN GLOBAL DEL JUEGO ---
# ----------------------------------------------------------------------

START_WIDTH, START_HEIGHT = 800, 600
SCREEN = None 
CLOCK = pygame.time.Clock()
FPS = 60
SCROLL_SPEED_BASE = 8.0 
SCROLL_SPEED = SCROLL_SPEED_BASE 
SPIKE_SIZE = 50

WIDTH, HEIGHT = START_WIDTH, START_HEIGHT
GROUND_Y = HEIGHT - 100 

game_over_time = 0 

# --- COLORES ESTÉTICOS MEJORADOS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_COLOR_FILL_BASE = (200, 200, 200) 
PLAYER_COLOR_BORDER_BASE = (50, 50, 50) 
GROUND_COLOR = (80, 80, 80) 
PROGRESS_BAR_COLOR = (0, 255, 0)

# Colores Estéticos para Botones Mejorados
BUTTON_PRIMARY = (50, 200, 50)         # Verde vibrante (Reintentar/Empezar)
BUTTON_PRIMARY_HOVER = (80, 255, 80)   # Verde más brillante al pasar el ratón
BUTTON_SECONDARY = (50, 100, 200)       # Azul (Menú)
BUTTON_SECONDARY_HOVER = (80, 150, 255) # Azul más brillante al pasar el ratón
BUTTON_SHADOW = (20, 20, 20)           # Sombra oscura
BUTTON_BORDER = (255, 255, 255)        # Borde blanco
TEXT_COLOR = (255, 255, 255)
MENU_BUTTON_VISUAL_COLOR = (255, 255, 0)

# --- PALETA DE COLORES Y TINTES ---
SECTION_COLORS = [
    ((255, 120, 120), (200, 60, 60)), # Rojo
    ((120, 255, 120), (60, 200, 60)), # Verde
    ((120, 120, 255), (60, 60, 200)), # Azul
    ((255, 255, 120), (200, 200, 60)), # Amarillo
    ((255, 120, 255), (200, 60, 200)), # Magenta
    ((120, 255, 255), (60, 200, 200)), # Cyan
    ((255, 180, 80), (200, 120, 40)), # Naranja
    ((150, 100, 255), (90, 50, 200)), # Púrpura
]
TINT_COLORS = [
    (100, 180, 255), (150, 255, 150), (200, 150, 255), (255, 220, 100),
    (255, 150, 150), (150, 255, 255), (255, 210, 130), (180, 150, 255),
]
TINT_ALPHA = 100 

# --- CARGA DE RECURSOS ---
MUSIC_FILE = 'Las Pastillas del Abuelo . Qué es Dios _ . Crisis . HD.mp3'
BACKGROUND_FILE = 'maradona.jpg' 
BACKGROUND_IMAGE = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# --- 2. MAPA DE NIVEL (Sintaxis Mejorada) ---
# ----------------------------------------------------------------------
LEVEL_MAP = []
SECTION_INDICES = [] 

def add_pattern(pattern):
    if pattern or not LEVEL_MAP:
        SECTION_INDICES.append(len(LEVEL_MAP))
    LEVEL_MAP.extend(pattern)

def R(min_val, max_val):
    return random.randint(min_val, max_val)

if 0 not in SECTION_INDICES:
    SECTION_INDICES.append(0) 

# Generación del nivel (patrones de obstáculos) - SINTAXIS MEJORADA
add_pattern([0] * 8) 
add_pattern(
    [1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1, 1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7)
)
add_pattern([0] * 8) 
add_pattern([1, 1, 1] + [0] * R(6, 7) + [0] * R(6, 7) + [0] * R(6, 7) + [0] * R(5, 8)) 
add_pattern([0] * R(5, 8)) 
add_pattern(
    [1, 0, 0, 1] + [0] * R(4, 5) + 
    [1, 1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7) + [0] * R(5, 8)
)
add_pattern([0] * R(6, 8)) 
add_pattern(
    [1] + [0] * R(4, 5) + 
    [1, 1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7) + 
    [1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7) + 
    [1] + [0] * R(4, 5) + [0] * R(5, 8)
)
add_pattern([0] * R(6, 8))
add_pattern(
    [1, 1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7) + 
    [1, 1] + [0] * R(4, 5) + 
    [1, 1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7)
)
add_pattern([0] * R(5, 8))
add_pattern(
    [1] + [0] * R(4, 5) + 
    [1] + [0] * R(4, 5) + 
    [1, 1, 1] + [0] * R(6, 7) + 
    [1] + [0] * R(4, 5) + [0] * R(6, 8)
)

LEVEL_MAP.append(9) 
LEVEL_LENGTH = len(LEVEL_MAP) * SPIKE_SIZE 

# ----------------------------------------------------------------------
# --- 3. CLASES DE JUEGO ---
# ----------------------------------------------------------------------

class TrailSegment(pygame.sprite.Sprite):
    def __init__(self, image, center_pos, initial_alpha=255):
        super().__init__()
        
        self.base_image = image.copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=center_pos)
        
        self.alpha = initial_alpha
        self.fade_rate = 15 
        
        self.image.set_alpha(int(self.alpha))

    def update(self):
        global SCROLL_SPEED
        self.rect.x -= SCROLL_SPEED 
        
        self.alpha -= self.fade_rate
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.alpha))

class CubePlayer(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        self.size = SPIKE_SIZE
        self.color_fill = PLAYER_COLOR_FILL_BASE 
        self.color_border = PLAYER_COLOR_BORDER_BASE 
        
        self.original_image = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        self._render_carabela_shape(self.color_fill, self.color_border) 
        
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image) 
        
        self.velocity_y = 0
        self.gravity = 1.2 
        self.jump_power = -19 
        self.on_ground = True
        self.is_dead = False
        self.rotation_angle = 0
        self.rotation_speed = 360 / (FPS / 2.0) 

        self.max_stretch_factor = 1.2 
        self.min_stretch_factor = 0.8 
        self.stretch_intensity = 0.2 
        
        self.trail_timer = 0
        self.trail_interval = 2 
        self.current_section_color = WHITE 

    def _render_carabela_shape(self, fill_color, border_color):
        self.original_image.fill((0,0,0,0)) 
        
        # Dibuja la calavera
        skull_rect = pygame.Rect(self.size * 0.1, self.size * 0.1, self.size * 0.8, self.size * 0.7)
        pygame.draw.ellipse(self.original_image, fill_color, skull_rect)
        pygame.draw.ellipse(self.original_image, border_color, skull_rect, 2)
        
        # Ojos
        eye_radius = self.size * 0.1
        pygame.draw.circle(self.original_image, BLACK, (int(self.size * 0.35), int(self.size * 0.35)), int(eye_radius))
        pygame.draw.circle(self.original_image, BLACK, (int(self.size * 0.65), int(self.size * 0.35)), int(eye_radius))
        
        # Nariz (triángulo invertido)
        nose_points = [
            (int(self.size * 0.5), int(self.size * 0.5)),
            (int(self.size * 0.4), int(self.size * 0.6)),
            (int(self.size * 0.6), int(self.size * 0.6))
        ]
        pygame.draw.polygon(self.original_image, BLACK, nose_points)

        # Boca (línea con pequeñas líneas verticales para dientes)
        mouth_y = int(self.size * 0.7)
        pygame.draw.line(self.original_image, BLACK, (int(self.size * 0.3), mouth_y), (int(self.size * 0.7), mouth_y), 2)
        for i in range(3):
            x_tooth = int(self.size * (0.35 + i * 0.15))
            pygame.draw.line(self.original_image, BLACK, (x_tooth, mouth_y), (x_tooth, mouth_y + self.size * 0.05), 1)

        # Huesos cruzados (simplificado)
        bone_width = self.size * 0.15
        
        # Hueso 1 (diagonal de abajo izquierda a arriba derecha)
        bone1_start = (self.size * 0.1, self.size * 0.9)
        bone1_end = (self.size * 0.9, self.size * 0.2)
        pygame.draw.line(self.original_image, fill_color, bone1_start, bone1_end, int(bone_width))
        pygame.draw.line(self.original_image, border_color, bone1_start, bone1_end, int(bone_width) + 2) 
        
        # Hueso 2 (diagonal de abajo derecha a arriba izquierda)
        bone2_start = (self.size * 0.9, self.size * 0.9)
        bone2_end = (self.size * 0.1, self.size * 0.2)
        pygame.draw.line(self.original_image, fill_color, bone2_start, bone2_end, int(bone_width))
        pygame.draw.line(self.original_image, border_color, bone2_start, bone2_end, int(bone_width) + 2) 


    def update(self, trail_group, current_section_color_tuple):
        global GROUND_Y 
        
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        dark_base_color = (self.color_border[0],self.color_border[1],self.color_border[2])
        
        time_ms = pygame.time.get_ticks() / 200.0
        pulse = (math.sin(time_ms) + 1) / 2 * 0.3 
        
        r_border = int(dark_base_color[0] + (255 - dark_base_color[0]) * pulse * 0.5)
        g_border = int(dark_base_color[1] + (255 - dark_base_color[1]) * pulse * 0.5)
        b_border = int(dark_base_color[2] + (255 - dark_base_color[2]) * pulse * 0.5)
        
        self.color_fill = PLAYER_COLOR_FILL_BASE 
        self.color_border = (r_border, g_border, b_border)
        
        self._render_carabela_shape(self.color_fill, self.color_border) 
        self.current_section_color = self.color_border 

        if not self.on_ground:
            self.rotation_angle += self.rotation_speed * (1 if not self.is_dead else 0.5) 
            self.rotation_angle %= 360
        else:
            self.rotation_angle = round(self.rotation_angle / 90) * 90
            
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.velocity_y = 0
            self.on_ground = True
            
        self.image = pygame.transform.rotate(self.original_image, -self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        
        if not self.is_dead: 
            self.trail_timer += 1
            if self.trail_timer >= self.trail_interval: 
                
                stretched_image, new_rect = self._get_rendered_image_and_rect()
                
                trail_group.add(TrailSegment(
                    stretched_image, 
                    new_rect.center,
                    initial_alpha=180 
                ))
                
                self.trail_timer = 0
            
    def _get_rendered_image_and_rect(self):
        
        stretch_y = 1.0
        stretch_x = 1.0

        if not self.on_ground:
            max_vel_ref = abs(self.jump_power) * 1.5 
            if self.velocity_y < 0:
                normalized_vel = min(1.0, -self.velocity_y / abs(self.jump_power))
                stretch_y = 1 + (normalized_vel * self.stretch_intensity * 1.5) 
                stretch_x = 1 - (normalized_vel * self.stretch_intensity * 0.75) 
            elif self.velocity_y > 0:
                normalized_vel = min(1.0, self.velocity_y / max_vel_ref)
                stretch_y = 1 - (normalized_vel * self.stretch_intensity * 1.5) 
                stretch_x = 1 + (normalized_vel * self.stretch_intensity * 0.75) 
            
            stretch_y = max(self.min_stretch_factor, min(self.max_stretch_factor, stretch_y))
            stretch_x = max(self.min_stretch_factor, min(self.max_stretch_factor, stretch_x))

        stretched_width = max(1, int(self.size * stretch_x))
        stretched_height = max(1, int(self.size * stretch_y))

        stretched_image_temp = pygame.Surface(
            (stretched_width, stretched_height), 
            pygame.SRCALPHA 
        )
        stretched_image_temp.fill((0,0,0,0)) 
        
        # Dibuja la carabela estirada
        scale_factor_x = stretched_width / self.size
        scale_factor_y = stretched_height / self.size

        skull_rect_scaled = pygame.Rect(
            int(self.size * 0.1 * scale_factor_x), 
            int(self.size * 0.1 * scale_factor_y), 
            int(self.size * 0.8 * scale_factor_x), 
            int(self.size * 0.7 * scale_factor_y)
        )
        pygame.draw.ellipse(stretched_image_temp, self.color_fill, skull_rect_scaled)
        pygame.draw.ellipse(stretched_image_temp, self.color_border, skull_rect_scaled, int(2 * min(scale_factor_x, scale_factor_y)))
        
        eye_radius_scaled = int(self.size * 0.1 * min(scale_factor_x, scale_factor_y))
        pygame.draw.circle(stretched_image_temp, BLACK, (int(self.size * 0.35 * scale_factor_x), int(self.size * 0.35 * scale_factor_y)), eye_radius_scaled)
        pygame.draw.circle(stretched_image_temp, BLACK, (int(self.size * 0.65 * scale_factor_x), int(self.size * 0.35 * scale_factor_y)), eye_radius_scaled)
        
        nose_points_scaled = [
            (int(self.size * 0.5 * scale_factor_x), int(self.size * 0.5 * scale_factor_y)),
            (int(self.size * 0.4 * scale_factor_x), int(self.size * 0.6 * scale_factor_y)),
            (int(self.size * 0.6 * scale_factor_x), int(self.size * 0.6 * scale_factor_y))
        ]
        pygame.draw.polygon(stretched_image_temp, BLACK, nose_points_scaled)

        mouth_y_scaled = int(self.size * 0.7 * scale_factor_y)
        pygame.draw.line(stretched_image_temp, BLACK, (int(self.size * 0.3 * scale_factor_x), mouth_y_scaled), (int(self.size * 0.7 * scale_factor_x), mouth_y_scaled), int(2 * min(scale_factor_x, scale_factor_y)))
        for i in range(3):
            x_tooth = int(self.size * (0.35 + i * 0.15) * scale_factor_x)
            pygame.draw.line(stretched_image_temp, BLACK, (x_tooth, mouth_y_scaled), (x_tooth, mouth_y_scaled + int(self.size * 0.05 * scale_factor_y)), 1)

        bone_width_scaled = int(self.size * 0.15 * min(scale_factor_x, scale_factor_y))
        
        bone1_start_scaled = (int(self.size * 0.1 * scale_factor_x), int(self.size * 0.9 * scale_factor_y))
        bone1_end_scaled = (int(self.size * 0.9 * scale_factor_x), int(self.size * 0.2 * scale_factor_y))
        pygame.draw.line(stretched_image_temp, self.color_fill, bone1_start_scaled, bone1_end_scaled, bone_width_scaled)
        pygame.draw.line(stretched_image_temp, self.color_border, bone1_start_scaled, bone1_end_scaled, bone_width_scaled + 2)
        
        bone2_start_scaled = (int(self.size * 0.9 * scale_factor_x), int(self.size * 0.9 * scale_factor_y))
        bone2_end_scaled = (int(self.size * 0.1 * scale_factor_x), int(self.size * 0.2 * scale_factor_y))
        pygame.draw.line(stretched_image_temp, self.color_fill, bone2_start_scaled, bone2_end_scaled, bone_width_scaled)
        pygame.draw.line(stretched_image_temp, self.color_border, bone2_start_scaled, bone2_end_scaled, bone_width_scaled + 2)
        
        rotated_stretched_image = pygame.transform.rotate(stretched_image_temp, -self.rotation_angle)
        
        new_rect = rotated_stretched_image.get_rect(center=self.rect.center)
        
        return rotated_stretched_image, new_rect
            
    def jump(self): 
        # Esta función solo ejecuta el salto si está en el suelo.
        # Ya no comprueba on_ground aquí; se comprueba en el loop principal (run_level)
        if self.on_ground and not self.is_dead: # <-- La lógica de base del salto
            self.velocity_y = self.jump_power
            self.on_ground = False

    def draw(self, surface):
        global GROUND_Y, HEIGHT, WIDTH
        
        rotated_stretched_image, new_rect = self._get_rendered_image_and_rect()
        
        stretch_x = rotated_stretched_image.get_width() / self.size 
        
        max_shadow_height = HEIGHT * 0.4 
        height_off_ground = GROUND_Y - self.rect.bottom
        shadow_alpha = max(0, 200 - int(height_off_ground / max_shadow_height * 200))

        shadow_stretch_factor = 1.0 + (GROUND_Y - self.rect.bottom) / (HEIGHT/3) * 0.5 
        shadow_width = int(self.size * stretch_x * (1 + shadow_stretch_factor * 0.2)) 
        shadow_height = int(self.size * 0.2 * (1 - shadow_stretch_factor * 0.1)) 
        
        shadow_width = max(1, shadow_width)
        shadow_height = max(1, shadow_height)
        
        shadow_surf = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0,0,0,shadow_alpha), shadow_surf.get_rect())
        pygame.draw.ellipse(shadow_surf, (0,0,0,shadow_alpha//2), shadow_surf.get_rect().inflate(-shadow_width//4,-shadow_height//4))
        
        shadow_rect = shadow_surf.get_rect(center=(self.rect.centerx, GROUND_Y + shadow_surf.get_height() // 2 - 5))
        surface.blit(shadow_surf, shadow_rect)

        surface.blit(rotated_stretched_image, new_rect)
        
        self.image = pygame.transform.rotate(self.original_image, -self.rotation_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, section_color_tuple):
        super().__init__()
        self.size = SPIKE_SIZE
        self.section_color_tuple = section_color_tuple 
        self.original_image_surface = pygame.Surface([self.size, self.size], pygame.SRCALPHA)
        self.time_offset = random.randint(0, 100) 
        self.alpha = 255 
        self.x = x

        # Estos métodos deben estar definidos DENTRO de la clase,
        # pero se ejecutan correctamente al inicio.
        self._render_spike_shape(self.section_color_tuple[0], BLACK) 
        self.image = self.original_image_surface.copy()
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.mask = pygame.mask.from_surface(self.image) 

        self.shadow_surface = pygame.Surface([self.size, self.size // 3], pygame.SRCALPHA)
        self.shadow_color = (0, 0, 0, 90) 
        self._render_spike_shadow()

    def _render_spike_shape(self, fill_color, border_color):
        self.original_image_surface.fill((0,0,0,0)) 
        p1 = (self.size // 2, 0)
        p2 = (0, self.size)
        p3 = (self.size, self.size)
        pygame.draw.polygon(self.original_image_surface, fill_color, [p1, p2, p3])
        pygame.draw.polygon(self.original_image_surface, border_color, [p1, p2, p3], 3)
    
    def _render_spike_shadow(self):
        self.shadow_surface.fill((0,0,0,0))
        p1_s = (self.size // 2, 0)
        p2_s = (self.size // 6, self.size // 3)
        p3_s = (self.size - self.size // 6, self.size // 3)
        pygame.draw.polygon(self.shadow_surface, self.shadow_color, [p1_s, p2_s, p3_s])

    def _update_color_pulse(self):
        time_ms = pygame.time.get_ticks() / 150.0 + self.time_offset
        pulse = (math.sin(time_ms) + 1) / 2 * 0.2 

        bright_color = self.section_color_tuple[0]
        
        r = int(bright_color[0] + (WHITE[0] - bright_color[0]) * pulse)
        g = int(bright_color[1] + (WHITE[1] - bright_color[1]) * pulse)
        b = int(bright_color[2] + (WHITE[2] - bright_color[2]) * pulse)
        
        current_color = (r, g, b)
        self._render_spike_shape(current_color, BLACK) 

    def update(self):
        global WIDTH 
        self._update_color_pulse()
        self.rect.x -= SCROLL_SPEED 
        
        dist_factor = 1.0
        if self.rect.centerx > WIDTH * 0.7: 
            dist_factor = 1.0 - ((self.rect.centerx - WIDTH * 0.7) / (WIDTH * 0.3))
            dist_factor = max(0.2, dist_factor) 

        screen_edge_alpha = 1.0
        if self.rect.right < SPIKE_SIZE:
            screen_edge_alpha = self.rect.right / SPIKE_SIZE
            screen_edge_alpha = max(0, screen_edge_alpha) 

        self.alpha = int(255 * dist_factor * screen_edge_alpha)
        self.alpha = max(0, self.alpha)

        self.image = self.original_image_surface.copy() 
        self.image.set_alpha(self.alpha) 
        
        if self.rect.right < 0:
            self.kill()

    def draw(self, surface):
        global GROUND_Y
        shadow_rect = self.shadow_surface.get_rect(midtop=(self.rect.centerx, GROUND_Y - 5))
        shadow_copy = self.shadow_surface.copy()
        shadow_copy.set_alpha(self.alpha) 
        surface.blit(shadow_copy, shadow_rect)
        surface.blit(self.image, self.rect)

class Portal(pygame.sprite.Sprite):
    def __init__(self,x,y, section_color_tuple):
        super().__init__()
        self.width = 30
        self.height = SPIKE_SIZE*2
        self.base_color_tuple = section_color_tuple
        self.image = pygame.Surface([self.width,self.height],pygame.SRCALPHA) 
        self.time_offset = random.randint(0, 100)
        self._update_color()
        self.rect = self.image.get_rect(bottomleft=(x,y))

    def _update_color(self):
        time_ms = pygame.time.get_ticks() / 100.0 + self.time_offset
        pulse = (math.sin(time_ms) + 1) / 2 * 0.4 
        
        bright_base = self.base_color_tuple[0]
        dark_base = self.base_color_tuple[1]

        r = int(dark_base[0] + (bright_base[0] - dark_base[0]) * pulse)
        g = int(dark_base[1] + (bright_base[1] - dark_base[1]) * pulse)
        b = int(dark_base[2] + (bright_base[2] - dark_base[2]) * pulse)
        
        current_color = (r, g, b)
        
        self.image.fill((0,0,0,0)) 
        pygame.draw.rect(self.image, current_color,(0,0,self.width,self.height),5)

    def update(self):
        self.rect.x -= SCROLL_SPEED 
        self._update_color() 
    
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

# ----------------------------------------------------------------------
# --- 4. FUNCIONES DE DIBUJO Y AYUDA ---
# ----------------------------------------------------------------------

def get_current_section_color(index, section_markers):
    """Devuelve la tupla de color (brillante, oscuro) para el índice de nivel dado."""
    current_section_idx = 0
    full_markers = sorted(list(set(section_markers)))
    if not full_markers or full_markers[-1] < len(LEVEL_MAP):
        full_markers.append(len(LEVEL_MAP))

    for idx_marker in range(len(full_markers) - 1):
        start = full_markers[idx_marker]
        end = full_markers[idx_marker+1]
        if start <= index < end:
            current_section_idx = idx_marker
            break
            
    if index >= len(LEVEL_MAP) - 1 and len(full_markers) > 1:
        current_section_idx = len(full_markers) - 2
        
    return SECTION_COLORS[current_section_idx % len(SECTION_COLORS)]

def create_level_objects(level_map, spikes_group, portal_group):
    global WIDTH, GROUND_Y, SECTION_INDICES
    
    for i, obj_type in enumerate(level_map):
        x_pos = WIDTH + (i * SPIKE_SIZE)
        y_pos = GROUND_Y
        
        section_color_tuple = get_current_section_color(i, SECTION_INDICES)

        if obj_type == 1:
            spikes_group.add(Spike(x_pos, y_pos, section_color_tuple))
        elif obj_type == 9:
            portal_group.add(Portal(x_pos, y_pos, section_color_tuple))

def draw_color_overlay(surface, color, alpha):
    global WIDTH, HEIGHT
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(color) 
    overlay.set_alpha(alpha)
    surface.blit(overlay, (0, 0))

def draw_progress_bar(surface, current_scroll, level_length):
    global WIDTH
    try:
        font = pygame.font.SysFont("Arial", 24, bold=True)
    except:
        font = pygame.font.Font(None, 24)
        
    BAR_HEIGHT = 20
    BAR_Y = 10
    
    BAR_WIDTH = WIDTH // 2 
    BAR_X = WIDTH // 2 - BAR_WIDTH // 2 

    progress_ratio = max(0.0, min(1.0, current_scroll / level_length))
    
    progress_width = BAR_WIDTH * progress_ratio
    
    # Fondo de la barra
    pygame.draw.rect(surface,(100,100,100),(BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT), border_radius=5)
    
    # Barra de progreso
    if progress_width > 0:
        pygame.draw.rect(surface,PROGRESS_BAR_COLOR,(BAR_X, BAR_Y, progress_width, BAR_HEIGHT), border_radius=5)
    
    # Texto de porcentaje
    text = font.render(f"{int(progress_ratio*100)}%", True, BLACK)
    surface.blit(text,(WIDTH//2 - text.get_width()//2,BAR_Y))

def draw_button_aesthetic(surface, text, center_pos, button_width, button_height, base_color, hover_color, text_color, font, mouse_pos):
    
    is_hovering = False
    
    # 1. Calcular el rectángulo principal (rect_main) y el de sombra (rect_shadow)
    rect_main = pygame.Rect(0, 0, button_width, button_height)
    rect_main.center = center_pos
    
    rect_shadow = pygame.Rect(rect_main.x + 2, rect_main.y + 4, button_width - 4, button_height - 4)
    
    # 2. Comprobar si el ratón está sobre el botón
    is_hovering = rect_main.collidepoint(mouse_pos)
    
    # 3. Ajustar la posición y color si el ratón está sobre el botón
    if is_hovering:
        current_color = hover_color
        # Efecto "elevado" (la sombra se mueve menos)
        shadow_offset_y = 2 
        rect_main.y -= 1
        rect_shadow.y = rect_main.y + shadow_offset_y
    else:
        current_color = base_color
        # Sombra normal (efecto 3D)
        shadow_offset_y = 4 
        rect_shadow.y = rect_main.y + shadow_offset_y
        
    # 4. Dibujar la sombra
    pygame.draw.rect(surface, BUTTON_SHADOW, rect_shadow, border_radius=10)
    
    # 5. Dibujar el cuerpo principal del botón
    pygame.draw.rect(surface, current_color, rect_main, border_radius=10)
    
    # 6. Dibujar el borde blanco
    pygame.draw.rect(surface, BUTTON_BORDER, rect_main, 3, border_radius=10)
    
    # 7. Dibujar el texto
    button_text_surface = font.render(text, True, text_color)
    button_text_rect = button_text_surface.get_rect(center=rect_main.center)
    surface.blit(button_text_surface, button_text_rect)
    
    return rect_main

def draw_game_over_screen(surface, mouse_pos):
    global WIDTH, HEIGHT, WHITE, BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, BUTTON_SECONDARY, BUTTON_SECONDARY_HOVER, TEXT_COLOR
    
    try:
        font_large = pygame.font.SysFont("Arial", 80, bold=True)
        font_button = pygame.font.SysFont("Arial", 40, bold=True)
    except:
        font_large = pygame.font.Font(None, 80)
        font_button = pygame.font.Font(None, 40)
    
    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 180))
    surface.blit(dark_overlay, (0, 0))
    
    text_surface = font_large.render("¡GAME OVER!", True, (255, 50, 50)) 
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    surface.blit(text_surface, text_rect)
    
    # Ancho ajustado a 250px para que 'REINTENTAR' quepa bien.
    BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
    
    # Botón REINTENTAR (Color Primario)
    retry_button_rect = draw_button_aesthetic(
        surface, "REINTENTAR", 
        (WIDTH // 2 - BUTTON_WIDTH // 2 - 20, HEIGHT // 2 + 50), 
        BUTTON_WIDTH, BUTTON_HEIGHT, 
        BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, 
        TEXT_COLOR, font_button, mouse_pos
    )
    
    # Botón MENÚ (Color Secundario)
    menu_button_rect = draw_button_aesthetic(
        surface, "MENÚ", 
        (WIDTH // 2 + BUTTON_WIDTH // 2 + 20, HEIGHT // 2 + 50), 
        BUTTON_WIDTH, BUTTON_HEIGHT, 
        BUTTON_SECONDARY, BUTTON_SECONDARY_HOVER, 
        TEXT_COLOR, font_button, mouse_pos
    )
    
    return retry_button_rect, menu_button_rect

def draw_victory_screen(surface, mouse_pos):
    global WIDTH, HEIGHT, BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, BUTTON_SECONDARY, BUTTON_SECONDARY_HOVER, TEXT_COLOR
    
    try:
        font_large = pygame.font.SysFont("Arial", 80, bold=True)
        font_button = pygame.font.SysFont("Arial", 40, bold=True)
    except:
        font_large = pygame.font.Font(None, 80)
        font_button = pygame.font.Font(None, 40)
    
    dark_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_overlay.fill((0, 0, 0, 180))
    surface.blit(dark_overlay, (0, 0))
    
    text_surface = font_large.render("¡NIVEL SUPERADO!", True, (255, 255, 0)) 
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    surface.blit(text_surface, text_rect)
    
    # Ancho ajustado a 250px para que 'REINTENTAR' quepa bien.
    BUTTON_WIDTH, BUTTON_HEIGHT = 250, 60
    
    # Botón VOLVER A JUGAR (REINTENTAR - Color Primario)
    play_button_rect = draw_button_aesthetic(
        surface, "REINTENTAR", 
        (WIDTH // 2 - BUTTON_WIDTH // 2 - 20, HEIGHT // 2 + 50), 
        BUTTON_WIDTH, BUTTON_HEIGHT, 
        BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER, 
        TEXT_COLOR, font_button, mouse_pos
    )
    
    # Botón MENÚ (Color Secundario)
    menu_button_rect = draw_button_aesthetic(
        surface, "MENÚ", 
        (WIDTH // 2 + BUTTON_WIDTH // 2 + 20, HEIGHT // 2 + 50), 
        BUTTON_WIDTH, BUTTON_HEIGHT, 
        BUTTON_SECONDARY, BUTTON_SECONDARY_HOVER, 
        TEXT_COLOR, font_button, mouse_pos
    )
    
    return play_button_rect, menu_button_rect

def draw_back_to_menu_button(surface, mouse_pos):
    BUTTON_SIZE = 40
    BUTTON_MARGIN = 10
    MENU_BUTTON_RECT = pygame.Rect(BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE) 
    
    is_hovering = MENU_BUTTON_RECT.collidepoint(mouse_pos)
    
    base_color = (150, 150, 150) # Gris suave para botón de pausa
    
    # Calcular el color de fondo y el desplazamiento para el efecto hover/click
    bg_color = base_color
    arrow_color = WHITE
    offset = 0
    if is_hovering:
        bg_color = (200, 200, 200)
        offset = -1 # Pequeño desplazamiento hacia arriba

    # Dibujar la sombra del botón
    shadow_rect = MENU_BUTTON_RECT.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2
    pygame.draw.circle(surface, BUTTON_SHADOW, shadow_rect.center, BUTTON_SIZE // 2, 0)
    
    # Dibujar el cuerpo del botón
    button_center = (MENU_BUTTON_RECT.centerx, MENU_BUTTON_RECT.centery + offset)
    pygame.draw.circle(surface, bg_color, button_center, BUTTON_SIZE // 2, 0)
    pygame.draw.circle(surface, BLACK, button_center, BUTTON_SIZE // 2, 2)
    
    # Dibujar el icono de menú/pausa (ejemplo: un icono de casa simple)
    # Triángulo de techo
    pygame.draw.polygon(surface, arrow_color, [
        (button_center[0], button_center[1] - 8),
        (button_center[0] - 10, button_center[1] + 2),
        (button_center[0] + 10, button_center[1] + 2)
    ])
    # Rectángulo de cuerpo de casa
    pygame.draw.rect(surface, arrow_color, pygame.Rect(button_center[0]-7, button_center[1]+2, 14, 10))
    
    return MENU_BUTTON_RECT 

def check_collision(player, obstacles):
    spike_hit = pygame.sprite.spritecollide(player, obstacles['spikes'], False, pygame.sprite.collide_mask)
    portal_hit = pygame.sprite.spritecollide(player, obstacles['portal'], False)
    return spike_hit, portal_hit

def load_and_scale_background(filename, w, h):
    global BASE_DIR
    path = os.path.join(BASE_DIR, filename)
    path = os.path.normpath(path) 
    if os.path.exists(path):
        try:
            temp_image = pygame.image.load(path).convert_alpha() 
            scaled_image = pygame.transform.scale(temp_image, (w, h)) 
            return scaled_image
        except pygame.error as e:
            print(f"Error de Pygame al reescalar o cargar la imagen: {e}. Ruta: {path}")
            return None
        except Exception as e:
            print(f"Error desconocido al reescalar la imagen: {e}. Ruta: {path}")
            return None
    return None

def load_music(filename):
    global BASE_DIR
    path = os.path.join(BASE_DIR, filename)
    path = os.path.normpath(path) 
    if os.path.exists(path):
        return path
    print(f"Advertencia: Archivo de música no encontrado en: {path}")
    return None

# ----------------------------------------------------------------------
# --- 5. LÓGICA DE JUEGO (run_level) ---
# ----------------------------------------------------------------------

def run_level(screen):
    
    global SCREEN, WIDTH, HEIGHT, GROUND_Y, BACKGROUND_IMAGE, BACKGROUND_FILE, SCROLL_SPEED, SCROLL_SPEED_BASE, game_over_time, MUSIC_FILE, SECTION_INDICES, TINT_COLORS, TINT_ALPHA

    SCREEN = screen
    SCROLL_SPEED = SCROLL_SPEED_BASE
    
    WIDTH, HEIGHT = SCREEN.get_size()
    GROUND_Y = HEIGHT - 100
    
    game_over_time = 0 
    
    BACKGROUND_IMAGE = load_and_scale_background(BACKGROUND_FILE, WIDTH, HEIGHT)

    music_path = load_music(MUSIC_FILE)
    if music_path:
        try:
            if not pygame.mixer.music.get_busy(): 
                pygame.mixer.music.load(music_path) 
                pygame.mixer.music.play(-1, 55.0) 
        except pygame.error as e:
            print(f"Advertencia: No se pudo reproducir la música de fondo: {e}.")
    
    player = CubePlayer(100, GROUND_Y-SPIKE_SIZE) 
    spikes = pygame.sprite.Group()
    portal_group = pygame.sprite.Group()
    trail_group = pygame.sprite.Group() 
    
    create_level_objects(LEVEL_MAP, spikes, portal_group)
    
    scroll_distance = 0
    level_finished = False 
    running = True
    fullscreen = False
    
    current_section_index = 0
    current_tint_color = TINT_COLORS[current_section_index % len(TINT_COLORS)]
    
    mouse_click_down = False 

    while running:
        
        mouse_click_down = False 
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                pygame.mixer.music.stop()
                return "QUIT"
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    pygame.mixer.music.stop()
                    return "MENU" 
                
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        SCREEN = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
                    
                    WIDTH, HEIGHT = SCREEN.get_size()
                    GROUND_Y = HEIGHT - 100
                    BACKGROUND_IMAGE = load_and_scale_background(BACKGROUND_FILE, WIDTH, HEIGHT)
                    spikes.empty()
                    portal_group.empty()
                    trail_group.empty()
                    create_level_objects(LEVEL_MAP, spikes, portal_group)
                    player.rect.y = GROUND_Y - player.size 

            if event.type == pygame.VIDEORESIZE and not fullscreen:
                new_width = max(START_WIDTH, event.w)
                new_height = max(START_HEIGHT, event.h)
                SCREEN = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                
                WIDTH, HEIGHT = SCREEN.get_size()
                GROUND_Y = HEIGHT - 100
                BACKGROUND_IMAGE = load_and_scale_background(BACKGROUND_FILE, WIDTH, HEIGHT)
                spikes.empty()
                portal_group.empty()
                trail_group.empty()
                create_level_objects(LEVEL_MAP, spikes, portal_group)
                player.rect.y = GROUND_Y - player.size 

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_down = True
                if not player.is_dead and not level_finished:
                    player.jump() # <-- Permite el salto si ya está en el suelo (mantiene la lógica de salto que te gusta)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if not player.is_dead and not level_finished:
                    player.jump() # <-- Permite el salto si ya está en el suelo (mantiene la lógica de salto que te gusta)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if player.is_dead: 
                    # Se usa draw_game_over_screen para obtener los rects con la posición actual del ratón
                    retry_rect, menu_rect = draw_game_over_screen(SCREEN, event.pos) 
                    if retry_rect.collidepoint(event.pos):
                        return "LEVEL" 
                    if menu_rect.collidepoint(event.pos):
                        return "MENU" 
                
                if level_finished: 
                    play_rect, menu_rect = draw_victory_screen(SCREEN, event.pos) 
                    if play_rect.collidepoint(event.pos):
                        return "LEVEL" 
                    if menu_rect.collidepoint(event.pos):
                        return "MENU" 
                
                if not player.is_dead and not level_finished:
                    menu_button_rect = draw_back_to_menu_button(SCREEN, event.pos) 
                    if menu_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        return "MENU"
         # --- AUTO-JUMP (mantener tecla arriba o espacio) ---
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and player.on_ground and not player.is_dead and not level_finished:
            player.jump()

        # --- LÓGICA DE ACTUALIZACIÓN ---
        if not player.is_dead and not level_finished:
            
            current_level_index = int((scroll_distance + player.rect.x) / SPIKE_SIZE)
            current_section_color_tuple = get_current_section_color(current_level_index, SECTION_INDICES)
            
            try:
                current_marker_index = 0
                full_markers = sorted(list(set(SECTION_INDICES)))
                if not full_markers or full_markers[-1] < len(LEVEL_MAP): full_markers.append(len(LEVEL_MAP))
                for i in range(len(full_markers) - 1):
                    if full_markers[i] <= current_level_index < full_markers[i+1]:
                        current_marker_index = i
                        break
                
                target_tint_color = TINT_COLORS[current_marker_index % len(TINT_COLORS)]
                
                lerp_factor = 0.05
                current_tint_color = tuple(
                    int(current_tint_color[i] + (target_tint_color[i] - current_tint_color[i]) * lerp_factor)
                    for i in range(3)
                )

            except Exception as e:
                current_tint_color = (200, 200, 200) 

            spikes.update()
            portal_group.update()
            trail_group.update() 
            
            player.update(trail_group, current_section_color_tuple)
            scroll_distance += SCROLL_SPEED
            
            spike_hit, portal_hit = check_collision(player, {'spikes': spikes, 'portal': portal_group})
            
            if spike_hit:
                player.is_dead = True
                SCROLL_SPEED = 0 
                game_over_time = pygame.time.get_ticks()
                # --- Detener la música al morir (mantenido) ---
                pygame.mixer.music.stop()

            if portal_hit and scroll_distance >= LEVEL_LENGTH - WIDTH:
                level_finished = True
                SCROLL_SPEED = 0
                pygame.mixer.music.fadeout(500) 

        # --- LÓGICA DE DIBUJO ---
        
        if BACKGROUND_IMAGE:
            SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
        else:
            SCREEN.fill(BLACK)
            
        draw_color_overlay(SCREEN, current_tint_color, TINT_ALPHA)
        
        pygame.draw.rect(SCREEN, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        
        trail_group.draw(SCREEN)

        for spike in spikes:
            spike.draw(SCREEN)
        portal_group.draw(SCREEN)
        
        player.draw(SCREEN)
        
        draw_progress_bar(SCREEN, scroll_distance, LEVEL_LENGTH)
        
        if not player.is_dead and not level_finished:
            draw_back_to_menu_button(SCREEN, mouse_pos)

        if player.is_dead:
            draw_game_over_screen(SCREEN, mouse_pos)
                
        if level_finished:
            draw_victory_screen(SCREEN, mouse_pos)

        pygame.display.flip()
        CLOCK.tick(FPS)

# ----------------------------------------------------------------------
# --- 6. BUCLE PRINCIPAL (main) ---
# ----------------------------------------------------------------------

def main():
    global SCREEN, WIDTH, HEIGHT, START_WIDTH, START_HEIGHT
    
    SCREEN = pygame.display.set_mode((START_WIDTH, START_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Dash")
    
    game_state = "MENU" 

    while game_state != "QUIT":
        
        if game_state == "LEVEL":
            game_state = run_level(SCREEN)
            
        elif game_state == "MENU":
            menu_running = True
            
            try:
                font_title = pygame.font.SysFont("Arial", 60, bold=True)
                font_button = pygame.font.SysFont("Arial", 40)
            except:
                font_title = pygame.font.Font(None, 60)
                font_button = pygame.font.Font(None, 40)
            
            title_text = font_title.render("PYGAME DASH", True, MENU_BUTTON_VISUAL_COLOR)
            
            start_button_width, start_button_height = 250, 70
            start_button_center = (WIDTH // 2, HEIGHT // 2 + 50)
            
            while menu_running:
                mouse_pos = pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_state = "QUIT"
                        menu_running = False
                    if event.type == pygame.K_ESCAPE:
                        game_state = "QUIT"
                        menu_running = False
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        # Se usa draw_button_aesthetic para obtener el rect con la posición actual del ratón
                        start_rect_temp = draw_button_aesthetic(
                            SCREEN, "EMPEZAR", 
                            start_button_center, 
                            start_button_width, start_button_height,
                            BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER,
                            TEXT_COLOR, font_button, mouse_pos
                        )
                        if start_rect_temp.collidepoint(event.pos):
                            game_state = "LEVEL"
                            menu_running = False
                        
                    if event.type == pygame.VIDEORESIZE:
                        new_width = max(START_WIDTH, event.w)
                        new_height = max(START_HEIGHT, event.h)
                        SCREEN = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                        WIDTH, HEIGHT = SCREEN.get_size() 
                        start_button_center = (WIDTH // 2, HEIGHT // 2 + 50) 
                        title_text = font_title.render("PYGAME DASH", True, MENU_BUTTON_VISUAL_COLOR) 

                SCREEN.fill(BLACK)
                
                title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                SCREEN.blit(title_text, title_rect)
                
                # Dibujar el botón "Empezar" con estética mejorada
                draw_button_aesthetic(
                    SCREEN, "EMPEZAR", 
                    start_button_center, 
                    start_button_width, start_button_height,
                    BUTTON_PRIMARY, BUTTON_PRIMARY_HOVER,
                    TEXT_COLOR, font_button, mouse_pos
                )
                
                pygame.display.flip()
                CLOCK.tick(30)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()