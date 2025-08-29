import pygame
import time

mensagem_famoso = ""
tempo_mensagem = 0

def exibir_pontuacao(tela, pontuacao):
    fonte = pygame.font.Font(None, 36)
    preto = (0, 0, 0)
    texto = fonte.render(f"Score: {pontuacao}", True, preto)
    tela.blit(texto, (10, 10))

def exibir_mensagem_bonus(tela):
    global mensagem_famoso, tempo_mensagem
    if mensagem_famoso and time.time() - tempo_mensagem < 2:
        fonte = pygame.font.Font(None, 48)
        vermelho = (255, 0, 0)
        texto = fonte.render(mensagem_famoso, True, vermelho)
        largura_texto = texto.get_width()
        altura_texto = texto.get_height()
        tela.blit(texto, ((tela.get_width() - largura_texto) // 2, tela.get_height() // 2 - altura_texto))
    elif mensagem_famoso:
        mensagem_famoso = ""  # Resetar após 2 segundos

def definir_mensagem_famoso(msg):
    global mensagem_famoso, tempo_mensagem
    mensagem_famoso = msg
    tempo_mensagem = time.time()

def desenhar_botao(tela, texto, x, y, largura, altura, cor_botao, cor_texto, eventos):
    fonte = pygame.font.Font(None, 36)
    retangulo = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, cor_botao, retangulo, border_radius=12)

    # Texto centralizado
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=retangulo.center)
    tela.blit(texto_renderizado, texto_rect)

    # Verifica se clicou no botão
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if retangulo.collidepoint(pygame.mouse.get_pos()):
                return True
    return False
