import pygame

CAMINHOS_OBSTACULOS = {
    1: "images/Vazamento1.png",
    2: "images/Vazamento2.png",
    3: "images/Bebedouro.png",
    4: "images/Ar_Condicionado.png",
}


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela, tipo, velocidade=6):
        super().__init__()
        self.tela = tela
        self.velocidade = velocidade

        self.imagem = self.carregar_imagem(tipo)
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))
        self.rect = self.imagem.get_rect(bottomleft=(largura_tela, altura_tela - 30))

    def carregar_imagem(self, tipo):
        caminho = CAMINHOS_OBSTACULOS.get(tipo)
        if caminho:
            try:
                return pygame.image.load(caminho).convert_alpha()
            except (pygame.error, FileNotFoundError):
                pass

        imagem_fallback = pygame.Surface((40, 40))
        imagem_fallback.fill((255, 0, 0))
        return imagem_fallback

    def mover(self):
        self.rect.x -= self.velocidade

    def fora_da_tela(self) -> bool:
        return self.rect.right < 0

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect.topleft)
