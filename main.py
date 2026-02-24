import pygame
import random
import os
from player import Player
from bonus import Bonus
from utils import exibir_pontuacao, desenhar_botao
from obstacle import Obstacle

# -------------------------
# Inicialização do Pygame
# -------------------------
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.init()

# -------------------------
# Diretório de trabalho
# -------------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -------------------------
# Configuração da tela
# -------------------------
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Goiabinha")

# -------------------------
# Sons
# -------------------------
som_botao = pygame.mixer.Sound(os.path.join(os.getcwd(), "sounds/botao_inicial.wav"))
som_morte = pygame.mixer.Sound(os.path.join(os.getcwd(), "sounds/Sad Violin.mp3"))

# Música de fundo
pygame.mixer.music.load(os.path.join(os.getcwd(), "sounds/musica.mp3"))
volume_atual = 0.5
pygame.mixer.music.set_volume(volume_atual)
pygame.mixer.music.play(-1)

# -------------------------
# Imagens de fundo
# -------------------------
fundo_jogo = pygame.image.load("images/Background.jpg").convert()
fundo_jogo = pygame.transform.scale(fundo_jogo, (largura_tela, altura_tela))
fundo_inicial = pygame.image.load("images/Background_TelaInicial.png").convert()
fundo_inicial = pygame.transform.scale(fundo_inicial, (largura_tela, altura_tela))

x_fundo = 0
velocidade_fundo = 2

# -------------------------
# Cores e FPS
# -------------------------
vermelho = (255, 0, 0)
preto = (0, 0, 0)
cinza = (200, 200, 200)
clock = pygame.time.Clock()

# -------------------------
# Variáveis do jogo
# -------------------------
velocidade_player = 5
player = Player(tela, largura_tela, altura_tela)
bonus = pygame.sprite.Group()
obstaculos = pygame.sprite.Group()
pontuacao = 0
velocidade_obstaculo = 6
ultimo_tempo_obstaculo = 0
intervalo_minimo = 1000
imune = False
tempo_imunidade = 0
mensagem_famoso = False
tempo_mensagem = 0
som_morte_tocado = False

fonte = pygame.font.Font(None, 36)

# -------------------------
# Estados do jogo
# -------------------------
TELA_INICIAL = 0
JOGANDO = 1
GAME_OVER = 2
CONFIG = 3
estado_jogo = TELA_INICIAL

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    mouse = pygame.mouse.get_pos()

    # -------------------------
    # TELA INICIAL
    # -------------------------
    if estado_jogo == TELA_INICIAL:
        tela.blit(fundo_inicial, (0, 0))

        # Botão Iniciar
        hover_start = (largura_tela//2 - 100 < mouse[0] < largura_tela//2 + 100) and (400 < mouse[1] < 450)
        if hover_start and not getattr(desenhar_botao, "ja_hover_start", False):
            som_botao.play()
        desenhar_botao.ja_hover_start = hover_start
        if desenhar_botao(tela, "Iniciar Jogo", largura_tela//2 - 100, 400, 200, 50, cinza, preto, eventos):
            estado_jogo = JOGANDO
            player = Player(tela, largura_tela, altura_tela)
            escudo_img = pygame.image.load("images/shield_force.png").convert_alpha()
            escudo_img = pygame.transform.scale(
                escudo_img,
                (player.image.get_width() + 50, player.image.get_height() + 50)
            )
            escudo_img.set_alpha(100)
            bonus.empty()
            obstaculos.empty()
            pontuacao = 0
            velocidade_obstaculo = 6
            imune = False
            som_morte_tocado = False

        # Botão Configuração
        hover_config = (largura_tela//2 - 100 < mouse[0] < largura_tela//2 + 100) and (470 < mouse[1] < 520)
        if hover_config and not getattr(desenhar_botao, "ja_hover_config", False):
            som_botao.play()
        desenhar_botao.ja_hover_config = hover_config
        if desenhar_botao(tela, "Configuração", largura_tela//2 - 100, 470, 200, 50, cinza, preto, eventos):
            estado_jogo = CONFIG

    # -------------------------
    # CONFIGURAÇÃO (POP-UP)
    # -------------------------
    elif estado_jogo == CONFIG:
        tela.blit(fundo_inicial, (0, 0))
        pygame.draw.rect(tela, (200, 200, 200), (200, 150, 400, 300))
        pygame.draw.rect(tela, (0, 0, 0), (200, 150, 400, 300), 3)

        texto = fonte.render("Ajuste a altura da música", True, (0, 0, 0))
        tela.blit(texto, (largura_tela//2 - texto.get_width()//2, 170))

        volume_pos_x = 250
        volume_pos_y = 250
        volume_largura = 300
        volume_altura = 20
        pygame.draw.rect(tela, (150, 150, 150), (volume_pos_x, volume_pos_y, volume_largura, volume_altura))
        barra_largura = volume_atual * volume_largura
        pygame.draw.rect(tela, (0, 200, 0), (volume_pos_x, volume_pos_y, barra_largura, volume_altura))

        if pygame.mouse.get_pressed()[0]:
            mouse_x = pygame.mouse.get_pos()[0]
            if volume_pos_x <= mouse_x <= volume_pos_x + volume_largura:
                volume_atual = (mouse_x - volume_pos_x) / volume_largura
                pygame.mixer.music.set_volume(volume_atual)

        # Botão Voltar
        hover_voltar = (largura_tela//2 - 50 < mouse[0] < largura_tela//2 + 50) and (400 < mouse[1] < 450)
        if hover_voltar and not getattr(desenhar_botao, "ja_hover_voltar", False):
            som_botao.play()
        desenhar_botao.ja_hover_voltar = hover_voltar
        if desenhar_botao(tela, "Voltar", largura_tela//2 - 50, 400, 100, 50, cinza, preto, eventos):
            estado_jogo = TELA_INICIAL
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume_atual)

    # -------------------------
    # JOGO
    # -------------------------
    elif estado_jogo == JOGANDO:
        rel_x = x_fundo % fundo_jogo.get_width()
        tela.blit(fundo_jogo, (rel_x - fundo_jogo.get_width(), 0))
        if rel_x < largura_tela:
            tela.blit(fundo_jogo, (rel_x, 0))
        x_fundo -= velocidade_fundo

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.rect.x -= velocidade_player
        if keys[pygame.K_d]:
            player.rect.x += velocidade_player
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > largura_tela:
            player.rect.right = largura_tela

        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                player.pular()

        player.atualizar()
        player.desenhar()

        if imune:
            shield_rect = escudo_img.get_rect(center=player.rect.center)
            tela.blit(escudo_img, shield_rect)

        # Obstáculos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo_obstaculo > intervalo_minimo and random.randint(1, 50) == 1:
            tipo_obstaculo = random.randint(1, 4)
            obstaculos.add(Obstacle(tela, largura_tela, altura_tela, tipo_obstaculo, velocidade_obstaculo))
            ultimo_tempo_obstaculo = tempo_atual
            velocidade_obstaculo += 0.1

        for obstaculo in list(obstaculos):
            obstaculo.mover()
            obstaculo.desenhar()
            if player.rect.colliderect(obstaculo.rect) and not imune:
                estado_jogo = GAME_OVER
                pygame.mixer.music.stop()
                if not som_morte_tocado:
                    som_morte.play()
                    som_morte_tocado = True
            if obstaculo.rect.right < 0:
                obstaculos.remove(obstaculo)

        # Bônus
        if random.randint(1, 400) == 1:
            bonus.add(Bonus(tela, largura_tela, altura_tela))

        for b in list(bonus):
            b.mover()
            b.desenhar()
            if player.rect.colliderect(b.rect):
                if b.tipo == "images/ferramenta_bonus.png":
                    imune = True
                    tempo_imunidade = pygame.time.get_ticks()
                elif b.tipo == "images/bebe_bonus.png":
                    pontuacao -= 10
                    mensagem_famoso = True
                    tempo_mensagem = pygame.time.get_ticks()
                elif b.tipo == "images/ppr_bonus.png":
                    pontuacao += 50
                bonus.remove(b)

        if imune and pygame.time.get_ticks() - tempo_imunidade > 5000:
            imune = False

        if mensagem_famoso:
            mensagem = fonte.render("Você ficou famoso no Instagram!", True, (255, 0, 0))
            tela.blit(mensagem, (largura_tela//2 - mensagem.get_width()//2, 200))
            if pygame.time.get_ticks() - tempo_mensagem > 2000:
                mensagem_famoso = False

        pontuacao += 1 / 60
        exibir_pontuacao(tela, int(pontuacao))

    # -------------------------
    # GAME OVER
    # -------------------------
    elif estado_jogo == GAME_OVER:
        # Fundo PB
        fundo_cinza = pygame.Surface((largura_tela, altura_tela))
        fundo_cinza.blit(fundo_jogo, (0, 0))
        arr = pygame.surfarray.array3d(fundo_cinza)
        cinza_arr = arr.mean(axis=2, keepdims=True).repeat(3, axis=2)
        pygame.surfarray.blit_array(fundo_cinza, cinza_arr)
        tela.blit(fundo_cinza, (0, 0))

        # Player PB
        player_img = player.image.copy()
        arr_player = pygame.surfarray.array3d(player_img)
        cinza_player = arr_player.mean(axis=2, keepdims=True).repeat(3, axis=2)
        pygame.surfarray.blit_array(player_img, cinza_player)
        tela.blit(player_img, player.rect.topleft)

        fonte_game_over = pygame.font.Font(None, 108)  # 72 é o tamanho da fonte
        game_over_texto = fonte_game_over.render("Morreu!", True, vermelho)
        tela.blit(game_over_texto, (largura_tela//2 - game_over_texto.get_width()//2, 200))

        # Botão Reiniciar
        hover_reiniciar = (largura_tela//2 - 100 < mouse[0] < largura_tela//2 + 100) and (300 < mouse[1] < 350)
        if hover_reiniciar and not getattr(desenhar_botao, "ja_hover_reiniciar", False):
            som_botao.play()
        desenhar_botao.ja_hover_reiniciar = hover_reiniciar
        if desenhar_botao(tela, "Reiniciar", largura_tela//2 - 100, 300, 200, 50, cinza, preto, eventos):
            estado_jogo = TELA_INICIAL
            som_morte.stop()
            som_morte_tocado = False
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume_atual)

    pygame.display.update()
    clock.tick(60)

pygame.quit()