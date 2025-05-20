from endpoints import Endpoints
from datetime import datetime, timedelta

import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
FATHER_PATH = os.path.dirname(ABS_PATH)
DATA_PATH = os.path.dirname(FATHER_PATH)
print(ABS_PATH)
print(FATHER_PATH)
print(DATA_PATH)

def main(): # Creamos una instancia de la clase Endpoint
    endpoint = Endpoints()
    # Realizamos el login
    response = endpoint.login()
    # # Obtenemos el reporte
    # start_date = datetime(2025, 4, 1)
    # end_date = datetime(2025, 4, 30)  # Adjust this date as needed

    # current_date = start_date

    # # Hacer peticiones por mes
    # while current_date < end_date:
    #     next_month = current_date + timedelta(days=31)
    #     next_month = next_month.replace(day=1)

    #     fecha_inicio = current_date.strftime("%Y-%m-%d")
    #     fecha_fin = (next_month - timedelta(days=1)).strftime("%Y-%m-%d")
        
    #     print('fecha inicio:', fecha_inicio)
    #     print('fecha fin:', fecha_fin)

    #     nombre_mes = current_date.strftime("%B")
    #     nombre_anio = current_date.strftime("%Y")

    #     print('nombre del mes:', nombre_mes)
    #     print('nombre del anio:', nombre_anio)

    #     name = f'Reporte {nombre_mes} {nombre_anio}'
    #     endpoint.obtener_reporte(name, fecha_inicio, fecha_fin)
    #     current_date = next_month

      
    #     # Luego cada mes procesarlo, dejar columnas importanes y guardarlo.
    #     ruta_archivo = os.path.join( FATHER_PATH+ "\\" + name + '.xls')
    #     data.delete_bloat_columns(ruta_archivo) 


if __name__ == "__main__":
    main()
