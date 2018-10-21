import json
import psycopg2
from parameters import *
import os

def run_query(query=''):
    #conn_string = "host='localhost' dbname='postgres' user='postgres' password='chucho'"
    #conn_string = "host='127.0.0.1' dbname='docker' user='docker' password='docker' port='49153' client_encoding=UTF8"
    conn_string = "host="+HOST+" dbname="+DATABASE+ " user="+USER+" password="+PASSWORD+" port="+PORT+" client_encoding=UTF8"
    conn = psycopg2.connect(conn_string) # Conectar a la base de datos
    #$conn.set_character_encoding('utf8')
    cursor = conn.cursor()         # Crear un cursor
    cursor.execute(query)          # Ejecutar una consulta

    #Le inclui insert
    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    elif query.upper().startswith('INSERT') and 'RETURNING' in query.upper():
        conn.commit()              # Hacer efectiva la escritura de datos
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        conn.commit()              # Hacer efectiva la escritura de datos
        data = None

    cursor.close()                 # Cerrar el cursor
    conn.close()                   # Cerrar la conexion

    return data
    
    
pimpri = run_query("""SELECT 
  afiliacion.nombre, 
  afiliacion.pais, 
  afiliacion.ciudad, 
  paper.id, 
  afiliacion.scopus_id
FROM 
  public.afiliacion, 
  public.paper, 
  public.paper_afiliacion
WHERE 
  paper.id = paper_afiliacion.paper_id AND
  paper_afiliacion.afiliacion_id = afiliacion.id;""")
  
resultado = []
  
for i in pimpri:
    
    resultado += [[i[0],i[1],i[2],i[3], i[4]]]
    
import os

path = os.path.abspath('parageo.txt')
f = open(path,'w')
f.write(str(resultado))  
  
