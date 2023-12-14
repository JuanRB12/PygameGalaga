import pygame
import random
import sys
import re
from Principal import *
from Jugador import *
import json
from proyectiles import *

def iniciar_nivel_2(enemigo, enemigo_que_dispara):
    fondo_nivel = pygame.image.load("PYGAME\GALAGA\imagen_nivel2.jpg") #Path relativo
    fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO_VENTANA, ALTO_VENTANA))

    #Crear enemigos que no disparan
    cantidad_enemigos = 2
    lista_enemigos = []
    lista_enemigos_disparadores = []

    for _ in range(cantidad_enemigos):
        colision = True

        while colision:
            x = random.randint(0, ANCHO_VENTANA - 100)
            y = random.randint(ALTO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 25)  # Ajusta el rango según tus necesidades

            colision = False
            nuevo_rect = pygame.Rect(x, y, 40, 40)

            for enemigo in lista_enemigos:
                if enemigo.rect.colliderect(nuevo_rect):
                    colision = True
                    break

        nuevo_enemigo = enemigo
        lista_enemigos.append(nuevo_enemigo)

    # Crear enemigos que disparan
    cantidad_enemigos_disparadores = 5
    for _ in range(cantidad_enemigos_disparadores):
        flag_colision_enemigo2 = True

        while flag_colision_enemigo2:
            x = random.randint(0, ANCHO_VENTANA - 100)
            y = random.randint(0, ALTO_VENTANA // 4 - 50)

            flag_colision_enemigo2 = False
            nuevo_rect = pygame.Rect(x, y, 60, 60)

            for enemigo in lista_enemigos_disparadores:
                if enemigo.rect.colliderect(nuevo_rect):
                    flag_colision_enemigo2 = True
                    break

        nuevo_enemigo_disparador = enemigo_que_dispara
        lista_enemigos_disparadores.append(nuevo_enemigo_disparador)

def iniciar_nivel_3(enemigo, enemigo_que_dispara):
    fondo_nivel = pygame.image.load("PYGAME\GALAGA\imagen_nivel3.jpg")
    fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO_VENTANA, ALTO_VENTANA))

    #Crear enemigos que no disparan
    cantidad_enemigos = 0
    lista_enemigos = []
    lista_enemigos_disparadores = []

    for _ in range(cantidad_enemigos):
        colision = True

        while colision:
            x = random.randint(0, ANCHO_VENTANA - 100)
            y = random.randint(ALTO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 25)  # Ajusta el rango según tus necesidades

            colision = False
            nuevo_rect = pygame.Rect(x, y, 40, 40)

            for enemigo in lista_enemigos:
                if enemigo.rect.colliderect(nuevo_rect):
                    colision = True
                    break

        nuevo_enemigo = enemigo
        lista_enemigos.append(nuevo_enemigo)

    # Crear enemigos que disparan
    cantidad_enemigos_disparadores = 1
    for _ in range(cantidad_enemigos_disparadores):
        flag_colision_enemigo2 = True

        while flag_colision_enemigo2:
            x = random.randint(0, ANCHO_VENTANA - 100)
            y = random.randint(0, ALTO_VENTANA // 4 - 50)

            flag_colision_enemigo2 = False
            nuevo_rect = pygame.Rect(x, y, 60, 60)

            for enemigo in lista_enemigos_disparadores:
                if enemigo.rect.colliderect(nuevo_rect):
                    flag_colision_enemigo2 = True
                    break

        nuevo_enemigo_disparador = enemigo_que_dispara
        lista_enemigos_disparadores.append(nuevo_enemigo_disparador)