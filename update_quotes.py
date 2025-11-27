import json
import random
import sys

def load_random_quote(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return random.choice(quotes)
    except Exception as e:
        print(f"Errore caricamento {filename}: {e}")
        return {"quote": "Error loading quote", "author": "System"}

def generate_html(bio_quote, ai_quote):
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

def update_readme():
    # 1. Definizione esatta dei marcatori
    start_marker = ""
    end_marker = ""
    
    # 2. Leggi TUTTO il file come una stringa unica
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Errore: README.md non trovato!")
        return

    # 3. Trova la posizione dei marcatori
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        print("Errore: Marcatori non trovati nel README. Assicurati che ci siano e ")
        return

    # 4. Genera il nuovo contenuto HTML
    bio = load_random_quote('bio_quotes.json')
    ai = load_random_quote('ai_quotes.json')
    new_html = generate_html(bio, ai)

    # 5. Costruisci il nuovo file (Taglia e Cuci)
    # Prende tutto PRIMA del marker iniziale + Marker Iniziale + Nuovo HTML + Marker Finale + Tutto DOPO il marker finale
    updated_content = (
        content[:start_index + len(start_marker)] + 
        "\n" + new_html + "\n" + 
        content[end_index:]
    )

    # 6. Scrivi il file
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("README aggiornato con successo!")

if __name__ == "__main__":
    update_readme()
