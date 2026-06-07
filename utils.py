import pygame
from pathlib import Path

ARQUIVO_RECORDE = Path("highscore.txt")


def carregar_recorde() -> int:
    try:
        return int(ARQUIVO_RECORDE.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError, OSError):
        return 0


def salvar_recorde(pontuacao: int) -> int:
    recorde = carregar_recorde()
    if pontuacao > recorde:
        ARQUIVO_RECORDE.write_text(str(pontuacao), encoding="utf-8")
        return pontuacao
    return recorde


def exibir_pontuacao(tela, pontuacao: int, fonte, recorde: int = 0):
    texto = fonte.render(f"Score: {pontuacao}", True, (255, 255, 255))
    tela.blit(texto, (20, 20))
    if recorde > 0:
        rec = fonte.render(f"Recorde: {recorde}", True, (255, 215, 0))
        tela.blit(rec, (20, 55))


def adicionar_tempo_escudo(tempo_fim_escudo: int, duracao_bonus: int) -> tuple[int, int]:
    agora = pygame.time.get_ticks()

    if tempo_fim_escudo > agora:
        tempo_restante = tempo_fim_escudo - agora
        nova_duracao_total = tempo_restante + duracao_bonus
    else:
        nova_duracao_total = duracao_bonus

    return agora + nova_duracao_total, nova_duracao_total


def escudo_ativo(tempo_fim_escudo: int) -> bool:
    return pygame.time.get_ticks() < tempo_fim_escudo


def desenhar_barra_escudo(tela, tempo_fim_escudo: int, duracao_total_escudo: int, fonte):
    agora = pygame.time.get_ticks()
    tempo_restante = max(0, tempo_fim_escudo - agora)

    if tempo_restante <= 0 or duracao_total_escudo <= 0:
        return

    proporcao = max(0, min(1, tempo_restante / duracao_total_escudo))

    largura_barra = 200
    altura_barra = 20
    x_barra = 580
    y_barra = 20

    pygame.draw.rect(tela, (80, 80, 80), (x_barra, y_barra, largura_barra, altura_barra))
    pygame.draw.rect(tela, (0, 200, 255), (x_barra, y_barra, largura_barra * proporcao, altura_barra))

    segundos = tempo_restante // 1000
    texto = fonte.render(f"Escudo: {segundos}s", True, (255, 255, 255))
    tela.blit(texto, (x_barra, y_barra + 25))


def exibir_mensagem_temporaria(tela, texto_msg: str, fonte, tempo_fim: int):
    if pygame.time.get_ticks() >= tempo_fim or not texto_msg:
        return

    texto = fonte.render(texto_msg, True, (255, 255, 255))
    x = (tela.get_width() - texto.get_width()) // 2
    tela.blit(texto, (x, 200))


def desenhar_botao(tela, texto, x, y, largura, altura, cor_botao, cor_texto, eventos, fonte=None):
    if fonte is None:
        fonte = pygame.font.Font(None, 36)

    retangulo = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, cor_botao, retangulo, border_radius=12)

    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=retangulo.center)
    tela.blit(texto_renderizado, texto_rect)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if retangulo.collidepoint(evento.pos):
                return True
    return False


def alterar_som(tela, fundo_inicial, fonte, largura_tela, mouse, som_botao, cinza, preto, eventos, estado_jogo, TELA_INICIAL, volume_atual):
    tela.blit(fundo_inicial, (0, 0))
    pygame.draw.rect(tela, (200, 200, 200), (200, 150, 400, 300))
    pygame.draw.rect(tela, (0, 0, 0), (200, 150, 400, 300), 3)

    texto = fonte.render("Ajuste o volume da música", True, (0, 0, 0))
    tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, 170))

    volume_pos_x = 250
    volume_pos_y = 250
    volume_largura = 300
    volume_altura = 20
    slider_rect = pygame.Rect(volume_pos_x, volume_pos_y, volume_largura, volume_altura)

    pygame.draw.rect(tela, (150, 150, 150), slider_rect)
    barra_largura = volume_atual * volume_largura
    pygame.draw.rect(tela, (0, 200, 0), (volume_pos_x, volume_pos_y, barra_largura, volume_altura))

    arrastando = getattr(alterar_som, "arrastando", False)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if slider_rect.collidepoint(evento.pos):
                arrastando = True
                volume_atual = max(0, min(1, (evento.pos[0] - volume_pos_x) / volume_largura))
                pygame.mixer.music.set_volume(volume_atual)
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            arrastando = False
        elif evento.type == pygame.MOUSEMOTION and arrastando:
            volume_atual = max(0, min(1, (evento.pos[0] - volume_pos_x) / volume_largura))
            pygame.mixer.music.set_volume(volume_atual)

    alterar_som.arrastando = arrastando

    hover_voltar = (largura_tela // 2 - 50 < mouse[0] < largura_tela // 2 + 50) and (400 < mouse[1] < 450)
    if hover_voltar and not getattr(alterar_som, "ja_hover_voltar", False):
        som_botao.play()
    alterar_som.ja_hover_voltar = hover_voltar
    if desenhar_botao(tela, "Voltar", largura_tela // 2 - 50, 400, 100, 50, cinza, preto, eventos, fonte):
        estado_jogo = TELA_INICIAL

    return volume_atual, estado_jogo
