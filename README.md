# Guardiões: O CInverno das Sombras

Projeto desenvolvido para a disciplina de Introdução à Programação do período de 2025-2.
Um jogo Roguelike top-down shooter desenvolvido em Python com PyGame.

## 🎮 Como Jogar
- **WASD / Setas**: Movimentação do Jack Frost.
- **Mouse / Espaço**: Disparar raios de gelo.
- **Objetivo**: Sobreviva aos pesadelos, salve as crianças nas gaiolas para coletar os Dentes e derrote o Breu.

## 🛠️ Instalação
1. Clone o repositório:

   ```bash
   git clone https://github.com/usuario/nome-do-jogo.git
   ```

2. Instale as dependências:

   ```py
   pip install -r requirements.txt
   ```
3. Execute o jogo:

   ```py
   python main.py
   ```

## 👥 Equipe

- **Arthur Luz**
- **Eduardo Neves**
- **Elias Cirilo**
- **Gabriel Belo**
- **Jéssica Torres**
- **Luiz Henrique**

## 📂 Estrutura

```
│
├── .gitignore          # Ignora lixo (venv, __pycache__, .DS_Store)
├── README.md           # Documentação (Como rodar, créditos)
├── requirements.txt    # Dependências (pygame)
├── main.py             # Ponto de entrada (Inicializa o Pygame e chama GameManager)
│
├── assets/             # MÍDIA (Designers D1 e D2 enchem isso aqui)
│   ├── images/
│   │   ├── characters/ # Sprites do Jack, Inimigos e Boss
│   │   ├── items/      # Sprites de Coração, Cristal, Dente, Gaiola, Projéteis
│   │   ├── ui/         # Botões, Logo, Ícones de HUD
│   │   └── background/ # O mapa único (chão de gelo/neve)
│   ├── sounds/         # SFX (tiro.wav, dano.wav) e Música de fundo
│   └── fonts/          # Fontes .ttf
│
└── src/                # LÓGICA (Programadores e Designers-Dev)
    ├── __init__.py     # Arquivo vazio (necessário para importar pastas)
    ├── config.py       # (Antigo settings.py) As "Leis": Tamanho tela, Cores, FPS
    │
    ├── game_manager.py # Loop principal, Spawner, Timer, Controle de Estados
    ├── menu.py         # Telas: Menu Inicial, Pause e Game Over
    ├── ui.py           # HUD: Desenha vida, pontuação e tempo DURANTE o jogo
    │
    ├── player.py       # Classe do Jack (Movimento, Inputs)
    ├── projectile.py   # Classe do Tiro de Gelo (pode ser separado ou dentro de player.py)
    │
    ├── enemies/        # PASTA DOS INIMIGOS (IA)
    │   ├── __init__.py
    │   ├── base.py     # Classe Pai (Vida, Movimento de perseguir)
    │   ├── common.py   # Classes Filhas (Espírito, Cavalo)
    │   └── boss.py     # Classe Filha Especial (O Breu)
    │
    └── collectibles.py # (Antigo items.py) Classes: Gaiola, Dente, Coração, Cristal
```

## ✅ Divisão de Tarefas

| Responsável | Tarefa |
| :--- | :--- |
| Arthur Luz | Interações & Coletáveis | 
| Eduardo Neves | Jogador & Combate |
| Elias Cirilo | Animação & Código UI | 
| Gabriel Belo | Câmera & Estados |
| Jéssica Torres | Cenário/Boss & Menu Code |
| Luiz Falcão | Inimigos & Boss |

## 📈 Desafios & Lições

Nada ainda!

## 🕹️ Capturas de Tela

Nada ainda!
