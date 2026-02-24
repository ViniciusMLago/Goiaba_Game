import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela, tipo, velocidade=6):
        super().__init__()
        self.tela = tela
        self.tipo = tipo
        self.velocidade = velocidade

        # Posição inicial do obstáculo (fora da tela à direita)
        self.rect = pygame.Rect(largura_tela, altura_tela - 70, 40, 40)

        # Carregamento da imagem de acordo com o tipo
        self.imagem = self.carregar_imagem(tipo)
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))

        # Ajuste da posição de alinhamento ao chão
        self.rect.bottomleft = (largura_tela, altura_tela - 30)

    def carregar_imagem(self, tipo):
        """Seleciona a imagem do obstáculo com base no tipo."""
        caminhos = {
            1: "images/Vazamento1.png",
            2: "images/Vazamento2.png",
            3: "images/Bebedouro.png",
            4: "images/Ar_Condicionado.png"
        }
        caminho = caminhos.get(tipo)
        try:
            return pygame.image.load(caminho)
        except:
            # Imagem padrão vermelha se o caminho não for válido
            imagem_fallback = pygame.Surface((40, 40))
            imagem_fallback.fill((255, 0, 0))
            return imagem_fallback

    def mover(self):
        """Move o obstáculo para a esquerda com a velocidade definida."""
        self.rect.x -= self.velocidade

    def desenhar(self):
        """Desenha o obstáculo na tela."""
        self.tela.blit(self.imagem, self.rect.topleft)
