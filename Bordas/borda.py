import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
def find_ponto_de_início(image):
    """Encontra o primeiro pixel de fronteira (mais à esquerda e no topo)."""
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            if image[row, col] == 255:
                return row, col
    return None

def get_neighbor(row, col, direction):
    """Retorna as coordenadas do vizinho na direção especificada."""
    directions = [
        (0, 1),   # Direita
        (1, 1),   # Diagonal direita-baixo
        (1, 0),   # Baixo
        (1, -1),  # Diagonal esquerda-baixo
        (0, -1),  # Esquerda
        (-1, -1), # Diagonal esquerda-cima
        (-1, 0),  # Cima
        (-1, 1)   # Diagonal direita-cima
    ]
    delta_row, delta_col = directions[direction]
    return row + delta_row, col + delta_col

def find_next_boundary_pixel(image, linha_atual, coluna_atual, previous_direction):
    """Encontra o próximo pixel de fronteira na ordem de busca."""
    search_order = [(previous_direction + i) % 8 for i in range(1, 9)]
    for direction in search_order:
        new_row, new_col = get_neighbor(linha_atual, coluna_atual, direction)
        if 0 <= new_row < image.shape[0] and 0 <= new_col < image.shape[1]:
            if image[new_row, new_col] == 255:
                return new_row, new_col, direction
    return None

def codigo_freeman(Imagem_Binaria):
    
    """Gera o código de Freeman para a fronteira do objeto na imagem binária.
    Args:
        Imagem_Binaria (np.ndarray): Imagem binária com objetos em branco e fundo em preto.
    Returns:
        str: Código de Freeman para a fronteira do objeto.
        list: Lista de pixels de fronteira.
    """
    
    # Encontra o primeiro pixel de fronteira
    ponto_de_início = find_ponto_de_início(Imagem_Binaria)
    
    # Verifica se o ponto de início é válido
    if ponto_de_início is None:
        print("Nenhum objeto encontrado na imagem.")
        return None
    
    # Inicializa as variáveis
    Codigo_freeman = ""
    linha_atual, coluna_atual = ponto_de_início
    previous_direction = 7  # Começa na direção 7 (direita-cima)
    visited_pixels = set()
    Pixels_limite = [(linha_atual, coluna_atual)]
    max_iterations = 10000  # Limite máximo de iterações para evitar loops infinitos
    iteration_count = 0     # Contador de iterações

    while True:
        iteration_count += 1
        
        # Verifica se o número máximo de iterações foi atingido
        if iteration_count > max_iterations:
            print("Número máximo de iterações atingido. Verifique a imagem.")
            break


        próxomo_pixel_info = find_next_boundary_pixel(Imagem_Binaria, linha_atual, coluna_atual, (previous_direction + 4) % 8)
        if proximo_pixel_info is None:
            break

        next_row, next_col, direction = proximo_pixel_info
        # Verifica se o próximo pixel é o ponto inicial e se a fronteira está completa
        if (next_row, next_col) == ponto_de_início and len(Pixels_limite) > 1:
            Codigo_freeman += str(direction)
            break

        if (next_row, next_col) in visited_pixels:
            print("Loop detectado. Encerrando a iteração.")
            break

        visited_pixels.add((next_row, next_col))
        Pixels_limite.append((next_row, next_col))

        Codigo_freeman += str(direction)
        linha_atual, coluna_atual = next_row, next_col
        previous_direction = direction

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