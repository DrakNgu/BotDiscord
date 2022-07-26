# Bot discord Projet Python


| Grosset Killian              |M2I                                                      |11/06/2021|
| ----------------------| ----------------------------------------------------------------------|-|


## Comment lancer le bot

Avant toutes chose il faut rejoindre le serveur discord ou le bot est membre

voici le liens pour rejoindre le discord

https://discord.gg/QEjerutRq6

Pour commencer il faut ce rendre dans votre console

Installer le requirements.txt :

```
pip install -r requirements.txt
```
Pour lancer le bot il vous faut le lancer avec python3
```
python3 bot.py
```
## Comment se servir du bot

Une fois le serveur rejoint et le bot lancé il suffit de rentrer la commande **!help** qui donne toutes les commandes dont le bot dispose. **Toutes les commandes doivent commencer par "!"**

## Organisation

Pour l'organisation du code j'ai séparé comme j'ai vu sur plusieurs bot en Cogs(documentation ci-dessous). C'est une manière de créer des package avec discord afin de justement alimenter automatiquement ma commande **!help** et d'avoir une organisation par type de commande (modération,event,fun ...)

**[Cogs](https://discordpy-redfork.readthedocs.io/en/latest/ext/commands/cogs.html)**

# Avertissement

Je pense que vous allez avoir un problème avec la commande **!nuke** car elle va chercher des images et le chemin ne sera pas le bon car je n'ai pas eu le temps de trouver une manière de faire un chemin dinamyque. 

Vous aurai aussi un problème avec les commandes de la catégorie **Owner** car il faudra rajouter manuellement votre ID dans le fichier config.yaml pour ce faire il faut activer le mode developper dans discord 
**[C'est par ici](https://support.discord.com/hc/fr/articles/206346498-O%C3%B9-trouver-l-ID-de-mon-compte-utilisateur-serveur-message-)**
Une fois votre identifiant récuperé il faut le mettre à la suite des owner dans le ficheir config.yaml







