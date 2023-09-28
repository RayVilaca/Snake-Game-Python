# Configurações iniciais
import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 800, 600
margem_total = 16
margem_borda = 11
espessura_borda_tela = 3
espessura_borda_cobra = 1

largura += 2 * margem_total
altura += 2 * margem_total

tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
cinza = (128,128,128)
verde_claro = (144,238,144)
verde_medio = (50,205,50)
verde_escuro = (0, 255, 0)

# Parâmetros da cobra
tamanho_quadrado = 20
velocidade_jogo = 10

def gerar_comida():
    comida_x = margem_total + round(random.randrange(0, largura - 2 * margem_total - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = margem_total + round(random.randrange(0, altura - 2 * margem_total - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    cor = random.choice([verde_claro, verde_medio, verde_escuro])
    
    pygame.draw.rect(tela, cor, [comida_x, comida_y, tamanho, tamanho])
    
def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, preta, [pixel[0], pixel[1], tamanho, tamanho], espessura_borda_cobra)
        pygame.draw.rect(tela, pixel[2], [pixel[0] + espessura_borda_cobra, pixel[1] + espessura_borda_cobra, tamanho - 2 * espessura_borda_cobra, tamanho - 2 * espessura_borda_cobra])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.Font("fonts/PixelifySans-VariableFont_wght.ttf", 50)
    texto = fonte.render(f"{pontuacao:04d}", True, branca)
    tela.blit(texto, [margem_total, 1])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    
    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = - tamanho_quadrado
    
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0  
    
    elif tecla == pygame.K_LEFT:
        velocidade_x = - tamanho_quadrado
        velocidade_y = 0
        
    return velocidade_x, velocidade_y

def desenhar_bordas():
    pygame.draw.rect(tela, branca, [margem_borda, margem_borda, largura - 2 * margem_borda, altura - 2 * margem_borda], espessura_borda_tela)

def rodar_jogo():
    fim_jogo = False
    
    x = largura / 2
    y = altura / 2
    
    velocidade_x = 0
    velocidade_y = 0
    
    tamanho_cobra = 1
    pixels = []
    
    comida_x, comida_y = gerar_comida()
    
    cor = cinza
    
    while not fim_jogo:
        tela.fill(preta)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)
        
        # Desenhar bordas
        desenhar_bordas()
        
        # Desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)
        
        if x < margem_total or x >= (largura - margem_total) or y < margem_total or y >= (altura - margem_total):
            fim_jogo = True
        
        # Atualizar a posição da cobra
        x += velocidade_x
        y += velocidade_y
        
        # Desenhar cobra
        pixels.append([x, y, cor])
        if len(pixels) > tamanho_cobra:
            del pixels[0]
        
        # Cobra colidiu em si mesma
        for pixel in pixels[:-1]:
            if pixel[:-1] == [x, y]:
                fim_jogo = True
        
        desenhar_cobra(tamanho_quadrado, pixels)
        
        # Desenhar os pontos
        desenhar_pontuacao(tamanho_cobra-1)
        
        # Atualização da tela
        pygame.display.update()
        
        # Criação de nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()
            
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)

            cor = (red, green, blue)
        
        relogio.tick(velocidade_jogo)

rodar_jogo()