from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, username, password, nome, cognome, portafoglio, data_nascita ):
        self.id = id
        self.email = email
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.portafoglio = portafoglio
        self.data_nascita = data_nascita

