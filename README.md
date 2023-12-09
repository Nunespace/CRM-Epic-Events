# Logiciel CRM interne pour Epic Events

***
Epic Events est une entreprise de conseil et de gestion dans l'événementiel qui répond aux besoins des start-up voulant organiser des « fêtes épiques ».
Epic Events souhaite se doter d'un système CRM (Customer Relationship Management) sécurisé interne à l'entreprise.

## Fonctionnalités de l'application

L'application permettra de gérer une base de données pour stocker et manipuler de manière sécurisée les informations de leurs clients, ainsi que les contrats et les événements qu'Epic Events organise.
L’application est faite en ligne de commande. Le principe du moindre privilège est appliqué lors de l'attribution de l'accès aux données.
Une journalisation est mise en oeuvre avec Sentry pour:
- toutes les exceptions inattendues, 
- chaque création/modiﬁcation d’un collaborateur,
- la signature d’un contrat.

## Permissions

Les différentes permissions sont récapitulées [sur ce tableau](docs/permissions.pdf).
 
## Configuration actuelle

L’application nécessite un fichier config.ini non présent dans ce dépôt github.

## Prérequis

L'application aura besoin de **Python** (version 3.12), **Git** et **Pipenv** pour fonctionner. Si besoin, vous pouvez les installer en suivant les instructions sur [cette page](docs/installation_python-git-pipenv.md).

L'application utilise le système de gestion de base de données **MySQL**. Pour l'installer, suivez ce lien [Comment installer MySQL](https://openclassrooms.com/fr/courses/6971126-implementez-vos-bases-de-donnees-relationnelles-avec-sql/7152681-installez-le-sgbd-mysql).


## Installation

Cette application exécutable localement peut être installée à l'aide de pipenv en suivant les étapes décrites ci-dessous.
> [!NOTE]  
> Si vous souhaitez utiliser pip à la place de pipenv, vous diposez du fichier *requirements.txt* pour installer toutes les dépendances du projet. Il vous faudra ensuite activer vous-même l'environnement virtuel (dans ce cas enlever "pipenv" ou "pipenv run" de toutes les commandes). 

1. Ouvrez le terminal et tapez :

```
git clone https://github.com/Nunespace/CRM-Epic-Events.git
```


2. Placez-vous dans le répertoire CRM-Epic-Events :
```
cd CRM-Epic-Events
```

3. Installez les dépendances du projet :
```
pipenv install

```

4. Créer le superutilisateur et la base de données.

Ouvrez **MySQL** et taper :
```
CREATE DATABASE epic_events;
```
puis
```
CREATE USER "admin"@"localhost" IDENTIFIED BY "password";
```
> [!IMPORTANT]  
> Mettre à la place de password le mot de passe indiqué dans le fichier config.ini

et taper:
```
GRANT ALL PRIVILEGES ON epic_events.* TO "admin"@"localhost";
```
enfin:
```
FLUSH PRIVILEGES;
```
5. Enregistrer le fichier config.ini dans le répertoire CRM-Epic-Events à la racine du projet

6. Créer un utilisateur de l'équipe Management (qui dispose des permissions pour créer les collaborateurs/utilsateurs).
Revenir sur le terminal et taper:
```
pipenv run python -m create_db
```
 
7. Démarrer l'application avec :
```
pipenv run python -m login
```


## Tests

Les tests de ce projet ont été écrits avec le framework pytest.

### Lancement des tests
Les tests sont executables avec la commande : 
```
pipenv run pytest
```

Il est possible de lancer qu'un seul test. Par exemple : 
```
pipenv run pytest tests/unit/test_managers.py::TestCrud::test_create_client_ok
```

### Couverture de test

Ce projet contient la librairie Python Coverage.py qui fournit un rapport qui nous donne le pourcentage de couverture de ligne par fichier source de couverture. Ce rapport peut être obtenu avec cette commande : 
```
pipenv run pytest --cov=.
```
Un rapport HTML, plus détaillé, peut aussi être généré en tapant : 
```
pipenv run pytest --cov=. --cov-report html
```
Nn nouveau dossier *htmlcov* est ainsi créé à l'endroit où vous avez lancé la commande. Avec votre navigateur, ouvrez le fichier *index.html*  qui contient un résumé du rapport de couverture. À partir de cette page, vous pourrez naviguer à travers les différents fichiers afin d’avoir le détail sur la couverture.






