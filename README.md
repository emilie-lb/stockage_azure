# stockage_azure
Un script main.py est un script python permettant de:  
* lister les fichiers d'un conteneur Azure Blob Storage, 
* envoyer un fichier dans un container Azure Blob Storage
* télécharger un fichier contenu dans un container Azure Blob Storage  

*remarque: Pour utiliser ce script vous devez avoir un compte Azure, créer un compte de stockage et un container.* 

## remplir le fichier config.ini: 
Le fichier config.ini contient vos informations personnelles (vos noms de compte de stockage et de container, la clé d'identification...)  
*remarque: dans le fichier config, les informations sont écrites sans guillemets.*  

Exemple du contenu du fichier config:
```[general]
restoredir=C:\Users\utilisateur\Documents\Dossier\download  (=> Ici, mettre le chemin vers votre dossier de télécargement)
[storage]
account=toto  (=> Ici, mettre le nom de votre compte de stockage)
container=container1 (=> Ici, mettre le nom de votre container) 
key=....................................==   (=> Ici, mettre la clé 1 de votre compte de stockage)
```


## fonctionnement du sript main.py: 
Le script python main.py se lance par l'intermédiaire d'arguments entrés directement en la ligne de commande.  
Pour lancer le script, écrire dans le temrinal:  
```python main.py```  
Suivi de l'argument de votre choix: ```"list"```, ```"upload"``` + le chemin du fichier à envoyer dans le container, ```"download"``` + le nom du fichier à télécharger sur le container.

Changer le comportement par défaut:  
Le programme se lance par défaut en appelant le fichier config.ini pour se relier au container Azure Blob Storage. Si vous souhaitez utiliser un autre fichier que le fichier par défaut, utilisez l'argument ```-cfg``` en écrivant dans le terminal:  
```python main.py -cfg autreconfig.ini``` + l'argument demandé  
Le programme se lance par défaut avec un niveau de logging "info". Si vous souhaiter changer le niveau de logging, utilisez l'argument ```-lvl``` suivi du niveau souhaité (info, debug, warning, error, critical):   
```python main.py -lvl debug``` + l'argument demandé  


## Librairies à installer : 
Les librairies utilisées dans ce script font quasiment toutes parties des librairies installées par défaut avec python. 
Seules les librairies liées à Azure nécessitent être installées. Vous pouvez le faire:  
-soit directement dans le terminal avec la commande ```pip install azure-storage-blob```  
-soit, si vous travaillez en environnement virtuel, vous pouvez utiliser le fichier requirements.txt 
