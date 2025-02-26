import requests

# Configuration
GITHUB_USERNAME = "armanceau"
TOPIC = "efrei-tag"

# URL de l'API GitHub publique (sans token)
url = f"https://api.github.com/search/repositories?q=topic:{TOPIC}+user:{GITHUB_USERNAME}"
response = requests.get(url)

if response.status_code == 200:
    repos = response.json()["items"]
    readme_content = "# 📚 EFREI\n\n"
    readme_content += "_Ce repository regroupe tous les travaux pratiques réalisés au cours des années suivante : Bachelor 3, Master 1 et Master 2 à l'__EFREI Paris Assas Panthéon__._\n\n"
    readme_content += "| Année | Nom du repos | Status | Lien |\n"
    readme_content += "|-------------------|----------------|--------|------|\n"
    
    for repo in repos:
       
        topics = repo.get("topics", [])
        
        for topic in topics:
            if "en-cours" in topic:
                statut_text = "En%20cours"
                statut_badge = "FF6600"
                statut_found = True
                break 
            elif "termine" in topic:
                statut_text = "Terminé"
                statut_badge = "brightgreen" 
                break 
            else:
                statut_text = "Non%20commencé"
                statut_badge = "red"

        for topic in topics:
            if "b3" in topic:
                annee_text = "B3"
                annee_badge = "blue"
                break 
            elif "m1" in topic:
                annee_text = "M1"
                annee_badge = "8A2BE2"
                break 
            elif "m2" in topic:
                annee_text = "M2"
                annee_badge = "060270"
                break 
            else:
                annee_text = "Non%20spécifié"
                annee_badge = "grey"
        
        readme_content += f"| ![{annee_text}](https://img.shields.io/badge/{annee_text}-{annee_badge}) | `{repo['name']}` | ![{statut_text}](https://img.shields.io/badge/{statut_text}-{statut_badge}) | [🔗]({repo['html_url']}) |\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("✅ README généré avec succès !")
else:
    print("❌ Impossible de récupérer les repositories :", response.text)
