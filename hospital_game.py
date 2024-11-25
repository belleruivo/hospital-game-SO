import threading
import time
import random
from threading import Semaphore
import os
from queue import PriorityQueue

class HospitalGame:
    def __init__(self):
        """
        SEMÁFOROS:
        Cada semáforo representa um recurso limitado do hospital.
        """
        # Inicialização dos semáforos para controle de recursos
        self.salas_cirurgicas = Semaphore(2)  # Máximo 2 cirurgias simultâneas
        self.medicos = Semaphore(3)           # Começa com 3 médicos
        self.enfermeiros = Semaphore(4)       # Começa com 4 enfermeiros
        
        # Lock para proteger recursos compartilhados
        self.recursos_lock = threading.Lock()
        
        # Estado inicial do jogo
        self.dinheiro = 1000
        self.reputacao = 50
        self.score = 0
        self.game_over = False
        self.pacientes_espera = []  # Lista de pacientes aguardando
        
        # Contadores para estatísticas
        self.cirurgias_realizadas = 0
        self.cirurgias_bem_sucedidas = 0

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def gerar_paciente(self):
        """Gera um novo paciente com características aleatórias"""
        urgencia = random.randint(1, 5)
        tempo_cirurgia = random.randint(20, 60)
        return {
            'urgencia': urgencia,
            'tempo': tempo_cirurgia,
            'tipo': random.choice(['Cardíaca', 'Neurológica', 'Ortopédica'])
        }

    def mostrar_status(self):
        self.limpar_tela()
        print("\n=== 🏥 Hospital Manager 🏥 ===")
        print(f"💰 Dinheiro: ${self.dinheiro}")
        print(f"⭐ Reputação: {self.reputacao}")
        print(f"🏆 Score: {self.score}")
        print(f"\nRecursos disponíveis:")
        print(f"🚪 Salas cirúrgicas: {self.salas_cirurgicas._value}")
        print(f"👨‍⚕️ Médicos: {self.medicos._value}")
        print(f"👩‍⚕️ Enfermeiros: {self.enfermeiros._value}")
        
        print("\n=== Pacientes aguardando ===")
        if not self.pacientes_espera:
            print("Nenhum paciente aguardando!")
        else:
            for i, paciente in enumerate(self.pacientes_espera, 1):
                print(f"{i}. Cirurgia {paciente['tipo']} - Urgência: {paciente['urgencia']}")

    def realizar_cirurgia(self, paciente):
        """Realiza uma cirurgia com o paciente selecionado"""
        print(f"\n🏥 Iniciando cirurgia {paciente['tipo']} (Urgência: {paciente['urgencia']})")
        input("Pressione Enter para começar a cirurgia...")
        
        print("\nAdquirindo recursos necessários...")
        self.salas_cirurgicas.acquire()
        print("✅ Sala cirúrgica preparada")
        self.medicos.acquire()
        print("✅ Médico designado")
        self.enfermeiros.acquire()
        print("✅ Enfermeiro designado")
        
        print("\nRealizando cirurgia...")
        time.sleep(2)  # Simula o tempo da cirurgia
        
        sucesso = random.random() < (0.5 + (self.reputacao / 200))
        
        if sucesso:
            ganho = paciente['tempo'] * (paciente['urgencia'] * 10)
            self.dinheiro += ganho
            self.reputacao += 1
            self.score += ganho
            self.cirurgias_bem_sucedidas += 1
            print(f"\n✅ Cirurgia bem sucedida!")
            print(f"💰 Ganho: ${ganho}")
        else:
            self.reputacao -= 2
            self.score -= 100
            print(f"\n❌ Cirurgia com complicações!")
            print("⚠️ Perda de reputação!")
        
        self.cirurgias_realizadas += 1
        
        # Libera recursos
        self.salas_cirurgicas.release()
        self.medicos.release()
        self.enfermeiros.release()
        
        input("\nPressione Enter para continuar...")

    def mostrar_menu(self):
        print("\nComandos:")
        print("1 - Realizar cirurgia")
        print("2 - Contratar médico ($500)")
        print("3 - Construir sala cirúrgica ($1000)")
        print("4 - Contratar enfermeiro ($300)")
        print("5 - Gerar novo paciente")
        print("6 - Ver estatísticas detalhadas")
        print("7 - Sair do jogo")

    def comprar_medico(self):
        if self.dinheiro >= 500:
            self.dinheiro -= 500
            self.medicos = Semaphore(self.medicos._value + 1)
            print("\n✅ Médico contratado!")
        else:
            print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def comprar_sala(self):
        if self.dinheiro >= 1000:
            self.dinheiro -= 1000
            self.salas_cirurgicas = Semaphore(self.salas_cirurgicas._value + 1)
            print("\n✅ Sala construída!")
        else:
            print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def comprar_enfermeiro(self):
        if self.dinheiro >= 300:
            self.dinheiro -= 300
            self.enfermeiros = Semaphore(self.enfermeiros._value + 1)
            print("\n✅ Enfermeiro contratado!")
        else:
            print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def mostrar_estatisticas(self):
        self.limpar_tela()
        print("\n=== 📊 Estatísticas do Hospital ===")
        print(f"Cirurgias realizadas: {self.cirurgias_realizadas}")
        if self.cirurgias_realizadas > 0:
            taxa_sucesso = (self.cirurgias_bem_sucedidas/self.cirurgias_realizadas)*100
            print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
        input("\nPressione Enter para voltar...")

    def iniciar_jogo(self):
        print("Bem-vindo ao Hospital Manager!")
        print("Você é o novo administrador do hospital.")
        print("Gerencie recursos e realize cirurgias com sabedoria!")
        input("Pressione Enter para começar...")

        # Gera alguns pacientes iniciais
        for _ in range(3):
            self.pacientes_espera.append(self.gerar_paciente())

        while not self.game_over:
            self.mostrar_status()
            self.mostrar_menu()
            
            comando = input("\nEscolha uma opção: ")
            
            if comando == '1':
                if not self.pacientes_espera:
                    print("\n❌ Não há pacientes aguardando!")
                    input("Pressione Enter para continuar...")
                    continue
                    
                print("\nEscolha o paciente para cirurgia:")
                for i, paciente in enumerate(self.pacientes_espera, 1):
                    print(f"{i}. Cirurgia {paciente['tipo']} - Urgência: {paciente['urgencia']}")
                
                try:
                    escolha = int(input("Número do paciente: ")) - 1
                    if 0 <= escolha < len(self.pacientes_espera):
                        paciente = self.pacientes_espera.pop(escolha)
                        self.realizar_cirurgia(paciente)
                    else:
                        print("Escolha inválida!")
                        input("Pressione Enter para continuar...")
                except ValueError:
                    print("Por favor, digite um número válido!")
                    input("Pressione Enter para continuar...")
                    
            elif comando == '2':
                self.comprar_medico()
            elif comando == '3':
                self.comprar_sala()
            elif comando == '4':
                self.comprar_enfermeiro()
            elif comando == '5':
                self.pacientes_espera.append(self.gerar_paciente())
                print("\n✅ Novo paciente chegou ao hospital!")
                input("Pressione Enter para continuar...")
            elif comando == '6':
                self.mostrar_estatisticas()
            elif comando == '7':
                self.game_over = True
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")