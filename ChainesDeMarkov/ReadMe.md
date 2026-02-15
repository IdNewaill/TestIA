# [<Retour](../ReadMe.md) | Chaînes de Markov
Ce script est un générateur de texte basé sur les [chaînes de Markov](https://fr.wikipedia.org/wiki/Cha%C3%AEne_de_Markov), en lui donnant du texte, il sera capable d'imaginer des phrases.

```Example
Exemple de résultat d'exécution

Freddy jaune et certaines
parties ne serait pas
autorisés à presque tous un
animatronique est un des
animatroniques plus de fils et
Foxy , et l'autre à gauche ,
restant un nom précis :
Freddy viendra causer un
gardien de Phone Guy , plus
particulièrement à l'aide de
fils et l'autre à l'aide de
celui-ci .
```

## Pour la petite histoire
Je ne m'étais basés sur un aucun tutoriel ou information, j'ai créer ce script sans recherches en imaginant m'être rapproché de ce qu'était un [LLM](https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage).

Après avoir fini le script et avoir fait quelques recherches, c'est là que je me suis rendu compte que ce script existe depuis bien longtemps !

## Que fait le script plus exactement ?
Ce script ne gérère pas des phrases qui ont un sens mais essaye simplement de dicerner un certain pattern qui lui autorise à non à placer un mot après un autre.

Chaque exécution de se script devrait donner un résultat différent (jusqu'à ce que toute les possibilités soient définies). Dans cette version, la vision du pattern ne se limite qu'à un mot.

## Comment tester ?
Il s'agît d'un script Python, donc l'ouverture du fichier depuis un explorateur (si python est installé) ou alors le clique du bouton démarrer le script représenter par une icone triangulaire en haut (depuis VS Code ou IntelliJ) permettra de faire apparaître une phrase plus ou moins longue à l'écran.

Le script Python se trouve juste ici :

[➜ Accéder au fichier](./ChainesDeMarkov.py)