import pandas as pd
import os
import re          
import smtplib
from datetime import datetime
from email.message import EmailMessage


class ProcesadorDatosEntregas():
    MESES = {
        'Enero': '01',
        'Febrero': '02',
        'Marzo': '03',
        'Abril': '04',
        'Mayo': '05',
        'Junio': '06',
        'Julio': '07',
        'Agosto': '08',
        'Septiembre': '09',
        'Octubre': '10',
        'Noviembre': '11',
        'Diciembre': '12'
    }
    
    def __init__(self, archivo_entrada):
        self.archivo_entrada = archivo_entrada
        self.datos = None
        self.datos_procesados = None

    def convertir_fecha(self, fecha):
        """
        Convierte una fecha en distintos formatos a 'YYYY-MM-DD'.
        Si la fecha ya está en formato datetime, la convierte al formato deseado.
        """
        if isinstance(fecha, datetime):
            return fecha.strftime("%Y-%m-%d")

        # Si es una cadena, procesamos como antes
        componentes = re.split(r'[\s,/-]+', fecha)
        for mes in componentes:
            if mes in ProcesadorDatosEntregas.MESES.keys():
                componentes[componentes.index(mes)] = ProcesadorDatosEntregas.MESES[mes]
            if len(str(mes)) == 4:
                componentes.insert(0, componentes.pop(componentes.index(mes)))

        componentes = '/'.join(componentes)

        formatos = ["%Y/%d/%m", "%Y/%m/%d"]
        for fmt in formatos:
            try:
                fecha = datetime.strptime(componentes, fmt)
                return fecha.strftime("%Y-%m-%d")
            except ValueError:
                pass


    def limpiar_valor(self, valor):
        """
        Convierte el valor a un número decimal con dos dígitos.
        """
        if isinstance(valor, str):
            valor = valor.replace(".", "").replace(",", ".")
        try:
            num = float(valor)
            return round(num, 2)
        except Exception as e:
            raise ValueError(f"Error al convertir el valor: {valor}") from e

    def procesar_datos(self):
        """
        Lee el archivo Excel, aplica las transformaciones necesarias y elimina filas con estado 'Devuelto'.
        """
        self.datos = pd.read_excel(self.archivo_entrada)
        self.datos["Fecha_Pedido"] = self.datos["Fecha_Pedido"].apply(self.convertir_fecha)
        self.datos["Cliente"] = self.datos["Cliente"].str.strip()
        self.datos["Valor"] = self.datos["Valor"].apply(self.limpiar_valor)
        self.datos_procesados = self.datos[self.datos["Estado_Entrega"].str.strip().str.lower() != "devuelto"].copy()

    def guardar_archivo_procesado(self, archivo_salida):
        """
        Guarda el DataFrame procesado en un archivo Excel.
        """
        if self.datos_procesados is not None:
            self.datos_procesados.to_excel(archivo_salida, index=False)
            print(f"Archivo procesado guardado en {archivo_salida}")
        else:
            print("No hay datos procesados para guardar.")


class EnviarCorreo:
    def __init__(self, sender_email, password=None):
        """
        Inicializa la clase con las credenciales.
        Si no se proporciona la contraseña, se solicita manualmente.
        """
        self.sender_email = sender_email
        if password is None:
            # Solicita la contraseña manualmente si no se proporciona como argumento
            password = input("Ingresa la contraseña de tu correo: ")
        self.password = password

    def enviar_correo(self, destinatario, asunto, cuerpo):
        """
        Envía un correo electrónico utilizando las credenciales y el servidor SMTP de Gmail.
        """
        try:
            # Crear el mensaje de correo utilizando EmailMessage
            msg = EmailMessage()
            msg.set_content(cuerpo)
            msg['From'] = self.sender_email
            msg['To'] = destinatario
            msg['Subject'] = asunto

            # Configurar el servidor SMTP de Gmail
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Iniciar TLS
                server.login(self.sender_email, self.password)
                server.send_message(msg)

            print(f"Correo enviado a {destinatario}.")
        except Exception as e:
            print(f"Error al enviar el correo a {destinatario}: {e}")

    def enviar_correos_desde_dataframe(self, df):
        """
        Envía correos electrónicos a los clientes del DataFrame según el estado de la entrega.
        """
        for index, row in df.iterrows():
            if row['Estado_Entrega'] == 'Pendiente':
                cliente = row['Cliente']
                correo_cliente = row['Correo_Cliente']
                asunto = "Tu pedido está en camino 🚚"
                cuerpo = (
                    f"Hola {cliente},\n\n"
                    f"Tu pedido con ID {row['ID_Entrega']} está en camino y será entregado pronto.\n\n"
                    "Gracias por confiar en nosotros."
                )
                self.enviar_correo(correo_cliente, asunto, cuerpo)
            
            elif row['Estado_Entrega'] == 'Entregado':
                cliente = row['Cliente']
                correo_cliente = row['Correo_Cliente']
                asunto = "Tu pedido ha sido entregado 🎉"
                cuerpo = (
                    f"Hola {cliente},\n\n"
                    f"Tu pedido con ID {row['ID_Entrega']} ha sido entregado con éxito.\n\n"
                    "Gracias por confiar en nosotros."
                )
                self.enviar_correo(correo_cliente, asunto, cuerpo)
            else:
                print(f"Pedido {row['ID_Entrega']} no tiene correo enviado debido a estado 'Devuelto' o no válido.")
                
                
class GeneradorReporte:
    def __init__(self, datos):
        self.datos = datos
        self.reporte = ""

    def generar_reporte(self):
        """
        Genera un reporte resumen con:
        - Número total de entregas procesadas.
        - Ciudades con más entregas pendientes.
        - Monto total de entregas realizadas (solo 'Entregado').
        """
        total_entregas = len(self.datos)
        pendientes = self.datos[self.datos["Estado_Entrega"].str.strip().str.lower() == "pendiente"]
        conteo_ciudades = pendientes["Ciudad"].value_counts()
        entregadas = self.datos[self.datos["Estado_Entrega"].str.strip().str.lower() == "entregado"]
        monto_total = entregadas["Valor"].sum()

        lineas_reporte = []
        lineas_reporte.append(f"Total de entregas procesadas: {total_entregas}")
        lineas_reporte.append("Ciudades con más entregas pendientes:")
        for ciudad, cantidad in conteo_ciudades.items():
            lineas_reporte.append(f"- {ciudad}: {cantidad}")
        lineas_reporte.append(f"Monto total de entregas realizadas: {monto_total:.2f}")

        self.reporte = "\n".join(lineas_reporte)
        return self.reporte

    def guardar_reporte(self, archivo_reporte):
        """
        Guarda el reporte generado en un archivo de texto.
        """
        if not self.reporte:
            self.generar_reporte()
        with open(archivo_reporte, "w", encoding="utf-8") as f:
            f.write(self.reporte)
        print(f"Reporte guardado en {archivo_reporte}")
        print("\nReporte Resumen:")
        print(self.reporte)


def main():
    archivo_entrada = 'entregas_pendientes.xlsx'
    archivo_salida = 'entregas_procesadas.xlsx'
    
    # Procesamiento de datos
    procesador = ProcesadorDatosEntregas(archivo_entrada)
    procesador.procesar_datos()
    procesador.guardar_archivo_procesado(archivo_salida)

    # Enviar correos a los clientes según el estado de la entrega
    sender_email = "rodriguezvivasbrianjourneyt@gmail.com"  # Asegúrate de usar un correo válido
    # O bien, pasar la contraseña directamente:
    enviar_correo_obj = EnviarCorreo(sender_email, "bvhc kzhg qwfl lfbg")
    # enviar_correo_obj = EnviarCorreo(sender_email)
    
    enviar_correo_obj.enviar_correos_desde_dataframe(procesador.datos_procesados)
    generador_reporte = GeneradorReporte(procesador.datos_procesados)
    reporte = generador_reporte.generar_reporte()
    print("Reporte Generado:")
    print(reporte)
    
    # Opcional: guardar el reporte en un archivo de texto
    generador_reporte.guardar_reporte("reporte.txt")

if __name__ == '__main__':
    main()
