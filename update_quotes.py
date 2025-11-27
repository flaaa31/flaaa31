import json
import random
import sys

# --- CONFIGURAZIONE POKÉMON ---
# Liste curate di ID Pokémon (puoi trovarli su Pokédex nazionale)
# Tema BIO: Cellule, DNA, natura antica, esperimenti genetici
BIO_POKEMON_IDS = [
    151, # Mew (L'origine)
    251, # Celebi (Natura/Tempo)
    577, # Solosis (La cellula)
    578, # Duosion (Mitosi)
    579, # Reuniclus (Organismo complesso)
    132, # Ditto (Il DNA mutabile)
    382, # Kyogre (Origine della vita marina)
    718, # Zygarde (L'ecosistema - Forma Cellula/Nucleo sarebbe top ma usiamo base)
    898, # Calyrex (Antica sapienza)
]

# Tema AI/TECH: Robot, computer, magneti, futuro, spazio
AI_POKEMON_IDS = [
    137, # Porygon (Il primo Pokémon digitale)
    233, # Porygon2
    474, # Porygon-Z (AI corrotta)
    81,  # Magnemite
    82,  # Magneton
    462, # Magnezone
    374, # Beldum (Robotico)
    375, # Metang
    376, # Metagross (Supercomputer)
    649, # Genesect (Cyborg antico)
    990, # Iron Treads (Futuro Paradox)
    993, # Iron Jugulis (Futuro Paradox)
    997, # Iron Valiant (Futuro Paradox - Robot Gardevoir/Gallade)
]
# ------------------------------


def load_random_quote(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return random.choice(quotes)
    except Exception as e:
        print(f"Errore caricamento {filename}: {e}")
        return {"quote": "Error loading quote", "author": "System"}

def generate_quote_html(bio_quote, ai_quote):
    return f"""
<table align="center">
  <tr>
    <td align="center" width="50%">
      <strong>🧬 Daily Bio Quote</strong><br><br>
      <em>"{bio_quote['quote']}"</em><br><br>
      — {bio_quote['author']}
    </td>
    <td align="center" width="50%">
      <strong>🤖 Daily AI Quote</strong><br><br>
      <em>"{ai_quote['quote']}"</em><br><br>
      — {ai_quote['author']}
    </td>
  </tr>
</table>
"""

def generate_pokemon_html(pokemon_id, height=80):
    # Usa gli sprite animati "Showdown" che sono di alta qualità
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{pokemon_id}.gif"
    return f'<img src="{url}" height="{height}" alt="Pokemon ID {pokemon_id}">'

def replace_chunk(content, start_marker, end_marker, new_html):
    """Funzione helper per sostituire il testo tra due marcatori."""
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        print(f"Attenzione: Marcatori {start_marker} non trovati. Salto questo blocco.")
        return content

    updated_content = (
        content[:start_index + len(start_marker)] + 
        "\n" + new_html + "\n" + 
        content[end_index:]
    )
    return updated_content

def update_readme():
    readme_path = 'README.md'
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Errore: {readme_path} non trovato!")
        return

    # --- 1. AGGIORNAMENTO POKÉMON ---
    # Scegli due ID a caso
    bio_poke_id = random.choice(BIO_POKEMON_IDS)
    ai_poke_id = random.choice(AI_POKEMON_IDS)
    
    # Genera l'HTML
    html_bio_poke = generate_pokemon_html(bio_poke_id)
    html_ai_poke = generate_pokemon_html(ai_poke_id)
    
    # Sostituisci nel contenuto
    content = replace_chunk(content, "", "", html_bio_poke)
    content = replace_chunk(content, "", "", html_ai_poke)


    # --- 2. AGGIORNAMENTO CITAZIONI ---
    bio_quote = load_random_quote('bio_quotes.json')
    ai_quote = load_random_quote('ai_quotes.json')
    html_quotes = generate_quote_html(bio_quote, ai_quote)
    
    content = replace_chunk(content, "", "", html_quotes)


    # --- SCRITTURA FILE FINALE ---
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"README aggiornato con successo! (Bio ID: {bio_poke_id}, AI ID: {ai_poke_id})")

if __name__ == "__main__":
    update_readme()
