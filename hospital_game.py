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
        O número no construtor representa quantas unidades do recurso estão disponíveis.
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
        
        # Lista de cirurgias em andamento
        self.cirurgias_ativas = []

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def gerar_paciente(self):
        """Gera um novo paciente com características aleatórias"""
        urgencia = random.randint(1, 5)
        tempo_cirurgia = random.randint(20, 60)
        return {
            'id': random.randint(1000, 9999),  # ID único para cada paciente
            'urgencia': urgencia,
            'tempo': tempo_cirurgia,
            'tipo': random.choice(['Cardíaca ❤️ ', 'Neurológica 🧠 ', 'Ortopédica 🦴 '])
        }

    def mostrar_status(self):
        self.limpar_tela()
        print("\n=== 🏥 Hospital Manager 🏥 ===")
        print(f"💰 Dinheiro: ${self.dinheiro}")
        print(f"⭐ Reputação: {self.reputacao}")
        print(f"🏆 Score: {self.score}")
        
        print(f"\n=== 🏨 RECURSOS ===")
        print(f"🚪 Salas disponíveis: {self.salas_cirurgicas._value}")
        print(f"👨‍⚕️ Médicos disponíveis: {self.medicos._value}")
        print(f"👩‍⚕️ Enfermeiros disponíveis: {self.enfermeiros._value}")
        
        print(f"\n=== 🔄 CIRURGIAS ATIVAS: {len(self.cirurgias_ativas)} ===")
        for cirurgia in self.cirurgias_ativas:
            print(f"→ Cirurgia {cirurgia['tipo']} #{cirurgia['id']}")
        
        print(f"\n=== 🚶 FILA DE ESPERA: {len(self.pacientes_espera)} ===")
        for i, paciente in enumerate(self.pacientes_espera, 1):
            print(f"{i}. {paciente['tipo']} (Urgência: {paciente['urgencia']}) #{paciente['id']}")

    def realizar_cirurgia(self, paciente):
        """
        THREAD + SEMÁFOROS:
        Cada cirurgia é uma thread separada que compete pelos recursos do hospital.
        """
        print(f"\n{'='*50}")
        print(f"🏥 NOVA CIRURGIA - {paciente['tipo']} (ID: {paciente['id']})")
        print(f"{'='*50}")
        
        # Verifica recursos
        if (self.salas_cirurgicas._value > 0 and 
            self.medicos._value > 0 and 
            self.enfermeiros._value > 0):
            
            # Prepara a equipe
            self.salas_cirurgicas.acquire()
            self.medicos.acquire()
            self.enfermeiros.acquire()
            
            print("✅ Equipe e sala preparadas")
            self.cirurgias_ativas.append(paciente)
            
            # Realiza a cirurgia
            print(f"⏳ Cirurgia em andamento (duração: 10 segundos)")
            time.sleep(10)
            
            # Resultado
            sucesso = random.random() < (0.5 + (self.reputacao / 200))
            print(f"\n{'='*50}")
            print(f"RESULTADO - Cirurgia {paciente['id']}")
            print(f"{'='*50}")
            
            if sucesso:
                ganho = paciente['tempo'] * (paciente['urgencia'] * 10)
                with self.recursos_lock:
                    self.dinheiro += ganho
                    self.reputacao += 1
                    self.score += ganho
                    self.cirurgias_bem_sucedidas += 1
                print(f"✅ Cirurgia bem sucedida!")
                print(f"💰 Ganho: ${ganho}")
            else:
                with self.recursos_lock:
                    self.reputacao -= 2
                    self.score -= 100
                print(f"❌ Cirurgia com complicações!")
                print("⚠️ Perda de reputação!")
            
            # Finaliza
            self.cirurgias_realizadas += 1
            self.cirurgias_ativas.remove(paciente)
            
            # Libera recursos
            self.salas_cirurgicas.release()
            self.medicos.release()
            self.enfermeiros.release()
            
        else:
            print("\n❌ Recursos insuficientes para iniciar a cirurgia!")
            print("Aguarde outras cirurgias terminarem ou contrate mais recursos!")

        print(f"\n{'='*50}")

    def iniciar_cirurgia(self, paciente):
        """
        THREAD:
        Inicia uma nova thread para a cirurgia, permitindo múltiplas cirurgias simultâneas
        """
        thread = threading.Thread(target=self.realizar_cirurgia, args=(paciente,))
        thread.start()
        return thread

    def mostrar_menu(self):
        print("\n=== 🎮 MENU DE AÇÕES ===")
        print("1 - 🔪 Realizar cirurgia")
        print("2 - 👨‍⚕️ Contratar médico ($500)")
        print("3 - 🏗️ Construir sala cirúrgica ($1000)")
        print("4 - 👩‍⚕️ Contratar enfermeiro ($300)")
        print("5 - 🚶 Gerar novo paciente")
        print("6 - 📊 Ver estatísticas detalhadas")
        print("7 - 🚪 Sair do jogo")

    def comprar_medico(self):
        with self.recursos_lock:
            if self.dinheiro >= 500:
                self.dinheiro -= 500
                self.medicos = Semaphore(self.medicos._value + 1)
                print("\n✅ Médico contratado!")
            else:
                print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def comprar_sala(self):
        with self.recursos_lock:
            if self.dinheiro >= 1000:
                self.dinheiro -= 1000
                self.salas_cirurgicas = Semaphore(self.salas_cirurgicas._value + 1)
                print("\n✅ Sala construída!")
            else:
                print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def comprar_enfermeiro(self):
        with self.recursos_lock:
            if self.dinheiro >= 300:
                self.dinheiro -= 300
                self.enfermeiros = Semaphore(self.enfermeiros._value + 1)
                print("\n✅ Enfermeiro contratado!")
            else:
                print("\n❌ Dinheiro insuficiente!")
        input("\nPressione Enter para continuar...")

    def mostrar_estatisticas(self):
        self.limpar_tela()
        print("\n=== 📊 ESTATÍSTICAS DO HOSPITAL ===")
        print(f"🎯 Total de cirurgias: {self.cirurgias_realizadas}")
        if self.cirurgias_realizadas > 0:
            taxa_sucesso = (self.cirurgias_bem_sucedidas/self.cirurgias_realizadas)*100
            print(f"📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
        print(f"\nCirurgias em andamento: {len(self.cirurgias_ativas)}")
        if self.cirurgias_ativas:
            for cirurgia in self.cirurgias_ativas:
                print(f"→ Cirurgia {cirurgia['tipo']} #{cirurgia['id']}")
        input("\nPressione Enter para voltar...")

    def iniciar_jogo(self):
        print("\n=== 🏥 Bem-vindo ao Hospital Manager! ===")
        print("\nVocê é o novo administrador do hospital.")
        print("Seu objetivo é gerenciar recursos e realizar cirurgias com sucesso.")
        print("\n💡 DICAS IMPORTANTES:")
        print("→ Você pode realizar várias cirurgias ao mesmo tempo!")
        print("→ Basta iniciar uma nova cirurgia enquanto outra está em andamento")
        print("→ Mas lembre-se: cada cirurgia precisa de 1 sala, 1 médico e 1 enfermeiro")
        print("\n🎮 Boa sorte em sua gestão! 🍀")
        input("\nPressione Enter para começar...")

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
                    
                print("\n=== SELECIONE O PACIENTE ===")
                for i, paciente in enumerate(self.pacientes_espera, 1):
                    print(f"{i}. {paciente['tipo']} (Urgência: {paciente['urgencia']}) #{paciente['id']}")
                
                try:
                    escolha = int(input("\nNúmero do paciente: ")) - 1
                    if 0 <= escolha < len(self.pacientes_espera):
                        paciente = self.pacientes_espera.pop(escolha)
                        self.iniciar_cirurgia(paciente)
                        print(f"\n✅ Cirurgia iniciada! Você pode realizar outras ações enquanto ela acontece.")
                    else:
                        print("❌ Escolha inválida!")
                    input("\nPressione Enter para continuar...")
                except ValueError:
                    print("❌ Por favor, digite um número válido!")
                    input("\nPressione Enter para continuar...")
                    
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
                print("❌ Opção inválida!")
                input("Pressione Enter para continuar...")