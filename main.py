import os
import random
import sys

try:
    import pygame
except ModuleNotFoundError:
    sys.stderr.write(
        "Erro: o módulo 'pygame' não está instalado.\n"
        "Use: py -3.11 -m pip install -r requirements.txt\n"
        "Depois execute: py -3.11 main.py\n"
    )
    raise SystemExit(1)

from bonus import Bonus
from boss import Boss
from obstacle import Obstacle
from player import Player
from projeteis import Projectile
from utils import (
    adicionar_tempo_escudo,
    alterar_som,
    carregar_recorde,
    desenhar_barra_escudo,
    desenhar_botao,
    escudo_ativo,
    exibir_mensagem_temporaria,
    exibir_pontuacao,
    salvar_recorde,
)

# -------------------------
# Inicialização do Pygame
# -------------------------
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -------------------------
# Configuração da tela
# -------------------------
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Goiabinha")

# -------------------------
# Sons
# -------------------------
som_botao = pygame.mixer.Sound(os.path.join(os.getcwd(), "sounds/botao_inicial.wav"))
som_morte = pygame.mixer.Sound(os.path.join(os.getcwd(), "sounds/Sad Violin.mp3"))

pygame.mixer.music.load(os.path.join(os.getcwd(), "sounds/musica.mp3"))
volume_atual = 0.5
pygame.mixer.music.set_volume(volume_atual)
pygame.mixer.music.play(-1)

# -------------------------
# Imagens
# -------------------------
fundo_jogo = pygame.image.load("images/Background.jpg").convert()
fundo_jogo = pygame.transform.scale(fundo_jogo, (LARGURA_TELA, ALTURA_TELA))
fundo_inicial = pygame.image.load("images/Background_TelaInicial.png").convert()
fundo_inicial = pygame.transform.scale(fundo_inicial, (LARGURA_TELA, ALTURA_TELA))

escudo_img = pygame.image.load("images/shield_force.png").convert_alpha()
escudo_img = pygame.transform.scale(escudo_img, (120, 120))
escudo_img.set_alpha(100)

overlay_jogo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
overlay_jogo.fill((50, 50, 50))
overlay_jogo.set_alpha(60)

# -------------------------
# Cores, fontes e clock
# -------------------------
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 36)
fonte_grande = pygame.font.Font(None, 108)
fonte_mensagem = pygame.font.Font(None, 42)

# -------------------------
# Constantes de gameplay
# -------------------------
VELOCIDADE_PLAYER = 5
VELOCIDADE_FUNDO_INICIAL = 2
VELOCIDADE_FUNDO_MAX = 8
VELOCIDADE_OBSTACULO_INICIAL = 6
VELOCIDADE_OBSTACULO_MAX = 14
INTERVALO_OBSTACULO_INICIAL = 1500
INTERVALO_OBSTACULO_MIN = 700
DURACAO_BONUS = 5000
DURACAO_MENSAGEM = 2000
PONTOS_BOSS = 150
DURACAO_ATAQUE_BOSS = 8000
TEMPO_MINIMO_REAPARECIMENTO = 20000
TEMPO_MAXIMO_REAPARECIMENTO = 60000

# -------------------------
# Estados do jogo
# -------------------------
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2
CONFIG = 3


def resetar_jogo():
    player = Player(tela, LARGURA_TELA, ALTURA_TELA)
    escudo = pygame.transform.scale(
        escudo_img,
        (player.image.get_width() + 50, player.image.get_height() + 50),
    )
    escudo.set_alpha(100)

    return {
        "player": player,
        "escudo_img": escudo,
        "bonus": pygame.sprite.Group(),
        "obstaculos": pygame.sprite.Group(),
        "projecteis": pygame.sprite.Group(),
        "boss": None,
        "boss_ataque_inicio": 0,
        "boss_ultimo_tiro": 0,
        "boss_proximo_tiro": 0,
        "boss_cooldown": 0,
        "pontuacao": 0.0,
        "velocidade_obstaculo": VELOCIDADE_OBSTACULO_INICIAL,
        "intervalo_obstaculo": INTERVALO_OBSTACULO_INICIAL,
        "ultimo_tempo_obstaculo": pygame.time.get_ticks(),
        "ultimo_tempo_bonus": pygame.time.get_ticks(),
        "imune": False,
        "tempo_fim_escudo": 0,
        "duracao_total_escudo": 0,
        "mensagem": "",
        "tempo_fim_mensagem": 0,
        "x_fundo": 0,
        "velocidade_fundo": VELOCIDADE_FUNDO_INICIAL,
        "som_morte_tocado": False,
    }


def mostrar_mensagem(estado, texto):
    estado["mensagem"] = texto
    estado["tempo_fim_mensagem"] = pygame.time.get_ticks() + DURACAO_MENSAGEM


def desenhar_fundo_parallax(estado):
    rel_x = estado["x_fundo"] % fundo_jogo.get_width()
    tela.blit(fundo_jogo, (rel_x - fundo_jogo.get_width(), 0))
    if rel_x < LARGURA_TELA:
        tela.blit(fundo_jogo, (rel_x, 0))
    estado["x_fundo"] -= estado["velocidade_fundo"]
    estado["velocidade_fundo"] = min(
        estado["velocidade_fundo"] + 0.001,
        VELOCIDADE_FUNDO_MAX,
    )


def spawn_obstaculo(estado):
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - estado["ultimo_tempo_obstaculo"] < estado["intervalo_obstaculo"]:
        return

    tipo_obstaculo = random.randint(1, 4)
    estado["obstaculos"].add(
        Obstacle(tela, LARGURA_TELA, ALTURA_TELA, tipo_obstaculo, estado["velocidade_obstaculo"])
    )
    estado["ultimo_tempo_obstaculo"] = tempo_atual
    estado["velocidade_obstaculo"] = min(
        estado["velocidade_obstaculo"] + 0.05,
        VELOCIDADE_OBSTACULO_MAX,
    )
    estado["intervalo_obstaculo"] = max(
        INTERVALO_OBSTACULO_MIN,
        estado["intervalo_obstaculo"] - 15,
    )


def spawn_bonus(estado):
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - estado["ultimo_tempo_bonus"] < 3000:
        return
    if random.randint(1, 100) > 8:
        return

    velocidade_bonus = min(estado["velocidade_obstaculo"], VELOCIDADE_OBSTACULO_MAX)
    estado["bonus"].add(Bonus(tela, LARGURA_TELA, ALTURA_TELA, velocidade_bonus))
    estado["ultimo_tempo_bonus"] = tempo_atual


def spawn_boss(estado):
    agora = pygame.time.get_ticks()
    if estado["boss"] is not None:
        return
    if estado["pontuacao"] < PONTOS_BOSS or agora < estado["boss_cooldown"]:
        return

    estado["boss"] = Boss(LARGURA_TELA, ALTURA_TELA)
    estado["boss_ataque_inicio"] = 0
    estado["boss_ultimo_tiro"] = agora
    estado["boss_proximo_tiro"] = agora + random.randint(250, 600)
    mostrar_mensagem(estado, "Boss apareceu! Prepare-se!")


def processar_bonus(estado):
    for b in list(estado["bonus"]):
        b.mover()
        b.desenhar()

        if b.fora_da_tela():
            estado["bonus"].remove(b)
            continue

        if not estado["player"].rect.colliderect(b.rect):
            continue

        if b.tipo == "images/ferramenta_bonus.png":
            estado["imune"] = True
            estado["tempo_fim_escudo"], estado["duracao_total_escudo"] = adicionar_tempo_escudo(
                estado["tempo_fim_escudo"],
                DURACAO_BONUS,
            )
            mostrar_mensagem(estado, "Escudo ativado!")
        elif b.tipo == "images/bebe_bonus.png":
            estado["pontuacao"] += 10
            mostrar_mensagem(estado, "Você ficou famoso no Instagram!")
        elif b.tipo == "images/ppr_bonus.png":
            estado["pontuacao"] += 50
            mostrar_mensagem(estado, "PPR coletado! +50 pontos!")

        estado["bonus"].remove(b)


def tocar_som_hover(flag_attr, hover, som):
    if hover and not getattr(desenhar_botao, flag_attr, False):
        som.play()
    setattr(desenhar_botao, flag_attr, hover)


# -------------------------
# Estado inicial
# -------------------------
recorde = carregar_recorde()
estado_jogo = TELA_INICIAL
jogo = resetar_jogo()

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    mouse = pygame.mouse.get_pos()

    if estado_jogo == TELA_INICIAL:
        tela.blit(fundo_inicial, (0, 0))

        if recorde > 0:
            rec_texto = fonte.render(f"Recorde: {recorde}", True, (255, 215, 0))
            tela.blit(rec_texto, (LARGURA_TELA // 2 - rec_texto.get_width() // 2, 200))

        controles = fonte.render("A/D mover  |  Espaço pular (duplo)", True, PRETO)
        tela.blit(controles, (LARGURA_TELA // 2 - controles.get_width() // 2, 360))

        tocar_som_hover("ja_hover_start", (LARGURA_TELA // 2 - 100 < mouse[0] < LARGURA_TELA // 2 + 100) and (400 < mouse[1] < 450), som_botao)
        if desenhar_botao(tela, "Iniciar Jogo", LARGURA_TELA // 2 - 100, 400, 200, 50, CINZA, PRETO, eventos, fonte):
            estado_jogo = JOGANDO
            jogo = resetar_jogo()

        tocar_som_hover("ja_hover_config", (LARGURA_TELA // 2 - 100 < mouse[0] < LARGURA_TELA // 2 + 100) and (470 < mouse[1] < 520), som_botao)
        if desenhar_botao(tela, "Configuração", LARGURA_TELA // 2 - 100, 470, 200, 50, CINZA, PRETO, eventos, fonte):
            estado_jogo = CONFIG

    elif estado_jogo == CONFIG:
        volume_atual, estado_jogo = alterar_som(
            tela, fundo_inicial, fonte, LARGURA_TELA, mouse, som_botao, CINZA, PRETO,
            eventos, estado_jogo, TELA_INICIAL, volume_atual,
        )

    elif estado_jogo == JOGANDO:
        desenhar_fundo_parallax(jogo)
        tela.blit(overlay_jogo, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            jogo["player"].rect.x -= VELOCIDADE_PLAYER
        if keys[pygame.K_d]:
            jogo["player"].rect.x += VELOCIDADE_PLAYER
        jogo["player"].rect.left = max(0, jogo["player"].rect.left)
        jogo["player"].rect.right = min(LARGURA_TELA, jogo["player"].rect.right)

        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                jogo["player"].pular()

        jogo["player"].atualizar()
        jogo["player"].desenhar()

        desenhar_barra_escudo(tela, jogo["tempo_fim_escudo"], jogo["duracao_total_escudo"], fonte)

        if jogo["imune"]:
            shield_rect = jogo["escudo_img"].get_rect(center=jogo["player"].rect.center)
            tela.blit(jogo["escudo_img"], shield_rect)

        if jogo["boss"] is None:
            spawn_obstaculo(jogo)
        spawn_boss(jogo)

        if jogo["boss"] is not None:
            agora = pygame.time.get_ticks()
            jogo["boss"].atualizar(LARGURA_TELA, ALTURA_TELA)
            jogo["boss"].desenhar(tela)
            jogo["boss"].mostrar_falas(tela, fonte_mensagem)

            if jogo["boss_ataque_inicio"] and agora - jogo["boss_ataque_inicio"] >= DURACAO_ATAQUE_BOSS:
                jogo["boss"] = None
                jogo["boss_ataque_inicio"] = 0
                jogo["boss_cooldown"] = agora + random.randint(TEMPO_MINIMO_REAPARECIMENTO, TEMPO_MAXIMO_REAPARECIMENTO)
                jogo["projecteis"].empty()
                jogo["boss_proximo_tiro"] = 0
                mostrar_mensagem(jogo, "O boss vai voltar novamente...")
            elif jogo["boss"].estado == jogo["boss"].ATACANDO:
                if jogo["boss_ataque_inicio"] == 0:
                    jogo["boss_ataque_inicio"] = jogo["boss"].tempo_inicio_ataque or agora
                    jogo["boss_ultimo_tiro"] = agora
                    jogo["boss_proximo_tiro"] = agora + random.randint(180, 520)

                if agora >= jogo["boss_proximo_tiro"]:
                    jogo["projecteis"].add(Projectile.criar_aleatorio(LARGURA_TELA, ALTURA_TELA))
                    jogo["boss_ultimo_tiro"] = agora
                    jogo["boss_proximo_tiro"] = agora + random.randint(220, 700)

                for proj in list(jogo["projecteis"]):
                    proj.mover()
                    proj.desenhar(tela)
                    if proj.rect.colliderect(jogo["player"].rect) and not jogo["imune"]:
                        estado_jogo = GAME_OVER
                        recorde = salvar_recorde(int(jogo["pontuacao"]))
                        pygame.mixer.music.stop()
                        if not jogo["som_morte_tocado"]:
                            som_morte.play()
                            jogo["som_morte_tocado"] = True
                        break
                    if proj.fora_da_tela():
                        jogo["projecteis"].remove(proj)

        for obstaculo in list(jogo["obstaculos"]):
            obstaculo.mover()
            obstaculo.desenhar()
            if jogo["player"].rect.colliderect(obstaculo.rect) and not jogo["imune"]:
                estado_jogo = GAME_OVER
                recorde = salvar_recorde(int(jogo["pontuacao"]))
                pygame.mixer.music.stop()
                if not jogo["som_morte_tocado"]:
                    som_morte.play()
                    jogo["som_morte_tocado"] = True
            if obstaculo.fora_da_tela():
                jogo["obstaculos"].remove(obstaculo)

        spawn_bonus(jogo)
        processar_bonus(jogo)

        if not escudo_ativo(jogo["tempo_fim_escudo"]):
            jogo["imune"] = False
            jogo["duracao_total_escudo"] = 0

        exibir_mensagem_temporaria(tela, jogo["mensagem"], fonte_mensagem, jogo["tempo_fim_mensagem"])

        jogo["pontuacao"] += 1 / FPS
        exibir_pontuacao(tela, int(jogo["pontuacao"]), fonte, recorde)

    elif estado_jogo == GAME_OVER:
        fundo_cinza = fundo_jogo.copy()
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        overlay.fill((100, 100, 100))
        overlay.set_alpha(150)
        fundo_cinza.blit(overlay, (0, 0))
        tela.blit(fundo_cinza, (0, 0))

        player_img = jogo["player"].image.copy()
        cinza_overlay = pygame.Surface(player_img.get_size())
        cinza_overlay.fill((180, 180, 180))
        player_img.blit(cinza_overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        player_img.set_alpha(180)
        tela.blit(player_img, jogo["player"].rect.topleft)

        game_over_texto = fonte_grande.render("Goiabinha faleceu!", True, VERMELHO)
        tela.blit(game_over_texto, (LARGURA_TELA // 2 - game_over_texto.get_width() // 2, 160))

        score_final = fonte.render(f"Pontuação: {int(jogo['pontuacao'])}", True, (255, 255, 255))
        tela.blit(score_final, (LARGURA_TELA // 2 - score_final.get_width() // 2, 260))

        rec_final = fonte.render(f"Recorde: {recorde}", True, (255, 215, 0))
        tela.blit(rec_final, (LARGURA_TELA // 2 - rec_final.get_width() // 2, 300))

        tocar_som_hover("ja_hover_reiniciar", (LARGURA_TELA // 2 - 100 < mouse[0] < LARGURA_TELA // 2 + 100) and (360 < mouse[1] < 410), som_botao)
        if desenhar_botao(tela, "Reiniciar", LARGURA_TELA // 2 - 100, 360, 200, 50, CINZA, PRETO, eventos, fonte):
            estado_jogo = TELA_INICIAL
            som_morte.stop()
            jogo["som_morte_tocado"] = False
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume_atual)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
