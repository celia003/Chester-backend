import json
import uuid
import logging
from requests_pkcs12 import post


class NOGASRestNotificationApi:
    def __init__(self, service_endpoint, connection_keystore_path, connection_keystore_password,
                 connection_keystore_type):
        #  , connection_truststore_path, connection_truststore_password,connection_truststore_type
        self.service_endpoint = service_endpoint
        self.connection_keystore_path = connection_keystore_path
        self.connection_keystore_password = connection_keystore_password
        self.connection_keystore_type = connection_keystore_type
        # self.connection_truststore_path = connection_truststore_path
        # self.connection_truststore_password = connection_truststore_password
        # self.connection_truststore_type = connection_truststore_type

   
    def send_basic_text_message(self, to, message ):
        try:
            url = f"{self.service_endpoint}/SendBasicTextMessage"

            # Construir el objeto de la solicitud
            request_data = {
                "addressee": to,
                "message": message,
                "tokenId": str(uuid.uuid4()),  
                "userId": "OI_CSS",
                "profileId": "OI_CSS"
            }

            # Convierte el diccionario a una cadena JSON
            request_data_json = json.dumps(request_data)

            response = post(
                url,
                data=request_data_json, 
                headers={'Content-Type': 'application/json'},
                verify=False,
                pkcs12_filename=self.connection_keystore_path,
                pkcs12_password=self.connection_keystore_password
            )
            #  verify=(self.connection_truststore_path, self.connection_truststore_password)
            # )

            # Manejar la respuesta según sea necesario

            status_code = response.status_code
            if status_code != 200 and status_code != 500:
                logging.error(
                    "Error obtenido del servicio NOGAS ==> Failed : HTTP error code : ", status_code)
            elif status_code == 500:
                logging.error(
                    "Error interno del servidor NOGAS (Internal Server Error)")
                print("Detalles adicionales: ", response.text)
            else:
                output = response.json()
                return output['messageId']

            response.raise_for_status()

            return response.json()
        except Exception as e:
           
            raise Exception("Error general en la petición.", e)
