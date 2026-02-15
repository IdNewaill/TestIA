# Importation des Modules
from random import *
from math import *

# Variables de base
mot_ecrit=[]
mot_poids=[]
mot_nombre=0


# [ Options ]
nombre_de_poid_par_mot=15
ponctuation=list(".?!")
taux_apprentissage=0.00001

# Variables à ne pas modifier
liste_poid_vide=[0]*nombre_de_poid_par_mot

def obtenir_poid_de_mot(mot):
    return mot_poids[mot_ecrit.index(mot)]
    
def obtenir_liste_poids_aleatoire():
    return [(mot_nombre*i)%100/100 for i in range(nombre_de_poid_par_mot)]

def modifier_poid_de_mot(mot,valeur):
    mot_poids[mot_ecrit.index(mot)]=valeur
    
def apprendre_phrase(phrase):
    # importation des variables nécessaires
    global mot_ecrit
    global mot_nombre

    #Modification de la phrase pour qu'elle puisse être gérée
    phrase=phrase.lower() 
    phrase=phrase.split(" ")

    # Attribution de token (ici les indices) aux nouveaux mots découverts et mise en 'vecteur' (ici liste) des mots
    phrase_en_token=[]
    for mot in phrase:
        if mot in mot_ecrit:
            phrase_en_token.append(mot_ecrit.index(mot))
        else:
            mot_ecrit.append(mot)
            mot_poids.append(obtenir_liste_poids_aleatoire())
            phrase_en_token.append(mot_nombre)
            mot_nombre+=1
    print(phrase_en_token)

#phrase="Bonjour , je suis une banane"
#apprendre_phrase(phrase)

def obtenir_similarite(p1,p2):
    res=0
    taille=len(p1)
    for index in range(taille):
        if p1[index]>p2[index]:
            res+=p1[index]-p2[index]
        else:
            res+=p2[index]-p1[index]
    return (res/taille)
def obtenir_addition_poids(p1,p2):
    liste_reponse=p1
    for i in range(nombre_de_poid_par_mot):
        p1[i]+=p2[i]
    return liste_reponse

def obtenir_representation_contextuelle(phrase):

    # # #
    # Il s'agit d'une moyenne des poids
    # # #
    
    # Pour faire cette moyenne, dans un premier temps j'additionne tous les poids
    
    liste_poid_moyenne=list(liste_poid_vide)
    nombre_mots=0
    for mot in phrase:
        liste_poid_moyenne=obtenir_addition_poids(liste_poid_moyenne,obtenir_poid_de_mot(mot))
        nombre_mots+=1
    # Maintenant que j'ai additionner tout les poids, je vais diviser cette somme de poids par le nombre de mots que j'ai lu

    nouvelle_liste_poids=[]
    for poid in liste_poid_moyenne:
        nouvelle_liste_poids.append(poid/nombre_mots)

    return list(nouvelle_liste_poids)

def obtenir_nouveau_poid(poids,probabilite):

    # Petits calculs permettant de recalculer les poids selon une probabilité
    
    nouvelle_liste_poids=[]
    for poid in poids:
        a=poid-(taux_apprentissage*probabilite)
        if a>0:
            nouvelle_liste_poids.append(poid-(taux_apprentissage*probabilite))
        else:
            nouvelle_liste_poids.append(poid+(taux_apprentissage*probabilite))
        
    return nouvelle_liste_poids

def actualiser_les_poids_sachant_erreur(mot_correct_ecrit,mot_incorrect_ecrit,mot_correct_poids,mot_incorrect_poids,mot_correct_proba,mot_incorrect_proba):

    # # #
    # Permet de modifier les poids selon la faute qui viens d'être faite
    # # #

    global mot_poids
    
    # Calculer les différences entre le bon et le mauvais poid
    diff_mot_correct=1-mot_correct_proba
    diff_mot_incorrect=mot_incorrect_proba

    # Calculer leur poid selon le Gradient (calculs aux dessus)    
    resultat_changements_mot_correct = obtenir_nouveau_poid(mot_correct_poids,diff_mot_correct)
    resultat_changements_mot_incorrect = obtenir_nouveau_poid(mot_incorrect_poids,diff_mot_incorrect)

    # Se souvenir du changement des poids
    modifier_poid_de_mot(mot_correct_ecrit,resultat_changements_mot_correct)
    modifier_poid_de_mot(mot_incorrect_ecrit,resultat_changements_mot_incorrect)

def actualiser_les_poids_du_mot_correct_seulement_sachant_erreur(mot_correct_ecrit,poid_mot_correct,mot_correct_proba):

    # # #
    # Permet de modifier les poids selon la faute qui viens d'être faite
    # # #

    global mot_poids
    
    # Calculer les différences entre le bon et le mauvais poid
    diff_mot_correct=1-poid_mot_correct

    # Calculer leur poid selon le Gradient (calculs aux dessus)    
    resultat_changements_mot_correct = obtenir_nouveau_poid(poid_mot_correct,diff_mot_correct)

    # Se souvenir du changement des poids
    modifier_poid_de_mot(mot_correct_ecrit,resultat_changements_mot_correct)

def obtenir_deduction_mot_manquant_dans_phrase(phrase_en_liste,representation_contextuelle=None):

    # On défini les poids du contexte de la phrase ( à moins que celle-ci sois déjà définie en arguments
    if representation_contextuelle is None:
        representation_contextuelle = obtenir_representation_contextuelle(phrase_en_liste)

    
    # On va utiliser notre fonction similitude() sur tous les mots puis vérifier lequel se rapproche la plus de =1
    # Ainsi que trouver quel poid est le plus proche de ce qui est recherché

    #   on défini d'abord quelques variables
    
    mot_le_plus_proche = ""
    proba_du_mot_le_plus_proche = 0

    #   puis on se lance à la recherche du mot qui à un résultat qui se rapproche le plus de 1
    #   lors de l'utilisation de la fonction obtenir_similarite entre le contexte de la phrase et tous les mots que je connais un par un
    
    for mot in mot_ecrit:
        proba_du_mot = obtenir_probabilite_de_mot_dans_representation_contextuelle(representation_contextuelle,mot)
        if proba_du_mot>proba_du_mot_le_plus_proche:
            mot_le_plus_proche = mot
            proba_du_mot_le_plus_proche = proba_du_mot
            
    return [mot_le_plus_proche,proba_du_mot_le_plus_proche]


def obtenir_probabilite_de_mot_dans_representation_contextuelle(representation_contextuelle,mot):
    return obtenir_similarite( list(representation_contextuelle) , obtenir_poid_de_mot(mot) )

    
def entrainement_sur_une_phrase(phrase_en_liste,mot_correct):

    # Etablir le contexte par l'établissement des poids
    representation_contextuelle = obtenir_representation_contextuelle(phrase_en_liste)
    
    # Répéter jusqu'à ce que le modèle aura appris de ses erreurs de trouver quel mot va combler la phrase

    deduction_bonne = None

    essai=0
    print("Début de l'entrainement pour le mot '",mot_correct,"' dans la phrase",phrase_en_liste)
    while not(deduction_bonne):

        
        essai+=1
        
        # demander quel mot correspondrais à la phrase dans cette representation_contextuelle

        mot_deduit , proba_que_le_model_pense_quil_a_raison = obtenir_deduction_mot_manquant_dans_phrase(phrase_en_liste,representation_contextuelle)

        # vérifier si le mot déduit est bien le mot trouvé

        
        if mot_deduit==mot_correct:
            # C'est bien le bon mot ! On peut quitter cette boucle d'apprentissage
            reelle_proba = obtenir_probabilite_de_mot_dans_representation_contextuelle( representation_contextuelle , mot_correct )
            deduction_bonne = True
            print("Mot trouvé !",essai,"ont été réalisés .")
            print("Amélioration de la connaissance")
            essai=0
            while reelle_proba<0.99 and essai<10000:
                reelle_proba = obtenir_probabilite_de_mot_dans_representation_contextuelle( representation_contextuelle , mot_correct )
                actualiser_les_poids_sachant_erreur( mot_correct , mot_deduit , obtenir_poid_de_mot(mot_correct) , obtenir_poid_de_mot(mot_deduit) , reelle_proba , proba_que_le_model_pense_quil_a_raison )
                mot_deduit , proba_que_le_model_pense_quil_a_raison = obtenir_deduction_mot_manquant_dans_phrase(phrase_en_liste,representation_contextuelle)
                essai+=1
            if essai>99999:
                print('Abandon')
            else:
                print("Amélioration terminée")
        else:

            # Calculer la proba qu'il a déduit pour le mot correct
            reelle_proba = obtenir_probabilite_de_mot_dans_representation_contextuelle( representation_contextuelle , mot_correct )

            # Lui faire comprendre ce qui est faut pour s'approcher petit à petit de la déduction correcte du mot attendu
            actualiser_les_poids_sachant_erreur( mot_correct , mot_deduit , obtenir_poid_de_mot(mot_correct) , obtenir_poid_de_mot(mot_deduit) , reelle_proba , proba_que_le_model_pense_quil_a_raison )
        if essai>99999:
            print("Abandon")
            break
    print("Mot trouvé !",essai,"ont été réalisés .")     

def apprentissage_de_plusieurs_phrases(texte_en_liste):
    for phrase in texte_en_liste:
        apprendre_phrase(phrase)
    print("Lecture terminée !")

def entrainement_en_masse(liste_phrases):
    for phrase in liste_phrases+liste_phrases[::-1]:
        nouvelle_phrase=phrase.lower().split(" ")
        for index_mot in range(len(nouvelle_phrase)):
            phrase_de_test=nouvelle_phrase[:]
            mot_correct=phrase_de_test.pop(index_mot)

            entrainement_sur_une_phrase(phrase_de_test,mot_correct)
def printall():
    for index_mot in range(len(mot_ecrit)):
        print(mot_ecrit[index_mot],mot_poids[index_mot])

def poser_question(phrase_normale):
    phrase=phrase_normale.lower() 
    nouvelle_phrase=phrase.split(" ")
    nouvelle_phrase.append("<start>")
    reponse=[]
    while True:
        dernier_mot=obtenir_deduction_mot_manquant_dans_phrase(nouvelle_phrase,representation_contextuelle=None)
        print(dernier_mot)
        dernier_mot=dernier_mot[0]
        if dernier_mot=="<end>":
            break
        else:
            nouvelle_phrase.append(dernier_mot)
            reponse.append(dernier_mot)
    print(reponse)
    return " ".join(reponse)
#####################################################################################

    # DEBUT DES TESTS
    #   Partie connaissance des mots
#####################################################################################

texte_en_liste = [
    "que fais le chat <start> le chat dort <end>",
    "que fais le chien <start> le chien abboie <end>"
                 ]

apprentissage_de_plusieurs_phrases(texte_en_liste)


#####################################################################################

    # DEBUT DES TESTS
    #   Partie entrainement
#####################################################################################

#phrase_teste = ["chat","dort"]
#mot_correct = "le"

#entrainement_sur_une_phrase(phrase_teste,mot_correct)


entrainement_en_masse(texte_en_liste)


print("Dans la phrase [le,chat] le mot prédit est",obtenir_deduction_mot_manquant_dans_phrase(["le","chat"],representation_contextuelle=None))
print("Dans la phrase [le,chien] le mot prédit est",obtenir_deduction_mot_manquant_dans_phrase(["le","chien"],representation_contextuelle=None))
print("Dans la phrase [chien,abboie] le mot prédit est",obtenir_deduction_mot_manquant_dans_phrase(["chien","abboie"],representation_contextuelle=None))
