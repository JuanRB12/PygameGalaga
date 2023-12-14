import pygame
import sys
import random
from constantes import *
from botones import *
from Jugador import *
from proyectiles import *
from niveles import *
import json
import time
import os
 
# Inicializar Pygame
pygame.init()

#Rutas imagenes y sonidos
current_dir = os.path.dirname(os.path.abspath(__file__))
fondo_path = os.path.join(current_dir, "espacio.jpg")
fondo_nivel1_path = os.path.join(current_dir, "imagen_nivel1.jpg")
fondo_nivel2_path = os.path.join(current_dir, "imagen_nivel2.jpg")
fondo_nivel3_path = os.path.join(current_dir, "imagen_nivel3.jpg")
fondo_puntajes_path = os.path.join(current_dir, "puntajes_fondo.jpg")
nave_jugador1_path = os.path.join(current_dir, "spaceships", "jugador1_nave.png")
nave_enemigo1_path = os.path.join(current_dir, "spaceships", "enemigo1_nave.png")
nave_enemigo2_path = os.path.join(current_dir, "spaceships", "enemyRed2.png")
nave_boss_path = os.path.join(current_dir, "spaceships", "enemyBlack1.png")
laser_jugador1_path = os.path.join(current_dir, "laser", "laserBlue07.png")
laser_enemigo1_path = os.path.join(current_dir, "laser", "laserGreen13.png")
laser_boss_path = os.path.join(current_dir, "laser", "laserRed08.png")
sonido_disparo_path = os.path.join(current_dir, "sonidos", "sfx_laser1.ogg")

# Configurar la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Galaga")

#Agregar Fondo
fondo = pygame.image.load(fondo_path) #Path relativo
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

#Cargar explosiones
def cargar_animacion_explosion():
    animacion_explosion = []
    for i in range(9):
        ruta_explosion = os.path.join(current_dir, "explosiones", f"explosion0{i}.png")
        imagen = pygame.image.load(ruta_explosion).convert()
        imagen.set_colorkey(COLOR_NEGRO)
        escala_imagen = pygame.transform.scale(imagen, (60, 60))
        animacion_explosion.append(escala_imagen)
    return animacion_explosion
animacion_explosion = cargar_animacion_explosion()

#Crear Sonidos
pygame.mixer.init()  # Inicializar el módulo de mezcla de sonido de Pygame
sonido_disparo_jugador = pygame.mixer.Sound(sonido_disparo_path)

def pasar_de_nivel():
    global nivel_actual
    nivel_actual += 1
    

#Reloj
reloj = pygame.time.Clock()

# Función principal del menu
def menu_principal():
    jugar_boton = Boton("Jugar", ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2 - 50, 200, 50, COLOR_AZUL, COLOR_CELESTE, jugar)
    puntajes_boton = Boton("Ver Puntajes", ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2 + 10, 200, 50, COLOR_AZUL, COLOR_CELESTE, ver_puntajes)
    salir_boton = Boton("Salir", ANCHO_VENTANA // 2 - 100, ALTO_VENTANA // 2 + 70, 200, 50, COLOR_AZUL, COLOR_CELESTE, salir)

    botones = [jugar_boton, puntajes_boton, salir_boton]

    while True:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    for boton in botones:
                        if boton.rect.collidepoint(evento.pos):
                            boton.accion()

        ventana.blit(fondo, (0,0))

        for boton in botones:
            boton.dibujar(ventana)
            boton.mostrar_texto(ventana)
            boton.actualizar()

        pygame.display.flip()

# Acciones de los botones
def jugar():
    iniciar_juego()

def ver_puntajes():

    puntajes_path = os.path.join(current_dir, "puntajes.json")

    fondo_puntajes = pygame.image.load(fondo_puntajes_path)
    fondo_puntajes = pygame.transform.scale(fondo_puntajes, (ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo_puntajes, (0,0))

    try:
        # Cargar puntajes desde el archivo JSON
        with open(puntajes_path, "r") as file:
            puntajes = json.load(file)
    except FileNotFoundError:
        puntajes = []
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if puntajes:
            # Ordenar los puntajes de mayor a menor
            puntajes_ordenados = sorted(puntajes, key=lambda x: x["puntaje"], reverse=True)

            # Obtener los mejores 5 puntajes o menos si hay menos de 5
            mejores_puntajes = puntajes_ordenados[:5]

            mostrar_mejores_puntajes_ventana(mejores_puntajes)
        else:
            print("No hay puntajes almacenados.")

            pygame.display.flip()

def salir():
    pygame.quit()
    sys.exit()

def iniciar_juego():

    fondo_nivel = pygame.image.load(fondo_nivel1_path) #Path relativo
    fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO_VENTANA, ALTO_VENTANA))

    # Crear al jugador
    jugador1 = Jugador()

    #Crear enemigos que no disparan
    cantidad_enemigos = 6
    lista_enemigos = []
    lista_enemigos_disparadores = []
    lista_jefes = []

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

        nuevo_enemigo = Enemigo(x, y)
        lista_enemigos.append(nuevo_enemigo)

    # Crear enemigos que disparan
    cantidad_enemigos_disparadores = 2
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

        nuevo_enemigo_disparador = EnemigoQueDispara(x, y)
        lista_enemigos_disparadores.append(nuevo_enemigo_disparador)
  
    #Explosiones
    explosiones_activas = pygame.sprite.Group()

    flag_nivel = 1
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        jugador1.actualizar()

        ventana.blit(fondo_nivel, (0,0))  #Dibujo del fondo del primer stage
        
        #Dibujar objetos del juego
        jugador1.dibujar(ventana)

        #Dibujar enemigo que no dispara
        for enemigo1 in lista_enemigos:
            if enemigo1 is not None:
                enemigo1.actualizar(lista_enemigos)
                enemigo1.dibujar(ventana)
        
        #Dibujar enemigo que dispara
        for nuevo_enemigo_disparador in lista_enemigos_disparadores:
            if nuevo_enemigo_disparador is not None:
                nuevo_enemigo_disparador.actualizar(lista_enemigos_disparadores)
                nuevo_enemigo_disparador.dibujar(ventana)
        
        #Dibujar Jefe
        for nuevo_jefe in lista_jefes:
            if nuevo_jefe is not None:
                nuevo_jefe.actualizar(lista_jefes)
                nuevo_jefe.dibujar(ventana)
        
        # Actualizar y dibujar proyectiles
        for proyectil in jugador1.proyectiles:
            proyectil.actualizar()
            ventana.blit(proyectil.image, proyectil.rect)
        
        # Actualizar y dibujar proyectiles enemigos
        for nuevo_enemigo_disparador in lista_enemigos_disparadores:
            if nuevo_enemigo_disparador is not None:
                nuevo_enemigo_disparador.actualizar(lista_enemigos_disparadores)
                nuevo_enemigo_disparador.dibujar(ventana)

            # Bucle para actualizar y dibujar proyectiles enemigos específicos de este enemigo
            for proyectil in nuevo_enemigo_disparador.proyectiles:
                proyectil.actualizar()
                ventana.blit(proyectil.image, proyectil.rect)
        
        # Actualizar y dibujar proyectiles enemigos
        for nuevo_jefe in lista_jefes:
            if nuevo_jefe is not None:
                nuevo_jefe.actualizar(lista_jefes)
                nuevo_jefe.dibujar(ventana)

            # Bucle para actualizar y dibujar proyectiles enemigos específicos del jefe
            for proyectil in nuevo_jefe.proyectiles:
                proyectil.actualizar()
                ventana.blit(proyectil.image, proyectil.rect)

            # Detectar colisión del láser enemigo con la parte inferior del jugador
                if proyectil.rect.colliderect(jugador1.rect) and proyectil.rect.bottom > jugador1.rect.bottom:
                    jugador1.perder_vida()
                    print(f"¡Has perdido una vida! Te quedan {jugador1.vidas} vidas.")
                    nuevo_jefe.proyectiles.remove(proyectil)
        
        #Detectar colisiones del laser contra el enemigo
        for proyectil in jugador1.proyectiles:
            for enemigo1 in lista_enemigos:
                if proyectil.rect.colliderect(enemigo1.rect):
                    jugador1.proyectiles.remove(proyectil)  # Elimina el proyectil después del impacto
                    explosion = Explosion(enemigo1.rect.center, animacion_explosion)
                    explosiones_activas.add(explosion)
                    lista_enemigos.remove(enemigo1)
                    jugador1.sumar_puntaje(10)
        
            for nuevo_enemigo_disparador in lista_enemigos_disparadores:
                if proyectil.rect.colliderect(nuevo_enemigo_disparador.rect):
                    jugador1.proyectiles.remove(proyectil)
                    explosion = Explosion(nuevo_enemigo_disparador.rect.center, animacion_explosion)
                    explosiones_activas.add(explosion)
                    lista_enemigos_disparadores.remove(nuevo_enemigo_disparador)
                    jugador1.sumar_puntaje(25)
            
            for nuevo_jefe in lista_jefes:
                if proyectil.rect.colliderect(nuevo_jefe.rect):
                    jugador1.proyectiles.remove(proyectil)
                    explosion = Explosion(nuevo_jefe.rect.center, animacion_explosion)
                    explosiones_activas.add(explosion)
                    lista_jefes.remove(nuevo_jefe)
                    jugador1.sumar_puntaje(100)
                
        # Detectar colisiones del láser enemigo contra el jugador
        for nuevo_enemigo_disparador in lista_enemigos_disparadores:
            if nuevo_enemigo_disparador is not None:
                nuevo_enemigo_disparador.actualizar(lista_enemigos_disparadores)
                nuevo_enemigo_disparador.dibujar(ventana)

                # Bucle para actualizar y dibujar proyectiles de los enemigos que no son jefe
                for proyectil in nuevo_enemigo_disparador.proyectiles:
                    proyectil.actualizar()
                    ventana.blit(proyectil.image, proyectil.rect)

                    # Detectar colisión del láser enemigo con la parte inferior del jugador
                    if proyectil.rect.colliderect(jugador1.rect) and proyectil.rect.bottom > jugador1.rect.bottom:
                        jugador1.perder_vida()
                        print(f"¡Has perdido una vida! Te quedan {jugador1.vidas} vidas.")
                        nuevo_enemigo_disparador.proyectiles.remove(proyectil)
        
        for explosion in explosiones_activas:
            explosion.actualizar(animacion_explosion)
            ventana.blit(explosion.imagen, explosion.rect)
        
        #NIVEL 2
        if len(lista_enemigos) == 0 and len(lista_enemigos_disparadores) == 0 and flag_nivel == 1:
            flag_nivel += 1
            fondo_nivel = pygame.image.load(fondo_nivel2_path) #Path relativo
            fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO_VENTANA, ALTO_VENTANA))

            #Crear enemigos que no disparan
            cantidad_enemigos = 4
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

                nuevo_enemigo = Enemigo(x, y)
                lista_enemigos.append(nuevo_enemigo)

            # Crear enemigos que disparan
            cantidad_enemigos_disparadores = 4
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

                nuevo_enemigo_disparador = EnemigoQueDispara(x, y)
                lista_enemigos_disparadores.append(nuevo_enemigo_disparador)


        #NIVEL 3
        if len(lista_enemigos) == 0 and len(lista_enemigos_disparadores) == 0 and flag_nivel == 2:
            flag_nivel += 1
            fondo_nivel = pygame.image.load(fondo_nivel3_path) #Path relativo
            fondo_nivel = pygame.transform.scale(fondo_nivel, (ANCHO_VENTANA, ALTO_VENTANA))

            #Crear enemigos
            cantidad_enemigos = 0
            lista_enemigos = []
            lista_enemigos_disparadores = []
            lista_jefes = []

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

                nuevo_enemigo = Enemigo(x, y)
                lista_enemigos.append(nuevo_enemigo)

            # Crear enemigos que disparan
            cantidad_enemigos_disparadores = 8
            for _ in range(cantidad_enemigos_disparadores):
                flag_colision_enemigo2 = True

                while flag_colision_enemigo2:
                    x = random.randint(0, ANCHO_VENTANA - 100)
                    y = random.randint(ALTO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 25)

                    flag_colision_enemigo2 = False
                    nuevo_rect = pygame.Rect(x, y, 60, 60)

                    for enemigo in lista_enemigos_disparadores:
                        if enemigo.rect.colliderect(nuevo_rect):
                            flag_colision_enemigo2 = True
                            break

                nuevo_enemigo_disparador = EnemigoQueDispara(x, y)
                lista_enemigos_disparadores.append(nuevo_enemigo_disparador)

            # Crear jefe
            cantidad_jefes = 2
            for _ in range(cantidad_jefes):
                flag_colision_jefe = True

                while flag_colision_jefe:
                    x = random.randint(0, ANCHO_VENTANA - 100)
                    y = random.randint(0, ALTO_VENTANA // 4 - 50)

                    flag_colision_jefe = False
                    nuevo_rect = pygame.Rect(x, y, 60, 60)

                    for enemigo in lista_jefes:
                        if enemigo.rect.colliderect(nuevo_rect):
                            flag_colision_jefe = True
                            break

                nuevo_jefe = EnemigoBoss(x, y)
                lista_jefes.append(nuevo_jefe)

        fuente_vidas = pygame.font.Font(None, 36)
        texto_vidas = fuente_vidas.render(f"Vidas: {jugador1.vidas}", True, COLOR_BLANCO)
        ventana.blit(texto_vidas, (10, ALTO_VENTANA - 40))

        if jugador1.vidas == 0 or (len(lista_enemigos) == 0 and len(lista_enemigos_disparadores) == 0 and len(lista_jefes) == 0):
            puntajes(jugador1.puntaje)
            menu_principal()

        # Mostrar puntaje en la pantalla
        fuente_puntaje = pygame.font.Font(None, 36)
        texto_puntaje = fuente_puntaje.render(f"Score: {jugador1.puntaje}", True, COLOR_BLANCO)
        ventana.blit(texto_puntaje, (ANCHO_VENTANA - 150, ALTO_VENTANA - 40))

        pygame.display.flip()  # Actualiza la pantalla
        reloj.tick(FPS)  # Controla la velocidad del juego


def puntajes(puntaje):
    puntajes_path = os.path.join(current_dir, "puntajes.json")
    try:
        # Cargar puntajes desde el archivo JSON
        with open(puntajes_path, "r") as file:
            puntajes = json.load(file)
    except FileNotFoundError:
        puntajes = []

    # Mostrar puntajes almacenados
    print("Puntajes almacenados:")
    for p in puntajes:
        print(p)

    # Agregar el puntaje actual a la lista
    puntajes.append({"puntaje": puntaje})

    # Guardar la lista actualizada en el archivo JSON
    with open(puntajes_path, "w") as file:
        json.dump(puntajes, file)

    print(f"Puntaje actual: {puntaje}")

def mostrar_mejores_puntajes_ventana(mejores_puntajes):

    fondo_puntajes = pygame.image.load(fondo_puntajes_path)
    fondo_puntajes = pygame.transform.scale(fondo_puntajes, (ANCHO_VENTANA, ALTO_VENTANA))

    # Configurar la fuente y crear una superficie de texto para los mejores puntajes
    fuente = pygame.font.Font(None, 30)
    texto_titulo = fuente.render("Mejores Puntajes", True, COLOR_BLANCO)
    rect_titulo = texto_titulo.get_rect()
    rect_titulo.center = (ANCHO_VENTANA // 2, 50)  # Centrar el título

    # Dibujar el título en la ventana
    ventana.blit(texto_titulo, rect_titulo.topleft)

    # Configurar la fuente para los puntajes y crear superficies de texto
    fuente_puntajes = pygame.font.Font(None, 24)
    y_offset = 100  # Desplazamiento vertical para los puntajes
    for i, puntaje_info in enumerate(mejores_puntajes):
        puntaje = puntaje_info["puntaje"]
        texto_puntaje = fuente_puntajes.render(f"{i + 1}. {puntaje}", True, COLOR_BLANCO)
        rect_puntaje = texto_puntaje.get_rect()
        rect_puntaje.center = (ANCHO_VENTANA // 2, y_offset)
        ventana.blit(texto_puntaje, rect_puntaje.topleft)
        y_offset += 30  # Ajustar el desplazamiento vertical para el próximo puntaje

    pygame.display.flip()



if __name__ == "__main__":
    menu_principal()