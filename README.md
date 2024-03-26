Saturne est un projet de création d'une application permettant de réaliser des interfaces Tkinter graphiquement, et de générer le code correspondant.
Prérequis et règles : 
Les prérequis de l'application sont à retrouver dans le fichier "requirements.txt"

règle : 
    
Le démonstrateur de Saturne est une application développée pour fonctionner SANS accéder au fichiers de l'application autre que le module main. Il est donc très fortement déconseillé d'ouvrir, de modifier, ou de supprimer les fichiers de l'application, au risque de corrompre des projets, voire l'application en elle-même. Si des erreurs critiques empêchent complètement l'utilisation de l'application, veuillez le faire remonter via github ( https://github.com/epsilonkn/Saturne-demonstration-app/issues).

Pour démarrer l'application, exécutez le module "main.py". Une fois cela fait, l'interface de projet va s'ouvrir, celle-ci contient un projet exemple montrant de manière rapide ce qui est possible de faire dans l'application. Pour créer un projet, il suffit d'entrer le nom du projet dans l'entrée texte au lancement de la fenêtre des projets, appuyez sur le bouton "Ajouter un projet"

Une fois le projet créé, appuyez sur son bouton correspondant à gauche. Une interface de personnalisation du projet s'ouvre à ce moment.

Le nom du projet est le nom utilisé pour nommer le dossier référence du projet
le nom de l'interface est le nom utilisé pour la fenêtre
la hauteur est celle de la fenêtre créé
la largeur est aussi celle de la fenêtre

"Supprimer" supprime le projet définitivement
"Modifier" enregistre les modifications apportées
"ouvrir" ouvre le projet dans l'interface principale
Ajouter des éléments dans l'interface


Une fois le projet ouvert, l'interface principale s'ouvre. Pour ajouter un élément dans le projet, il suffit de cliquer sur le bouton "Ajouter", puis de sélectionner le widget désiré dans la fenêtre ouverte.

Une fois celui-ci ajouté, il faut appuyer sur son bouton correspondant sur le côté, sous le bouton "Ajouter". La Fenêtre de modification va alors s'ouvrir, permettant les modifications du widget.

Note 1 : Tant qu'un widget n'est pas modifié au moins une fois, il n'est pas ajouté dans le code

Note 2 : Les boutons "Supprimer" et "Modifier" sont liés au widget ouvert, ils permettent respectivement de le supprimer et de le modifier ( attention, toute action est irréversible ! )

Une fois les éléments ajouté, vous pouvez tester votre interface via le bouton "Aperçu", et copier le code via le bouton "Copier" ( la fonction de copie écrase le presse-papier actuel pour le remplacer par le code ).