import pygame
import sys
import random

# Inicializar
pygame.init()

# Janela
LARGURA = 800
ALTURA = 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("pon")

FPS = 60
CLOCK = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (25, 215, 25)       
LILAS = (240, 45, 125)      
CINZA = (100, 100, 100)
AZUL_CIANO = (30, 136, 229)  

# Objetos
largura_barra = 15
altura_barra = 100

barra_esq = pygame.Rect(20, ALTURA//2 - altura_barra//2, largura_barra, altura_barra)
barra_dir = pygame.Rect(LARGURA - 40, ALTURA//2 - altura_barra//2, largura_barra, altura_barra)

# Bola
bola = pygame.Rect(LARGURA//2 - 10, ALTURA//2 - 10, 20, 20)

# Velocidade
vel_bola_x = 4
vel_bola_y = 4
vel_barra = 6

# Pontuação
ponto_esq = 0
ponto_dir = 0
fonte = pygame.font.SysFont(None, 40)
fonte_grande = pygame.font.SysFont(None, 60)
fonte_pequena = pygame.font.SysFont(None, 30)

# Superfície para o rastro permanente
rastro_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
rastro_surface.fill(PRETO) 

# Controlador de rastro
ESPESURA = 20
ultima_posicao = None
cor_bola_atual = BRANCO  # Cor atual da bola
rastro_espessura = ESPESURA  # Espessura do traço do rastro

# Estado do jogo
jogo_ativo = True
vencedor = None
espaco_verde = 0
espaco_lilas = 0

# Variáveis para controle da IA
DIFICULDADE = 0.8  # 0.0 a 1.0 - quanto mais perto de 1, mais precisa
CHANCE_ERRO = 0.2    # Chance da IA errar 

def resetar_bola():
    global vel_bola_x, vel_bola_y, ultima_posicao, cor_bola_atual
    bola.center = (LARGURA//2, ALTURA//2)
    vel_bola_x = random.choice([-4, 4])  # Direção aleatória inicial
    vel_bola_y = random.uniform(-3, 3)   # Ângulo aleatório inicial
    ultima_posicao = None
    cor_bola_atual = BRANCO  # Bola volta a ser branca

def desenhar_ponto_rastro(posicao, cor):
    # Desenha um círculo na posição
    pygame.draw.circle(rastro_surface, cor, posicao, rastro_espessura//2)

def mover_ia():
    global barra_dir
    
    # Chance de errar propositalmente
    if random.random() < CHANCE_ERRO:
        # Movimento aleatório (errando)
        if random.random() < 0.5:
            barra_dir.y += random.randint(-vel_barra, vel_barra)
        return
    
    # Previsão da posição Y da bola
    if vel_bola_x > 0:  # Bola indo para a direita
        # Tempo até a bola chegar na barra
        tempo = (barra_dir.left - bola.right) / vel_bola_x if vel_bola_x != 0 else 0
        
        # Posição prevista da bola
        posicao_prevista = bola.centery + vel_bola_y * tempo
        
        # Aplica dificuldade (0 = não move, 1 = perfeito)
        if random.random() < DIFICULDADE:
            alvo_y = posicao_prevista
        else:
            # Erro controlado baseado na dificuldade
            erro = random.uniform(-50, 50) * (1 - DIFICULDADE)
            alvo_y = posicao_prevista + erro
    else:
        # Se a bola está indo para a esquerda, a IA volta para o centro
        alvo_y = ALTURA // 2
    
    # Move a barra em direção ao alvo
    if barra_dir.centery < alvo_y - 10:
        barra_dir.y += vel_barra
    elif barra_dir.centery > alvo_y + 10:
        barra_dir.y -= vel_barra
    
    # Mantém a barra dentro da tela
    barra_dir.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

def calcular_espaco_colorido():
    """Calcula quantos pixels de cada cor existem no rastro - SÓ NO FIM DO JOGO"""
    pixels_verde = 0
    pixels_lilas = 0
    
    # Lock a superfície para acesso aos pixels
    rastro_surface.lock()
    
    # Percorre uma amostra dos pixels (a cada 2 pixels para ser mais rápido)
    for y in range(0, ALTURA, 2):
        for x in range(0, LARGURA, 2):
            cor = rastro_surface.get_at((x, y))
            if cor[0:3] == VERDE:  # Compara apenas RGB (ignora alpha)
                pixels_verde += 4  # Multiplica por 4 pois pulamos pixels
            elif cor[0:3] == LILAS:
                pixels_lilas += 4
    
    rastro_surface.unlock()
    
    # Calcula porcentagens
    total_pixels = LARGURA * ALTURA
    porcentagem_verde = (pixels_verde / total_pixels) * 100
    porcentagem_lilas = (pixels_lilas / total_pixels) * 100
    
    return pixels_verde, pixels_lilas, porcentagem_verde, porcentagem_lilas

def finalizar_jogo():
    """Finaliza o jogo quando um ponto é marcado"""
    global jogo_ativo, vencedor, espaco_verde, espaco_lilas
    
    jogo_ativo = False
    
    # Calcula espaço colorido APENAS UMA VEZ no final
    pixels_verde, pixels_lilas, porcent_verde, porcent_lilas = calcular_espaco_colorido()
    espaco_verde = porcent_verde
    espaco_lilas = porcent_lilas
    
    # Determina o vencedor
    if porcent_verde > porcent_lilas:
        vencedor = "VERDE"
        cor_vencedor = VERDE
    elif porcent_lilas > porcent_verde:
        vencedor = "LILÁS"
        cor_vencedor = LILAS
    else:
        vencedor = "EMPATE"
        cor_vencedor = BRANCO
    
    return vencedor, cor_vencedor, pixels_verde, pixels_lilas, porcent_verde, porcent_lilas

def resetar_jogo():
    """Reseta o jogo completamente"""
    global ponto_esq, ponto_dir, ultima_posicao, cor_bola_atual, jogo_ativo, vencedor, espaco_verde, espaco_lilas
    ponto_esq = 0
    ponto_dir = 0
    ultima_posicao = None
    cor_bola_atual = BRANCO
    jogo_ativo = True
    vencedor = None
    espaco_verde = 0
    espaco_lilas = 0
    
    # Limpa a superfície de rastro (volta para preto)
    rastro_surface.fill(PRETO)
    
    # Reseta a posição da bola e barras
    resetar_bola()
    barra_esq.center = (20 + largura_barra//2, ALTURA//2)
    barra_dir.center = (LARGURA - 40 + largura_barra//2, ALTURA//2)

while True:
    # Observar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Tecla R para resetar o jogo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                resetar_jogo()

    if jogo_ativo:
        # Movimentação jogador esquerdo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] and barra_esq.top > 0:
            barra_esq.y -= vel_barra
        if teclas[pygame.K_s] and barra_esq.bottom < ALTURA:
            barra_esq.y += vel_barra
        
        # Movimentação IA
        mover_ia()
        
        # Adiciona marca de rastro se a bola se moveu
        posicao_atual = bola.center
        if ultima_posicao is not None:
            # Desenha ponto na posição atual
            desenhar_ponto_rastro(posicao_atual, cor_bola_atual)
            
            # Desenha pontos intermediários para traço contínuo
            distancia = ((posicao_atual[0] - ultima_posicao[0])**2 + 
                        (posicao_atual[1] - ultima_posicao[1])**2)**0.5
            
            if distancia > 2:  # Se moveu o suficiente
                # Interpola pontos entre as posições
                passos = int(distancia / 2) + 1
                for i in range(1, passos):
                    t = i / passos
                    x = int(ultima_posicao[0] + (posicao_atual[0] - ultima_posicao[0]) * t)
                    y = int(ultima_posicao[1] + (posicao_atual[1] - ultima_posicao[1]) * t)
                    desenhar_ponto_rastro((x, y), cor_bola_atual)
        
        ultima_posicao = posicao_atual
        
        # Movimentação da bola
        bola.x += vel_bola_x
        bola.y += vel_bola_y
        
        # Colisão com as bordas superior e inferior
        if bola.top <= 0:
            vel_bola_y = abs(vel_bola_y)  # Força para baixo
            bola.top = 1  # Corrige posição
        elif bola.bottom >= ALTURA:
            vel_bola_y = -abs(vel_bola_y)  # Força para cima
            bola.bottom = ALTURA - 1  # Corrige posição
        
        # Colisão com as barras - A bola assume a cor da barra que bateu
        if bola.colliderect(barra_esq):
            vel_bola_x = abs(vel_bola_x)  # Garante que vá para a direita
            # Ângulo baseado na posição de contato
            fator = (bola.centery - barra_esq.centery) / (altura_barra / 2)
            vel_bola_y = fator * 5
            # Corrige posição para evitar colisão múltipla
            bola.left = barra_esq.right + 1
            # Bola assume a cor da barra esquerda (VERDE)
            cor_bola_atual = VERDE
        
        if bola.colliderect(barra_dir):
            vel_bola_x = -abs(vel_bola_x)  # Garante que vá para a esquerda
            # Ângulo baseado na posição de contato
            fator = (bola.centery - barra_dir.centery) / (altura_barra / 2)
            vel_bola_y = fator * 5
            # Corrige posição para evitar colisão múltipla
            bola.right = barra_dir.left - 1
            # Bola assume a cor da barra direita (LILÁS)
            cor_bola_atual = LILAS
        
        # Marcar ponto - O jogo termina após qualquer ponto
        if bola.left <= 0:
            ponto_dir += 1
            vencedor_info, cor_vencedor, pixels_verde, pixels_lilas, porcent_verde, porcent_lilas = finalizar_jogo()
            
        if bola.right >= LARGURA:
            ponto_esq += 1
            vencedor_info, cor_vencedor, pixels_verde, pixels_lilas, porcent_verde, porcent_lilas = finalizar_jogo()
    
    # Desenho
    TELA.fill(PRETO)
    
    # Desenha a superfície de rastro (fundo)
    TELA.blit(rastro_surface, (0, 0))
    
    if jogo_ativo:
        # Desenha barras com cores diferentes
        pygame.draw.rect(TELA, VERDE, barra_esq)
        pygame.draw.rect(TELA, LILAS, barra_dir)
        
        # Desenha a bola com a cor atual (que muda quando bate nas barras)
        pygame.draw.rect(TELA, cor_bola_atual, bola)
        
        # Linha do centro pontilhada
        for y in range(0, ALTURA, 20):
            pygame.draw.line(TELA, BRANCO, (LARGURA//2, y), (LARGURA//2, y + 10), 1)
    else:
        # Tela de fim de jogo        
        # Mostra o vencedor baseado no espaço colorido
        vencedor_texto = fonte_grande.render(f"VENCEDOR: {vencedor_info}", True, AZUL_CIANO)
        TELA.blit(vencedor_texto, (LARGURA//2 - vencedor_texto.get_width()//2, ALTURA//2 - 80))
        
        # Mostra estatísticas de espaço colorido (já calculadas)
        stats_texto = fonte.render(
            f"Espaço Verde: {espaco_verde:.1f}%  |  Espaço Lilás: {espaco_lilas:.1f}%", 
            True, AZUL_CIANO
        )
        TELA.blit(stats_texto, (LARGURA//2 - stats_texto.get_width()//2, ALTURA//2))
        
        # Instruções para reiniciar
        reiniciar_texto = fonte.render("Pressione R para jogar novamente", True, AZUL_CIANO)
        TELA.blit(reiniciar_texto, (LARGURA//2 - reiniciar_texto.get_width()//2, ALTURA - 100))
        
        # Mostra barras cinzas (jogo pausado)
        pygame.draw.rect(TELA, CINZA, barra_esq)
        pygame.draw.rect(TELA, CINZA, barra_dir)
        
        # Bola no centro (cinza)
        bola.center = (LARGURA//2, ALTURA//2)
        pygame.draw.rect(TELA, CINZA, bola)
    
    pygame.display.update()
    CLOCK.tick(FPS)