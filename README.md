# Projet 16: Extraction de données de l’API AlumnForce et enregistrement en base de données  

## Introduction  

Depuis un an, AlumnForce, le prestataire de stockage en base de données de Centrale Nantes Alumni (CNA), a mis en place une API de service qui facilite l’interaction avec la base de données, tant pour l’importation que pour l’exportation des données.  

Ce projet vise à développer une solution locale permettant d'exploiter les données disponibles via cette API. L’objectif principal est de fournir au personnel de CNA un accès simplifié et efficace aux données des étudiants.  

Les livrables incluent :  
- Un script pour la création de la base de données.  
- Un script pour la population et la mise à jour des données.  
- Une documentation technique détaillée assurant une utilisation et une gestion continues.  

## Documentation  

- La **documentation technique complète**, décrivant les fonctions du programme, est disponible dans le fichier suivant :  
  ```  
  documentation/build/html/index.html  
  ```  

- Les **rapports détaillés**, expliquant le processus de création, les points d'amélioration et les réflexions intermédiaires, se trouvent dans :  
  ```  
  documentation/rapports/  
  ```  

## Prérequis  

Avant de commencer, assurez-vous que :  
1. **[pgAdmin 4](https://www.pgadmin.org/download/)** est installé sur votre ordinateur pour gérer la base de données PostgreSQL.  
2. **[Python 3](https://www.python.org/downloads/)** est installé pour exécuter les scripts du projet.  

## Étapes d'installation et d'exécution  

### 1. Cloner le projet  
Clonez le dépôt GitHub sur votre machine locale :  
```bash  
git clone https://github.com/PAPPL-Clari/projet-application.git  
```  

### 2. Créer une base de données dans pgAdmin  
1. Ouvrez **pgAdmin** et connectez-vous à votre serveur PostgreSQL local.  
2. Créez une nouvelle base de données en suivant ces étapes :  
   - Clic droit sur "Bases de données" > "Créer" > "Base de données...".  
   - Donnez un nom à votre base (ex. `AlumnForceBase`).  
   - Sélectionnez un propriétaire pour cette base.  
   - Enregistrez.  

### 3. Exécuter le script SQL pour créer les tables  
1. Accédez à votre base de données dans pgAdmin.  
2. Ouvrez le fichier `CreateDatabase.sql` dans l’onglet **Query Tool** (trouvé dans `database/CreateDatabase.sql`).  
3. Exécutez le script pour créer les tables nécessaires.  

### 4. Installer les dépendances Python  
1. Allez dans le répertoire `code` du projet :  
   ```bash  
   cd projet-application/code  
   ```  

2. (Optionnel) Créez et activez un environnement virtuel :  
   ```bash  
   python3 -m venv env  
   source env/bin/activate  # Sur Windows : env\Scripts\activate  
   ```  

3. Installez les dépendances à l'aide du fichier `requirements.txt` :  
   ```bash  
   pip install -r requirements.txt  
   ```  

### 5. Configurer le fichier `config.py`  
Dans le répertoire `code`, créez un fichier nommé `config.py` avec le contenu suivant :  
```python  
secret = 'votre_secret_pour_l_api'  
key = 'votre_clé_pour_l_api'  
login = 'votre_login_pgAdmin'  
password = 'votre_mot_de_passe_pgAdmin'  
database = 'nom_de_votre_base'  
```  
Remplacez les valeurs par vos informations.  

### 6. Exécuter le script de population de la base de données  
Exécutez le script `databasePush.py` pour peupler la base de données :  
```bash  
python databasePush.py  
```  

## Remarques supplémentaires  

- La structure des répertoires doit être respectée pour garantir le bon fonctionnement du projet.  
- En cas de problème, vérifiez que vos informations de configuration sont correctes (dans `config.py`).  
- Vous pouvez trouver des améliorations possibles et des informations supplémentaires dans les rapports fournis dans `documentation/rapports`.  
