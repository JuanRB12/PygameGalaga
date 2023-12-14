import pygame
from constantes import *
def obtener_superficie_de_sprite(path):
    lista = []
    imagen_superficie = pygame.image.load(path)
    lista.append(imagen_superficie)
    return lista

class Proyectil():
    def __init__(self, x, y, sprite_path, speed, speed_x):
        self.sprite = obtener_superficie_de_sprite(sprite_path)
        self.frame = 0
        self.image = pygame.transform.scale(self.sprite[self.frame], (10, 30))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
        self.speed_x = speed_x

    def actualizar(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x

class ProyectilEnemigo():
    def __init__(self, x, y, sprite_path, speed, speed_x):
        self.sprite = obtener_superficie_de_sprite(sprite_path)
        self.frame = 0
        self.image = pygame.transform.scale(self.sprite[self.frame], (10, 30))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
        self.speed_x = speed_x
    
    def actualizar(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x

class ProyectilEnemigoBoss():
    def __init__(self, x, y, sprite_path, speed, speed_x):
        self.sprite = obtener_superficie_de_sprite(sprite_path)
        self.frame = 0
        self.image = pygame.transform.scale(self.sprite[self.frame], (150, 150))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
        self.speed_x = speed_x
    
    def actualizar(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x

# if len(lista_enemigos) < 5:
        #     x = random.randint(0, ANCHO_VENTANA - 100)  # Ajusta el rango según tus necesidades
        #     y = random.randint(0, ALTO_VENTANA // 2 - 50)   # Ajusta el rango según tus necesidades
        #     lista_enemigos.append(Enemigo(x,y))