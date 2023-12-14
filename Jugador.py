import pygame
import random
import sys
from pygame.sprite import Group
from constantes import *
from proyectiles import *
from Principal import *

def obtener_superficie_de_sprite(path):
    lista = []
    imagen_superficie = pygame.image.load(path)
    lista.append(imagen_superficie)
    return lista

# Clase para representar al jugador
class Jugador():
    def __init__(self):
        self.sprite = obtener_superficie_de_sprite(nave_jugador1_path)
        self.frame = 0
        self.vidas = 3
        self.score = 0
        self.imagen = pygame.transform.scale(self.sprite[self.frame], (60, 60))
        self.rect = self.imagen.get_rect()
        self.proyectiles = []
        self.ultimo_disparo = pygame.time.get_ticks()
        self.velocidad_disparo = 500
        self.vidas = 3
        self.puntaje = 0
        self.sonido_disparo_jugador = pygame.mixer.Sound(sonido_disparo_path)

        # Establecer la posición inicial
        self.rect.bottom = ALTO_VENTANA - 50
        self.rect.centerx = ANCHO_VENTANA // 2

    
    def sumar_puntaje(self, puntos):
        self.puntaje += puntos
    
    def perder_vida(self):
        self.vidas -= 1
        if self.vidas <= 0:
            print("¡Juego terminado! Has perdido todas tus vidas.")
            pygame.quit()
            sys.exit()
            

    def disparar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.velocidad_disparo:
            nuevo_proyectil = Proyectil(self.rect.centerx, self.rect.top, laser_jugador1_path, -5, 0)
            self.proyectiles.append(nuevo_proyectil)
            self.ultimo_disparo = ahora
            self.sonido_disparo_jugador.play()

    def actualizar(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO_VENTANA:
            self.rect.x += 5
        if keys[pygame.K_SPACE]:
            self.disparar()

    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)

# Clase para representar a los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.sprite = obtener_superficie_de_sprite(nave_enemigo1_path)
        self.frame = 0
        self.imagen = pygame.transform.scale(self.sprite[self.frame], (40, 40))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direccion = 1  # 1 para moverse hacia la derecha, -1 para moverse hacia la izquierda

    def actualizar(self, lista_enemigos):
        self.rect.x += 2 * self.direccion

        # Verificar si el enemigo alcanzó el borde izquierdo o derecho de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO_VENTANA:
            self.direccion *= -1  # Cambia de dirección al chocar con el borde

        # Verificar colisión con otras naves enemigas
        for otro_enemigo in lista_enemigos:
            if otro_enemigo != self and self.rect.colliderect(otro_enemigo.rect):
                self.direccion *= -1  # Cambia de dirección al chocar con otra nave enemiga


    def dibujar(self, ventana):
            ventana.blit(self.imagen, self.rect)

# Clase para representar a los enemigos
class EnemigoQueDispara(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.sprite = obtener_superficie_de_sprite(nave_enemigo2_path)
        self.frame = 0
        self.imagen = pygame.transform.scale(self.sprite[self.frame], (40, 40))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = 1  # 1 para moverse hacia la derecha, -1 para moverse hacia la izquierda
        self.proyectiles = []
        self.ultimo_disparo = pygame.time.get_ticks()
        self.velocidad_disparo = 2000
        self.velocidad_movimiento = 1  # Puedes ajustar este valor según sea necesario

    def disparar_laser(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.velocidad_disparo:
            nuevo_proyectil = ProyectilEnemigo(self.rect.centerx, self.rect.bottom, laser_enemigo1_path, 5, 0)
            retraso_aleatorio = random.randint(500, 5000)
            self.proyectiles.append(nuevo_proyectil)
            self.ultimo_disparo = ahora + retraso_aleatorio
    
    def actualizar(self, lista_enemigos):
        self.rect.x += self.velocidad_movimiento * self.direccion

        # Verificar si el enemigo alcanzó el borde izquierdo o derecho de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO_VENTANA:
            self.direccion *= -1

        # Verificar colisión con otras naves enemigas
        for otro_enemigo in lista_enemigos:
            if otro_enemigo != self and self.rect.colliderect(otro_enemigo.rect):
                self.direccion *= -1 
        
        self.disparar_laser()
    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)

class EnemigoBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.sprite = obtener_superficie_de_sprite(nave_boss_path)
        self.frame = 0
        self.imagen = pygame.transform.scale(self.sprite[self.frame], (60, 60))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direccion = 1  # 1 para moverse hacia la derecha, -1 para moverse hacia la izquierda
        self.proyectiles = []
        self.ultimo_disparo = pygame.time.get_ticks()
        self.velocidad_disparo = 3000
        self.velocidad_movimiento = 1  # Puedes ajustar este valor según sea necesario

    def disparar_laser(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.velocidad_disparo:
            nuevo_proyectil = ProyectilEnemigoBoss(self.rect.centerx, self.rect.bottom, laser_boss_path, 5, 0)
            retraso_aleatorio = random.randint(1000, 5000)
            self.proyectiles.append(nuevo_proyectil)
            self.ultimo_disparo = ahora + retraso_aleatorio
    
    def actualizar(self, lista_enemigos):
        self.rect.x += self.velocidad_movimiento * self.direccion

        # Verificar si el enemigo está cerca del borde izquierdo o derecho de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO_VENTANA:
            self.direccion *= -1

        # Verificar colisión con otras naves enemigas
        for otro_enemigo in lista_enemigos:
            if otro_enemigo != self and self.rect.colliderect(otro_enemigo.rect):
                self.direccion *= -1 
        
        self.disparar_laser()
    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,animacion_explosion) -> None:
        super().__init__()
        self.imagen = animacion_explosion[0]
        self.rect = self.imagen.get_rect()
        self.frame = 0 #Sirve para iterar sobre la lista de las explosiones
        self.frame_rate = 50 #Velocidad de explosion
        self.ultima_actualizacion = 0
        self.center = center
    
    def actualizar(self, animacion_explosion):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultima_actualizacion > self.frame_rate:
            self.ultima_actualizacion = ahora
            self.frame += 1
            if self.frame == len(animacion_explosion):
                self.kill()
            else:
                self.imagen = animacion_explosion[self.frame]
                self.rect = self.imagen.get_rect(center=self.center)