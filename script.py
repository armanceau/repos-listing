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
    readme_content += "| Nom de la matière | Nom du repos | Status | Lien |\n"
    readme_content += "|-------------------|----------------|--------|------|\n"
    
    for repo in repos:
        matiere = "Non spécifié"
        statut_text = "Non%20commencé"
        statut_badge = "red"
        
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
        
        readme_content += f"| {matiere} | `{repo['name']}` | ![{statut_text}](https://img.shields.io/badge/{statut_text}-{statut_badge}) | [🔗]({repo['html_url']}) |\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("✅ README généré avec succès !")
else:
    print("❌ Impossible de récupérer les repositories :", response.text)
