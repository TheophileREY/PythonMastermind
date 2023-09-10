import random

# Liste des couleurs et leur code (initiale)
couleurs = {
    'R': 'Rouge',
    'V': 'Vert',
    'B': 'Bleu',
    'J': 'Jaune',
    'M': 'Mauve',
    'N': 'Noir'
    }

# Nombre max d'essai avant l'echec du joueur
essai_max = 12

#Nombre de couleur du code secret
nbr_couleur = 5

# Générer le code secret
code_secret = ''
for i in range(nbr_couleur):
    code_secret += random.choice(list(couleurs.keys())) # On choisit un code au hasard dans le dictionnaire des couleurs

# Afficher les regles et les couleurs possibles
print("Bienvenue dans le jeu Mastermind !")
print("Pour consulter les regles completes du jeu : https://fr.wikipedia.org/wiki/Mastermind")
print("Les couleurs possibles sont :")
for code, couleur in couleurs.items():
    print(code + " : " + couleur)

# Initialiser le nombre d'essais effectue par le joueur
essais = 0

while essais < essai_max:
    essais += 1
    print("Essai #" + str(essais) + ": Entrez le code a " + str(nbr_couleur) + " couleurs (Exemple pour 4 : 'RVBJ'):")
    reponse = input().upper() # Pour mettre la reponse en MAJ dans tout les cas

    # Vérifier la validité de la réponse (longueur)
    if len(reponse) != nbr_couleur:
        print("Erreur : Le code entre possede plus de 4 lettres")
        continue

    # Vérifier la validité de la réponse (couleur)
    valide = True
    for c in reponse:
        if c not in couleurs:
            valide = False
            break

    if not valide:
        print("Erreur : Le code entre ne correspond pas aux couleurs proposees")
        continue

    # Vérifier si la réponse est correcte
    correct = 0
    partiel = 0
    for i in range(nbr_couleur):
        if reponse[i] == code_secret[i]:
            correct += 1
        elif reponse[i] in code_secret:
            partiel += 1

    # Afficher le resultat
    print("Correct : " + str(correct) + " | Partiel : " + str(partiel))

    # Vérifier si le joueur a gagne
    if correct == nbr_couleur:
        print("Felicitations, vous avez trouve le code secret !")
        break

# Afficher le score
score = essai_max - essais
print("Votre score est : " + str(score))