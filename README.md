# 💊 Hospital Manager - Manual do Jogo
Este é um jogo realizado em Python para a matéria de Sistemas Operacioanais (SO), focando em implementar os conceitos de Threads e Semáforos.

## Como Jogar

1. **Objetivo do Jogo**
   - Gerencie um hospital realizando cirurgias
   - Ganhe dinheiro e mantenha uma boa reputação
   - Gerencie recursos (médicos, salas, enfermeiros) de forma eficiente

2. **Comandos**
   - 1: Realizar cirurgia
   - 2: Contratar médico ($500)
   - 3: Construir sala cirúrgica ($1000)
   - 4: Contratar enfermeiro ($300)
   - 5: Gerar novo paciente
   - 6: Ver estatísticas
   - 7: Sair do jogo

3. **Dicas**
   - Mantenha recursos suficientes para realizar cirurgias
   - Priorize pacientes com maior urgência
   - Equilibre gastos com contratações e ganhos das cirurgias

## Implementação dos Conceitos de SO

### 1. Threads (Processos Paralelos)

No jogo, as threads são utilizadas para simular operações simultâneas no hospital:

1. **Cirurgias Simultâneas**
   ```python
   threading.Thread(target=self.realizar_cirurgia, args=(paciente,)).start()
   ```
   - Cada cirurgia roda em sua própria thread
   - Permite realizar múltiplas cirurgias ao mesmo tempo
   - Simula o paralelismo real de um hospital

2. **Por que usar Threads?**
   - Permite operações simultâneas
   - Simula um ambiente real de hospital
   - Demonstra concorrência por recursos

### 2. Semáforos (Controle de Recursos)

Os semáforos são utilizados para controlar recursos limitados do hospital:

1. **Recursos Controlados**
   ```python
   self.salas_cirurgicas = Semaphore(2)  # 2 salas
   self.medicos = Semaphore(3)           # 3 médicos
   self.enfermeiros = Semaphore(4)       # 4 enfermeiros
   ```

2. **Como funcionam**
   - `acquire()`: Reserva um recurso
   - `release()`: Libera um recurso
   - Se não há recursos disponíveis, a thread espera

3. **Por que usar Semáforos?**
   - Evita sobreutilização de recursos
   - Garante que cada recurso só é usado por uma cirurgia por vez
   - Simula limitações reais de um hospital

### 3. Sincronização

1. **Locks para Recursos Compartilhados**
   ```python
   self.recursos_lock = threading.Lock()
   ```
   - Protege variáveis compartilhadas (dinheiro, reputação)
   - Evita condições de corrida
   - Garante consistência dos dados

## Pontos de Implementação no Código

### Threads
- Cada cirurgia é uma thread independente
- Permite paralelismo real
- Demonstra concorrência por recursos

### Semáforos
- Controlam acesso a recursos limitados
- Implementam exclusão mútua
- Previnem deadlocks

### Exemplo de Fluxo
1. Usuário inicia cirurgia
2. Thread é criada
3. Recursos são reservados via semáforos
4. Cirurgia é realizada
5. Recursos são liberados

## Conceitos de SO Demonstrados

1. **Concorrência**
   - Múltiplas cirurgias simultâneas
   - Competição por recursos

2. **Sincronização**
   - Uso de semáforos
   - Proteção de recursos compartilhados

3. **Gerenciamento de Recursos**
   - Alocação controlada
   - Prevenção de deadlocks

4. **Exclusão Mútua**
   - Recursos não podem ser usados simultaneamente
   - Garante consistência das operações

## Requisitos Técnicos
- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária

## Como Executar