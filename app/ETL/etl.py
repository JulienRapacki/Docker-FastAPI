import pandas as pd
import requests
import psycopg2
from io import StringIO

def extract_csv_data():
    """Télécharge le CSV des communes"""
    url = "https://www.data.gouv.fr/fr/datasets/r/dbe8a621-a9c4-4bc3-9cae-be1699c5ff25"
    response = requests.get(url)
    return pd.read_csv(StringIO(response.text))

def transform_data(df):
    """Nettoie et transforme les données"""
    # Sélectionne les colonnes nécessaires
    df_clean = df[['code_postal', 'nom_commune_complet']].copy()
    
    # Noms en majuscules
    df_clean['nom_commune_complet'] = df_clean['nom_commune_complet'].str.upper()
    
    # Calcul le département 
    df_clean['departement'] = df_clean['code_postal'].astype(str).str[:2]
       
    return df_clean

def load_to_db(df, db_connection):
    """Charge les données en base"""
    cursor = db_connection.cursor()
    
    # Créer la table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS communes (
            id SERIAL PRIMARY KEY,
            code_postal VARCHAR(10),
            nom_commune VARCHAR(255),
            departement VARCHAR(5)
        )
    """)
    
    # Insérer les données
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO communes (code_postal, nom_commune, departement) 
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (row['code_postal'], row['nom_commune_complet'], row['departement']))
    
    db_connection.commit()

def run_etl():
    """ETL principal"""
    # Extract 
    raw_data = extract_csv_data()
    
    # Transform  
    clean_data = transform_data(raw_data)
    
    # Load 
    conn = psycopg2.connect("postgresql://user:password@db:5432/communes")
    load_to_db(clean_data, conn)
    conn.close()
    
    return len(clean_data)