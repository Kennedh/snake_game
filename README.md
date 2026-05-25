# Jogo da Cobrinha

Um clássico jogo da cobrinha (Snake Game) desenvolvido em Python com interface gráfica usando Pygame. O jogo conta com sistema de dificuldades com base na velocidade programada em código através do Pygame.

## Bibliotecas utilizadas

O projeto utiliza três bibliotecas principais:

```python
import pygame   # Interface gráfica, desenho dos elementos e captura de teclas
import random   # Geração de posições aleatórias para a comida
import sys      # Controle do sistema para fechar o jogo corretamente
```
## Como funciona
### Classes principais

#### Cobra

- Armazena as posições de cada segmento do corpo

- Controla a direção atual do movimento

- Verifica colisões com paredes e o próprio corpo

#### Comida

- Gera uma posição aleatória dentro da tela

- Garante que a comida não apareça em cima da cobra

## Mecânicas

- Movimento: A cobra se move continuamente na direção atual

- Crescimento: Ao comer a comida, a cobra aumenta de tamanho e a pontuação sobe

## Colisões:

- Bateu na parede? Game Over!

- Encostou no próprio corpo? Game Over também!

## Dificuldades:

- Fácil (velocidade 6)

- Normal (velocidade 10)

- Difícil (velocidade 18)
