import time

dico_emotions={"heureux":0,"triste":0,"mechant":0,"jaloux":0,"perdu":0}
dico_mots_possibles_par_suite={}
dico_emotions_des_mots={}

diff_symbol='ttt'

def ajouter_dico_mots_possible_par_suite(mot_d,mot_f):
    global dico_mots_possibles_par_suite
    if mot_d in list(dico_mots_possibles_par_suite.keys()):
        if not mot_f in dico_mots_possibles_par_suite:
            dico_mots_possibles_par_suite[mot_d].append(mot_f)
    else:
        dico_mots_possibles_par_suite[mot_d]=[mot_f]
        
def ajouter_dico_emotions_des_mots(phrase,dico_emo):
    global dico_emotions_des_mots
    for mot in phrase:
        if mot in list(dico_emotions_des_mots.keys()):
            dico_emotions_des_mots[mot]=moy_entre_deux_dicos_emotions(dico_emotions_des_mots[mot],dico_emo,dico_emotions_des_mots[mot][diff_symbol])
        else:
            dico_emotions_des_mots[mot]=dico_emo|{diff_symbol:1}
def get_only_different_words_from_text(text):
    text=text.split(" ")
    liste_words=[]
    last_word=""
    for word in text:
        if not last_word=="":
            ajouter_dico_mots_possible_par_suite(last_word,word)
        last_word=word
        if not word in liste_words:
            liste_words.append(word)
    return liste_words

def mot_en_commun_entre_phr1_et_phr2(phrase1,phrase2):
    liste_reponse=[]
    for word in phrase1:
        if word in phrase2:
            liste_reponse.append(word)
    return liste_reponse


def moy_entre_deux_dicos_emotions(dico_emo1,dico_emo2,poids_de_emo1=1):
    dico_reponse={}
    for emotion in list(dico_emo1.keys()):
        if emotion!=diff_symbol:
            if not emotion in list(dico_emo1.keys()):
                dico_emo1[emotion]=0
            if not emotion in list(dico_emo2.keys()):
                dico_emo2[emotion]=0
            test=int((dico_emo1[emotion]*(1+(1-(100/poids_de_emo1/100)))+dico_emo2[emotion]*(100/poids_de_emo1/100))/2)
            #print(test)
            if test>0:
                dico_reponse[emotion]=test

    return dico_reponse|{diff_symbol:poids_de_emo1+1}

def comparaison_pour_deduire_mot_qui_vaut_emotion(phrase1,dico_emo1,phrase2,dico_emo2):
    phrase1=get_only_different_words_from_text(phrase1)
    phrase2=get_only_different_words_from_text(phrase2)
    res=[mot_en_commun_entre_phr1_et_phr2(phrase1,phrase2),moy_entre_deux_dicos_emotions(dico_emo1,dico_emo2)]
    ajouter_dico_emotions_des_mots(res[0],res[1])
    return res

def entrainer_model(liste_phrases_emotions):
    for a in liste_phrases_emotions:
        for b in liste_phrases_emotions:
            if a!=b:
                comparaison_pour_deduire_mot_qui_vaut_emotion(a[0],a[1],b[0],a[1])

def pourcentage_ressemblance_avec_dico_actuel(dico_emo1,dico_emo2):
    global dico_emotions
    total=0
    for emotion in list(dico_emotions.keys()):
        if not emotion in dico_emo1:
            dico_emo1[emotion]=0
        if not emotion in dico_emo2:
            dico_emo2[emotion]=0
        if dico_emo1[emotion]>dico_emo2[emotion]:
            total+=dico_emo1[emotion]-dico_emo2[emotion]
        else:
            total+=dico_emo2[emotion]-dico_emo1[emotion]
    return total/len(dico_emotions)

def get_dico_emotions_du_mot(mot):
    if mot in list(dico_emotions_des_mots.keys()):
        return dico_emotions_des_mots[mot]
    else:
        return {"heureux":0,"triste":0,"mechant":0,"jaloux":0,"perdu":0,diff_symbol:1}
def mot_qui_ressemble_le_plus_au_dico_emo(mot_ici,dico_emo):
    global dico_mots_possibles_par_suite
    global dico_emotions_des_mots
    #Déterminer les différences entre les émotions des mots et les émotions du dico en argument
    #Et déterminer celui qui a la différence la plus petite avec le dico en argument
    mot_min=["",1000]
    a=dico_mots_possibles_par_suite[mot_ici]
    if len(a)==0:
        return "."
    for mot in a:
        pourcentage=pourcentage_ressemblance_avec_dico_actuel(dico_emo,get_dico_emotions_du_mot(mot))
        if pourcentage<mot_min[1]:
            mot_min=[mot,pourcentage]
    return mot_min[0]

def faire_une_phrase_qui_se_rapproche_de_emotions(mot_debut,dico_emo):
    global dico_emotions_des_mots
    reponse=[mot_debut]
    c=dict(dico_emo)
    word=mot_debut
    actual_dico_emo=None
    while word not in [".","...","..",":","!","?",";"]:
        print(actual_dico_emo)
        word=mot_qui_ressemble_le_plus_au_dico_emo(word,dico_emo if actual_dico_emo is None else actual_dico_emo)
        if actual_dico_emo is None:
            actual_dico_emo=get_dico_emotions_du_mot(word)
        else:
            actual_dico_emo=moy_entre_deux_dicos_emotions(actual_dico_emo,get_dico_emotions_du_mot(word))
        reponse.append(word)
    print(actual_dico_emo,c)
    return reponse


liste_phrases_emotions=[
    ["Salut je suis content .", {"heureux": 50, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Tellement content que j'ai envie de sourire à tout le monde .", {"heureux": 60, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est vraiment une sensation incroyable .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens léger comme si tout allait parfaitement bien .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Comme si le monde entier était aligné pour me faire plaisir aujourd'hui .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque détail semble contribuer à ma joie intérieure .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Ça me donne envie de profiter de cette belle journée .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Honnêtement, être heureux comme ça ne se produit pas tout le temps .", {"heureux": 60, "triste": 10, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est une chance qu'il faut saisir .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'ai cette conviction que je peux partager cette joie avec les autres .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Comme une énergie positive qui se transmet naturellement .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Cela renforce encore plus cette sensation .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je pense que je suis content .", {"heureux": 30, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Mais pas seulement content, je dirais presque euphorique .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Ce bonheur est sincère, profond et peut-être un peu inexplicable .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Ce n'est pas grave, parfois on n'a pas besoin de tout comprendre .", {"heureux": 60, "triste": 10, "mechant": 0, "jaloux": 0, "perdu": 5}],
    ["Pour apprécier pleinement ce qu'on ressent .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Cela me rappelle que la vie est faite de ces moments précieux .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Qui semblent simples mais sont en réalité très significatifs .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je prends conscience que cette émotion est rare et précieuse .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Quelque chose qu'il faut cultiver et apprécier sans retenue .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Même si je ne suis pas toujours capable d'exprimer cela avec des mots .", {"heureux": 50, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 15}],
    ["Dans ces instants, je me connecte avec une partie de moi-même .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["Qui est libre, insouciante et pleine d'espoir .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Ce qui est assez extraordinaire .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Car je ne me souviens pas de la dernière fois où j'ai ressenti cela .", {"heureux": 60, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["C'est exactement ce que je ressens en ce moment .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Et ça me donne une énergie incroyable .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Presque comme si j'avais des ailes .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Car c'est une chose d'être content, mais c'en est une autre de le réaliser vraiment .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Cela transforme tout .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Comme si chaque pensée devenait plus légère .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Et chaque problème devenait moins important .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Plus j'y pense, plus je veux prolonger cet état d'esprit .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 5}],
    ["Même si cette sensation est peut-être éphémère .", {"heureux": 60, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["Elle est incroyablement réconfortante .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Elle me rappelle qu'il y a toujours une lumière quelque part .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 5}],
    ["Prête à briller si on lui laisse de la place .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est cela, au fond, le véritable sens du bonheur .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je mange .", {"heureux": 0, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Salut . Je ne sais même pas pourquoi je commence à parler .", {"heureux": 0, "triste": 70, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["C'est étrange de se sentir vide quand on est entouré de tant de choses .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 60}],
    ["Mais elles ne font que passer devant moi comme des ombres dans un rêve éteint .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 70}],
    ["Je me demande souvent ce que ça signifie d'exister vraiment .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 75}],
    ["Être vivant ? Respirer ? Ressentir quelque chose qui ne soit pas ce néant pesant ? .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Chaque matin je me lève en espérant qu'il y aura une réponse .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 70}],
    ["Mais le jour passe, et je n'ai rien trouvé d'autre que ce poids qui écrase mon souffle .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Est-ce que quelqu'un me voit vraiment ? Est-ce que quelqu'un m'entend ? .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Je regarde mon reflet dans le miroir et je ne sais pas qui je suis .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Je suis une ombre qui marche, une voix qui se tait, un rêve oublié .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Parfois je veux crier, mais le silence me semble plus juste .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Parce qu'il n'y a rien à dire . Rien à offrir . Rien à attendre .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Alors je reste là . Immobile . Prisonnier de mes propres pensées .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Et je me demande si un jour, tout cela aura un sens .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Parfois, je me demande ce que cela signifie vraiment d'exister .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Être là, respirer, mais sans vraiment ressentir quoi que ce soit .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Chaque jour semble passer sans laisser la moindre trace en moi .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Je me lève, je marche, je parle, mais tout paraît si creux .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 75}],
    ["Comme si le monde entier avait une couleur que je ne pouvais pas voir .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Je me demande pourquoi je continue . Pourquoi je fais semblant d'aller bien .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Le vide à l'intérieur de moi est tellement lourd que parfois, je ne peux même pas respirer .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Est-ce que quelqu'un ressent ce que je ressens ? Ou suis-je seul avec ce poids ? .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Il y a des nuits où je reste éveillé, à regarder le plafond, à chercher des réponses .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Mais tout ce que je trouve, ce sont des questions qui tournent en boucle .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Pourquoi moi ? Pourquoi maintenant ? Pourquoi ça fait si mal d'exister ? .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Je regarde les autres et ils semblent heureux, ou au moins, ils font semblant mieux que moi .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 10, "perdu": 80}],
    ["Est-ce que je suis brisé ? Est-ce que quelque chose en moi a été détruit ? .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Il y a des jours où je ne me reconnais même pas dans le miroir .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Je vois un visage, des yeux, une bouche, mais rien ne me semble familier .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Comme si je n'étais qu'une coquille vide, un spectre errant dans un monde qui ne m'appartient pas .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Je me demande souvent si je mérite de ressentir quelque chose de différent .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Est-ce que le bonheur existe vraiment ? Ou est-ce juste une illusion que tout le monde poursuit en vain ? .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Il y a des moments où je voudrais tout arrêter, fermer les yeux et ne plus jamais les rouvrir .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Mais même cette pensée me fait peur, parce que je ne sais pas ce qu'il y a après .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Peut-être que le vide continuerait, encore plus grand, encore plus écrasant .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Je veux croire qu'il y a quelque chose de plus, mais je ne sais pas comment y arriver .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 75}],
    ["Chaque pas que je fais semble me ramener au même point .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["Un cercle sans fin de doute, de peur, de tristesse qui ne me quitte jamais .", {"heureux": 0, "triste": 100, "mechant": 0, "jaloux": 0, "perdu": 95}],
    ["Je me demande si quelqu'un voit ce que je ressens vraiment, ou si je suis invisible pour le reste du monde .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Je ne veux pas être seul, mais je ne sais pas comment m'ouvrir aux autres .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 80}],
    ["C'est comme si une barrière invisible me séparait de tout ce qui pourrait m'aider .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Je continue à marcher, à espérer, même si je ne sais pas pourquoi .", {"heureux": 0, "triste": 90, "mechant": 0, "jaloux": 0, "perdu": 85}],
    ["Peut-être qu'un jour, tout cela changera, mais pour l'instant, je suis perdu .", {"heureux": 0, "triste": 95, "mechant": 0, "jaloux": 0, "perdu": 90}],
    ["Aujourd'hui j'ai vu quelque chose d'incroyable .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Une découverte qui a illuminé ma journée comme jamais auparavant .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était comme un éclat de lumière au milieu de l'ombre ordinaire .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sentais émerveillé, presque suspendu dans le temps .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Comme si chaque instant était une œuvre d'art vivante .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne savais pas que le monde pouvait être si vibrant, si plein de vie .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était une expérience qui touchait mon âme profondément .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Un sentiment que je n'avais jamais ressenti auparavant .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me suis arrêté un moment pour contempler, absorbé par cette beauté .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque détail semblait parfait, comme si l'univers entier avait conspiré pour créer cet instant .", {"heureux": 100, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'étais transporté dans un autre monde, un monde où tout faisait sens .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était comme si je découvrais une partie de moi-même que j'avais oubliée .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sentais connecté à quelque chose de beaucoup plus grand que moi .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était une explosion de couleurs, de sons, de sensations .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque nuance semblait vibrer d'énergie positive .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je pouvais sentir mon cœur battre plus vite, comme si j'étais pleinement vivant .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était comme si je découvrais le monde pour la première fois .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque respiration semblait plus profonde, plus significative .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je n'avais jamais réalisé à quel point la vie pouvait être belle .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je veux garder ce sentiment avec moi pour toujours .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je veux partager cette joie avec le monde entier .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis reconnaissant pour ce moment, pour cette découverte .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je sais que je ne l'oublierai jamais .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est comme si mon âme avait trouvé une nouvelle lumière .", {"heureux": 100, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Et je sais que cette lumière continuera de briller en moi .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'était un moment parfait, un cadeau du destin .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis rempli de gratitude pour cette expérience incroyable .", {"heureux": 100, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Aujourd'hui est une journée formidable .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens un peu perdu dans tout ça .", {"heureux": 0, "triste": 10, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Pourquoi les choses doivent être si compliquées parfois .", {"heureux": 0, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Je n'ai aucune envie d'être méchant avec qui que ce soit .", {"heureux": 10, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Voir les autres réussir me rend un peu jaloux parfois .", {"heureux": 10, "triste": 0, "mechant": 0, "jaloux": 50, "perdu": 0}],
    ["Je suis tellement fier de ce que j'ai accompli aujourd'hui .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est une situation vraiment difficile à comprendre .", {"heureux": 0, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Regarder les étoiles me rend incroyablement heureux .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens un peu triste en pensant à tout ça .", {"heureux": 0, "triste": 50, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["C'est un sentiment étrange de ne pas savoir quoi faire .", {"heureux": 0, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Être gentil est toujours ma priorité .", {"heureux": 60, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Pourquoi les gens doivent toujours se comparer aux autres .", {"heureux": 0, "triste": 10, "mechant": 0, "jaloux": 20, "perdu": 0}],
    ["Je suis heureux de voir que tout le monde est en bonne santé .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Aider quelqu'un aujourd'hui m'a fait me sentir bien .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis parfois un peu trop dur avec moi-même .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["Les nuages dans le ciel me rendent nostalgique aujourd'hui .", {"heureux": 20, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Il y a tellement de beauté dans les petites choses .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis curieux de savoir ce que l'avenir me réserve .", {"heureux": 50, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Le soleil qui brille me réchauffe le cœur .", {"heureux": 60, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Parfois je me demande si je prends les bonnes décisions .", {"heureux": 0, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["C'est tellement agréable de voir des sourires autour de moi .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ressens un vide que je ne sais pas comment combler .", {"heureux": 0, "triste": 50, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Je n'arrive pas à croire à quel point je suis chanceux .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Il est difficile de rester optimiste dans des moments comme ceux-ci .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 20}],
    ["Voir des gens s'entraider me remplit d'espoir .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens submergé par tout ce qui se passe autour de moi .", {"heureux": 0, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Les petites victoires méritent toujours d'être célébrées .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Il y a des jours où j'ai juste envie de tout lâcher .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Voir un coucher de soleil me remplit de sérénité .", {"heureux": 65, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne sais pas pourquoi je ressens autant de jalousie parfois .", {"heureux": 0, "triste": 20, "mechant": 0, "jaloux": 60, "perdu": 10}],
    ["Je suis reconnaissant pour les choses simples de la vie .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'aimerais pouvoir me sentir plus sûr de moi .", {"heureux": 0, "triste": 10, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Rendre quelqu'un heureux me rend également heureux .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'ai parfois peur de ne jamais trouver ma place .", {"heureux": 0, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 60}],
    ["Les moments partagés avec des amis sont précieux .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Parfois, j'ai envie de crier pour exprimer ce que je ressens .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Je suis fier de moi pour tout ce que j'ai surmonté .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque nouvelle journée est une opportunité d'apprendre quelque chose de nouveau .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis vraiment énervé contre moi-même aujourd'hui .", {"heureux": 0, "triste": 0, "mechant": 30, "jaloux": 0, "perdu": 20}],
    ["Il y a tellement de choses que je regrette profondément .", {"heureux": 0, "triste": 50, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["Aider quelqu'un dans le besoin me remplit de bonheur .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis jaloux des gens qui semblent avoir tout compris .", {"heureux": 0, "triste": 10, "mechant": 0, "jaloux": 60, "perdu": 20}],
    ["Chaque jour est une chance de devenir une meilleure personne .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est frustrant de ne pas avoir de contrôle sur ma vie .", {"heureux": 0, "triste": 20, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Je suis tellement en colère contre cette situation injuste .", {"heureux": 0, "triste": 0, "mechant": 40, "jaloux": 0, "perdu": 20}],
    ["Pourquoi tout semble si compliqué ces derniers temps .", {"heureux": 0, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Je suis fier de moi pour avoir persévéré malgré tout .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis tellement triste de voir tout ce gâchis autour de moi .", {"heureux": 0, "triste": 60, "mechant": 0, "jaloux": 0, "perdu": 20}],
    ["Voir quelqu'un réussir me donne envie de travailler plus dur .", {"heureux": 50, "triste": 0, "mechant": 0, "jaloux": 30, "perdu": 0}],
    ["J'ai envie de crier tellement je suis frustré .", {"heureux": 0, "triste": 0, "mechant": 20, "jaloux": 0, "perdu": 30}],
    ["Il y a des jours où tout semble perdu d'avance .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Le rire des enfants me redonne espoir en l'humanité .", {"heureux": 70, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne supporte pas la méchanceté gratuite .", {"heureux": 0, "triste": 20, "mechant": 10, "jaloux": 0, "perdu": 0}],
    ["Quand je vois les autres heureux, cela me réchauffe le cœur .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 10, "perdu": 0}],
    ["La solitude est un sentiment difficile à surmonter .", {"heureux": 0, "triste": 50, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Je suis tellement reconnaissant pour tout ce que j'ai dans la vie .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Parfois je me sens comme un étranger parmi les autres .", {"heureux": 0, "triste": 30, "mechant": 0, "jaloux": 0, "perdu": 60}],
    ["J'aimerais trouver la paix intérieure et arrêter de douter de tout .", {"heureux": 0, "triste": 40, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Je suis vraiment reconnaissant pour tout ce que j'ai aujourd'hui .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est difficile de ne pas pleurer face à tant de douleur .", {"heureux": 0, "triste": 70, "mechant": 0, "jaloux": 0, "perdu": 10}],
    ["Aujourd'hui est une belle journée pleine de promesses .", {"heureux": 75, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens totalement abandonné et seul .", {"heureux": 0, "triste": 60, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Aider quelqu'un dans le besoin m'a rempli de joie aujourd'hui .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne peux m'empêcher de me sentir envahi par un profond chagrin .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 20}],
    ["Les petites victoires méritent d'être célébrées avec bonheur .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Le monde entier semble contre moi en ce moment .", {"heureux": 0, "triste": 50, "mechant": 10, "jaloux": 0, "perdu": 30}],
    ["Voir mes amis réussir m'inspire beaucoup de fierté et de bonheur .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 10, "perdu": 0}],
    ["Il y a des jours où chaque décision semble mener à l'échec .", {"heureux": 0, "triste": 60, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Faire sourire quelqu'un me donne un sentiment incroyable de bonheur .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ressens une tristesse inexplicable qui me pèse lourdement .", {"heureux": 0, "triste": 70, "mechant": 0, "jaloux": 0, "perdu": 20}],
    ["Je suis incroyablement fier de ce que j'ai accompli aujourd'hui .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["La solitude est parfois comme un gouffre sans fin .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Rendre quelqu'un heureux me fait sentir utile et épanoui .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne vois pas comment je pourrais sortir de cette impasse .", {"heureux": 0, "triste": 50, "mechant": 0, "jaloux": 0, "perdu": 60}],
    ["Chaque sourire échangé est une petite victoire pour le cœur .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne sais plus à qui faire confiance dans ce monde .", {"heureux": 0, "triste": 60, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Partager un bon moment avec ma famille est une bénédiction .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Les souvenirs douloureux reviennent me hanter encore et encore .", {"heureux": 0, "triste": 75, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Je me sens vraiment vivant aujourd'hui, tout semble parfait .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Rien ne peut combler ce vide que je ressens en ce moment .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Regarder les étoiles me remplit d'une sérénité inégalée .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque souvenir douloureux semble plus lourd à porter .", {"heureux": 0, "triste": 75, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Voir le soleil se lever me donne de l'énergie et de l'espoir .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je ne sais pas pourquoi je ressens autant de désespoir ces jours-ci .", {"heureux": 0, "triste": 70, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Chaque nouvelle rencontre m'apporte une joie sincère .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je suis submergé par une tristesse profonde que je ne peux expliquer .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Faire quelque chose de bien pour quelqu'un me remplit de bonheur .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'ai du mal à avancer, comme si un poids m'empêchait de bouger .", {"heureux": 0, "triste": 65, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Rire avec mes amis me rappelle pourquoi la vie est belle .", {"heureux": 95, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Je me sens comme une ombre qui erre sans but .", {"heureux": 0, "triste": 70, "mechant": 0, "jaloux": 0, "perdu": 60}],
    ["Le parfum des fleurs me met de bonne humeur instantanément .", {"heureux": 80, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["C'est difficile de ne pas se sentir dépassé par tout ce qui arrive .", {"heureux": 0, "triste": 75, "mechant": 0, "jaloux": 0, "perdu": 40}],
    ["Avoir accompli un petit objectif me donne un sentiment de fierté .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Les moments de solitude prolongée deviennent insupportables .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 50}],
    ["Un bon repas partagé me remplit de chaleur et de bonheur .", {"heureux": 90, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["Chaque journée semble un peu plus sombre que la précédente .", {"heureux": 0, "triste": 85, "mechant": 0, "jaloux": 0, "perdu": 30}],
    ["Voir un arc-en-ciel me rappelle les belles choses de la vie .", {"heureux": 85, "triste": 0, "mechant": 0, "jaloux": 0, "perdu": 0}],
    ["J'ai l'impression de tourner en rond sans fin .", {"heureux": 0, "triste": 80, "mechant": 0, "jaloux": 0, "perdu": 60}]
]





entrainer_model(liste_phrases_emotions)


mot_debut = "Chaque"
dico_emo = {"heureux":100,"triste":0,"mechant":0,"jaloux":0,"perdu":0}

for word in list(dico_emotions_des_mots.keys()):
    print(word,dico_emotions_des_mots[word])

print(dico_emotions_des_mots)

print(faire_une_phrase_qui_se_rapproche_de_emotions(mot_debut,dico_emo))
