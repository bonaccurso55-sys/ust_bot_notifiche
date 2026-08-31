import os
import json
import requests
from bs4 import BeautifulSoup

# INSERISCI QUI I TUOI DATI
BOT_TOKEN = "8886900020:AAHendxWaPTaf2gT_IXDS94nQyNaUct0xo4"
CHAT_ID = "621508022"

URL_SITO = "https://www.mim.gov.it/web/brescia"
FILE_MEMORIA = "viste.json"

def invia_notifica(titolo, link):
    messaggio = (
        f"🔔 <b>Nuova Comunicazione UST Brescia!</b>\n\n"
        f"📌 <b>Titolo:</b> {titolo}\n\n"
        f"🔗 <a href='{link}'>Apri la comunicazione</a>"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": messaggio,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def main():
    # Carica storico link già inviati
    if os.path.exists(FILE_MEMORIA):
        with open(FILE_MEMORIA, "r", encoding="utf-8") as f:
            viste = set(json.load(f))
    else:
        viste = set()

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL_SITO, headers=headers)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    nuove_viste = set(viste)

    # Scansione dei link presenti nella pagina
    for a in soup.find_all("a", href=True):
        titolo = a.get_text(strip=True)
        href = a["href"]

        # Filtraggio dei link ad avvisi e circolari
        if titolo and len(titolo) > 15 and ("/web/brescia/" in href or "/web/brescia/-/" in href):
            link_completo = href if href.startswith("http") else f"https://www.mim.gov.it{href}"
            
            if link_completo not in viste:
                invia_notifica(titolo, link_completo)
                nuove_viste.add(link_completo)

    # Salva il nuovo storico
    with open(FILE_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(list(nuove_viste), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
