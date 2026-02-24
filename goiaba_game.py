import pygame
import random

pygame.init()

# Configuração da janela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Goiabinha")

# Cores e FPS
branco = (255, 255, 255)
preto = (0, 0, 0)
clock = pygame.time.Clock()

# Carregamento da folha de sprites do player
sprite_sheet = pygame.image.load("images/sprite_sheet-.png")  # Certifique-se de ter essa imagem

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        
        largura_frame_original = 800
        altura_frame_original = 500
        largura_frame_escalonado = 70
        altura_frame_escalonado = 70

        self.frames = []
        total_frames_horizontais = self.sprite_sheet.get_width() // largura_frame_original
        total_frames_verticais = self.sprite_sheet.get_height() // altura_frame_original

        for linha in range(total_frames_verticais):
            for coluna in range(total_frames_horizontais):
                x = coluna * largura_frame_original
                y = linha * altura_frame_original
                frame = self.sprite_sheet.subsurface((x, y, largura_frame_original, altura_frame_original))
                frame_escalonado = pygame.transform.scale(frame, (largura_frame_escalonado, altura_frame_escalonado))
                self.frames.append(frame_escalonado)

        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, altura_tela - altura_frame_escalonado - 30)
        self.velocidade_y = 0
        self.no_chao = True
        self.contador_frame = 0
        self.atraso_frame = 5

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -16
            self.no_chao = False

    def atualizar(self):
        self.rect.y += self.velocidade_y
        self.velocidade_y += 1

        if self.rect.y >= altura_tela - 70 - 30:
            self.rect.y = altura_tela - 70 - 30
            self.no_chao = True

        self.contador_frame += 1
        if self.contador_frame >= self.atraso_frame:
            self.contador_frame = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

    def desenhar(self):
        tela.blit(self.image, self.rect.topleft)

# Classe do bônus
class Bonus(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.x = largura_tela
        self.y = random.randint(altura_tela - 200, altura_tela - 150)
        if tipo == 1:
            self.imagem = pygame.image.load("images/ferramenta_bonus.png")
        elif tipo == 2:
            self.imagem = pygame.image.load("images/bebe_bonus.png")
        else:
            self.imagem = pygame.image.load("images/ppr_bonus.png")
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))
        self.rect = self.imagem.get_rect(topleft=(self.x, self.y))

    def mover(self):
        self.rect.x -= 6

    def desenhar(self):
        tela.blit(self.imagem, self.rect.topleft)

# Função para exibir a pontuação
def exibir_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f"Score: {pontuacao}", True, preto)
    tela.blit(texto, (10, 10))

# Inicialização dos objetos
player = Player()
bonus = pygame.sprite.Group()
pontuacao = 0

rodando = True
while rodando:
    tela.fill(branco)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                player.pular()

    player.atualizar()
    player.desenhar()

    if random.randint(1, 200) == 1:
        bonus.add(Bonus(random.choice([1, 2, 3])))

    for b in bonus:
        b.mover()
        b.desenhar()
        if player.rect.colliderect(b.rect):
            pontuacao += 1  # Incrementa a pontuação ao coletar um bônus
            bonus.remove(b)

    exibir_pontuacao(pontuacao)
    pygame.display.update()
    clock.tick(60)

pygame.quit()