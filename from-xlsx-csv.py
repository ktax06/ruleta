import pandas as pd
import sys
import os
import csv

if len(sys.argv) < 2:
    print("Uso: python from-xlsx-csv.py archivo.xlsx")
    sys.exit(1)

xlsx_file = sys.argv[1]
excel = pd.ExcelFile(xlsx_file)

for sheet_name in excel.sheet_names:
    df = pd.read_excel(xlsx_file, sheet_name=sheet_name)
    # Mapea nombres de columnas normalizados a los originales
    col_map = {str(c).strip().lower(): c for c in df.columns}
    cols = list(col_map.keys())

    # Caso 1: categoria/subcategoria
    if set(cols) == {"categoria", "subcategoria"}:
        out_name = f"{sheet_name}.csv"
        with open(out_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Categoria", "Incidencia", "Observacion", "Carga"])
            for _, row in df.iterrows():
                writer.writerow([
                    row[col_map["categoria"]],
                    row[col_map["subcategoria"]],
                    "",  # Observacion vacío
                    ""   # Carga vacío
                ])
        print(f"Generado: {out_name}")

    # Caso 2: Grupo, Proyecto1, Proyecto2, NumIntegrantes, Integrante1...
    elif "grupo" in cols and any(c.startswith("integrante") for c in cols):
        out_name = f"{sheet_name}.csv"
        grupo_col = col_map["grupo"]
        integrante_cols = [col_map[c] for c in cols if c.startswith("integrante")]
        with open(out_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Grupo", "Integrante"])
            for _, row in df.iterrows():
                grupo = row[grupo_col]
                for ic in integrante_cols:
                    if pd.notnull(row[ic]):
                        writer.writerow([grupo, row[ic]])
        print(f"Generado: {out_name}")

    else:
        print(f"Hoja '{sheet_name}' no coincide con ninguna estructura esperada, omitida.")

print("¡Conversión completa!")