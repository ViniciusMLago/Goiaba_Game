import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela):
        super().__init__()
        self.tela = tela
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Carregando sprite sheet e ajustando quadros de animação
        self.sprite_sheet = pygame.image.load("images/sprite_sheet-.png")
        self.frames = self.carregar_frames(largura_frame=70, altura_frame=70)
        
        # Inicialização do personagem
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, self.altura_tela - 70 - 30)

        self.velocidade_y = 0
        self.velocidade_x = 0
        self.pulos_restantes = 2
        self.contador_frame = 0
        self.atraso_frame = 8
        self.no_chao = True
        self.imune = False
        self.tempo_imunidade = 0

    def carregar_frames(self, largura_frame, altura_frame):
        """Corta a sprite sheet em quadros escalonados."""
        total_colunas = 2
        largura_original = self.sprite_sheet.get_width() // total_colunas
        altura_original = self.sprite_sheet.get_height()

        frames = []
        for i in range(total_colunas):
            x = i * largura_original
            frame = self.sprite_sheet.subsurface((x, 0, largura_original, altura_original))
            frame_escalonado = pygame.transform.scale(frame, (largura_frame, altura_frame))
            frames.append(frame_escalonado)
        return frames

    def pular(self):
        if self.pulos_restantes > 0:
            self.velocidade_y = -16
            self.pulos_restantes -= 1

    def movimento(self):
        self.velocidade_x = 15

    def atualizar(self):
        # Atualiza posição vertical (gravidade)
        self.rect.y += self.velocidade_y
        self.velocidade_y += 1

        # Verifica se tocou o chão
        if self.rect.y >= self.altura_tela - 70 - 30:
            self.rect.y = self.altura_tela - 70 - 30
            self.no_chao = True
            self.pulos_restantes = 2
        else:
            self.no_chao = False

        # Atualiza animação do sprite
        self.contador_frame += 1
        if self.contador_frame >= self.atraso_frame:
            self.contador_frame = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

        # Controla duração da imunidade
        if self.imune and pygame.time.get_ticks() - self.tempo_imunidade > 5000:
            self.imune = False

    def ativar_imunidade(self):
        self.imune = True
        self.tempo_imunidade = pygame.time.get_ticks()

    def desenhar(self):
        self.tela.blit(self.image, self.rect.topleft)
