from jobspy import scrape_jobs
import pandas as pd

def buscar_vagas():
    vagas = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor"],
        search_term="Estágio Software",
        location="Florianópolis, SC",
        results_wanted=30,
        hours_old=72, # Vagas fresquinhas dos últimos 3 dias
        country_indeed='brazil'
    )
    
    # Salvando para você ter os dados sem precisar rodar o scraper toda hora
    vagas.to_csv("vagas_brutas.csv", index=False)
    print(f"Sucesso! {len(vagas)} vagas encontradas e salvas.")

if __name__ == "__main__":
    buscar_vagas()