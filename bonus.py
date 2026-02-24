import pygame
import random

class Bonus(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela):
        super().__init__()
        self.tela = tela
        self.x = largura_tela
        self.y = random.randint(altura_tela - 300, altura_tela - 150)

        self.tipo = random.choices(
            ["images/ferramenta_bonus.png", "images/bebe_bonus.png", "images/ppr_bonus.png"],
            weights=[5, 3, 1],  # Menos chances do PPR
            k=1
        )[0]

        self.imagem = pygame.image.load(self.tipo)
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))
        self.rect = self.imagem.get_rect(topleft=(self.x, self.y))

    def mover(self):
        self.rect.x -= 6

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect.topleft)
