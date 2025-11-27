import json
import random
import sys

# --- CONFIGURAZIONE POKÉMON ---
BIO_POKEMON_IDS = [151, 251, 577, 578, 579, 132, 382, 718, 898]
AI_POKEMON_IDS = [137, 233, 474, 81, 82, 462, 374, 375, 376, 649, 990, 993, 997]

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
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{pokemon_id}.gif"
    return f'<img src="{url}" height="{height}" alt="Pokemon ID {pokemon_id}">'

def replace_chunk(content, start_marker, end_marker, new_html):
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        print(f"Attenzione: Marcatori {start_marker} non trovati.")
        return content

    # Sostituisce tutto quello che c'è tra START ed END (inclusi i ### se ci sono)
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

    # 1. POKÉMON
    bio_poke_id = random.choice(BIO_POKEMON_IDS)
    ai_poke_id = random.choice(AI_POKEMON_IDS)
    html_bio = generate_pokemon_html(bio_poke_id)
    html_ai = generate_pokemon_html(ai_poke_id)
    
    content = replace_chunk(content, "<!-- POKE_BIO_START -->", "<!-- POKE_BIO_END -->", html_bio)
    content = replace_chunk(content, "<!-- POKE_AI_START -->", "<!-- POKE_AI_END -->", html_ai)

    # 2. CITAZIONI
    bio_quote = load_random_quote('bio_quotes.json')
    ai_quote = load_random_quote('ai_quotes.json')
    html_quotes = generate_quote_html(bio_quote, ai_quote)
    
    content = replace_chunk(content, "<!-- DAILY_QUOTES_START -->", "<!-- DAILY_QUOTES_END -->", html_quotes)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("README aggiornato!")

if __name__ == "__main__":
    update_readme()
