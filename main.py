from hospital_game import HospitalGame

if __name__ == "__main__":
    jogo = HospitalGame()
    try:
        jogo.iniciar_jogo()
    except KeyboardInterrupt:
        print("\nJogo encerrado pelo usuário.")
    finally:
        print(f"\nPontuação final: {jogo.score}")