# boss.py (corrigido)
import pygame
import random

class Boss:
    def __init__(self, largura_tela, altura_tela):
        """
        Boss inicializado fora da tela (à direita). Será redimensionado para 500x500.
        """

        # >>> Dimensões fixas do boss (requisito)
        self.width = 500
        self.height = 500

        altura_chao = 80  # mesma margem usada para o player

        # Posição inicial (fora da tela, à direita)
        self.x = largura_tela
        # Coloca o boss um pouco abaixo do topo (ou alinhado ao "chão")
        self.y = altura_tela - self.height - altura_chao

        self.velocidade = 4  # velocidade de entrada/saída (ajustável)

        # Estados
        self.ENTRANDO = 0
        self.FALANDO  = 1
        self.SAINDO   = 2
        self.ATACANDO = 3

        self.estado = self.ENTRANDO

        # Falas e controle de diálogo
        self.falas = [
            "Então você chegou longe...",
            "Mas agora enfrentará meu poder!",
            "Prepare-se!"
        ]
        self.indice_fala = 0
        self.tempo_fala = 0
        self.delay_entre_falas = 2500  # ms

        # Tempo de início do ataque (setado quando começa a atacar)
        self.tempo_inicio_ataque = 0

        # >>> Carrega a imagem e força tamanho 500x500
        self.imagem = pygame.image.load("images/Boss Goiaba - JS.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (self.width, self.height))

        # Rect baseado na imagem
        self.rect = self.imagem.get_rect(topleft=(self.x, self.y))

        # Posição alvo (quando aparecer totalmente na tela)
        # Por exemplo, para ficar totalmente visível no canto direito:
        self.target_x = max(0, largura_tela - self.width - 50)

    def atualizar(self, largura_tela, altura_tela):
        """
        Atualiza posição do boss de acordo com o estado.
        ENTRANDO: move para a esquerda até target_x -> FALANDO
        SAINDO: move para a direita até sair totalmente da tela -> ATACANDO
        ATACANDO: permanece (tempo de ataque controlado externamente)
        """

        # ENTRANDO: desliza da direita para a posição alvo
        if self.estado == self.ENTRANDO:
            self.x -= self.velocidade
            if self.x <= self.target_x:
                self.x = self.target_x
                self.estado = self.FALANDO
                self.tempo_fala = pygame.time.get_ticks()

        # SAINDO: desliza para a direita até sair (x > largura_tela)
        elif self.estado == self.SAINDO:
            self.x += self.velocidade
            if self.x > largura_tela:
                # Quando sair fora da tela, inicia o modo de ataque
                self.estado = self.ATACANDO
                self.tempo_inicio_ataque = pygame.time.get_ticks()

        # Se estiver em FALANDO ou ATACANDO, a atualização da lógica além do movimento
        # (avançar falas / iniciar ataque) é feita por mostrar_falas() ou por main.

        # Atualiza rect para colisões/desenho
        self.rect.topleft = (int(self.x), int(self.y))

    def desenhar(self, tela):
        """
        Desenha o boss na tela (baseado no self.x, self.y)
        """
        tela.blit(self.imagem, (int(self.x), int(self.y)))

    def mostrar_falas(self, tela, fonte, pos=(50, 30), cor=(255,50,50)):
        """
        Desenha a fala atual na tela e avança as falas de acordo com o tempo.
        Quando terminar as falas, altera o estado para SAINDO.
        Retorna True se as falas terminaram (ou já estiver em SAINDO/ATACANDO).
        """
        agora = pygame.time.get_ticks()

        # Se não está em fala, nada a fazer
        if self.estado != self.FALANDO:
            return False

        # Renderiza a fala atual
        texto = fonte.render(self.falas[self.indice_fala], True, cor)
        tela.blit(texto, pos)

        # Avança a fala quando passar o tempo
        if agora - self.tempo_fala > self.delay_entre_falas:
            self.indice_fala += 1
            self.tempo_fala = agora

            # Se acabou as falas, inicia saída
            if self.indice_fala >= len(self.falas):
                self.estado = self.SAINDO
                return True

        return False

    def iniciar_ataque(self):
        """
        Marca o tempo de início do ataque (chamar quando cortar para BOSS_ATAQUE se desejar).
        """
        self.tempo_inicio_ataque = pygame.time.get_ticks()