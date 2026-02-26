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

def alterar_som(tela, fundo_inicial, fonte, largura_tela, mouse, som_botao, cinza, preto, eventos, estado_jogo, TELA_INICIAL, volume_atual):
        tela.blit(fundo_inicial, (0, 0))
        pygame.draw.rect(tela, (200, 200, 200), (200, 150, 400, 300))
        pygame.draw.rect(tela, (0, 0, 0), (200, 150, 400, 300), 3)

        texto = fonte.render("Ajuste a altura da música", True, (0, 0, 0))
        tela.blit(texto, (largura_tela//2 - texto.get_width()//2, 170))

        arrastando = False
        volume_pos_x = 250
        volume_pos_y = 250
        volume_largura = 300
        volume_altura = 20
        pygame.draw.rect(tela, (150, 150, 150), (volume_pos_x, volume_pos_y, volume_largura, volume_altura))
        volume_atual = float(volume_atual)  # Certifica de que é um float
        barra_largura = volume_atual * volume_largura
        pygame.draw.rect(tela, (0, 200, 0), (volume_pos_x, volume_pos_y, barra_largura, volume_altura))

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo do mouse foi clicado
                if pygame.Rect(volume_pos_x, volume_pos_y, volume_largura, volume_altura).collidepoint(evento.pos):
                    arrastando = True   

            if evento.type == pygame.MOUSEBUTTONUP:
                arrastando = False

            if evento.type == pygame.MOUSEMOTION and arrastando:
                mouse_x = evento.pos[0]
                volume_atual = (mouse_x - volume_pos_x) / volume_largura
                volume_atual = max(0, min(1, volume_atual))
                pygame.mixer.music.set_volume(volume_atual)

        # Botão Voltar
        hover_voltar = (largura_tela//2 - 50 < mouse[0] < largura_tela//2 + 50) and (400 < mouse[1] < 450)
        if hover_voltar and not getattr(desenhar_botao, "ja_hover_voltar", False):
            som_botao.play()
        desenhar_botao.ja_hover_voltar = hover_voltar
        if desenhar_botao(tela, "Voltar", largura_tela//2 - 50, 400, 100, 50, cinza, preto, eventos):
            estado_jogo = TELA_INICIAL
        
        return volume_atual, estado_jogo