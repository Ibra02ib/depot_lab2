# Gestionnaire de tickets UQAC — Laboratoire 2 (6GEI311)

Cours : 6GEI311 — Architecture des logiciels, UQAC, automne 2026
Équipe : Djan Ibrahim Doumbia: DOUD23110200 , Ouedraogo Fayçal Franck wend lassida:OUEF30050300


Ce dépôt contient un outil de gestion de tickets en ligne de commande, écrit en Python. La partie 1 implémente le diagramme de classes fourni par l'énoncé. La partie 2 implémente notre diagramme amélioré, qui permet de décrire un ticket avec du texte, des images ou des vidéos.

Le rapport détaillé (critique du diagramme initial, justification des changements, leçons apprises) se trouve dans `Rapport_Lab2_6GEI311.docx`.

# Table des matières

1. Structure du dépôt
2. Résultats : fonctionnalités implémentées
3. Diagrammes UML
4. Démonstration
5. Ce que nous avons appris

## Structure du dépôt

```
.
├── README.md
├── Rapport_Lab2_6GEI311.docx
├── docs/
│   ├── diagramme_partie1.png    # diagramme fourni par l'énoncé
│   └── diagramme_partie2.png    # notre diagramme amélioré
├── partie1/                     # implémentation du diagramme initial
│   ├── main.py
│   ├── user.py
│   ├── admin.py
│   └── ticket.py
└── partie2/                     # implémentation du diagramme amélioré
    ├── main.py
    ├── user.py
    ├── developer.py
    ├── ticket.py
    └── piece_jointe.py
```

# Partie 1

Un seul menu donne accès à toutes les actions. On crée d'abord au moins un utilisateur (option 1) et un admin (option 2), puis des tickets (option 3).

 Option/Action 

1  Créer un utilisateur (nom, courriel, rôle) 
2 Créer un admin (nom, courriel) 
3  Créer un ticket : on choisit d'abord l'utilisateur créateur, puis on saisit titre, description et priorité 
4  Afficher un ticket (description et commentaires) 
5  Mettre à jour le titre, la description ou la priorité (laisser vide pour ne pas changer) 
6  Ajouter un commentaire 
7  Assigner un ticket à un utilisateur (par un admin) 
8  Mettre un ticket en validation 
9  Terminer un ticket 
10  Fermer un ticket (par un admin, seulement s'il est OUVERT) 
11  Afficher tous les tickets (par un admin) 
12  Quitter 

# Partie 2

Le programme commence par une connexion. On choisit son type de compte (utilisateur ou développeur), puis on se connecte à un compte existant ou on en crée un. Chaque type de compte a son propre menu.

Menu utilisateur : un utilisateur n'a accès qu'aux tickets qu'il a lui-même créés.

 Option  Action 
  
 1  Créer un ticket (titre, priorité) 
 2  Ajouter du contenu à un de ses tickets : texte, image ou vidéo, en donnant le chemin du fichier 
 3  Afficher un de ses tickets (le contenu est chargé selon son type, puis les commentaires) 
 4  Mettre à jour le titre ou la priorité 
 5  Ajouter un commentaire 
 6  Se déconnecter 

Menu développeur : un développeur a accès à tous les tickets, et peut faire en plus tout ce qu'un utilisateur fait.

 Option  Action 

 1 à 5  Mêmes actions que l'utilisateur, sur n'importe quel ticket 
 6  Assigner un ticket à un développeur 
 7  Mettre un ticket en validation 
 8  Terminer un ticket 
 9  Fermer un ticket (seulement s'il est OUVERT) 
 10  Afficher tous les tickets 
 11  Se déconnecter 



# Cycle de vie d'un ticket

Dans les deux parties, les changements de statut sont contrôlés. Une transition non permise est refusée avec le message `Transition refusée : X -> Y`, et le statut ne change pas.

 Statut actuel  Statuts suivants permis  Remarque 

 OUVERT  ASSIGNE, FERME  statut de départ de tout ticket 
 ASSIGNE  VALIDATION, ASSIGNE  ASSIGNE → ASSIGNE : réassignation 
 VALIDATION  TERMINE, ASSIGNE  retour à ASSIGNE si la validation échoue 
 TERMINE  aucun  état final : ticket résolu 
 FERME  aucun  état final : ticket écarté sans résolution 

La fermeture n'est possible que depuis OUVERT : elle sert à écarter un ticket non pertinent (problème propre à l'utilisateur, ou non prioritaire) avant qu'il soit pris en charge. Un ticket déjà assigné doit donc aller au bout du cycle.

## Résultats : fonctionnalités implémentées

# Partie 1 — implémentation du diagramme initial

- Les trois classes du diagramme (`User`, `Admin`, `Ticket`) avec tous leurs attributs et méthodes.
- Association `creates` réalisée dans les deux sens : `User.created_tickets` et `Ticket.creator`.
- Association `assigns` réalisée par `Admin.assignTicket()`, qui délègue à `Ticket.assignTo()`. La personne assignée est conservée dans `Ticket.assignedTo`.
- Association `closes` réalisée par `Admin.closeTicket()`.
- `viewAllTickets()` retourne la liste de tous les tickets créés.
- Identifiants uniques générés automatiquement par un compteur de classe.
- Dates de création et de dernière modification mises à jour à chaque changement.
- Contrôle des transitions de statut (voir le tableau ci-dessus).
- Un ticket ne peut pas être créé sans créateur : le créateur est choisi avant la construction du ticket.

# Partie 2 — implémentation du diagramme amélioré

- `Developer` hérite de `User` et ajoute l'assignation, la fermeture et la consultation de tous les tickets. Un compteur d'identifiants unique est partagé : un utilisateur et un développeur ne peuvent pas avoir le même ID.
- La description d'un ticket est une liste de pièces jointes (`Ticket.pieces_jointes`), ajoutées par `Ticket.ajouterContenu()`.
- Classe abstraite `PieceJointe` (module `abc`) avec trois sous-classes, dont chacune se charge différemment :
  - `TextePieceJointe` lit et affiche le contenu du fichier ;
  - `ImagePieceJointe` vérifie l'existence du fichier et affiche sa taille ;
  - `VideoPieceJointe` vérifie l'existence du fichier et le présente comme une référence à lire.
- Chaque pièce jointe fournit `exporterPDF()`, qui produit le contenu destiné au PDF. Une vidéo ne pouvant pas être intégrée dans un PDF, son export contient une référence vers le chemin du fichier.
- `PieceJointe` ne peut pas être instanciée directement (Python lève une `TypeError`).
- Connexion par type de compte et deux menus distincts : les actions réservées à l'équipe n'apparaissent pas dans le menu utilisateur.
- Contrôle d'accès : un utilisateur ne peut choisir que parmi ses propres tickets ; un développeur choisit parmi tous les tickets.
- Même contrôle des transitions de statut que la partie 1.

## Diagrammes UML

# Partie 1 — diagramme fourni par l'énoncé

Diagramme de classes de la partie 1 (docs/diagramme_partie1.png)

Écart assumé avec ce diagramme : `assignTo()` et `updateStatus()` retournent un booléen plutôt que `void`, afin que l'interface ne confirme une action que si la transition de statut est permise.

# Partie 2 — diagramme amélioré

Diagramme de classes de la partie 2 (docs/diagramme_partie2.png)

Principaux changements par rapport au diagramme initial :

- `Admin` est renommé `Developer`, le terme employé par l'énoncé, et hérite de `User`.
- L'association `assignedTo` (Ticket 0..* → User 0..1) est ajoutée ; l'association `views` est retirée.
- L'attribut `description: String` est remplacé par une composition `Ticket ◆— PieceJointe`, avec une classe abstraite et trois sous-classes.
- `Ticket` reçoit la table statique `TRANSITIONS` et la méthode `ajouterContenu()`.

La justification de chaque changement se trouve dans la Section II du rapport.

## Démonstration

Les sessions ci-dessous ont été produites en exécutant le programme. Pour la lisibilité, les menus affichés entre chaque action ont été retirés ; seuls les choix saisis et les réponses du programme sont conservés.

# Partie 1 — cycle de vie complet et transitions refusées

Scénario : création d'un utilisateur, d'un admin et d'un ticket ; ajout d'un commentaire ; tentative de terminer le ticket trop tôt (refusée deux fois) ; assignation, validation, puis terminaison.

```
Ton choix : 1
Nom : Bob
Email : bob@uqac.ca
Rôle : Étudiant
Utilisateur créé avec succès.
Ton choix : 2
Nom : Alice
Email : alice@uqac.ca
Admin créé avec succès.
Ton choix : 3
Qui crée ce ticket ?
Choisis un utilisateur :
1. Bob (ID: 1, Étudiant)
Ton choix : 1
Titre : Bug connexion
Description : Le bouton ne répond pas
Priorité : Haute
Ticket créé avec succès.
Ton choix : 6
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Commentaire : Bloquant pour les examens
Commentaire ajouté.
Ton choix : 9
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Transition refusée : OUVERT -> TERMINE
Ton choix : 7
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Choisis un admin :
1. Alice (ID: 1, alice@uqac.ca)
Ton choix : 1
À qui assigner ce ticket ?
Choisis un utilisateur :
1. Bob (ID: 1, Étudiant)
Ton choix : 1
Ticket #1 assigné à Bob
Ton choix : 9
Choisis un ticket :
1. Bug connexion (ID: 1, ASSIGNE)
Ton choix : 1
Transition refusée : ASSIGNE -> TERMINE
Ton choix : 8
Choisis un ticket :
1. Bug connexion (ID: 1, ASSIGNE)
Ton choix : 1
Ticket mis en validation.
Ton choix : 9
Choisis un ticket :
1. Bug connexion (ID: 1, VALIDATION)
Ton choix : 1
Ticket terminé.
Ton choix : 4
Choisis un ticket :
1. Bug connexion (ID: 1, TERMINE)
Ton choix : 1
Qui consulte ce ticket ?
Choisis un utilisateur :
1. Bob (ID: 1, Étudiant)
Ton choix : 1
Ticket #1 - Bug connexion
Statut: TERMINE  Priorité: Haute
Description: Le bouton ne répond pas
Commentaires :
  - Bloquant pour les examens
Ton choix : 11
Choisis un admin :
1. Alice (ID: 1, alice@uqac.ca)
Ton choix : 1
       Tous les tickets 
#1 - Bug connexion - Statut: TERMINE
Ton choix : 12
Au revoir.
```

# Partie 2 — pièces jointes, rôles et transitions

Scénario : un utilisateur crée un ticket et y ajoute un texte et une image (le fichier image n'existe pas, ce qui montre que chaque type gère son chargement) ; un développeur voit tous les tickets, assigne le ticket, le fait passer par la validation, puis tente de fermer un ticket terminé (refusé) et ferme un ticket encore ouvert.

```
Ton choix : 1        (je suis un utilisateur)
Ton choix : 2        (créer un nouveau compte)
Nom : Bob
Email : bob@uqac.ca
Rôle : Étudiant
Utilisateur créé avec succès.
Ton choix : 1
Titre : Bug connexion
Priorité : Haute
Ticket créé avec succès.
Ton choix : 2
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Type de contenu : 1. Texte  2. Image  3. Vidéo
Ton choix : 1
Chemin du fichier : description.txt
Contenu ajouté au ticket.
Ton choix : 2
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Type de contenu : 1. Texte  2. Image  3. Vidéo
Ton choix : 2
Chemin du fichier : capture.png
Contenu ajouté au ticket.
Ton choix : 3
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
Ticket #1 - Bug connexion
Statut: OUVERT  Priorité: Haute
Contenu :
[Texte] Le bouton de connexion du portail ne répond pas.
[Image] Fichier introuvable : capture.png
Ton choix : 6
À bientôt, Bob.
Ton choix : 2        (je suis un développeur)
Ton choix : 2        (créer un nouveau compte)
Nom : Ana
Email : ana@uqac.ca
Développeur créé avec succès.
Ton choix : 10
=== Tous les tickets ===
#1 - Bug connexion - Statut: OUVERT
Ton choix : 6
Choisis un ticket :
1. Bug connexion (ID: 1, OUVERT)
Ton choix : 1
À quel développeur assigner ce ticket ?
Choisis un développeur :
1. Ana (ID: 2, Développeur)
Ton choix : 1
Ticket #1 assigné à Ana
Ton choix : 8
Choisis un ticket :
1. Bug connexion (ID: 1, ASSIGNE)
Ton choix : 1
Transition refusée : ASSIGNE -> TERMINE
Ton choix : 7
Choisis un ticket :
1. Bug connexion (ID: 1, ASSIGNE)
Ton choix : 1
Ticket mis en validation.
Ton choix : 8
Choisis un ticket :
1. Bug connexion (ID: 1, VALIDATION)
Ton choix : 1
Ticket terminé.
Ton choix : 1
Titre : Ticket test
Priorité : Basse
Ticket créé avec succès.
Ton choix : 9
Choisis un ticket :
1. Bug connexion (ID: 1, TERMINE)
2. Ticket test (ID: 2, OUVERT)
Ton choix : 1
Transition refusée : TERMINE -> FERME
Ton choix : 9
Choisis un ticket :
1. Bug connexion (ID: 1, TERMINE)
2. Ticket test (ID: 2, OUVERT)
Ton choix : 2
Ticket #2 fermé.
Ton choix : 10
=== Tous les tickets ===
#1 - Bug connexion - Statut: TERMINE
#2 - Ticket test - Statut: FERME
Ton choix : 11
À bientôt, Ana.
Ton choix : 3
Au revoir.
```

## Ce que nous avons appris

Un diagramme correct peut être infidèle à son domaine. Rien n'était syntaxiquement faux dans la classe `Admin`, mais l'énoncé ne parle jamais d'administrateur : il parle de développeurs et d'équipe de développement. Relire le texte de l'énoncé avant le diagramme nous a évité de conserver un acteur inventé.

Le sens d'un héritage se démontre. Le principe de substitution de Liskov nous a donné un critère objectif : un développeur peut faire tout ce que fait un utilisateur, l'inverse est faux. `Developer` hérite donc de `User`, et non l'inverse.

Toute interaction n'est pas une association. La question « reste-t-il un lien après l'opération ? » distingue `views` (non, c'est une simple consultation) de `assignedTo` (oui, le ticket garde la personne assignée).

La modificabilité se joue aux points de variation. En plaçant l'abstraction sur les types de contenu, un futur `AudioPieceJointe` s'ajouterait sans toucher à `Ticket`, à `User` ni au menu de consultation. De même, toutes les règles de transition sont rassemblées dans une seule table.

Le comportement fait partie de la conception. Un `status: String` libre acceptait n'importe quelle valeur, et notre première version laissait passer un ticket directement de OUVERT à TERMINÉ. Nous avons aussi comparé deux façons de contrôler les transitions : une table de transitions et le patron État. Nous avons retenu la table, parce que seule la liste des statuts suivants varie d'un état à l'autre, pas le comportement.

Les principes GRASP donnent un vocabulaire pour justifier. Expert en information, Créateur, Contrôleur et Variation protégée nous ont permis d'expliquer des choix qui auraient autrement semblé relever du goût personnel.

L'exécution révèle ce que le diagramme cache. Le problème de contrôle d'accès, le ticket créé sans créateur et les commentaires jamais affichés ne sont apparus qu'en utilisant réellement le programme.
