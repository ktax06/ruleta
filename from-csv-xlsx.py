import sys
import os
import pandas as pd

if len(sys.argv) < 2:
    print("Uso: python from-csv-xlsx.py archivo1.csv archivo2.csv ...")
    sys.exit(1)

excel_name = "incidencias.xlsx"
with pd.ExcelWriter(excel_name, engine='openpyxl') as writer:
    for csv_file in sys.argv[1:]:
        sheet_name = os.path.splitext(os.path.basename(csv_file))[0][:31]  # Excel limita a 31 caracteres
        df = pd.read_csv(csv_file)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"¡Archivo Excel generado como {excel_name} con {len(sys.argv)-1} hojas!")