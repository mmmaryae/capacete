
from CamCore import app, database

# Isso força a criação de todas as tabelas vazias no Render logo que o servidor ligar
with app.app_context():
    database.create_all()

if __name__ == "__main__":
    app.run(debug=True) #qualquer mudança feita já vai ser implantada