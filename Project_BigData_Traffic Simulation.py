"""
Objetivo do Código:
Este código simula o tráfego numa interseção de ruas, onde carros se movem em direções aleatórias.
Cada carro é representado por uma thread. O sistema inclui um mecanismo de semáforo que coordena
a passagem dos carros, considerando condições como tráfego intenso e carros avariados. O código
regista o estado dos carros, movimentos na interseção e relatórios detalhados para possíveis
condições de competição. Além disso, são simulados tempos de movimento e espera variáveis para
tornar a simulação mais realista.

"""
import threading
import time
import random
import psutil

def menu():

    print(" ======================")
    print("|  Traffic Simulation  |")
    print("|                      |")
    print("| 1 - Made by          |")
    print("| 2 - Start            |")
    print("| 3 - Exit             |")
    print(" ======================")

menu()
n = int((input("Choice: ")))

while True:

    if n == 1:
        time.sleep(0.2)
        print("This work was done by:")
        print()
        print("João Almeida")
        print("João Venâncio")
        print()
        print(input("Press 'Enter' to go back to Menu."))
        menu()
        n = int((input("Choice: ")))

    elif n == 2:

        class Carro(threading.Thread):
            
            #Classe que representa um carro que se move em direções aleatórias e interage com uma interseção.
            
            def __init__(self, carro_id, direcao, intersecao):
                super(Carro, self).__init__()
                self.carro_id = carro_id                        # Identificação única do carro
                self.direcao = direcao                          # Direção inicial do carro
                self.direcao_apos_intersecao = None             # Direção que o carro seguirá após a interseção
                self.intersecao = intersecao                    # Objeto da classe Intersecao responsável pela coordenação do tráfego
                self.tempo_espera = 0                           # Tempo total que o carro espera na interseção
                self.esta_avariado = random.random() < 0.1      # Indica se o carro está avariado com base em uma probabilidade
                self.tempo_espera_semaforo = 0                  # Tempo total que o carro espera pelo semáforo
                
                
            def run(self):
                
                #Método que inicia o movimento do carro e interage com a interseção.
                
                print(f'Carro {self.carro_id} iniciou sua rota na direção {self.direcao}')   # Carro inicia sua rota
                tempo_movimento = random.randint(1, 5)                                       # Simulação do tempo de movimento
                time.sleep(tempo_movimento)
                print(f'Carro {self.carro_id} chegou à interseção')                          # Carro chegou à interseção
                self.direcao_apos_intersecao = random.choice(['Norte', 'Sul', 'Este', 'Oeste'])
                print(f'Carro {self.carro_id} chegou na interseção e vai verificar o semaforo da direção {self.direcao} para poder avançar para a direção {self.direcao_apos_intersecao}')
                self.intersecao.coordenar_passagem(self)                                     # Coordenar passagem do carro pela interseção

        class Intersecao:
            
            # Classe que representa uma interseção com semáforo, coordenando a passagem dos carros.
            
            def __init__(self, semaforo, monitor_relatorio):                            
                self.semaforo = semaforo                                                # Objeto da classe Semaforo responsável pelo controle do fluxo de tráfego
                self.monitor_relatorio = monitor_relatorio                              # Objeto da classe MonitorRelatorio para exibir relatórios de status
                self.status_carros = {}                                                 # Dicionário para rastrear o status de cada carro
                self.carros_esperando = []                                              # Lista de carros aguardando a passagem na interseção
                self.carros_passados = 0                                                # Número total de carros que passaram pela interseção
                self.update_event = threading.Event()                                   # Evento para sinalizar a necessidade de atualizar o semáforo
                self.carros_na_rota = {'Norte': 0, 'Sul': 0, 'Este': 0, 'Oeste': 0}     # Dicionário para rastrear a quantidade de carros em cada direção
                self.limite_de_trafego = 2                                              # Limite de carros permitidos em uma direção antes de considerar tráfego intenso
                self.carros_no_transito = []                                            # Lista de carros que enfrentaram tráfego intenso
                self.carros_avariados = []    
                self.programa_is_running = True                                          # Lista de carros que ficaram avariados
                
                    
            def update_light(self):
                
                # Método que atualiza o semáforo de acordo com a passagem dos carros.
                
                while self.programa_is_running:
                    if self.carros_passados >=3:
                        # Reinicia a contagem de carros passados, atualiza o semáforo e exibe a direção atual
                        self.carros_passados = 0
                        self.semaforo.atualizar()
                        print(f'\nSemaforo atualizado. Direção {self.semaforo.verde}')
                                
                    else:
                        # Se nenhum carro passou, aguarda o evento de atualização ou aguarda 3 segundos antes de atualizar o semáforo
                        print(f'\nNenhum carro passou. Semaforo atualizado após 3 segundos')
                        self.update_event.wait(timeout=3)
                        self.semaforo.atualizar()
                        print(f'\nSemaforo atualizado. Direção {self.semaforo.verde}')
                        self.update_event.clear()

                    time.sleep(1)
                    
                    
            def coordenar_passagem(self, carro):
                
                # Método que coordena a passagem de um carro pela interseção.

                # Parâmetros:
                # - carro (Carro): O carro que deseja passar pela interseção.
                
                with self.semaforo:
                    if carro.esta_avariado:
                        # Caso o carro esteja avariado, espera mais 2 segundos antes de prosseguir
                        print(f'Carro {carro.carro_id} está avariado. Aguardando mais 2 segundos')
                        tempo_adicional = 2
                        time.sleep(tempo_adicional)
                        carro.tempo_espera += tempo_adicional
                        self.carros_avariados.append(carro)

                    # Adiciona o carro à lista de carros esperando na interseção e incrementa o contador de carros que passaram
                    self.carros_esperando.append(carro) 
                    self.carros_passados += 1

                    # Registra o tempo de início da espera e incrementa a contagem de carros na rota        
                    start_time = time.time()

                    self.carros_na_rota[carro.direcao] += 1

                    # Aguarda até que o semáforo permita a passagem na direção do carro
                    while self.semaforo.verde != carro.direcao:
                        self.semaforo.condition.wait()

                    # Registra o tempo de fim da espera e calcula o tempo total de espera
                    end_time = time.time()
                    carro.tempo_espera_semaforo = int(end_time - start_time)
                    print(f'Carro {carro.carro_id} avançou após esperar {carro.tempo_espera_semaforo} segundos')

                    if self.carros_na_rota[carro.direcao] > self.limite_de_trafego:
                        # Relata tráfego intenso se o número de carros na rota exceder o limite
                        print(f'Tráfego intenso na rota {carro.direcao}')
                        self.carros_no_transito.append(carro)
                    
                    # Atualiza contadores, sinaliza para atualizar o semáforo e notifica outras threads
                    self.carros_na_rota[carro.direcao] -= 1

                    self.update_event.set()
                    self.semaforo.condition.notify_all()

            def relatorio_status(self):
                
                # Método que exibe o status atual de todos os carros na interseção.
                
                print('\nStatus dos Carros:')
                for carro in self.carros_esperando:
                        status_message = f'Carro {carro.carro_id} veio de {carro.direcao} e prosseguiu para {carro.direcao_apos_intersecao} após a interseção. Esperou no semáforo por {carro.tempo_espera_semaforo} segundos'
                        # Adiciona informações sobre tráfego intenso e avarias, se aplicável
                        if carro in self.carros_no_transito and carro in self.carros_avariados:
                            status_message += ' - Este carro apanhou transito - Este carro ficou avariado'
                        elif carro in self.carros_no_transito:
                            status_message += ' - Este carro apanhou transito'
                        elif carro in self.carros_avariados:
                            status_message += ' - Este carro ficou avariado'
                        print(status_message)
                    
            
        class Semaforo:
            
            # Classe que representa um semáforo que controla o fluxo de tráfego na interseção.
            
            def __init__(self):
                self.verde = None                                       # Direção atual do semáforo (Norte, Sul, Este, Oeste)
                self.mutex = threading.Lock()                           # Objeto de bloqueio para garantir acesso seguro às variáveis compartilhadas
                self.condition = threading.Condition(self.mutex)        # Objeto de condição para coordenar a espera de threads
                self.update_directions = []                             # Lista das direções recentemente atualizadas do semáforo

            def __enter__(self):
                self.mutex.acquire()
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                self.mutex.release()

            def atualizar(self):
                
                # Método que atualiza a direção do semáforo de forma aleatória.
                
                with self.mutex:
                    # Lista de direções possíveis inicialmente
                    direcoes_possiveis = ['Norte', 'Sul', 'Este', 'Oeste']
                    # Remove as direções já atualizadas recentemente
                    for direction in self.update_directions:
                        if direction in direcoes_possiveis:
                            direcoes_possiveis.remove(direction)
                    # Se todas as direções foram recentemente atualizadas, reinicia a lista
                    if not direcoes_possiveis:
                        self.update_directions = []
                        direcoes_possiveis = ['Norte', 'Sul', 'Este', 'Oeste']
                    # Escolhe aleatoriamente uma nova direção verde e registra a escolha    
                    self.verde = random.choice(direcoes_possiveis)
                    self.update_directions.append(self.verde)
                    # Notifica todas as threads em espera que o semáforo foi atualizado
                    self.condition.notify_all()
                    
        class MonitorRelatorio:
            
            # Classe que monitora e exibe relatórios de status da interseção.
            
            def __init__(self):
                self.mutex = threading.Lock()       # Objeto de bloqueio para garantir acesso seguro às variáveis compartilhadas

            def exibir_relatorio(self, intersecao, tempo_execucao, cpu_usage, memoria_usage):
                """
                Método que exibe o relatório de status da interseção.
                """
                with self.mutex:
                    intersecao.relatorio_status()   # Objeto da classe Intersecao contendo informações sobre o status dos carros

                    # Imprime o relatório de desempenho
                    print('\nRelatório de Desempenho:')
                    print(f'Tempo de Execução: {tempo_execucao} segundos')
                    print(f'Uso da CPU: {cpu_usage}%')
                    print(f'Uso de Memória: {memoria_usage} MB')

        def main():
            
            # Função principal que testa as classes com tráfego intenso e carros avariados.
            
            semaforo = Semaforo()
            monitor_relatorio = MonitorRelatorio()
            intersecao = Intersecao(semaforo, monitor_relatorio)

            start_time = time.time()

            # Inicia uma thread para atualizar o semáforo periodicamente
            update_thread = threading.Thread(target=intersecao.update_light, daemon=True)
            update_thread.start()

            direcoes_possiveis = ['Norte', 'Sul', 'Este', 'Oeste']

            random.shuffle(direcoes_possiveis)

            # Cria carros e inicia suas threads
            carros = [Carro(i, direcao, intersecao) for i, direcao in zip(range(1, 5), direcoes_possiveis)]

            carros += [Carro(i, random.choice(['Norte', 'Sul', 'Este', 'Oeste']), intersecao) for i in range(5, 13)]
            
            # Inicia as threads dos carros
            for carro in carros:
                carro.start()

            # Aguarda todas as threads dos carros terminarem
            for carro in carros:
                carro.join()
                
            end_time = time.time()
            
            # Calcula o tempo de execução, uso da CPU e uso de memória
            tempo_execucao = end_time - start_time
            cpu_usage = psutil.cpu_percent()
            memoria_usage = psutil.virtual_memory().used / (1024 ** 2)        # Memória usada em MB

            # Exibe o relatório de status da interseção e do desempenho usando as métricas calculadas
            monitor_relatorio.exibir_relatorio(intersecao, tempo_execucao, cpu_usage, memoria_usage)
            intersecao.programa_is_running = False

        if __name__ == "__main__":
            main()
            menu()
            n = int((input("Choice: ")))
            

    elif n == 3:
        print("See ya next time :)")
        break

    else:
        print("Wrong choice. Make another choice")
        menu()
        n = int((input("Choice: ")))

    