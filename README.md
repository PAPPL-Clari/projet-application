# projet-application
Development of the application project of the cursus of INFOSI at Centrale Nantes.

Voici un guide détaillé pour exécuter le script `databasePush.py` et peupler une base de données locale. Suivez attentivement chaque étape pour assurer le bon fonctionnement du processus.

## Prérequis

1. **pgAdmin 4** : Assurez-vous que pgAdmin est installé sur votre ordinateur. C'est un outil de gestion pour les bases de données PostgreSQL.

2. **Python 3** : Vérifiez que Python 3 est installé. Vous pouvez le télécharger depuis le site officiel de Python.

3. **Dépendances Python** : Les bibliothèques nécessaires sont listées dans le fichier `requirements.txt` du dépôt.

## Étapes à suivre

### 1. Cloner le dépôt GitHub

Clonez le dépôt sur votre machine locale en utilisant la commande suivante :

```bash
git clone https://github.com/PAPPL-Clari/projet-application.git
```

### 2. Créer une base de données dans pgAdmin

1. **Ouvrir pgAdmin** : Lancez pgAdmin et connectez-vous à votre serveur PostgreSQL local.

2. **Créer une nouvelle base de données** :
   - Cliquez avec le bouton droit sur "Bases de données" dans l'arborescence et sélectionnez "Créer" > "Base de données...".
   - Donnez un nom à votre base de données (par exemple, `ma_base_de_donnees`).
   - Sélectionnez un propriétaire pour la base de données.
   - Cliquez sur "Enregistrer" pour créer la base de données.

### 3. Exécuter le script `CreateDatabase.sql`

1. **Ouvrir le fichier SQL** :
   - Dans pgAdmin, accédez à votre nouvelle base de données.
   - Cliquez sur l'onglet "Outils" et sélectionnez "Query Tool".
   - Ouvrez le fichier `CreateDatabase.sql` situé dans le dossier `database` du dépôt cloné.

2. **Exécuter le script** :
   - Copiez le contenu du fichier et collez-le dans l'outil de requête.
   - Cliquez sur le bouton "Exécuter" pour créer les tables nécessaires dans votre base de données.

### 4. Installer les dépendances Python

1. **Naviguer vers le répertoire du projet** :

   ```bash
   cd projet-application/code
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)** :

   ```bash
   python3 -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installer les dépendances** :

   ```bash
   pip install -r requirements.txt
   ```

### 5. Créer le fichier `config.py`

Dans le répertoire `code`, créez un fichier nommé `config.py` contenant les variables suivantes :

```python
secret = 'votre_secret_pour_l_api'
key = 'votre_clé_pour_l_api'
login = 'votre_login_pgAdmin'
password = 'votre_mot_de_passe_pgAdmin'
database = 'nom_de_votre_base_de_donnees'
```

Remplacez les valeurs par vos informations spécifiques :

- `secret` et `key` : Les identifiants pour accéder à l'API.
- `login` et `password` : Vos identifiants pgAdmin pour accéder à la base de données.
- `database` : Le nom de la base de données que vous avez créée.

### 6. Exécuter le script `databasePush.py`

Assurez-vous que votre environnement virtuel est activé (si vous en utilisez un), puis exécutez le script :

```bash
python databasePush.py
```

Ce script se connectera à l'API en utilisant les informations de `config.py`, récupérera les données nécessaires et les insérera dans votre base de données PostgreSQL.

## Remarques supplémentaires

- **Structure des répertoires** : Le fichier `databasePush.py` et le fichier `config.py` doivent se trouver dans le même répertoire (`code`).

- **Dépendances supplémentaires** : Si le fichier `requirements.txt` n'est pas présent, vous devrez installer manuellement les bibliothèques nécessaires, telles que `requests` pour les requêtes HTTP et `psycopg2` pour la connexion à PostgreSQL.

- **Gestion des erreurs** : Assurez-vous que les informations dans `config.py` sont correctes pour éviter les erreurs de connexion à l'API ou à la base de données.

En suivant ces étapes, vous devriez être en mesure de configurer votre environnement et de peupler votre base de données avec succès. 
