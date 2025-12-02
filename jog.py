import pygame
import sys

# inicializar
pygame.init()

# Janela
LARGURA = 800
ALTURA = 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("pog")

FPS = 60
CLOCK = pygame.time.Clock()

#CORES 
BRANCO = (255,255,255)
PRETO = (0,0,0)

#objetos
largura_barra = 15
altura_barra = 100

barra_esq = pygame.Rect(20, ALTURA//2 - altura_barra//2,largura_barra,altura_barra)
barra_dir = pygame.Rect(LARGURA - 40, ALTURA//2 - altura_barra//2,largura_barra,altura_barra)

# bola
bola= pygame.Rect(LARGURA//2 - 10,ALTURA//2 - 10,20,20)

#velocidade
vel_bola_x = 4
vel_bola_y = 4
vel_barra= 6

# pontuação
ponto_esq = 0
ponto_dir = 0
fonte = pygame.font.SysFont(None,40)

def resetar_bola():
    global vel_bola_x, vel_bola_y
    bola.center = (LARGURA//2, ALTURA//2)
    vel_bola_x *= -1

while True:
    #observar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.quit
    #movimentação jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and barra_esq.top > 0 :
        barra_esq.y -= vel_barra
    if teclas[pygame.K_s] and barra_esq.bottom < ALTURA:
        barra_esq.y += vel_barra

    # acompanhar bolo
    if bola.centery > barra_dir.centery:
        barra_dir.y += vel_barra
    else:
        barra_dir.y -= vel_barra

#evita que barra passa da tela
    barra_dir.clamp_ip(pygame.Rect(0,0,LARGURA,ALTURA))

# movimentação
    bola.x += vel_bola_x
    bola.y += vel_bola_y
    # passa da tela
    if bola.top <= 0 or bola.bottom >= ALTURA :
        vel_bola_y *=-1
    # colisão bola
    if bola.colliderect(barra_esq) or bola.colliderect(barra_dir):
        vel_bola_x *= -1
    #marcar ponto
    if bola.left <=0 :
        ponto_dir += 1
        resetar_bola()

    if bola.right >= LARGURA:
        ponto_esq += 1 
        resetar_bola()   
#desenho 
    TELA.fill(PRETO)
    #desenha barras
    pygame.draw.rect(TELA, BRANCO, barra_esq)    
    pygame.draw.rect(TELA, BRANCO, barra_dir)   
    #desenha bola
    pygame.draw.rect(TELA, BRANCO, bola)

    #linha do centro
    pygame.draw.aaline(TELA,BRANCO,(LARGURA//2,0),(LARGURA//2,ALTURA))
    #exibir pts
    ponto_texto = fonte.render(f"{ponto_esq}x{ponto_dir}",True , BRANCO)
    TELA.blit(ponto_texto, (LARGURA//2 - ponto_texto.get_width()//2,20))

    pygame.display.update()
    CLOCK.tick(FPS)