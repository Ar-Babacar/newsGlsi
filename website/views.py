from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Article, User
from . import db
views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    articles = Article.query.all()
    return render_template("home.html", user=current_user, articles=articles)

@views.route("/create-article", methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        titre = request.form.get('titre')
        categorie = request.form.get('categorie')
        text = request.form.get('text')
        
        if not titre:
            flash("Veuillez entrer le titre de l article", category='error')
        elif not categorie :
            flash("Veuillez entrer la categorie de l article", category='error')
        elif not text:
            flash("Veuillez entrer la categorie de l article", category='error')
        else:
            article= Article(titre=titre, categorie=categorie, text=text, author=current_user.id)
            db.session.add(article)
            db.session.commit()
            flash('Article cree avec succe', category='success')
            return redirect(url_for('views.home'))
    
    return render_template("create_article.html", user=current_user)

@views.route("/delete-article/<id>")
@login_required
def delete_article(id):
    article = Article.query.filter_by(id=id).first()
    
    if not article:
        flash("Cet article n esxiste pas", category='error')
        
    elif current_user.id != article.id:
        flash("Vous n etes pas autorise a supprimer ce article", category='error')
    else:
        db.session.delete(article)
        db.session.commit()
        flash("Article supprime", category='success')
        
    return redirect(url_for('views.home'))

@views.route("/articles/<username>")
@login_required
def articles(username):
    user = User.query.filter_by(username=username).first()
    
    
    if not user:
        flash("Cet utilisateur n existe pas", category='error')
        return redirect(url_for('views.home'))
    articles = Article.query.filter_by(author=user.id).all()
    return render_template("articles.html", user=current_user, articles=articles, username=username)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     