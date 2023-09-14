import random
import os
import itertools


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
# Nombre de couleur du code secret
nbr_couleur = 4

# Pour initialiser ou charger les statistiques depuis un fichier
def initialiser_statistiques():
    # On initialise les stats a 0
    statistiques = {
        "Nombre de parties": 0,
        "Score total": 0
    }
    if os.path.isfile(".statistiques"): # On met un point devant le fichier pour le cacher a l'utilisateur du prgm
        with open(".statistiques", "r") as fichier:
            lignes = fichier.readlines()
            if len(lignes) == 2:
                statistiques["Nombre de parties"] = int(lignes[0].strip())
                statistiques["Score total"] = int(lignes[1].strip())
    return statistiques


# Pour enregistrer les statistiques dans un fichier
def enregistrer_statistiques(statistiques):
    with open(".statistiques", "w") as fichier: # On ouvre le fichier de statistique cache et on ecrit dedans
        fichier.write(str(statistiques["Nombre de parties"]) + "\n")
        fichier.write(str(statistiques["Score total"]) + "\n")


# Pour verifier les biens places et les mal places
def verification(code_secret, reponse):
    correct = 0 # correct correspond au nbr de couleur correct et bien placee
    partiel = 0 # partiel correspond au nbr de couleur correct mais mal placee
    temp = list(reponse)
    for i in range(len(code_secret)):
        if temp[i] == code_secret[i]:
            correct += 1
            temp[i] = '.'  # On met un point pour ne pas compter deux fois une couleur

    for i in range(len(code_secret)):
        if temp[i] in code_secret:
            partiel += 1
            temp[i] = '.'  # On met un point pour ne pas compter deux fois une couleur

    return {'correct': correct, 'partiel': partiel}


# Pour jouer une partie (deviner le code avec les indications)
def jouer_partie(couleurs):
    # Generer le code secret
    code_secret = ''
    for i in range(nbr_couleur):
        code_secret += random.choice(
            list(couleurs.keys()))  # On choisit un code au hasard dans le dictionnaire des couleurs
    # Initialiser le nombre d'essais effectues par le joueur
    essais = 0
    while essais < essai_max:
        essais += 1
        print("Essai #" + str(essais) + ": Entrez le code a " + str(nbr_couleur) + " couleurs (Exemple pour 4 : 'RVBJ'):")
        reponse = input().upper()  # Pour mettre la reponse en MAJ dans tous les cas
        # Verifier la validite de la reponse (longueur)
        if len(reponse) != nbr_couleur:
            print("Erreur : Le code entre ne possede pas " + str(nbr_couleur) + " lettres")
            continue
        # Verifier la validite de la reponse (couleur)
        valide = True
        for c in reponse:
            if c not in couleurs:
                valide = False
                break
        if not valide:
            print("Erreur : Le code entre ne correspond pas aux couleurs proposees")
            continue
        # Verifier si la reponse est correcte en utilisant la fonction de verification
        resultat = verification(code_secret, reponse)
        # Afficher le resultat
        print(f"Correct : {resultat['correct']} | Partiel : {resultat['partiel']}")
        # Verifier si le joueur a gagne
        if resultat['correct'] == nbr_couleur:
            print("Felicitations, vous avez trouve le code secret !")
            return essai_max - essais
    # Si le joueur n'a pas trouve le code secret
    return 0


# Pour resoudre le jeu avec l'ordinateur
def resolution_mastermind():
    essai_ia = 0
    combinaison_secrete = input("Entrez la combinaison secrete a " + str(nbr_couleur) + " couleurs a resoudre (Exemple pour 4 : 'RVBJ'): ").upper()
    combinaison_possible = generer_toutes()
    while essai_ia < essai_max:
        # Proposition de combinaison basee sur les combinaisons possibles restantes
        proposition = random.choice(combinaison_possible)
        # Evaluation
        resultat = verification(combinaison_secrete, proposition)
        correct, partiel = resultat['correct'], resultat['partiel']
        print("Essai #" +str(essai_ia + 1) +  ": " + str(proposition) + "    Correctes: " + str(correct) + ", Partiel: "+ str(partiel))
        # Verifier si la combinaison secrete a ete trouvee
        if correct == nbr_couleur:
            print("Combinaison secrete trouvee : " + str(proposition))
            return proposition
        # Mise a jour des combinaisons possibles
        combinaison_possible = maj_combinaison(combinaison_possible, proposition, correct, partiel)
        essai_ia += 1
    print("Limite d'essais atteinte. La combinaison secrete n'a pas ete trouvee.")
    return None


# Pour mettre a jour les combinaisons possibles
def maj_combinaison(combinaison_possible, proposition, correct, partiel):
    # Liste vide pour stocker les combinaisons mises a jour
    combinaison_maj = []
    # Parcourt chaque combinaison dans la liste des combinaisons possibles
    for combination in combinaison_possible:
        # Evalue la proposition actuelle par rapport a la combinaison en cours
        resultat_verification = verification(combination, proposition)
        # Verifie si le nombre de couleurs correctes et le nombre de positions correctes correspondent
        if resultat_verification['correct'] == correct and resultat_verification['partiel'] == partiel:
            # Si les indices correspondent : ajoute cette combinaison a la liste des combinaisons mises a jour
            combinaison_maj.append(combination)
    # Renvoie la liste mise a jour des combinaisons possibles
    return combinaison_maj


# Pour generer toute les combinaisons possibles
def generer_toutes():
    return [''.join(combinaison) for combinaison in itertools.product(couleurs.keys(), repeat=nbr_couleur)]


def main():
    print("Bienvenue dans le jeu Mastermind !")
    print ("Couleur disponible :")
    print(couleurs)
    statistiques = initialiser_statistiques()

    while True:
        print("\nMenu Principal:")
        print("1. Jouer une partie")
        print("2. Resolution par IA")
        print("3. Remettre a zero les statistiques")
        print("4. Quitter")

        choix_menu_principal = input("Choisissez une option (1 OU 2 OU 3 OU 4): ")

        if choix_menu_principal == "1":
            score_partie = jouer_partie(couleurs)
            statistiques["Nombre de parties"] += 1
            statistiques["Score total"] += score_partie
            enregistrer_statistiques(statistiques)
        elif choix_menu_principal == "2":
            resolution_mastermind()
        elif choix_menu_principal == "3":
            statistiques = {
                "Nombre de parties": 0,
                "Score total": 0
            }
            enregistrer_statistiques(statistiques)
            print("Statistiques remises a zero.")
        elif choix_menu_principal == "4":
            print("Au revoir !")
            break
        else:
            print("Erreur : Choix invalide")

# On lance le jeu
main()