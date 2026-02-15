# [<Retour](../ReadMe.md) | Test de création d'un LLM
Le script que j'ai écrit est censé reprendre le fonctionnement (bien simplifié d'un [LLM](https://fr.wikipedia.org/wiki/Grand_mod%C3%A8le_de_langage)) sans utiliser de modules Python liés au LLM. Malheureusement, avec son fonctionnement actuel, il est pratiquement impossible d'obtenir une réponse un tant soit peu intelligente ou du moins faisant sens.

Ce script inclu l'entrainement sur un texte et la génération d'un texte qu'il considère comme faisant sens pour lui ou d'une réponse à une question.

## Tester

Il s'agît d'un script Python, donc l'ouverture du fichier depuis un explorateur (si python est installé) ou alors le clique du bouton démarrer le script représenter par une icone triangulaire en haut (depuis VS Code ou IntelliJ) permettra de faire apparaître une phrase plus ou moins longue à l'écran.

Le script Python se trouve juste ici :

[➜ Accéder au fichier](./intelligence%20artificielle%20niveau%20d'intelligence%20faible.py)

## Pour les plus avancés
Comme vous pouvez le voir juste ici :
```Python
texte_en_liste = [
"que fais le chat <start> le chat dort <end>",
"que fais le chien <start> le chien abboie <end>"
]
```
Chaque phrase est constitué de deux tokens, le premier est \<start> pour indiquer l'attente d'une réponse et le deuxième est \<end> pour annoncer la fin de la réponse (notre script sait qu'à la réception de ce token end, il doit renvoyer la phrase).

Le problème ici est que l'apprentissage n'est pas assez développée et donc le modèle oublie facilement ce qu'il venait d'apprendre puisque lors de l'apprentissage d'une nouvelle phrase, il oublie comment formuler les phrases d'avant ou les mots d'avant.