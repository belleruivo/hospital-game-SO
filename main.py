"""
Hospital Manager Game

Este jogo demonstra conceitos fundamentais de Sistemas Operacionais:

THREADS:
- Gerador de pacientes (eventos)
- Processador de cirurgias
- Múltiplas cirurgias simultâneas

SEMÁFOROS:
- Controle de salas cirúrgicas
- Controle de equipe médica
- Controle de enfermeiros
- Prevenção de deadlocks

SINCRONIZAÇÃO:
- Locks para recursos compartilhados
- Regiões críticas
- Padrão produtor-consumidor

Como jogar:
1. Use os números 1-5 para selecionar as opções
2. Mantenha o hospital funcionando
3. Ganhe dinheiro e reputação
4. Gerencie seus recursos com sabedoria
"""

from hospital_game import HospitalGame

if __name__ == "__main__":
    jogo = HospitalGame()
    try:
        jogo.iniciar_jogo()
    except KeyboardInterrupt:
        print("\nJogo encerrado pelo usuário.")
    finally:
        print(f"\nPontuação final: {jogo.score}")