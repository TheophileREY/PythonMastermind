import random
import os

# Liste des couleurs et leur code (initiale)
couleurs = {
    'R': 'Rouge',
    'V': 'Vert',
    'B': 'Bleu',
    'J': 'Jaune',
    'M': 'Mauve',
    'N': 'Noir'
}

# Fonction pour initialiser ou charger les statistiques depuis un fichier
def initialiser_statistiques():
    # On initialise les stats à 0
    statistiques = {
        "Nombre de parties": 0,
        "Score total": 0
    }
    if os.path.isfile(".statistiques"): # On met un point devant le fichier pour le cacher à l'utilisateur du prgm
        with open(".statistiques", "r") as fichier:
            lignes = fichier.readlines()
            if len(lignes) == 2:
                statistiques["Nombre de parties"] = int(lignes[0].strip())
                statistiques["Score total"] = int(lignes[1].strip())
    return statistiques

# Fonction pour enregistrer les statistiques dans un fichier
def enregistrer_statistiques(statistiques):
    with open(".statistiques", "w") as fichier: # On ouvre le fichier de statistique cache et on ecrit dedans
        fichier.write(str(statistiques["Nombre de parties"]) + "\n")
        fichier.write(str(statistiques["Score total"]) + "\n")

# Fonction pour jouer une partie
def jouer_partie(couleurs):
    # Nombre max d'essai avant l'echec du joueur
    essai_max = 12

    # Nombre de couleur du code secret
    nbr_couleur = 4

    # Générer le code secret
    code_secret = ''
    for i in range(nbr_couleur):
        code_secret += random.choice(list(couleurs.keys()))  # On choisit un code au hasard dans le dictionnaire des couleurs

    # Initialiser le nombre d'essais effectues par le joueur
    essais = 0

    while essais < essai_max:
        essais += 1
        print("Essai #" + str(essais) + ": Entrez le code à " + str(nbr_couleur) + " couleurs (Exemple pour 4 : 'RVBJ'):")
        reponse = input().upper()  # Pour mettre la reponse en MAJ dans tout les cas

        # Vérifier la validité de la réponse (longueur)
        if len(reponse) != nbr_couleur:
            print("Erreur : Le code entré possède plus de 4 lettres")
            continue

        # Verifier la validité de la reponse (couleur)
        valide = True
        for c in reponse:
            if c not in couleurs:
                valide = False
                break

        if not valide:
            print("Erreur : Le code entré ne correspond pas aux couleurs proposées")
            continue

        # Verifier si la reponse est correcte
        correct = 0
        partiel = 0
        for i in range(nbr_couleur):
            if reponse[i] == code_secret[i]:
                correct += 1
            elif reponse[i] in code_secret:
                partiel += 1

        # Afficher le resultat
        print("Correct : " + str(correct) + " | Partiel : " + str(partiel))

        # Verifier si le joueur a gagne
        if correct == nbr_couleur:
            print("Félicitations, vous avez trouvé le code secret !")
            return essai_max - essais

    # Si le joueur n'a pas trouvé le code secret
    return 0

def main():
    print("Bienvenue dans le jeu Mastermind !")
    statistiques = initialiser_statistiques()

    while True:
        print("\nMenu Principal:")
        print("1. Jouer une partie")
        print("2. Remettre à zéro les statistiques")
        print("3. Quitter")

        choix_menu_principal = input("Choisissez une option (1 OU 2 OU 3): ")

        if choix_menu_principal == "1":
            score_partie = jouer_partie(couleurs)
            statistiques["Nombre de parties"] += 1
            statistiques["Score total"] += score_partie
            enregistrer_statistiques(statistiques)
        elif choix_menu_principal == "2":
            statistiques = {
                "Nombre de parties": 0,
                "Score total": 0
            }
            enregistrer_statistiques(statistiques)
            print("Statistiques remises à zero.")
        elif choix_menu_principal == "3":
            print("Au revoir !")
            break
        else:
            print("Erreur : Choix invalide")

# On lance le jeu
main()