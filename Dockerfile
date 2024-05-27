# Use a imagem oficial do Python como base
FROM python:3.8

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o script wait-for-it.sh para o container
COPY wait-for-it.sh /wait-for-it.sh


# Copia o restante do código do projeto para o container
COPY . .

# Expõe a porta que o Django vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

