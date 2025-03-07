import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os
import cv2
from PIL import Image
from io import BytesIO
import requests

def leitura_Imagem(nome):
    
    # Carrega a imagem
    Imagem = cv2.imread(nome, cv2.IMREAD_GRAYSCALE)
    
    # Retorna a imagem
    return Imagem

def download_imagem(args):
    
    # Baixa a imagem da URL
    response = requests.get(args.url)
    
    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        
        # Lê a imagem
        Imagem = Image.open(BytesIO(response.content))
        
        # Salva a imagem
        Imagem.save('./imagens/{}'.format(args.url.split('/')[-1]))
        
    else:
        console.print('Erro ao baixar a imagem. Tente novamente.')


def deletar_imagem(nome):
    
    # Deleta a imagem
    os.remove('./imagens/{}'.format(nome))

def binarizacao_imagem(nome, threshold):
    
    # Leitura da imagem original convertida para RGB
    Imagem_Original = Image.open(nome).convert('RGB')
    
    # Converte a imagem Pillow para um array NumPy
    Imagem_Original_np = np.array(Imagem_Original)
    
    # Converte a imagem para escala de cinza (OpenCV requer isso para binarização)
    Imagem_Cinza = cv2.cvtColor(Imagem_Original_np, cv2.COLOR_RGB2GRAY)
    
    # Binariza a imagem
    _, Imagem_Binaria = cv2.threshold(Imagem_Cinza, threshold, 255, cv2.THRESH_BINARY)
    
    # Inverte a imagem binária (objetos em branco e fundo em preto)
    Imagem_Binaria = cv2.bitwise_not(Imagem_Binaria)
    
    # Retorna a imagem original (Pillow) e a imagem binarizada (NumPy)
    return Imagem_Original, Imagem_Binaria

# Realiza a plotagem das imagens com o matplotlib
def plotagem_imagem(Imagem_Original, Imagem_Binaria, Pixels_limite):
    
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    # Adiciona as imagens nos subplots
    axs[0].imshow(Imagem_Original)
    axs[0].set_title('Imagem Original')
    
    # Adiciona os pixels de fronteira na imagem binária
    for row, col in Pixels_limite:
        Imagem_Binaria[row, col] = 128
        
    axs[1].imshow(Imagem_Binaria, cmap='Greys')
    axs[1].set_title('Imagem Binária com Pixels de Fronteira')
    
    # Remove os eixos dos subplots
    for ax in axs.flat:
        ax.set(xticks=[], yticks=[])
    
    # Mostra a figura com os subplots
    plt.show()
    
def salvar_imagem(Imagem, nome):
    
    plt.imsave(nome, Imagem, cmap='Greys')
    
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        console.print('{}. {}'.format(i+1, imagem))
        
    return imagens

def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o Watershed
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o [bold purple]Watershed[/bold purple]:', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')
    