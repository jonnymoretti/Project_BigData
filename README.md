# Simulação de Tráfego em uma Interseção
<a href="docs/readme_en.md">Versão em Inglês</a>

Este projeto consiste em uma simulação de tráfego em uma interseção de ruas, onde carros se
movem em direções aleatórias. O objetivo é modelar um sistema realista de coordenação de tráfego,
incluindo semáforos, condições de tráfego intenso e carros avariados.

### Funcionalidades Principais

- **Carros Aleatórios:** Cada carro é representado por uma thread e se move em direções aleatórias, iniciando e terminando sua rota na interseção.
- **Semáforo:** O sistema inclui um semáforo que coordena a passagem dos carros, levando em consideração as condições de tráfego e avarias.
- **Condições de Tráfego:** É simulado tráfego intenso, e os carros enfrentam espera adicional caso estejam avariados.
- **Relátorios Detalhados:** O código gera relátorios detalhados sobre o estado dos carros, seus movimentos na interseção e condições especiais, como tráfego intenso e avarias.

### Como Executar

Para testar a simulação, basta executar o script principal `main()` presente no arquivo. O código cira threads para carros e uma thread para atualizar o semáforo, proporcionando uma simulação dinâmica e interativa.

```
python Grupo6_BigData.py
```
Também é possível executar o ficheiro no Google Colab:
<a target="_blank" href="https://colab.research.google.com/drive/12tn7Qrr3XnC6aeO6cGkT2JIpTCXd3BFn?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

### Personalização

- **Direções Iniciais dos Carros:** O código permite personalizar as direções inicias dos carros para simular diferentes cenários de tráfego.
- **Probabilidade de Carros Avariados:** A variável `self.esta_avariado` é definida aleatoriamente para cada carro com base em uma probabilidade, proporcionando flexibilidade na simulação de avarias.

### Resultados

Ao final da execução, um relatório de status da interseção é exibido, fornecendo informação sobre cada carro, suas direções e tempos de espera.
