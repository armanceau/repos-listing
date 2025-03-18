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
    readme_content += "_Ce repository regroupe tous les travaux pratiques réalisés au cours des années suivantes : Bachelor 3, Master 1 et Master 2 à l'__EFREI Paris Assas Panthéon__._\n\n"
    
    annee_repos = {"B3": [], "M1": [], "M2": []}
    
    for repo in repos:
        topics = repo.get("topics", [])
        
        statut_text = "Non%20commencé"
        statut_badge = "red"
        annee_text = "Non%20spécifié"
        annee_badge = "grey"
        
        for topic in topics:
            if "en-cours" in topic:
                statut_text = "En%20cours"
                statut_badge = "FF6600"
                break 
            elif "termine" in topic:
                statut_text = "Terminé"
                statut_badge = "brightgreen" 
                break 
        
        for topic in topics:
            if "b3" in topic:
                annee_text = "B3"
                annee_repos["B3"].append(repo)
                break
            elif "m1" in topic:
                annee_text = "M1"
                annee_repos["M1"].append(repo) 
                break
            elif "m2" in topic:
                annee_text = "M2"
                annee_repos["M2"].append(repo)
                break
    
    for annee, repos_annee in annee_repos.items():
        if repos_annee:  
            if annee == "B3":
                annee_badge = "blue" 
            elif annee == "M1":
                annee_badge = "8A2BE2"
            elif annee == "M2":
                annee_badge = "060270"

            readme_content += f"\n## ![{annee}](https://img.shields.io/badge/{annee}-{annee_badge})\n\n"
            readme_content += "| Nom du repo | Status | Lien |\n"
            readme_content += "|----------------|--------|------|\n"
            
            for repo in repos_annee:
                statut_text = "Non%20commencé"
                statut_badge = "red"

                for topic in repo.get("topics", []):
                    if "en-cours" in topic:
                        statut_text = "En%20cours"
                        statut_badge = "FF6600"
                        break 
                    elif "termine" in topic:
                        statut_text = "Terminé"
                        statut_badge = "brightgreen" 
                        break

                readme_content += f"| `{repo['name']}` | ![{statut_text}](https://img.shields.io/badge/{statut_text}-{statut_badge}) | [🔗]({repo['html_url']}) |\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("✅ README généré avec succès !")
else:
    print("❌ Impossible de récupérer les repositories :", response.text)
