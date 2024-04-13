import pmd
import csv
from git import Repo

def cloner_repo(url, chemin_destination):
  try:
    Repo.clone_from(url, chemin_destination)
    print(f"Repository cloné avec succès: {url}")
  except Exception as e:
    print(f"Erreur lors du clonage du repository {url}: {e}")

def analyser_projet(chemin_projet):
  """
  Analyse un projet avec PMD et extrait les informations sur les code smells.

  Args:
      chemin_projet (str): Chemin du dossier du projet.
  """
  # Configurez les règles PMD
  regles = pmd.PMDConfiguration()
  regles.rule_sets = "rulesets/java/quickstart.xml"  # Adaptez les règles à votre langage

  # Analysez le projet
  rapport = pmd.Report.run(chemin_projet, config=regles)

  # Extrayez les informations sur les code smells
  smells = []
  for violation in rapport.violations:
    smells.append({
      "fichier": violation.filename,
      "ligne": violation.beginline,
      "type": violation.rule.name,
      "gravite": violation.priority.name,
      "description": violation.message
    })

  # Enregistrez les données dans un fichier CSV
  with open(f"{chemin_projet}/smells.csv", "w", newline="") as fichier_csv:
    writer = csv.DictWriter(fichier_csv, fieldnames=smells[0].keys())
    writer.writeheader()
    writer.writerows(smells)
  print(f"Informations sur les code smells enregistrées dans {chemin_projet}/smells.csv")

def main():
  """
  Fonction principale du programme.
  """
  # Liste des URLs des repositories
  urls_repos = [
    "https://github.com/user/repo1.git",
    "https://github.com/user/repo2.git",
    # ... ajoutez les URLs de vos repositories
  ]

  # Chemin de base pour cloner les repositories
  chemin_base = "C:\Users\norhe\pfaa"

  # Cloner les repositories et analyser les projets
  for i, url_repo in enumerate(urls_repos):
    chemin_projet = f"{chemin_base}/projet_{i+1}"
    cloner_repo(url_repo, chemin_projet)
    analyser_projet(chemin_projet)

if __name__ == "__main__":
  main()