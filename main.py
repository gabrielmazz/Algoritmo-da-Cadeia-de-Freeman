import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import Bordas.borda as borda
import Utils.utils_imagem as ut_img
import Utils.utils_code as ut_code
import numpy as np
import time

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')
INFO = parser.add_argument('--info', action='store_true', help='Exibir o tempo de execução')
URL_IMAGE = parser.add_argument('--url', type=str, help='URL da imagem para usar no algoritmo')

def freeman(imagem_escolhida, tipo, threshold, args):
    
    # Inicializa o tempo de execução
    start_time = time.time()
    
    with Progress() as progress:
        
        # Adiciona uma tarefa barra de progresso
        task = progress.add_task("[cyan]Processando...", total=3)
        
        # Leitura da imagem
        progress.update(task, advance=1, description='[green]Lendo e binarizando a imagem...')
        Imagem_Original, Imagem_Binaria = ut_img.binarizacao_imagem('./imagens/{}'.format(imagem_escolhida), threshold)
        
        time.sleep(1)
        
        # Aplica a cadeia de Freeman
        progress.update(task, advance=1, description='[green]Aplicando a cadeia de Freeman...')
        Codigo_freeman, Pixels_limite = borda.cadeia_freeman(Imagem_Binaria)
    
        time.sleep(1)
    
        # Finaliza o tempo de execução
        end_time = time.time() - start_time - 2
        
        # Realiza a plotagem das imagens
        progress.update(task, advance=1, description='[green]Plotando as imagens...')
        ut_img.plotagem_imagem(Imagem_Original, Imagem_Binaria, Pixels_limite)
        
    time.sleep(1)
    ut_code.clear_terminal()

    # Deleta a imagem baixada
    if args.url:
        ut_img.deletar_imagem(imagem_escolhida)

    # Imprime as informações na tela
    if args.info:
        ut_code.print_infos_table(end_time, tipo, threshold, Codigo_freeman, imagem_escolhida)
        
    # Salva a imagem na pasta de resultados
    if args.save:
        plt.savefig('./resultados/{}'.format(imagem_escolhida.split('.')[0]))

if __name__ == '__main__':
    
    # Funções triviais
    ut_code.clear_terminal()
    ut_code.print_title()
    
    # Verifica se o usuário passou uma URL de imagem
    args = parser.parse_args()
    
    # Baixa a imagem da URL
    if args.url:
        ut_img.download_imagem(args)
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)  
    
    # Escolhe uma imagem para aplicar o método de Freeman
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    # Define os valores de sigma e threshold
    threshold = float(Prompt.ask('\nDigite o [bold purple]valor[/bold purple] do [bold cyan](threshold)[/bold cyan] [green](default 128)[/green]', default=128))
    
    # Aplica o método de Freeman
    freeman(imagem_escolhida, 'freeman', threshold, args)