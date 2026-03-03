import pygame
import time

mensagem_famoso = ""
tempo_mensagem = 0

def exibir_pontuacao(tela, pontuacao):
    fonte = pygame.font.Font(None, 36)
    cor_texto = (255, 255, 255)
    texto = fonte.render(f"Score: {pontuacao}", True, cor_texto)
    tela.blit(texto, (20, 20))

def adicionar_tempo_escudo(tempo_fim_escudo, duracao_bonus):
    """
    Adiciona tempo ao escudo de forma acumulativa.
    Retorna o novo tempo final.
    """
    agora = pygame.time.get_ticks()

    if tempo_fim_escudo > agora:
        # Escudo já ativo → acumula
        return tempo_fim_escudo + duracao_bonus
    else:
        # Escudo inativo → inicia novo
        return agora + duracao_bonus


def escudo_ativo(tempo_fim_escudo):
    """
    Retorna True se o escudo ainda estiver ativo.
    """
    return pygame.time.get_ticks() < tempo_fim_escudo


def desenhar_barra_escudo(tela, tempo_fim_escudo, duracao_bonus, fonte):
    """
    Desenha barra de tempo restante + contador.
    """
    agora = pygame.time.get_ticks()
    tempo_restante = max(0, tempo_fim_escudo - agora)

    if tempo_restante <= 0:
        return  # não desenha se não estiver ativo

    proporcao = tempo_restante / duracao_bonus
    proporcao = max(0, min(1, proporcao))

    # Configurações visuais
    largura_barra = 200
    altura_barra = 20
    x_barra = 580
    y_barra = 20

    # Fundo
    pygame.draw.rect(tela, (80, 80, 80),
                     (x_barra, y_barra, largura_barra, altura_barra))

    # Barra azul
    pygame.draw.rect(tela, (0, 200, 255),
                     (x_barra, y_barra, largura_barra * proporcao, altura_barra))

    # Texto em segundos
    segundos = tempo_restante // 1000
    texto = fonte.render(f"Escudo: {segundos}s", True, (255, 255, 255))
    tela.blit(texto, (x_barra, y_barra + 25))

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