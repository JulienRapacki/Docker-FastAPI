

## Prérequis

- installer Docker & Git

## STRUCTURE DU PROJET

DIGITALISIM/
├── docker-compose.yml    # Configuration 
├── app/
|    ├─ main.py           # API FastAPI                          
|    ├─ requirements.txt  # Dépendances Python
|    ├─ ETL/
|       ├─ Dockerfile     # Image de l'application
|       ├─ etl.py         # Pipiline récupération donnée / transformation / chargement 
│── .env                  # Variables d'environnement 
└── README.md


## Endpoints ##


| POST | `/import-data`                         | Importe le dataset des communes depuis l'URL et chargement dans bdd|
| POST | `/communes`                            | Crée ou met à jour une commune |
| GET  | `/communes/{nom_commune}`              | Récupère les informations d'une commune par son nom |
| GET  | `/departements/{departement}/communes` | Liste toutes les communes d'un département |
| GET  | `/`                                    | Point d'entrée de l'API |

