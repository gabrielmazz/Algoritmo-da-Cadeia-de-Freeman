import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
import Bordas.borda as borda
import Utils.utils_imagem as ut_img
import Utils.utils_code as ut_code
import numpy as np

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')

def freeman(imagem_escolhida, tipo):
    
    # Leitura da imagem
    Imagem_Original, Imagem_Binaria = ut_img.binarizacao_imagem('./imagens/{}'.format(imagem_escolhida), 128)
    
    # Aplica a cadeia de Freeman
    Codigo_freeman, Pixels_limite = borda.cadeia_freeman(Imagem_Binaria)
    
    # Realiza a plotagem das imagens
    ut_img.plotagem_imagem(Imagem_Original, Imagem_Binaria, Pixels_limite)
    
    # Salva a imagem na pasta de resultados
    # if SAVE:
    #     ut_img.salvar_imagem(Imagem_Filtrada, './resultados/{}_{}_sigma_{}_levels_{}.png'.format(imagem_escolhida.split('.')[0], tipo, sigma, levels))

if __name__ == '__main__':
    
    ut_code.clear_terminal()
    ut_code.print_title()
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Otsu
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    # Define os valores de sigma e threshold
    #sigma = float(Prompt.ask('\nDigite o [bold purple]valor[/bold purple] do [bold purple]sigma[/bold purple] [cyan](sigma)[/cyan] [green](default 1)[/green]', default=1))
    #levels = int(Prompt.ask('Digite o [bold purple]número[/bold purple] de [bold purple]níveis[/bold purple] [cyan](levels)[/cyan] [green](default 64)[/green]', default=64))

    freeman(imagem_escolhida, 'watershed')