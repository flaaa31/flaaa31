import json
import random
import sys

# --- CONFIGURAZIONE POKÉMON ---
BIO_POKEMON_IDS = [94, 260, 181, 229]
AI_POKEMON_IDS = [39, 133, 136]

def load_random_quote(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return random.choice(quotes)
    except Exception as e:
        # Fallback sicuro
        return {"quote": "Science is magic that works.", "author": "Kurt Vonnegut"}

def generate_quote_html(bio_quote, ai_quote):
    return f"""<table align="center"><tr><td align="center" width="50%"><strong>🧬 Daily Bio Quote</strong><br><br><em>"{bio_quote['quote']}"</em><br><br>— {bio_quote['author']}</td><td align="center" width="50%"><strong>🤖 Daily AI Quote</strong><br><br><em>"{ai_quote['quote']}"</em><br><br>— {ai_quote['author']}</td></tr></table>"""

def generate_pokemon_html(pokemon_id, height=80):
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/{pokemon_id}.gif"
    return f'<img src="{url}" height="{height}" alt="Pokemon ID {pokemon_id}">'

def replace_chunk(content, start_marker, end_marker, new_html):
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        return content
        
    # Sostituisce mantenendo i marker per il prossimo giro
    return content[:start_index + len(start_marker)] + "\n" + new_html + "\n" + content[end_index:]

def update_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return

    # 1. POKÉMON
    html_bio = generate_pokemon_html(random.choice(BIO_POKEMON_IDS))
    html_ai = generate_pokemon_html(random.choice(AI_POKEMON_IDS))
    
    content = replace_chunk(content, "<!-- POKE_BIO_START -->", "<!-- POKE_BIO_END -->", html_bio)
    content = replace_chunk(content, "<!-- POKE_AI_START -->", "<!-- POKE_AI_END -->", html_ai)

    # 2. CITAZIONI
    bio_q = load_random_quote('bio_quotes.json')
    ai_q = load_random_quote('ai_quotes.json')
    content = replace_chunk(content, "<!-- DAILY_QUOTES_START -->", "<!-- DAILY_QUOTES_END -->", generate_quote_html(bio_q, ai_q))

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
