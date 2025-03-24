import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

chrome_driver_path = "/usr/local/bin/chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode sans interface graphique
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
def get_article_links(url="https://senego.com/rubrique/actualites", max_links=310):
    # Configuration du WebDriver


    # Ouvrir la page
    driver.get(url)
    time.sleep(3)  # Attendre le chargement initial

    # Fonction pour faire défiler la page
    def scroll_down():
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # Attendre le chargement

    # Récupérer les liens des articles
    article_links = set()
    while len(article_links) < max_links:
        scroll_down()
        try:
            posts_section = driver.find_element(By.CSS_SELECTOR, "section.postsSectionCenter")
            articles = posts_section.find_elements(By.CSS_SELECTOR, "article a[href]")
            for article in articles:
                link = article.get_attribute("href")
                article_links.add(link)
                print(f" -[{len(article_links)}] Ajouté : {link}")
        except Exception as e:
            print(f"Erreur : {e}")

    driver.quit()  # Fermer le navigateur
    return list(article_links)[:max_links]

def extract_and_save_articles(links, output_file="data/db/senego/senego_articles.json"):
    # Configuration du WebDriver
    chrome_driver_path = "/usr/local/bin/chromedriver"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    articles_data = []
    
    for id, link in enumerate(links):
        print(f"Extraction de l'article {id+1}/{len(links)}")
        try:
            driver.get(link)
            time.sleep(2)  # Attente pour le chargement de la page
            
            title = driver.find_element(By.TAG_NAME, "h1").text
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
            content = "\n".join([p.text for p in paragraphs])
            date = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")

            articles_data.append({"id": id, "title": title, "url": link, "content": content, "date": date})
        
        except Exception as e:
            print(f"Erreur sur {link} : {e}")
    
    driver.quit()

    # Sauvegarde des articles
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=4)

    print(f"Extraction terminée ! {len(articles_data)} articles sauvegardés dans '{output_file}'.")

# Exemple d'utilisation
links = get_article_links()  # Récupérer les liens avec la fonction précédente
extract_and_save_articles(links)
