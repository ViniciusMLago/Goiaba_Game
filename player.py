import pygame

ALTURA_PLAYER = 70
MARGEM_CHAO = 30
GRAVIDADE = 0.8
FORCA_PULO = -16
PULOS_MAXIMOS = 2


class Player(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela):
        super().__init__()
        self.tela = tela
        self.altura_tela = altura_tela

        self.sprite_sheet = pygame.image.load("images/sprite_sheet-.png").convert_alpha()
        self.frames = self.carregar_frames(ALTURA_PLAYER, ALTURA_PLAYER)

        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, self.altura_tela - ALTURA_PLAYER - MARGEM_CHAO)

        self.velocidade_y = 0
        self.pulos_restantes = PULOS_MAXIMOS
        self.contador_frame = 0
        self.atraso_frame = 8
        self.no_chao = True

    def carregar_frames(self, largura_frame, altura_frame):
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
            self.velocidade_y = FORCA_PULO
            self.pulos_restantes -= 1
            self.no_chao = False

    def atualizar(self):
        self.rect.y += self.velocidade_y
        self.velocidade_y += GRAVIDADE

        chao_y = self.altura_tela - ALTURA_PLAYER - MARGEM_CHAO
        if self.rect.y >= chao_y:
            self.rect.y = chao_y
            self.no_chao = True
            self.pulos_restantes = PULOS_MAXIMOS
        else:
            self.no_chao = False

        self.contador_frame += 1
        if self.contador_frame >= self.atraso_frame:
            self.contador_frame = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)
            self.image = self.frames[self.frame_atual]

    def desenhar(self):
        self.tela.blit(self.image, self.rect.topleft)
