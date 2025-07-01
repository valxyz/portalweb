from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy() # Creamos una instancia aquí, la app la configurará.

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Text, nullable=False, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'

    # Relación a los registros de login
    # 'Login' es el nombre de la clase del modelo para la tabla 'Logins'
    login_records = db.relationship('Login', backref='user', lazy='dynamic', order_by="desc(Login.session_started_at)")

    profile = db.relationship(
        'Profile',  # Name of the related class (Profile model)
        backref=db.backref('user', uselist=False),  # Creates 'user' attribute on Profile instances
        lazy=True,
        cascade="all, delete-orphan"  # Ensures profile is deleted if user is deleted
    )
    
    def get_current_active_session(self):
        # Retorna el objeto Login de la sesión activa, si existe
        return self.login_records.filter_by(is_active=True).first()

    def is_logged_in(self):
        # Verifica si el usuario tiene alguna sesión activa
        return self.login_records.filter_by(is_active=True).count() > 0
    
    # ¡¡ADVERTENCIA!! Estos métodos son para contraseñas HASHEADAS.
    # Si estás guardando texto plano, NO los uses así.
    # Los dejo aquí como recordatorio de a dónde debes ir.
    # def set_password(self, password_to_hash):
    #     from werkzeug.security import generate_password_hash
    #     self.password = generate_password_hash(password_to_hash) # Asumiría que 'password' es 'password_hash'

    # def check_password(self, password_to_check):
    #     from werkzeug.security import check_password_hash
    #     return check_password_hash(self.password, password_to_check) # Asumiría que 'password' es 'password_hash'


class Login(db.Model): # Modelo para tu tabla 'Logins'
    __tablename__ = 'Logins'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False) # ondelete en el modelo también
    ip_address = db.Column(db.String(45), nullable=False) # Usar String con longitud en SQLAlchemy
    user_agent = db.Column(db.Text, nullable=True)
    session_started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    session_ended_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False) # SQLAlchemy usa Boolean para INTEGER 0/1


class Profile(db.Model):
    __tablename__ = 'Profiles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id is a foreign key to Users.id and must be unique for a one-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False, unique=True)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    card_id = db.Column(db.Text, nullable=True) # For Cedula/ID card
    phone_number = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True, unique=True) # Email should ideally be unique

    # The backref 'user' in the User model's profile relationship
    # already provides access from Profile back to User (e.g., profile_instance.user)

    def __repr__(self):
        return f'<Profile id={self.id} user_id={self.user_id} email={self.email}>'
