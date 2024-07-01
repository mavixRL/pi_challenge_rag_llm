# Usar la imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos de requisitos primero para aprovechar la caché de Docker
# COPY requirements.txt .
COPY requirements/base.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r base.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto 80 para la aplicación
EXPOSE 8007

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
