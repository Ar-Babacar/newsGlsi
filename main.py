from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#creation de l'app

app = Flask(__name__)
api = Api(app)
#Creation de ma bdd dans mon dossier local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Creation d'un modele pour nos articles
class ArticleModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Titre = db.Column(db.String(50), nullable = False)
    Categorie = db.Column(db.String(30), nullable = False)
    Contenu = db.Column(db.String(500), nullable = False)
    
    def __repr__(self):
        return f"Article(Titre = {Titre}, Categorie = {Categorie}, Contenu = {Contenu})"
#permet de creer la base en fonction du modele donne.A ne faire qu'une fois
#db.create_all()

article_put_args = reqparse.RequestParser()
article_put_args.add_argument("Titre", type = str, help = "Veuillez entrer le titre de l'article", required = True)
article_put_args.add_argument("Categorie", type = str, help = "Veuillez preciser la categorie de l'article", required = True)
article_put_args.add_argument("Contenu", type = str, help = "Veuillez entrer le contenu de l'article", required = True)


article_update_args = reqparse.RequestParser()
article_update_args.add_argument("Titre", type = str, help = "Veuillez entrer le titre de l'article")
article_update_args.add_argument("Categorie", type = str, help = "Veuillez preciser la categorie de l'article")
article_update_args.add_argument("Contenu", type = str, help = "Veuillez entrer le contenu de l'article")

#Serialisation des Donnees

resource_fields = {
    'id': fields.String,
    'Titre': fields.String,
    'Categorie': fields.String,
    'Contenu': fields.String
    }

#Creattion de ressources 
class Article(Resource):
    
    @marshal_with(resource_fields)
    def get(self, article_id):
        result = ArticleModel.query.filter_by(id = article_id).first()
        if not result:
            abort(404, message="Cet id ne correspond a aucun article")
        return result
    @marshal_with(resource_fields)
    def put(self, article_id):
        args = article_put_args.parse_args()
        result = ArticleModel.query.filter_by(id = article_id).first()
        if result:
            abort(409, message="Cet Article existe deja")
        article = ArticleModel(id=article_id, Titre=args['Titre'], Categorie=args['Categorie'], Contenu=args['Contenu'])
        db.session.add(article)
        db.session.commit()
        return article, 201
    
    @marshal_with(resource_fields)
    def patch(self, article_id):
        args = article_update_args.parse_args()
        result = ArticleModel.query.filter_by(id = article_id).first()
        if not result:
            abort(404, message="Cet article n'existe pas, impossible de mettre a jour")
        if args['Titre']:
            result.Titre = args['Titre']
        if args['Categorie']:
            result.Categorie = args['Categorie']
        if args['Contenu']:
            result.Contenu = args['Contenu']
        db.session.commit()
        return result
            
    def delete(self, article_id):
        abort_si_art_existe_pas(article_id)
        del Articles[article_id]
        return '', 204
    
#AJOUT DE LA RESSOURCE A L'API
api.add_resource(Article, "/article/<int:article_id>")

#permet de lancer notre app et le server en mode debug()
if __name__ == "__main__":
    app.run(debug=True)