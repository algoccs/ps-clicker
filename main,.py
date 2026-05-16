import pygame
from random import *

pygame.init()

ANCHO, ALTO = 500, 500
COLOR_FONDO = (64, 201, 144)
COLOR_CARD = (227, 172, 54)
COLOR_BORDER = (71, 11, 222)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (25, 235, 14)
RED = (235, 14, 29)
FPS = 40

screen = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# CLASES 
class Area():
    def __init__(self, x, y, ancho, alto, color=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
    
    def fill(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def change_color(self, new_color):
        self.color = new_color

    def set_border(self, border_color, border_size):
        pygame.draw.rect(screen, border_color, self.rect, border_size)
    
    def is_collide(self, x, y):
        # devuelve True o False en caso de colision con el rectangulo
        return self.rect.collidepoint(x, y) 

class Label(Area):
    def set_text(self, text, size, text_color=BLACK):
        self.image = pygame.font.SysFont("Arial", size).render(text, 1, text_color)

    def draw(self, dist_x=10, dist_y=10):
        self.fill()
        screen.blit(self.image, (self.rect.x + dist_x, self.rect.y + dist_y))

# CREANDO OBJETOS
lista_cards = []
x = 50
for i in range(4):
    card = Label(x, 150, 80, 100, COLOR_CARD)
    card.set_text('Click!', 24)
    lista_cards.append(card)
    x += 110

# TEXTO PARA ESTADISTICAS
point_text = Label(50, 50, 100, 50, COLOR_FONDO)
timer_text = Label(350, 50, 100, 50, COLOR_FONDO)

wait = 0
points = 0

finish = False
condicion = ''

while True:
    # Validar si el juego ha finalizado
    if not finish:
        seg = pygame.time.get_ticks() // 1000

        if wait == 0:
            screen.fill(COLOR_FONDO)
            point_text.set_text(f'PUNTAJE: {points}', 30)
            point_text.draw(0, 0)
            timer_text.set_text(f'TIEMPO: {seg}', 30)
            timer_text.draw(0, 0)

            wait = 20
            click = randint(0, 3)

            for i in range(4):
                lista_cards[i].change_color(COLOR_CARD)
                if i == click:
                    lista_cards[i].draw(15, 30)
                    lista_cards[i].set_border(COLOR_BORDER, 5)
                else:
                    lista_cards[i].fill()
        else:
            wait -= 1

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                for i in range(4):
                    if lista_cards[i].is_collide(x, y):
                        if click == i:
                            points += 1
                            lista_cards[i].change_color(GREEN)
                            lista_cards[i].set_border(COLOR_BORDER, 5)
                        else:
                            points -= 1
                            lista_cards[i].change_color(RED)
                            lista_cards[i].set_border(COLOR_BORDER, 5)
                    
                        lista_cards[i].fill()
    
    # CONDICION DE VICTORIA
        if points >= 1:
            finish = True
            condicion = 'victoria'
    # FALTA LA CONDICION DE DERROTA
        if seg >= 10:
            finish = True
            condicion = 'derrota'

    else:
        if condicion == 'victoria':
            # RENDERIZAMOS LA IMAGEN DE VICTORIA
            victoria = Label(0, 0, ANCHO, ALTO, GREEN)
            victoria.set_text('GANASTE!', 50, WHITE)
            victoria.draw(150, (ALTO // 2) - 50)
        elif condicion == 'derrota':
            derrota = Label(0, 0, ANCHO, ALTO, RED)
            derrota.set_text('PERDISTE!', 50, WHITE)
            derrota.draw(150, (ALTO // 2) - 50)


    pygame.display.update()
    reloj.tick(FPS)


pygame.quit()