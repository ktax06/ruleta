from flask import jsonify, current_app
import psycopg2
import os
import logging


def obtener_estadisticas():
    conn = None
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        
        # Frecuencia por categoría
        cur.execute("SELECT categoria, COUNT(*) FROM sorteo GROUP BY categoria")
        categorias = cur.fetchall()
        freq_categoria = {
            "titulo": "Frecuencia por Categoría",
            "datos": {
                "x": [row[0] for row in categorias],
                "y": [row[1] for row in categorias]
            }
        }
        
        # Frecuencia de incidencias en general
        cur.execute("SELECT incidencia, COUNT(*) FROM sorteo GROUP BY incidencia")
        incidencias_gen = cur.fetchall()
        freq_incidencias = {
            "titulo": "Frecuencia de Incidencias",
            "datos": {
                "x": [row[0] for row in incidencias_gen],
                "y": [row[1] for row in incidencias_gen]
            }
        }

        # Frecuencia de incidencias por categoría
        cur.execute("SELECT categoria, incidencia, COUNT(*) FROM sorteo GROUP BY categoria, incidencia")
        incidencias = cur.fetchall()
        # Agrupar por categoría
        incidencias_por_categoria = {}
        for cat, inc, count in incidencias:
            if cat not in incidencias_por_categoria:
                incidencias_por_categoria[cat] = {"x": [], "y": []}
            incidencias_por_categoria[cat]["x"].append(inc)
            incidencias_por_categoria[cat]["y"].append(count)
        freq_incidencia_categoria = [
            {
                "titulo": f"Frecuencia de Incidencias en {cat}",
                "datos": data
            }
            for cat, data in incidencias_por_categoria.items()
        ]

        
        resultado = [freq_categoria] + freq_incidencia_categoria + [freq_incidencias]

        return jsonify(resultado)

    except Exception as e:
        logging.error(f"Error obteniendo estadísticas: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()