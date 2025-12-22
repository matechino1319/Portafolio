import pygame
import sys
import random
import os
import math 
import time 
import level_one 

# 🎵 REEMPLAZA ESTO CON EL NOMBRE DE TU ARCHIVO DE MÚSICA (ej: "tu_cancion.ogg")
MUSIC_FILENAME = "Habits - Vintage 1930's Jazz Tove Lo Cover ft. Haley Reinhart.mp3" 
# ⚠️ ADVERTENCIA: Si el nombre largo falla, renómbralo a algo simple como "habits.mp3" y actualiza aquí.

# --- CONFIGURACIÓN ESTÁTICA ---
WIDTH, HEIGHT = 800, 600 # Dimensiones base de referencia
CUBE_COUNT = 15 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_MAGENTA = (40, 0, 40)
GROUND_COLOR = (150, 50, 150) 
FPS = 60
HUE_SPEED = 1.0
TRANSITION_DURATION = 1500 # Duración de la pausa en milisegundos (1.5 segundos)

# Variables Globales
SCREEN = None
CLOCK = None
BACKGROUND_HUE = 0 
TITLE_PARTICLES = pygame.sprite.Group() 

# 🆕 VARIABLES GLOBALES DINÁMICAS (Para redimensionamiento)
current_width = WIDTH
current_height = HEIGHT
TITLE_Y_BASE = HEIGHT // 2 - 50 
BUTTON_Y_BASE_MENU = HEIGHT // 2 + 50
BUTTON_Y_BASE_LEVEL = HEIGHT // 2 - 20 

# --- FUNCIONES DE UTILIDAD (Sin cambios aquí) ---
# ... (hsv_to_rgb, get_text_data, draw_text_static, play_music son las mismas)
# --------------------------------------------------

def hsv_to_rgb(h, s, v):
    if s == 0.0: return (int(v * 255), int(v * 255), int(v * 255))
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    colors = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    r, g, b = colors[int(i % 6)]
    return (int(r * 255), int(g * 255), int(b * 255))

def get_text_data(text, font_size, color):
    font = pygame.font.Font(None, font_size)
    surf = font.render(text, True, color)
    width, height = surf.get_size()
    
    start_x = current_width // 2 - width // 2
    start_y = current_height // 2 - (100 // 2) - 50 
    
    particles_data = []
    for x in range(width):
        for y in range(height):
            if x < surf.get_width() and y < surf.get_height() and surf.get_at((x, y))[3] > 0: 
                particles_data.append({
                    'target_x': start_x + x, 
                    'target_y': start_y + y, 
                    'color': surf.get_at((x, y))
                })
    return particles_data

def draw_text_static(surface, text, font_size, color, center_x, center_y):
    font = pygame.font.Font(None, font_size)
    text_surf = font.render(text, True, color)
    dy = (current_height - HEIGHT) // 2
    
    new_center_x = current_width // 2 
    new_center_y = center_y + dy 
    text_rect = text_surf.get_rect(center=(new_center_x, new_center_y))
    surface.blit(text_surf, text_rect)

def play_music(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, filename)
    
    if os.path.exists(file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"🛑 Error al reproducir {filename}: {e}.")
    else:
        print(f"❌ ADVERTENCIA: Archivo de música '{filename}' NO encontrado en la carpeta del script.")


# --- NUEVA FUNCIÓN DE TRANSICIÓN ---

def load_level_transition(screen, clock, level_name):
    """Muestra una pantalla de carga y desvanece la música."""
    
    # 1. Desvanece la música del menú durante la transición
    # 500ms es un desvanecimiento rápido
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(500)
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < TRANSITION_DURATION:
        
        # Manejo de eventos (para poder salir si es necesario)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.VIDEORESIZE:
                # Si se redimensiona durante la carga, actualizamos las dimensiones
                global current_width, current_height
                current_width, current_height = event.size
                global SCREEN 
                SCREEN = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

        # 2. Dibujar la pantalla de carga
        screen.fill(BLACK) # Fondo negro o un color sólido
        
        # Texto de "Cargando..."
        draw_text_static(
            screen, 
            f"CARGANDO NIVEL: {level_name}", 
            50, 
            WHITE, 
            current_width // 2, 
            current_height // 2
        )

        # Barra de progreso simple (animación)
        time_passed = pygame.time.get_ticks() - start_time
        progress = time_passed / TRANSITION_DURATION
        bar_width = int(current_width * 0.6 * progress)
        bar_height = 10
        
        bar_x = current_width // 2 - int(current_width * 0.6) // 2
        bar_y = current_height // 2 + 50
        
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, int(current_width * 0.6), bar_height), 2)
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    return level_name # Retorna el estado del nivel para que el bucle principal lo ejecute


# --- CLASES (Sin cambios sustanciales) ---

class Player(pygame.sprite.Sprite):
    # ... (código Player, con ajustes dinámicos)
    def __init__(self, x, y, size):
        super().__init__()
        self.original_x = x
        self.original_y = y 
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity_y = 0
        self.on_ground = False
        self.jump_timer = random.randint(60, 180) 

    def update(self):
        dx = (current_width - WIDTH) // 2
        dy = (current_height - HEIGHT) // 2
        
        self.rect.x = self.original_x + dx
        
        self.velocity_y += 1 
        self.rect.y += self.velocity_y
        
        ground_y = 500 + dy
        
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True
        if self.on_ground:
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.jump()
                self.jump_timer = random.randint(60, 180)
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = -18
            self.on_ground = False

    def draw(self, surface, current_hue):
        dynamic_color = hsv_to_rgb(current_hue / 360, 1.0, 1.0) 
        pygame.draw.rect(surface, dynamic_color, self.rect, 4) 
        pygame.draw.rect(surface, dynamic_color, self.rect, 2)
        pygame.draw.rect(surface, dynamic_color, self.rect, 1)

class TitleParticle(pygame.sprite.Sprite):
    # ... (código TitleParticle)
    def __init__(self, target_x, target_y, color, is_falling):
        super().__init__()
        self.target_x, self.target_y = target_x, target_y 
        self.color = color
        self.is_falling = is_falling
        self.alpha = 255
        self.gravity = 0.2
        self.speed = 10 
        
        if self.is_falling:
            self.rect = pygame.Rect(target_x, target_y, 1, 1)
            self.velocity_x = random.uniform(-1, 1) 
            self.velocity_y = random.uniform(1, 3) 
        else:
            self.rect = pygame.Rect(random.randint(0, current_width), -50, 1, 1) 
            
        self.update_image()
        
    def update_image(self):
        self.image = pygame.Surface([1, 1], pygame.SRCALPHA)
        fade_color = (self.color[0], self.color[1], self.color[2], max(0, self.alpha))
        self.image.set_at((0, 0), fade_color)
        
    def update(self):
        if self.is_falling:
            self.velocity_y += self.gravity
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.alpha -= 5 
            if self.alpha <= 0:
                self.kill()
        else: 
            dx = self.target_x - self.rect.x
            dy = self.target_y - self.rect.y
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                self.rect.x += dx / dist * self.speed
                self.rect.y += dy / dist * self.speed
            else:
                self.rect.x, self.rect.y = self.target_x, self.target_y
                self.speed = 0 
            self.alpha = min(255, self.alpha + 10) 
        self.update_image()

class HoverButton:
    # ... (código HoverButton)
    def __init__(self, text, x, y, width, height, action, base_y_anchor):
        self.base_x = x 
        self.base_y = y 
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font(None, 40)
        self.base_y_anchor = base_y_anchor

    def recalculate_position(self):
        dy = (current_height - HEIGHT) // 2
        new_x = current_width // 2 - self.width // 2
        new_y = self.base_y + dy
        self.rect.topleft = (new_x, new_y)

    def draw(self, surface, mouse_pos, current_hue):
        self.recalculate_position()
        
        base_color = hsv_to_rgb(current_hue / 360, 1.0, 1.0)
        hover_color = hsv_to_rgb(current_hue / 360, 1.0, 0.7)
            
        is_hovering = self.rect.collidepoint(mouse_pos)
        current_color = hover_color if is_hovering else base_color
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, current_color, self.rect, 5, border_radius=10) 
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TitleManager:
    # ... (código TitleManager)
    def __init__(self):
        self.data = get_text_data("GEOMETRY PRO", 100, WHITE)
        self.state = "START" 
        self.start_time = time.time()
        self.delay_time = 3.0 
    
    def recalculate_particles(self):
        self.data = get_text_data("GEOMETRY PRO", 100, WHITE)
        self.launch_falling()
        self.state = "FALLING"
        self.start_time = time.time()

    def update(self):
        if self.state == "START":
            self.launch_falling()
            self.state = "FALLING"
            self.start_time = time.time()
        elif self.state == "FALLING":
            if len(TITLE_PARTICLES) < 5 and (time.time() - self.start_time > 1.0):
                self.state = "WAIT_REGENERATE"
                self.start_time = time.time()
        elif self.state == "WAIT_REGENERATE":
            if time.time() - self.start_time > self.delay_time:
                self.launch_regenerate()
                self.state = "REGENERATE"
        elif self.state == "REGENERATE":
            is_complete = all(p.speed == 0 for p in TITLE_PARTICLES)
            if is_complete:
                self.state = "WAIT_FALLING"
                self.start_time = time.time()
        elif self.state == "WAIT_FALLING":
            if time.time() - self.start_time > 2.0:
                self.launch_falling()
                self.state = "FALLING"
                self.start_time = time.time()

    def launch_falling(self):
        TITLE_PARTICLES.empty()
        for item in self.data:
            TITLE_PARTICLES.add(TitleParticle(item['target_x'], item['target_y'], item['color'], is_falling=True))

    def launch_regenerate(self):
        TITLE_PARTICLES.empty()
        for item in self.data:
            TITLE_PARTICLES.add(TitleParticle(item['target_x'], item['target_y'], item['color'], is_falling=False))


def handle_resize(event, title_manager):
    """Actualiza las dimensiones globales y recrea la pantalla."""
    global SCREEN, current_width, current_height
    if event.type == pygame.VIDEORESIZE:
        current_width, current_height = event.size
        SCREEN = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
        title_manager.recalculate_particles()
        return True 
    return False

# --- BUCLE PRINCIPAL DEL MENÚ ---

def menu_loop():
    global BACKGROUND_HUE 
    global SCREEN, CLOCK 
    
    play_music(MUSIC_FILENAME) 
    
    title_manager = TitleManager() 
    animated_sprites = pygame.sprite.Group()
    
    # Inicialización dinámica de cubos
    for i in range(CUBE_COUNT):
        x_pos = 50 + i * ((WIDTH - 100) / (CUBE_COUNT - 1)) if CUBE_COUNT > 1 else WIDTH // 2
        cube = Player(x_pos, 400, 30) 
        animated_sprites.add(cube)

    # Inicialización de botones
    main_menu_button = HoverButton(
        "NIVELES", 
        WIDTH // 2 - 120, BUTTON_Y_BASE_MENU, 240, 60, "LEVEL_SELECT", BUTTON_Y_BASE_MENU
    )
    level_maradona_btn = HoverButton(
        "MARADONA", 
        WIDTH // 2 - 120, BUTTON_Y_BASE_LEVEL, 240, 60, "MARADONA", BUTTON_Y_BASE_LEVEL
    )
    
    current_state = "MAIN_MENU" 
        
    running = True
    while running:
        
        BACKGROUND_HUE = (BACKGROUND_HUE + HUE_SPEED) % 360
        mouse_pos = pygame.mouse.get_pos()
        
        # --- Manejo de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" 
            
            handle_resize(event, title_manager)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if current_state == "LEVEL_SELECT":
                    current_state = "MAIN_MENU"
                else:
                    return "QUIT" 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == "MAIN_MENU" and main_menu_button.is_clicked(event.pos):
                    current_state = "LEVEL_SELECT"
                elif current_state == "LEVEL_SELECT" and level_maradona_btn.is_clicked(event.pos):
                    
                    # 🚀 ¡AQUÍ ESTÁ EL CAMBIO CLAVE!
                    # Llamamos a la transición antes de salir del menú.
                    # Esto garantiza la pausa y el desvanecimiento de la música.
                    return load_level_transition(SCREEN, CLOCK, "MARADONA")
                    
        
        # --- Actualizaciones y Dibujo ---
        animated_sprites.update()
        title_manager.update()
        TITLE_PARTICLES.update()
        
        SCREEN.fill(DARK_MAGENTA) 
        
        ground_y_draw = 500 + (current_height - HEIGHT) // 2
        pygame.draw.line(SCREEN, GROUND_COLOR, (0, ground_y_draw), (current_width, ground_y_draw), 10)
        
        for cube in animated_sprites:
            cube.draw(SCREEN, BACKGROUND_HUE) 

        TITLE_PARTICLES.draw(SCREEN)

        if current_state == "MAIN_MENU":
            main_menu_button.draw(SCREEN, mouse_pos, BACKGROUND_HUE)
            
        elif current_state == "LEVEL_SELECT":
            level_maradona_btn.draw(SCREEN, mouse_pos, BACKGROUND_HUE)
            
            draw_text_static(SCREEN, "Canción: Qué es Dios", 30, GRAY, current_width // 2, level_maradona_btn.rect.bottom + 30)
            draw_text_static(SCREEN, "PRÓXIMAMENTE MÁS NIVELES", 35, WHITE, current_width // 2, HEIGHT - 50)


        pygame.display.flip()
        CLOCK.tick(FPS)
        
    return "QUIT"

def run_menu():
    return menu_loop()

if __name__ == "__main__":
    
    pygame.init() 
    pygame.mixer.init()
    
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    current_width = WIDTH
    current_height = HEIGHT
    
    pygame.display.set_caption("GEOMETRY PRO - Menú de Niveles Dinámico")
    CLOCK = pygame.time.Clock()

    game_state = "MENU" 
    
    while game_state != "QUIT":
        
        if game_state == "MENU":
            game_state = run_menu() 
            
        elif game_state == "MARADONA" or game_state == "LEVEL":
            
            # Aseguramos que la música se detenga completamente si el fadeout falló
            if pygame.mixer.music.get_busy():
                 pygame.mixer.music.stop()
                 
            # Ejecutamos el nivel
            game_state = level_one.run_level(SCREEN) 
            
            
    if pygame.get_init():
        pygame.quit()
    sys.exit()