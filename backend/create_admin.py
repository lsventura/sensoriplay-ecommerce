import getpass

import bcrypt
from dotenv import load_dotenv

import database


def create_admin():
    """Cria um usuário admin na tabela users.

    Uso:
        python -m backend.create_admin
    (executar a partir da raiz do projeto, com DATABASE_URL configurada)
    """

    load_dotenv()

    if database.SessionLocal is None:
        print("DATABASE_URL não configurada. Defina a conexão com o PostgreSQL antes de criar um admin.")
        return

    name = input("Nome do admin: ")
    email = input("E-mail do admin: ")

    password = getpass.getpass("Senha: ")
    password_confirm = getpass.getpass("Confirme a senha: ")

    if password != password_confirm:
        print("As senhas não conferem. Tente novamente.")
        return

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    db = database.SessionLocal()
    try:
        existing = db.query(database.User).filter(database.User.email == email).first()
        if existing:
            print("Já existe um usuário com esse e-mail.")
            return

        admin_user = database.User(
            name=name,
            email=email,
            password_hash=password_hash,
            is_admin=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"Usuário admin criado com sucesso! ID: {admin_user.id}")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
