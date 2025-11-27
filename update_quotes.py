import json
import random
import os

def load_random_quote(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        return random.choice(quotes)
    except Exception as e:
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
    # 1. Carica le citazioni
    bio = load_random_quote('bio_quotes.json')
    ai = load_random_quote('ai_quotes.json')
    
    # 2. Prepara il nuovo testo
    new_content = generate_html(bio, ai)
    
    # 3. Leggi il README attuale
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_lines = f.readlines()
    
    # 4. Sostituisci la parte tra i marcatori
    # IMPORTANTE: I marcatori devono includere il ritorno a capo \n per essere riconosciuti
    start_marker = '\n'
    end_marker = '\n'
    
    new_readme = []
    in_zone = False
    found = False
    
    for line in readme_lines:
        # strip() rimuove spazi vuoti inizio/fine per fare il confronto sicuro
        if line.strip() == start_marker.strip():
            in_zone = True
            found = True
            new_readme.append(start_marker)
            new_readme.append(new_content + '\n') 
        elif line.strip() == end_marker.strip():
            in_zone = False
            new_readme.append(end_marker)
        elif not in_zone:
            # Aggiunge la riga solo se NON siamo dentro la zona da sostituire
            new_readme.append(line)
            
    if not found:
        print("Errore: Marcatori non trovati nel README!")
        # Se non trova i marker, non sovrascrivere il file per sicurezza
        return

    # 5. Scrivi il file aggiornato
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(new_readme)
    
    print("README aggiornato con successo!")

if __name__ == "__main__":
    update_readme()
