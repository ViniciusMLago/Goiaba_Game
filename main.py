import pygame
import random
import os
from player import Player
from bonus import Bonus
from utils import adicionar_tempo_escudo, desenhar_barra_escudo, escudo_ativo, exibir_pontuacao, desenhar_botao, alterar_som
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
volume_atual = float(0.5)
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
ppr = False
chamado = False
tempo_escudo = 0
tempo_fim_escudo = 0
duracao_escudo = 5000
mensagem_famoso = False
tempo_mensagem = 0
som_morte_tocado = False

tempo_fim_escudo = 0
duracao_bonus = 5000  # 5 segundos por ferramenta

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
        volume_atual, estado_jogo = alterar_som(tela, fundo_inicial, fonte, largura_tela, mouse, som_botao, cinza, preto, eventos, estado_jogo, TELA_INICIAL, volume_atual)

    # -------------------------
    # JOGO
    # -------------------------
    elif estado_jogo == JOGANDO:
        rel_x = x_fundo % fundo_jogo.get_width()
        tela.blit(fundo_jogo, (rel_x - fundo_jogo.get_width(), 0))
        if rel_x < largura_tela:
            tela.blit(fundo_jogo, (rel_x, 0))
        x_fundo -= velocidade_fundo
        velocidade_fundo += 0.001
        print(f"Velocidade do fundo: {velocidade_fundo:.2f}")

        overlay = pygame.Surface((largura_tela, altura_tela))
        overlay.fill((50, 50, 50))
        overlay.set_alpha(60)
        tela.blit(overlay, (0, 0))

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

        desenhar_barra_escudo(
            tela,
            tempo_fim_escudo,
            duracao_bonus,
            fonte
        )

        if imune:
            shield_rect = escudo_img.get_rect(center=player.rect.center)
            tela.blit(escudo_img, shield_rect)

        # Obstáculos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo_obstaculo > intervalo_minimo and random.randint(1, 100) == 1:
            tipo_obstaculo = random.randint(1, 4)
            obstaculos.add(Obstacle(tela, largura_tela, altura_tela, tipo_obstaculo, velocidade_obstaculo))
            ultimo_tempo_obstaculo = tempo_atual
            velocidade_obstaculo += 0.05  # Aumenta a velocidade dos obstáculos a cada geração

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
                    chamado = True
                    tempo_fim_escudo = adicionar_tempo_escudo(tempo_fim_escudo,duracao_bonus)    
                    
                elif b.tipo == "images/bebe_bonus.png":
                    pontuacao += 10
                    mensagem_famoso = True
                    tempo_mensagem = pygame.time.get_ticks()
                elif b.tipo == "images/ppr_bonus.png":
                    pontuacao += 50
                    ppr = True
                bonus.remove(b)  

        if not escudo_ativo(tempo_fim_escudo):        
                imune = False

        if mensagem_famoso:
            mensagem = fonte.render("Você ficou famoso no Instagram!", True, (255, 255, 255))
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
        fundo_cinza = fundo_jogo.copy()
        overlay = pygame.Surface((largura_tela, altura_tela))
        overlay.fill((100, 100, 100))  # tom de cinza
        overlay.set_alpha(150)  # intensidade do efeito

        fundo_cinza.blit(overlay, (0, 0))
        tela.blit(fundo_cinza, (0, 0))

        # Player PB
        player_img = player.image.copy()

        # Criar superfície cinza
        cinza_overlay = pygame.Surface(player_img.get_size())
        cinza_overlay.fill((180, 180, 180))  # intensidade do cinza

        # Aplicar efeito multiplicação
        player_img.blit(cinza_overlay, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        player_img.set_alpha(180)  # intensidade do efeito
        tela.blit(player_img, player.rect.topleft)

        fonte_game_over = pygame.font.Font(None, 108)  # 72 é o tamanho da fonte
        game_over_texto = fonte_game_over.render("Goiabinha faleceu!", True, vermelho)
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