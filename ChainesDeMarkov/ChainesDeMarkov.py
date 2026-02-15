from random import *
text="""
Five Nights at Freddy's est un jeu vidéo de genre survival horror en pointer-cliquer (point-and-click) développé par Scott Cawthon, sorti en 2014.

Le jeu se déroule dans une pizzeria, dans laquelle un gardien de sécurité appelé Mike Schmidt doit se protéger d'antagonistes animatroniques (Freddy, Bonnie, Chica et Foxy), communs à presque tous les jeux, qui sont censés divertir les clients lors des journées.

L'histoire du jeu est très controversée, et certaines parties ne sont que supposées. D'après les appels de Phone Guy lors du premier jour, le programme des animatroniques leur fait prendre le gardien de nuit pour un endosquelette d'animatronique sans aucun costume. Or selon le Phone Guy, les endosquelettes sans costume ne sont pas autorisés à se montrer au public, et donc les animatroniques ont été programmés pour emmener les endosquelettes dans les coulisses afin de leur faire enfiler un costume. Et toujours selon le Phone Guy, ce ne serait pas si grave si les costumes n'étaient pas remplis de barres transversales, de fils et de dispositifs animatroniques, en particulier dans le masque.

Le gardien de nuit doit surveiller chacun de leurs mouvements à l'aide de caméras de surveillance et en se protégeant avec des portes blindées. Mais il faut faire attention à certains animatroniques plus qu'aux autres, plus particulièrement à « Foxy » qui court vers la salle où se trouve le joueur contrairement aux autres. Il faut également surveiller la batterie qui se déchargera en fonction des actions comme allumer la lumière du couloir, fermer les portes... Car si celle-ci tombe à 0 %, Freddy viendra causer un Game Over, car celui-ci a une particularité : il n’apparaît que lorsque le joueur n'a plus de courant ou qu’il a atteint la nuit 4. Lorsque ça arrive, on peut voir ses yeux dans le noir mais on peut aussi entendre une berceuse, reprise d'une partie de l’air du toréador de Georges Bizet.

La pièce où se retrouve le joueur comporte deux portes, l'une à droite et l'autre à gauche, et quatre boutons, deux pour chaque porte. Ces boutons servent à bloquer l'accès aux animatroniques lorsqu'ils sont près du joueur ou à allumer une lumière permettant de distinguer si un animatronique est près de celui-ci. Les robots que le joueur doit éviter ont tous un nom précis : Freddy, l'ours, la mascotte du restaurant, Bonnie le lapin, le violoniste, Chica, le poussin, et enfin Foxy, le renard pirate.

Un costume de rechange de Freddy jaune et sans yeux apparaît dans le jeu si on bascule plusieurs fois d'une caméra à la caméra 2B1, ainsi nommé par les fans « Golden Freddy », restant un des personnages mystérieux du jeu.
"""
text=text.replace(" .",".")
text=text.replace("."," .")
text=text.replace(" ,",",")
text=text.replace(","," ,")
text=text.split()
dico={}
size=len(text)
for index in range(0,size-1):
    if not text[index] in dico.keys():dico[text[index]]={}
    if text[index+1] in dico[text[index]].keys():dico[text[index]][text[index+1]]+=1
    else:dico[text[index]][text[index+1]]=1
for main_word in dico:
    words_number=0
    for word in dico[main_word]:words_number+=dico[main_word][word]
    for word in dico[main_word]:dico[main_word][word]=int(dico[main_word][word]/words_number*100)
del text
def choose_random_word(dico):
    r=randint(1,100)
    keys=list(dico.keys())
    index=-1
    actual_sum=0
    while r>actual_sum:
        index+=1
        if index>len(keys)-1:return keys[len(keys)-1]
        actual_sum+=dico[keys[index]]
    return keys[index]
def ponct(word):return word in [".","!","?","..."]
def say_stm(dico):
    word="."
    start_words=list(dico.keys())
    while ponct(word) or not 64<ord(word[0])<91:
        if not ponct(word):start_words.remove(word)
        word=start_words[randint(0,len(start_words)-1)]
    phrase=[word]
    while not ponct(word):
        word=choose_random_word(dico[word])
        phrase.append(word)
    return phrase
def tell(p):
    restant=p
    while restant!=[]:
        c=30
        br=[]
        while restant!=[] and len(restant[0])<=c:
            c-=len(restant[0])+1
            br.append(restant.pop(0))
        print(" ".join(br))

tell(say_stm(dico))
