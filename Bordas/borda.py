import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
def find_ponto_de_início(image):
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image[row, col] == 255:
                return row, col
    return None

def obtem_vizinhos(row, col, direcao):
    
    direcoes = [
        (0, 1),   # Direita
        (1, 1),   # Diagonal direita-baixo
        (1, 0),   # Baixo
        (1, -1),  # Diagonal esquerda-baixo
        (0, -1),  # Esquerda
        (-1, -1), # Diagonal esquerda-cima
        (-1, 0),  # Cima
        (-1, 1)   # Diagonal direita-cima
    ]
    
    # Obtém as coordenadas do vizinho
    delta_row, delta_col = direcoes[direcao]
    
    # Retorna as coordenadas do vizinho
    return row + delta_row, col + delta_col

def find_proximo_pixel_de_limite(image, linha_atual, coluna_atual, direcao_anterior):
    
    # Ordem de busca para os vizinhos
    ordem_busca = [(direcao_anterior + i) % 8 for i in range(1, 9)]
    
    # Verifica se os vizinhos estão dentro dos limites da imagem
    # e se o pixel é um pixel de fronteira, retornando o primeiro encontrado
    for direcao in ordem_busca:
        
        # Obtém as coordenadas do vizinho
        nova_linha, nova_coluna = obtem_vizinhos(linha_atual, coluna_atual, direcao)
        
        # Verifica se o vizinho está dentro dos limites da imagem
        if 0 <= nova_linha < image.shape[0] and 0 <= nova_coluna < image.shape[1]:
            if image[nova_linha, nova_coluna] == 255:
                return nova_linha, nova_coluna, direcao
    
    # Se nenhum vizinho for encontrado, retorna None
    return None

def codigo_freeman(Imagem_Binaria):
    
    # Encontra o primeiro pixel de fronteira
    ponto_de_início = find_ponto_de_início(Imagem_Binaria)
    
    # Verifica se o ponto de início é válido
    if ponto_de_início is None:
        print("Nenhum objeto encontrado na imagem.")
        return None
    
    # Inicializa as variáveis
    Codigo_freeman = ""
    linha_atual, coluna_atual = ponto_de_início
    direcao_anterior = 7  # Começa na direção 7 (direita-cima)
    vizinhos_visitados = set()
    Pixels_limite = [(linha_atual, coluna_atual)]
    max_iterations = 10000  # Limite máximo de iterações para evitar loops infinitos
    iteration_count = 0     # Contador de iterações

    while True:
        
        # Incrementa o contador de iterações
        iteration_count += 1
        
        # Verifica se o número máximo de iterações foi atingido
        if iteration_count > max_iterations:
            print("Número máximo de iterações atingido. Verifique a imagem.")
            break

        # Encontra o próximo pixel de fronteira na ordem de busca
        proximo_pixel_info = find_proximo_pixel_de_limite(Imagem_Binaria, linha_atual, coluna_atual, (direcao_anterior + 4) % 8)
        
        # Verifica se o próximo pixel é válido
        if proximo_pixel_info is None:
            break

        # Atualiza as variáveis para o próximo pixel
        proxima_linha, proxima_coluna, direcao = proximo_pixel_info
        
        # Verifica se o próximo pixel é o ponto inicial e se a fronteira está completa
        if (proxima_linha, proxima_coluna) == ponto_de_início and len(Pixels_limite) > 1:
            
            # Adiciona o último pixel de fronteira
            Codigo_freeman += str(direcao)
            break

        # Verifica se o próximo pixel já foi visitado
        if (proxima_linha, proxima_coluna) in vizinhos_visitados:
            print("Loop detectado. Encerrando a iteração.")
            break

        # Adiciona o próximo pixel de fronteira aos vizinhos visitados
        vizinhos_visitados.add((proxima_linha, proxima_coluna))
        
        # Adiciona o próximo pixel de fronteira à lista de pixels de fronteira
        Pixels_limite.append((proxima_linha, proxima_coluna))

        # Adiciona a direção ao código de Freeman
        Codigo_freeman += str(direcao)
        
        # Atualiza as variáveis para a próxima iteração
        linha_atual, coluna_atual = proxima_linha, proxima_coluna
        
        # Atualiza a direção anterior
        direcao_anterior = direcao

    return Codigo_freeman, Pixels_limite

def cadeia_freeman(Imagem_Binaria):
    
    # Verifica se a imagem binária é válida e aplica a cadeia de Freeman
    if Imagem_Binaria is not None:
        
        # Aplica a cadeia de Freeman
        Codigo_freeman, Pixels_limite = codigo_freeman(Imagem_Binaria)
        
        # Retorna o código de Freeman e os pixels de fronteira
        return Codigo_freeman, Pixels_limite
    else:
        print("Imagem binária inválida.")
        return None, None