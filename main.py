from src.game_manager import GameManager

def inicializar_jogo():
    
    jogo = GameManager()
    jogo.run_loop()

if __name__ == "__main__":
    inicializar_jogo()

