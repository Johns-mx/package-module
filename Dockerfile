# Usa la imagen base de Python adecuada
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto al contenedor
COPY . .

# Exponer el puerto en el que se ejecuta tu aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "Api.main:app", "--host", "0.0.0.0", "--port", "8000"]
