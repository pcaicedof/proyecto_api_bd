# Utiliza la imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY api_db/requirements.txt .

COPY api_db/ ./api_db

RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Inicia la aplicación cuando se ejecute el contenedor
CMD ["uvicorn", "api_db.main:app", "--host", "0.0.0.0", "--port", "8000"]