import os
import requests
from datetime import datetime
from dotenv import load_dotenv

ABS_PATH = os.path.dirname(os.path.abspath(__file__))


class Endpoints:
    def __init__(self):
        
        load_dotenv()
        self.basePath = os.getenv("API_URL")
        self.baseURL  = f"{self.basePath}web/api"
        self.loginURL = f"{self.basePath}web/api/chess/v1/auth/login"
        self.credentials = {
            "usuario": os.getenv("USERNAME"), "password": os.getenv("PASSWORD")
        }
        self.sessionId = None
        self.depositos = {"1": ""}

    
    def login(self):
        try:
            # Realizamos la solicitud POST para loguearnos
            print("basePath:", self.basePath)
            print("loginUrl:", self.loginURL)
            response = requests.post(self.loginURL, json=self.credentials)

            # Verificamos si la respuesta es JSON y obtenemos el sessionId
            if response.status_code == 200:
                try:
                    # Intentamos extraer el sessionId del JSON
                    response_json = response.json()
                    sessionId = response_json.get("sessionId")  
                    self.sessionId = sessionId
                    self.response = response   
                    if sessionId:
                        print(f"SessionId obtenido: {sessionId}")
                        return response.json()

                    else:
                        print("Error: No se encontró 'sessionId' en la respuesta del servidor.")
                        
                except ValueError:
                    print("Error: La respuesta no es un JSON válido.")
                    
            else:
                print(f"Error en el login: {response.status_code}, Respuesta: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión o solicitud: {e}")
            
    
    def obtener_reporte(self, name, fecha_desde, fecha_hasta):
        # Formato fecha desde y hasta: "AAAA-MM-DD"
        reporte_url = self.baseURL + "/reporteComprobantesVta/exportarExcel"
        header = {"Cookie": self.sessionId}
        data_post = {
            "dsFiltrosRepCbtsVta": {
                "eFiltros": [
                    {
                        "letra": None,
                        "serie": None,
                        "numero": None,
                        "numeroHasta": None,
                        "fechadesde": fecha_desde,
                        "fechahasta": fecha_hasta,
                        "idsucur": "1,3,4,5,6,7,9,10,11,12,13,14,15,16",
                        "timbrado": "",
                        "empresas": "1",
                        "idsucur": "1",
                        "tiposdoc": "DVVTA,FCVTA",
                        "formasagruart": "MARCA,GENERICO,,,,,,,,"
                    }
                ]
            },
            "pcTipo": "D"
        }

        try:
            # Realizamos la solicitud POST para exportar el reporte
            response_reporte = requests.post(reporte_url, json=data_post, headers=header)

            # Comprobamos si la respuesta contiene el archivo para descargar
            if response_reporte.status_code == 200:
                # Extraemos el path del archivo del reporte
                response_json = response_reporte.json()
                pcArchivo = response_json.get("pcArchivo")
                
                if pcArchivo:
                    print(f"Archivo para descargar: {self.basePath + pcArchivo}")
                else:
                    print("Error: No se encontró 'pcArchivo' en la respuesta.")
                    exit()

                # Paso 3: Descargar el archivo
                archivo_url = self.basePath + pcArchivo
                response_excel = requests.get(archivo_url, headers=header)

                if response_excel.status_code == 200:
                    # Guardamos el archivo temporalmente
                    with open(f"{name}.xls", "wb") as f:
                        f.write(response_excel.content)
                    print("Archivo descargado correctamente.")

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión o solicitud: {e}")
            exit()
    
    def get_sessionId(self):
        return self.sessionId    

    def get_stock(self, date=datetime.now().strftime("%d-%m-%Y"), idDeposito="1"):
        stock_url = self.baseURL + "/chess/v1/stock/"
        headers = {"Cookie": self.sessionId}
        params = {
            "idDeposito": idDeposito,
            "frescura": "false",
            "DD-MM-AAAA": date 
        }
        try:
            params['idDeposito'] = idDeposito
            params['DD-MM-AAAA'] = date
            response = requests.get(url=stock_url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as error:
                print("Error processing stock", error)


if __name__ == "__main__":
    endpoint = Endpoints()
    endpoint.login()
    stock = endpoint.get_stock()
    print(endpoint.get_sessionId())
    print(stock)
    print(type(stock))

