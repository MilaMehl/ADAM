from jobspy import scrape_jobs
import pandas as pd
from rich.console import Console
from rich.table import Table
import webbrowser
import os
from datetime import datetime

console = Console()

def executar_adam_v2():
    # Captura a escolha do usuário e guarda na variável 'cidade_alvo'
    # O .strip().title() limpa espaços extras e deixa a Primeira Letra Maiúscula (ex:' palhoça' vira 'Palhoça')
    cidade_alvo = console.input("[bold #ff3399]Digite a cidade alvo (ex: Palhoça, Florianópolis, São José): [/bold #ff3399]").strip().title()
    
    console.print(f"[yellow]Entendido. Focando os radares em: {cidade_alvo}...[/yellow]")
    console.print("[bold blue]ADAM v2.0:[/bold blue] Iniciando busca cirúrgica (Local + Remote)...")

    termo_ti = 'Estágio (Python OR Software OR "Developer" OR "Programador" OR "Dados")'
    ...
    
    try:
        # Busca 1: Local (SC)
        vagas_locais = scrape_jobs(
            site_name = ["indeed", "linkedin"],
            search_term = termo_ti,
            location = f"{cidade_alvo}, SC",
            results_wanted = 20,
            country_indeed ='brazil'
        )

        # Busca 2: Remota (Brasil todo)
        vagas_remotas = scrape_jobs(
            site_name =["indeed", "linkedin"],
            search_term = termo_ti,
            is_remote = True,
            results_wanted = 20,
            country_indeed = 'brazil'
        )

        # Une as duas buscas
        jobs = pd.concat([vagas_locais, vagas_remotas]).drop_duplicates(subset=['job_url'])

        if not jobs.empty:
            # FILTRO: Remove vagas de engenharia (por algum motivo aparece várias)
            excluir = ['Civil', 'Elétrica', 'Mecânica', 'Eletrotécnica', 'Logística', 'Comércio Exterior']
            pattern = '|'.join(excluir)
            jobs = jobs[~jobs['title'].str.contains(pattern, case=False, na=False)]

            # Filtro geográfico
            locais_permitidos = [cidade_alvo, 'Remoto', 'Remote']
            padrao_locais = '|'.join(locais_permitidos)
            jobs = jobs[jobs['location'].str.contains(padrao_locais, case=False, na=False)]

            # ORDENAÇÃO: Vagas mais novas primeiro
            # (Se a coluna de data existir e for tratável)

            console.print(f"[bold green]Sucesso![/bold green] {len(jobs)} vagas de TI filtradas.")

            # Cria um excel com as vagas selecionadas
            jobs.to_excel("vagas_selecionadas.xlsx", index=False)
            
            # cria um arquivo HTML para poder clicar nas vagas e abrir direto no navegador
            html_file = "radar_vagas.html"
            #jobs[['company', 'title', 'location', 'job_url']].to_html(html_file, render_links=True, index=False) -> ta muito feio

            # --- Design do HTML ---
            #INJETANDO DESIGN E TEMPO NO HTML
            tabela_html = jobs[['company', 'title', 'location', 'job_url']].to_html(render_links=True, index=False, escape=False)
            
            # 1. Capturando a hora exata da varredura
            agora = datetime.now().strftime("%H:%M %d/%m/%Y")
            
            # 2. O Design (Pink + Dark Mode)
            estilo_css = """
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; padding: 30px; }
                h1 { color: #ff3399; margin-bottom: 5px; } /* Rosa Choque */
                .descricao { 
                    color: #b0b0b0;
                    font-size: 1.1em; 
                    margin-top: 0; 
                    margin-bottom: 5px; /* Deixa um espacinho pequeno para a data */
                }
                .timestamp { color: #888; font-size: 0.9em; font-style: italic; margin-top: 0; margin-bottom: 20px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #1e1e1e; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
                th { background-color: #cc0066; color: white; padding: 15px; text-align: left; text-transform: uppercase; letter-spacing: 1px;} /* Rosa Escuro */
                td { padding: 12px 15px; border-bottom: 1px solid #333; }
                tr:hover { background-color: #2c2c2c; }
                a { color: #ff3399; text-decoration: none; font-weight: bold; }
                a:hover { color: #ff99cc; text-decoration: underline; } /* Rosa Claro no Hover */
            </style>
            """
            
            # 3. O Cabeçalho + Qual o horário da varredura
            cabecalho = f"""
            <h1>Radar ADAM: Vagas de TI </h1>
            <p class="timestamp">Última varredura de vagas foi às {agora}.</p>
            """
            
            # 4. Juntando as peças e salvando o arquivo
            with open(html_file, "w", encoding="utf-8") as arquivo:
                arquivo.write(estilo_css + cabecalho + tabela_html)
            
            console.print(f"[bold]Planilha Excel e Radar HTML gerados![/bold]")
            
            # Abre o HTML automaticamente no navegador
            webbrowser.open('file://' + os.path.realpath(html_file))

        else:
            console.print("[yellow]Nada encontrado com esses critérios.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]Erro de Execução:[/bold red] {e}")

if __name__ == "__main__":
    executar_adam_v2()