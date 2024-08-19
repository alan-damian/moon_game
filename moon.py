import pygame
import random

pygame.init()

# Inicia la pantalla del juego en una ventana
w, h = 1000, 600
reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption('mi juego')

# Colores básicos para el juego
rojo = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)
negro = (0, 0, 0)
blanco = (255, 255, 255)

# Fondo blanco en la pantalla
pantalla.fill(blanco)

# Icono y título
icono = pygame.image.load('./static/logo_juego.png')
pygame.display.set_icon(icono)
pygame.display.set_caption('MOON')

# Fondo estático
fondo = pygame.image.load('./static/fondo_arcade_1.png')

# Ubicación del fondo

x = 0

# Clase Jugador-------------------------------------------------------------------------
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Parámetros
        self.rect = pygame.Rect(x, y, 10, 20)
        self.velocidad = 8
        self.direccion = None
        self.cuenta_pasos = 0
        self.movimiento_fondo = False
        self.limite_derecha = w - self.rect.width
        self.saltando = False
        self.velocidad_salto = 20
        self.gravedad = 2
        # Imágenes
        self.quieto = pygame.image.load('./static/moon_stand_r.png')
        self.camina_R = [pygame.image.load('./static/moon_run_r.png'),
                         pygame.image.load('./static/moon_run_r.png'),
                         pygame.image.load('./static/moon_run_r2.png'),
                         pygame.image.load('./static/moon_run_r3.png'),
                         pygame.image.load('./static/moon_run_r2.png'),
                         pygame.image.load('./static/moon_run_r3.png')]
        self.camina_L = [pygame.image.load('./static/moon_run_l.png'),
                         pygame.image.load('./static/moon_run_l.png'),
                         pygame.image.load('./static/moon_run_l2.png'),
                         pygame.image.load('./static/moon_run_l3.png'),
                         pygame.image.load('./static/moon_run_l2.png'),
                         pygame.image.load('./static/moon_run_l3.png')]

    def movimiento(self):
        if self.cuenta_pasos + 1 >= 6:
            self.cuenta_pasos = 0

        if self.direccion == 'izquierda':
            pantalla.blit(self.camina_L[self.cuenta_pasos // 1], self.rect)
            self.cuenta_pasos += 1

        elif self.direccion == 'derecha':
            pantalla.blit(self.camina_R[self.cuenta_pasos // 1], self.rect)
            self.cuenta_pasos += 1

        else:
            pantalla.blit(self.quieto, self.rect)

    def salto(self):
        if not self.saltando:
            self.saltando = True
            self.velocidad_salto = 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > self.velocidad:
            self.rect.x -= self.velocidad
            self.direccion = 'izquierda'
            self.movimiento_fondo = False
        elif keys[pygame.K_d] and self.rect.x < 1200:
            self.rect.x += self.velocidad
            self.direccion = 'derecha'
            self.movimiento_fondo = True
        elif keys[pygame.K_w] and not self.saltando:
            self.salto()
        else:
            self.direccion = None
            self.cuenta_pasos = 0
            self.movimiento_fondo = False
            
        if self.saltando:
            self.rect.y -= self.velocidad_salto
            self.velocidad_salto -= self.gravedad
            if self.rect.y >= 492:
                self.saltando = False
                self.rect.y = 492
                self.velocidad_salto = 20
                
#creacion clase disparo.--------------------------------------------------------------
class DisparoEnemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion):
        super().__init__()
        self.rect = pygame.Rect(x, 492, 10, 10)
        self.velocidad = 10
        self.direccion = direccion
        self.imagen = pygame.image.load('./static/hunter-son-disparo.png')

    def update(self):
        if self.direccion == 'izquierda':
            self.rect.x -= self.velocidad
        elif self.direccion == 'derecha':
            self.imagen = pygame.image.load('./static/hunter-son-disparo-r.png')
            self.rect.x += self.velocidad

#clase enemigo.------------------------------------------------------------------------
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidad = 4
        self.imagen = pygame.image.load('./static/hunter-son.png')
        self.disparos = pygame.sprite.Group()

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.x < 0:
            self.rect.x = w
    
    def disparar(self):
        if self.rect.x < jugador.rect.x:
            direccion = 'derecha'
        else:
            direccion = 'izquierda'
        disparo = DisparoEnemigo(self.rect.x, self.rect.y, direccion)
        self.disparos.add(disparo)
        
#clase vidas---------------------------------------------------------------------------
class Vidas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 30)
        self.imagen = pygame.image.load("./static/moon_health.png")
        
    def mostrar(self):
        pantalla.blit(vidas.imagen, vidas.rect)    

# Lista para almacenar las instancias de Vidas
vidas_lista = []

# INSTANCIAS///////////////////////////////////////////////////////////////////////////
jugador = Jugador(50, 492)
enemigo = Enemigo(800, 492)
vidas = Vidas(300, 400)


        

# Pantalla de introducción
pantalla.fill(negro)
intro = pygame.image.load('./static/portada.png')
pantalla.blit(intro, (w/2 - intro.get_width()/2, h/2 - intro.get_height()/2))
pygame.display.update()

# Temporizador para esperar 2 segundos
inicio_tiempo = pygame.time.get_ticks()
while pygame.time.get_ticks() - inicio_tiempo < 2000:
    pygame.event.pump()  # Procesar eventos para evitar que el juego se congele

        
# Crear botón de restart
restart_button = pygame.Rect(160, 50, 200, 50)
restart_button_color = (255, 0, 0)

# Variable para contar los impactos
impactos = 0

# Variable para controlar el estado de pausa del juego
pausa = False

# Variable para controlar la distancia recorrida por el jugador
distancia_recorrida = 0

# Crear variable reloj
reloj = pygame.time.Clock()

# Crear variable tiempo_pausa
tiempo_pausa = 0

# Bucle principal
ejecuta = True
while ejecuta:
    
    # FPS
    reloj.tick(18)


    # Actualizar distancia recorrida
    distancia_recorrida += jugador.velocidad

    # Comprobar si el jefe debe aparecer
    if distancia_recorrida >= 10000:  # ajusta este valor según sea necesario
        # Hacer que el jefe aparezca
        enemigo.rect.x = 700
        enemigo.rect.y = 345
        enemigo.velocidad = 4
        enemigo.imagen = pygame.image.load('./static/th.png')

    if jugador.rect.colliderect(enemigo.rect or enemigo.disparos):
        jugador.quieto = pygame.image.load("./static/moon_stand_r_hit.png")
        jugador.camina_R = [pygame.image.load('./static/moon_run_r_hit.png'),
                         pygame.image.load('./static/moon_run_r_hit.png'),
                         pygame.image.load('./static/moon_run_r2_hit.png'),
                         pygame.image.load('./static/moon_run_r3_hit.png'),
                         pygame.image.load('./static/moon_run_r2_hit.png'),
                         pygame.image.load('./static/moon_run_r3_hit.png')]
        jugador.camina_L = [pygame.image.load('./static/moon_run_l_hit.png'),
                         pygame.image.load('./static/moon_run_l_hit.png'),
                         pygame.image.load('./static/moon_run_l2_hit.png'),
                         pygame.image.load('./static/moon_run_l3_hit.png'),
                         pygame.image.load('./static/moon_run_l2_hit.png'),
                         pygame.image.load('./static/moon_run_l3_hit.png')]
        print("Colisión detectada!")

    # Movimiento del fondo

    x_relativa = x % fondo.get_rect().width
    pantalla.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
    if x_relativa < w:
        pantalla.blit(fondo, (x_relativa, 0))
        
    # Dibujar reloj
    font = pygame.font.Font(None, 36)
    text = font.render("Tiempo sin morir acumulado: {}s".format(int(pygame.time.get_ticks() / 1000)), True, (0, 0, 0))
    
    
    keys = pygame.key.get_pressed()
    
    #efecto volar
    if keys[pygame.K_UP]:
        x -= 5
        reloj.tick(60)
        jugador.rect.y = 400
        vidas.rect.x -= 5
        enemigo.rect.x -= 5
    
        
    
    if keys[pygame.K_d]:
        if jugador.rect.x < 1200:
            jugador.rect.x += jugador.velocidad
        x -= 5
        vidas.rect.x -= 5
        
    if jugador.rect.x >= 500:
        if jugador.movimiento_fondo:
            x -= 5

    # Limitar la posición del jugador en la pantalla
    if jugador.rect.left < 0:
        jugador.rect.left = 0
    elif jugador.rect.right > w:
        jugador.rect.right = w

    # Si el jugador llega al límite derecho, mueve el fondo y el jugador hacia la izquierda
    if jugador.rect.x >= jugador.limite_derecha:
        jugador.rect.x = jugador.limite_derecha
        x -= 5
        vidas.rect.x -= 5

    # Generar un número aleatorio para crear una nueva instancia de Vidas
    if random.randint(0, 1000) < 5:  # 5% de probabilidad de crear una nueva instancia
        vidas_lista.append(Vidas(random.randint(0, w*2), 400))  # Generar una nueva instancia en una posición aleatoria


    # Bucle del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecuta = False

    # Actualizar jugador
    jugador.update()
    jugador.movimiento()
    
    enemigo.update()
    pantalla.blit(enemigo.imagen, enemigo.rect)
    
    # Disparar un proyectil cada 2 segundos
    if pygame.time.get_ticks() % 5000 < 50:
        enemigo.disparar()
    
    # Verifica si el jugador es golpeado por un disparo
    for disparo in enemigo.disparos:
        if jugador.rect.colliderect(disparo):
            # Incrementa el contador de golpes recibidos
            impactos += 1
    
    # Verifica si el jugador ha recibido 5 golpes
    if impactos >= 5:
        pausa = True

    # Actualizar disparos
    enemigo.disparos.update()
    for disparo in enemigo.disparos:
        pantalla.blit(disparo.imagen, disparo.rect)
        if disparo.rect.x > w:
            enemigo.disparos.remove(disparo)
        elif jugador.rect.colliderect(disparo):
            jugador.quieto = pygame.image.load("./static/moon_stand_r_hit.png")
            jugador.camina_R = [pygame.image.load('./static/moon_run_r_hit.png'),
                         pygame.image.load('./static/moon_run_r_hit.png'),
                         pygame.image.load('./static/moon_run_r2_hit.png'),
                         pygame.image.load('./static/moon_run_r3_hit.png'),
                         pygame.image.load('./static/moon_run_r2_hit.png'),
                         pygame.image.load('./static/moon_run_r3_hit.png')]
            jugador.camina_L = [pygame.image.load('./static/moon_run_l_hit.png'),
                         pygame.image.load('./static/moon_run_l_hit.png'),
                         pygame.image.load('./static/moon_run_l2_hit.png'),
                         pygame.image.load('./static/moon_run_l3_hit.png'),
                         pygame.image.load('./static/moon_run_l2_hit.png'),
                         pygame.image.load('./static/moon_run_l3_hit.png')]
    
    for vidas in vidas_lista:
        vidas.mostrar()
        if jugador.rect.colliderect(vidas.rect):
            impactos = 0
            jugador.quieto = pygame.image.load("./static/moon_stand_r.png")
            jugador.camina_R = [pygame.image.load('./static/moon_run_r.png'),
                         pygame.image.load('./static/moon_run_r.png'),
                         pygame.image.load('./static/moon_run_r2.png'),
                         pygame.image.load('./static/moon_run_r3.png'),
                         pygame.image.load('./static/moon_run_r2.png'),
                         pygame.image.load('./static/moon_run_r3.png')]
            jugador.camina_L = [pygame.image.load('./static/moon_run_l.png'),
                         pygame.image.load('./static/moon_run_l.png'),
                         pygame.image.load('./static/moon_run_l2.png'),
                         pygame.image.load('./static/moon_run_l3.png'),
                         pygame.image.load('./static/moon_run_l2.png'),
                         pygame.image.load('./static/moon_run_l3.png')]
            vidas_lista.remove(vidas)  # Eliminar la instancia de Vidas cuando el jugador la recoge


    if jugador.rect.colliderect(enemigo.rect):
        impactos += 1
        if impactos >= 2:
            pausa = True


    # Pausar juego si hay 2 o más impactos
    if pausa:
        pantalla.fill((255, 255, 255))  # Poner fondo blanco para indicar pausa
        pantalla.blit(text, (10, 10))
        font = pygame.font.Font(None, 36)
        text = font.render("R", True, (0, 0, 0))
        pantalla.blit(text, (w/2 - text.get_width()/2, h/2 - text.get_height()/2))
        pygame.display.update()
        while pausa:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pausa = False
                        impactos = 0
                        jugador.rect.x = 50
                        jugador.rect.y = 492
                        enemigo.rect.x = 800
                        enemigo.rect.y = 492
                        vidas_lista = []
                        x = 0
                        


    # Dibujar botón de restart
    pygame.draw.rect(pantalla, restart_button_color, restart_button)
    font = pygame.font.Font(None, 36)
    text = font.render("R para reiniciar", True, (255, 255, 255))
    pantalla.blit(text, (restart_button.x + 10, restart_button.y + 10))

    # Detectar clic en botón de restart
    if keys[pygame.K_r]:
        # Reiniciar juego
        jugador.rect.x = 50
        jugador.rect.y = 492
        enemigo.rect.x = 800
        enemigo.rect.y = 492
        vidas_lista = []
        x = 0
        jugador.quieto = pygame.image.load('./static/moon_stand_r.png')
        jugador.camina_R = [pygame.image.load('./static/moon_run_r.png'),
                 pygame.image.load('./static/moon_run_r.png'),
                 pygame.image.load('./static/moon_run_r2.png'),
                 pygame.image.load('./static/moon_run_r3.png'),
                 pygame.image.load('./static/moon_run_r2.png'),
                 pygame.image.load('./static/moon_run_r3.png')]
        jugador.camina_L = [pygame.image.load('./static/moon_run_l.png'),
                 pygame.image.load('./static/moon_run_l.png'),
                 pygame.image.load('./static/moon_run_l2.png'),
                 pygame.image.load('./static/moon_run_l3.png'),
                 pygame.image.load('./static/moon_run_l2.png'),
                 pygame.image.load('./static/moon_run_l3.png')]

    # Actualizar pantalla
    pygame.display.update()

# Cerrar juego
pygame.quit()