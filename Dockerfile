# Usando uma versão estável e slim do Python
FROM python:3.11-slim

# Instalando as dependências com os nomes atualizados para o Debian mais novo
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usando o formato JSON (entre colchetes) para o CMD 
# Isso resolve o aviso "JSONArgsRecommended" e ajuda no gerenciamento de sinais do SRE
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000"]