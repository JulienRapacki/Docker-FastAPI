

## Prérequis

- installer Docker & Git

## Structure du projet

'''
DIGITALISIM/
├── docker-compose.yml    # Configuration 
├── app/
│    ├─ main.py           # API FastAPI                          
│    ├─ requirements.txt  # Dépendances Python
|    ├─ ETL/
|       ├─ Dockerfile     # Image de l'application
|       ├─ etl.py         # Pipiline récupération donnée / transformation / chargement 
│── .env                  # Variables d'environnement 
└── README.md
'''
```
poc-communes/
├── docker-compose.yml      # Configuration des services
├── app/
│   ├── main.py             # API FastAPI
│   ├── etl.py              # Pipeline ETL
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image de l'application
├── data/                   # Dossier pour les données (vide)
└── README.md               # Cette documentation
```
## Endpoints ##


- POST | `/import-data`                         | Importe le dataset des communes depuis l'URL et chargement dans bdd|
- POST | `/communes`                            | Crée ou met à jour une commune |
- GET  | `/communes/{nom_commune}`              | Récupère les informations d'une commune par son nom |
- GET  | `/departements/{departement}/communes` | Liste toutes les communes d'un département |
- GET  | `/`                                    | Point d'entrée de l'API |

