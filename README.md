# Procesador de Entregas y Envío de Correos

## Descripción

Este proyecto procesa un archivo Excel con información de entregas, aplicando transformaciones para limpiar y normalizar los datos, generar un archivo con la información corregida, enviar correos automáticos a los clientes según el estado de la entrega y crear un reporte resumen.

## Tabla de Contenidos

- [Estructura del Archivo Excel](#estructura-del-archivo-excel)
- [Transformaciones y Funcionalidades](#transformaciones-y-funcionalidades)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Requisitos y Dependencias](#requisitos-y-dependencias)
- [Contacto](#contacto)

## Estructura del Archivo Excel

El archivo Excel de entrada (por ejemplo, `entregas_pendientes.xlsx`) debe contener las siguientes columnas:

- **ID_Entrega**: Identificador único de la entrega.
- **Fecha_Pedido**: Fecha del pedido en distintos formatos (e.g., `2025/02/15`, `15-02-2025`, `Febrero 15, 2025`).
- **Cliente**: Nombre del cliente (se eliminarán espacios innecesarios).
- **Correo_Cliente**: Dirección de correo electrónico del cliente.
- **Ciudad**: Ciudad de destino de la entrega.
- **Estado_Entrega**: Estado de la entrega; puede ser `Pendiente`, `Entregado` o `Devuelto`.
- **Valor**: Precio de la entrega, que se unificará a un formato decimal (con punto y dos decimales).

## Transformaciones y Funcionalidades

El código realiza las siguientes operaciones:

1. **Lectura y Procesamiento de Datos**:
   - Lee el archivo Excel de entregas.
   - Convierte la columna `Fecha_Pedido` a formato `YYYY-MM-DD`.
   - Limpia la columna `Cliente` eliminando espacios adicionales.
   - Normaliza el campo `Valor` a un número decimal con dos dígitos.
   - Elimina las filas donde `Estado_Entrega` es `Devuelto`.

2. **Generación de Archivo Procesado**:
   - Crea un nuevo archivo Excel (por ejemplo, `datos_procesados.xlsx` o `entregas_procesadas.xlsx`) con los datos corregidos y organizados.

3. **Envío Automático de Correos**:
   - **Si el estado es "Entregado":**
     - **Asunto:** "Tu pedido ha sido entregado 🎉"
     - **Cuerpo:** Se notifica al cliente que su pedido (identificado con `ID_Entrega`) ha sido entregado exitosamente.
   - **Si el estado es "Pendiente":**
     - **Asunto:** "Tu pedido está en camino 🚚"
     - **Cuerpo:** Se informa al cliente que su pedido está en camino y será entregado pronto.
   - **Para entregas "Devuelto":** No se envía correo.

4. **Generación de Reporte Resumen**:
   - Se genera un reporte (mostrado en consola y/o guardado en un archivo `reporte.txt`) que incluye:
     - Número total de entregas procesadas.
     - Ciudades con mayor cantidad de entregas pendientes.
     - Monto total de las entregas realizadas (sólo aquellas con estado `Entregado`).

## Instalación y Ejecución
Sigue estos pasos para instalar y configurar el proyecto:

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/brianrodriguezvivas/plaza_medicina.git
    ```

2. **Accede a la carpeta del proyecto**:
    ```bash
    cd entrevista
    ```

3. **Instala las dependencias**:
    
    ```bash
    pip install -r requirements.txt
    ```

## Requisitos y Dependencias

- **Python 3.x**  
- Las siguientes librerías:
  - `pandas`
  - `openpyxl` (para manipular archivos Excel)
  - `smtplib` y `email` (para el envío de correos)
  - `datetime` y `re` (para el procesamiento de fechas y cadenas)


## Contacto

- **Autor**: [Brian Journeyt Rodriguez Vivas ](brianjourneytrodriguezvivas@gmial.com)
- **Repositorio**: [https://github.com/brianrodriguezvivas/plaza_medicina](https://github.com/brianrodriguezvivas/plaza_medicina)




## Documentación Adicional

Para obtener más información sobre las clases y métodos disponibles, consulta la [documentación completa](Docs).
