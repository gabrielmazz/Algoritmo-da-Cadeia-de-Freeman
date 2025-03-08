from rich.progress import Progress
import time

# Cria uma instncia de Progress
with Progress() as progress:

    # Adiciona uma tarefa barra de progresso
    task = progress.add_task("[cyan]Processando...", total=100)

    # Simula um processo demorado
    while not progress.finished:
        progress.update(task, advance=1)  # Avana a barra de progresso
        time.sleep(0.01)  # Simula um atraso