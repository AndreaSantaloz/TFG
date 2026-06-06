FROM python:3.10-slim

# Instalar las librerías científicas que necesitas
RUN pip install --no-cache-dir numpy pandas scipy

# Dejar el contenedor listo
WORKDIR /app
CMD ["sh", "-c", "mkdir -p /app && tail -f /dev/null"]