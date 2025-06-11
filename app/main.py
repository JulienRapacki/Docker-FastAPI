from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from ETL.etl import run_etl

app = FastAPI(title="API Communes", version="1.0.0")

# Modèles Pydantic
class CommuneCreate(BaseModel):
    code_postal: str
    nom_commune: str
    departement: str

class CommuneResponse(BaseModel):
    id: int
    code_postal: str
    nom_commune: str
    departement: str

def get_db_connection():
    """Connexion à la base de données"""
    return psycopg2.connect(
        os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/communes"),
        cursor_factory=RealDictCursor
    )

@app.get("/")
def root():
    return {"message": "API Communes - DIGITALISIM"}

@app.post("/import-data")
def import_data():
    """Importe les données CSV via ETL"""
    try:
        count = run_etl()
        return {"message": f"{count} communes importées"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/communes", response_model=CommuneResponse)
def create_or_update_commune(commune: CommuneCreate):
    """Créer ou mettre à jour une commune"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO communes (code_postal, nom_commune, departement) 
            VALUES (%s, %s, %s)
            ON CONFLICT (nom_commune) DO UPDATE SET
                code_postal = EXCLUDED.code_postal,
                departement = EXCLUDED.departement
            RETURNING *
        """, (commune.code_postal, commune.nom_commune.upper(), commune.departement))
        
        result = cursor.fetchone()
        conn.commit()
        return CommuneResponse(**result)
        
    finally:
        conn.close()

@app.get("/communes/{nom_commune}", response_model=CommuneResponse)
def get_commune_by_name(nom_commune: str):
    """Récupérer une commune par son nom"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT * FROM communes WHERE nom_commune = %s", 
            (nom_commune.upper(),)
        )
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Commune non trouvée")
            
        return CommuneResponse(**result)
        
    finally:
        conn.close()

@app.get("/departements/{departement}/communes")
def get_communes_by_departement(departement: str):
    """Récupérer toutes les communes d'un département"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT * FROM communes WHERE departement = %s ORDER BY nom_commune", 
            (departement,)
        )
        results = cursor.fetchall()
        
        return [CommuneResponse(**row) for row in results]
        
    finally:
        conn.close()
        
        
@app.get("/debug/count")
def count_communes():
    """Debug: compter les communes en base"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) as total FROM communes")
        result = cursor.fetchone()
        return {"total_communes": result['total']}
    finally:
        conn.close()