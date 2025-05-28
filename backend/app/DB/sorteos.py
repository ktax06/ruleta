from flask import jsonify, current_app
import psycopg2
import os
import logging
from dateutil import parser

def subir_sorteo(datos_sorteo):
    conn = None
    try:
        if 'fecha' in datos_sorteo:
            try:
                # Normaliza sufijos de hora en español a inglés
                fecha_str = datos_sorteo['fecha'].replace('a.m.', 'AM').replace('p.m.', 'PM')
                fecha_obj = parser.parse(fecha_str)
                datos_sorteo['fecha'] = fecha_obj.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                current_app.logger.error(f"Error al formatear la fecha: {e}")
                return None
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO sorteo (fecha, categoria, incidencia, grupo, alumno, mensaje) 
            VALUES (%(fecha)s, %(categoria)s, %(incidencia)s, %(grupo)s, %(alumno)s, %(mensaje)s)
            """,
            datos_sorteo
        )
        conn.commit()
        cur.close()
        return "Sorteo subido correctamente"
    except (Exception, psycopg2.DatabaseError) as error:
        current_app.logger.error(f"Error al subir el sorteo: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()

def obtener_sorteos():
    conn = None
    sorteos = []
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("SELECT * FROM sorteo")
        rows = cur.fetchall()
        for row in rows:
            sorteos.append({
                'id': row[0],
                'fecha': row[1],
                'categoria': row[2],
                'incidencia': row[3],
                'grupo': row[4],
                'alumno': row[5],
                'mensaje': row[6],
            })
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        current_app.logger.error(f"Error al obtener los sorteos: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()
    return sorteos