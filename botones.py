import pygame
import json
from constantes import *

# Clase para representar botones
class Boton:
    def __init__(self, texto, x, y, ancho, alto, color_normal, color_resaltado, accion):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_normal = color_normal
        self.color_resaltado = color_resaltado
        self.superficie = pygame.Surface(self.rect.size)
        self.superficie.fill(self.color_normal)
        self.texto = texto
        self.accion = accion
        self.resaltado = False

    def mostrar_texto(self, ventana):
        fuente = pygame.font.Font(None, 28)
        texto_superficie = fuente.render(self.texto, True, COLOR_BLANCO)
        texto_rect = texto_superficie.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        ventana.blit(texto_superficie, texto_rect.topleft)

    def actualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_mouse):
            self.resaltado = True
        else:
            self.resaltado = False

    def dibujar(self, ventana):
        if self.resaltado:
            self.superficie.fill(self.color_resaltado)
        else:
            self.superficie.fill(self.color_normal)

        pygame.draw.rect(self.superficie,COLOR_NEGRO, self.rect, 2)

        self.mostrar_texto(ventana)

        ventana.blit(self.superficie, self.rect)