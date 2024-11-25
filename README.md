<<<<<<< HEAD
# 🏥 Hospital Manager - Manual do Jogo
Este é um jogo realizado em Python para a matéria de Sistemas Operacioanais (SO), focando em implementar os conceitos de Threads e Semáforos.
=======
# 💊 Hospital Manager - Manual do Jogo
Este é um jogo realizado em Python para a matéria de Sistemas Operacionais (SO), focando em implementar os conceitos de Threads e Semáforos.
>>>>>>> d0da7bc34f076e5747757e0364e2d5995084f320

## Sumário
1. [Como Jogar](#como-jogar)
2. [Implementação Técnica](#implementação-técnica)
3. [Conceitos de SO Demonstrados](#conceitos-de-so-demonstrados)
4. [Requisitos e Execução](#requisitos-e-execução)

## Como Jogar

### Objetivo do Jogo
- Gerencie um hospital realizando cirurgias
- Ganhe dinheiro e mantenha uma boa reputação
- Gerencie recursos (médicos, salas, enfermeiros) de forma eficiente
- Realize múltiplas cirurgias simultaneamente para maximizar os ganhos

### Comandos
1. Realizar cirurgia
2. Contratar médico ($500)
3. Construir sala cirúrgica ($1000)
4. Contratar enfermeiro ($300)
5. Gerar novo paciente
6. Ver estatísticas detalhadas
7. Sair do jogo

### Cirurgias Simultâneas
Para realizar cirurgias ao mesmo tempo:
- Certifique-se de ter recursos suficientes
  * Cada cirurgia requer: 1 sala, 1 médico e 1 enfermeiro
- Inicie uma cirurgia (opção 1)
- Sem esperar ela terminar, inicie outra cirurgia (opção 1 novamente)
- Você pode continuar gerenciando o hospital enquanto as cirurgias acontecem

### Dicas
- Mantenha recursos suficientes para realizar múltiplas cirurgias
- Contrate mais recursos quando necessário
- Priorize pacientes com maior urgência
- Equilibre gastos com contratações e ganhos das cirurgias
- Monitore os recursos disponíveis antes de iniciar novas cirurgias

## Implementação Técnica

### Threads no Projeto
- **Onde:** Cada cirurgia roda em uma thread separada
- **Como:** Usando `threading.Thread(target=self.realizar_cirurgia, args=(paciente,))`
- **Por que:** Permite que múltiplas cirurgias aconteçam simultaneamente, simulando um hospital real
- **Implementação:**
  ```python
  def iniciar_cirurgia(self, paciente):
      thread = threading.Thread(target=self.realizar_cirurgia, args=(paciente,))
      thread.start()
      return thread
  ```

### Semáforos no Projeto
- **Onde:** Controle de recursos limitados (salas, médicos, enfermeiros)
- **Como:** Usando `threading.Semaphore(quantidade)`
- **Por que:** Garante que não ultrapassamos o limite de recursos disponíveis
- **Implementação:**
  ```python
  self.salas_cirurgicas = Semaphore(2)  # 2 salas
  self.medicos = Semaphore(3)           # 3 médicos
  self.enfermeiros = Semaphore(4)       # 4 enfermeiros
  ```

### Exemplo de Fluxo
1. Usuário inicia cirurgia
2. Nova thread é criada
3. Thread tenta adquirir recursos via semáforos
4. Se conseguir recursos, realiza a cirurgia
5. Ao terminar, libera os recursos
6. Outras threads podem usar os recursos liberados

### Prevenção de Deadlocks
- Recursos são sempre adquiridos na mesma ordem
- Lock protege recursos compartilhados
- Verificação prévia de recursos disponíveis

## Conceitos de SO Demonstrados

### 1. Concorrência
- Múltiplas cirurgias simultâneas
- Competição por recursos limitados
- Threads independentes

### 2. Sincronização
- Uso de semáforos para controle de recursos
- Lock para proteção de variáveis compartilhadas
- Coordenação entre threads

### 3. Gerenciamento de Recursos
- Alocação controlada via semáforos
- Prevenção de deadlocks
- Liberação adequada de recursos

### 4. Exclusão Mútua
- Recursos não podem ser usados simultaneamente
- Proteção de regiões críticas
- Garantia de consistência

## Requisitos e Execução

### Requisitos Técnicos
- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária

### Como Executar
   ```python
   python main.py
   ```
<<<<<<< HEAD

### Estrutura do Projeto
- `main.py`: Arquivo principal do jogo
- `hospital_game.py`: Implementação da lógica do jogo
- `README.md`: Documentação e manual

### Observações Importantes
1. O jogo utiliza threads reais do sistema operacional
2. Os semáforos garantem o uso seguro dos recursos
3. A interface é atualizada em tempo real
4. O sistema previne deadlocks e race conditions

## Contribuição

Este projeto foi desenvolvido para demonstrar conceitos de Sistemas Operacionais, especificamente:
- Threads e processamento paralelo
- Semáforos e controle de recursos
- Sincronização e exclusão mútua
=======
>>>>>>> d0da7bc34f076e5747757e0364e2d5995084f320
