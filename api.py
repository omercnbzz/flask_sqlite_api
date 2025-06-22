# Flask uygulaması ve gerekli eklentileri import et
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy  # ORM için
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort  # REST API araçları

app = Flask(__name__)  # Flask uygulama örneği oluştur
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite veritabanı konfigürasyonu
db = SQLAlchemy(app)  # SQLAlchemy'yi uygulamaya bağla
api = Api(app)  # RESTful API örneği oluştur

# Kullanıcı veri modelini tanımla
class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(80), unique=True, nullable=False)  # Benzersiz isim
    email = db.Column(db.String(80), unique=True, nullable=False)  # Benzersiz email

    def __repr__(self): 
        return f"User(name = {self.name}, email = {self.email})"  # Nesne gösterimi

# İstek verisi ayrıştırıcı (POST/PATCH için)
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")  # Zorunlu name alanı
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")  # Zorunlu email alanı

# API çıktı formatı (JSON serialization için)
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

# Tüm kullanıcıları yöneten endpoint (/api/users/)
class Users(Resource):
    @marshal_with(userFields)  # Çıktıyı userFields formatında dönüştür
    def get(self):
        users = UserModel.query.all()  # Tüm kullanıcıları veritabanından çek
        return users  # Otomatik JSON'a dönüşür
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()  # Gelen veriyi doğrula
        # Yeni kullanıcı oluştur
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)  # Veritabanına ekle
        db.session.commit()  # Değişiklikleri kaydet
        users = UserModel.query.all()  # Güncel listeyi al
        return users, 201  # 201 Created status kodu ile dön

# Tekil kullanıcı yönetimi (/api/users/<id>)
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()  # ID'ye göre kullanıcı ara
        if not user: 
            abort(404, message="User not found")  # 404 hata mesajı
        return user 
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()  # Güncelleme verisini al
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        # Kullanıcı bilgilerini güncelle
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()  # Değişiklikleri kaydet
        return user  # Güncellenmiş kullanıcıyı dön
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        db.session.delete(user)  # Kullanıcıyı sil
        db.session.commit()
        users = UserModel.query.all()  # Güncel kullanıcı listesini al
        return users  # Silme sonrası tüm listeyi dön

# API endpoint'lerini kaydet
api.add_resource(Users, '/api/users/')         # Çoğul endpoint
api.add_resource(User, '/api/users/<int:id>')   # Tekil endpoint

# Kök dizin için basit HTML response
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'  # Ana sayfa mesajı

# Uygulamayı çalıştır (sadece main modülünde)
if __name__ == '__main__':
    app.run(debug=True)  # Debug modunda çalıştır
