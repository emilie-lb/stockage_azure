import sys
import argparse
# permet de rendre utilisable fichier config par python (création d'un dictionnaire)
import configparser
import logging
import os.path
# BlobServiceClient => manipuler les ressources de stockage Azure et les conteneurs blob
from azure.storage.blob import BlobServiceClient
# ContainerClient => manipuler des conteneurs de stockage Azure et leurs blobs
# BlobClient => manipuler des blobs de stockage Azure
#, ContainerClient, BlobClient (ils ne sont pas utilisés dans ici)


def listb(containerclient):
    # containerclient => le container que l'on souhaite manipuler
    """ Créer la liste des objets blobs d'un container """
    logging.info("Récupération de la liste des blobs")
    # initialise variable blob_list qui stocke la liste des blob contenus dans le container
    blob_list=containerclient.list_blobs()
    logging.info("affichage de la liste")
    # permet d'afficher le nom de chaque blob
    for blob in blob_list:
        print(blob.name)


def upload(cible, blobclient):
    # cible => le chemin (path) vers le fichier stocké en local
    # blobclient => 
    """ Charger un objet blob sur un container """
    logging.info(f"ouverture du fichier {cible} avant chargement sur le container")
    # ouvre le fichier bianire en lecture seule
    with open(cible, "rb") as f:
        logging.warning("Démarrage du chargement du fichier sur le container")
        blobclient.upload_blob(f)


def download(filename, dl_folder, blobclient):
    # filename => le nom que l'on souhaite donner au fichier sur le dépot local
    # dl_forder => le chemin (path) du dossier local cible
    # blobclient => 
    """ Télécharger des objets blobs (sur dossier local) """
    logging.debug(f"ouverture du fichier {filename} avant téléchargement sur dossier local")
    # ouverture du fichier bianire en écriture 
    with open(os.path.join(dl_folder,filename), "wb") as my_blob:
        logging.info("Démarrage du téchargement du blob")
        # téléchargement de l'objet blob depuis container Azure
        blob_data = blobclient.download_blob()
        logging.warning("Ecriture du blob dans mon fichier local")
        blob_data.readinto(my_blob)


def main(args,config):
    # args => tous les arguments passés en ligne de commande
    # config => objet Configparser contenant les information contenues dans config
    logging.debug(f"démarrage du programme, recherche de connection au compte de stockage {config['storage']['account']}")
    # création d'une instance de classe BlobServiceClient, identification compte de stockage son url
    blobclient=BlobServiceClient(
        f"https://{config['storage']['account']}.blob.core.windows.net",
        config["storage"]["key"],
        logging_enable=False)
    logging.info(f"Connection au compte de stockage {config['storage']['account']} réussie")
    logging.debug(f"recherche de connection au container Azure {config['storage']['container']}")
    # initialise containerclient qui pemet d'identifier le container d'interêt
    containerclient=blobclient.get_container_client(config["storage"]["container"])
    logging.info(f"Connection au container Azure {config['storage']['container']} réussie")
    # si argument list => lance fonction listb
    if args.action=="list":
        logging.debug("action demandée : afficher list des blobs, lancement de la fonction listb")
        return listb(containerclient)
    # sinon, 
    else:
        # soit on charge les objets blob sur container
        if args.action=="upload":
            # réinitialisation de la variable blobclient pour qu'elle 'pointe' sur le dossier local 
            blobclient=containerclient.get_blob_client(os.path.basename(args.cible))
            # lancement de la fonction upload
            log.debug("action demandée : charger des blobs dans un container, lancement de la fonction upload")
            return upload(args.cible, blobclient)
        # soit on télécharge des objets blob dnas un dossier local
        elif args.action=="download":
            # réinitialisation de la variable blobclient pour qu'elle 'pointe' sur le dossier local 
            # args.cible => le chemin vers le dossier local
            blobclient=containerclient.get_blob_client(os.path.basename(args.remote))
            log.debug("action demandée : charger des blobs dans un container, lancement de la fonction upload")
            # lancement de la fonction download
            return download(args.remote, config["general"]["restoredir"], blobclient)
    

if __name__=="__main__":
    parser=argparse.ArgumentParser("Logiciel d'archivage de documents")
    parser.add_argument("-cfg",default="config.ini",help="chemin du fichier de configuration")
    parser.add_argument("-lvl",default="info",help="niveau de log")
    subparsers=parser.add_subparsers(dest="action",help="type d'operation")
    subparsers.required=True
    
    parser_s=subparsers.add_parser("upload")
    parser_s.add_argument("cible",help="fichier à envoyer")

    parser_r=subparsers.add_parser("download")
    parser_r.add_argument("remote",help="nom du fichier à télécharger")
    parser_l=subparsers.add_parser("list")

    args=parser.parse_args()

    loglevels={"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
    print(loglevels[args.lvl.lower()])
    logging.basicConfig(level=loglevels[args.lvl.lower()])

    # parser les informations contenues dans fichier config.ini sous forme de dico
    config=configparser.ConfigParser()
    config.read(args.cfg)

    sys.exit(main(args,config))