from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment
import random


def todo():
    User.objects.all().delete()
    Category.objects.all().delete()

    jimmy_user = User.objects.create_user(username='jimmy', email='jimmy@mail.ru', password='jimmy_password')
    fred_user = User.objects.create_user(username='fred', email='fred@mail.ru', password='fred_password')

    jimmy = Author.objects.create(user=jimmy_user)
    fred = Author.objects.create(user=fred_user)

    cat_sport = Category.objects.create(name="Спорт")
    cat_music = Category.objects.create(name="Музыка")
    cat_cinema = Category.objects.create(name="Кино")
    cat_IT = Category.objects.create(name="IT")

    text_article_sport_cinema = """статья_спорт_кино_Джимми__статья_спорт_кино_Джимми__статья_спорт_кино_Джимми_
                                   _статья_спорт_кино_Джимми__статья_спорт_кино_Джимми__"""

    text_article_music = """статья_музыка_Томми__статья_музыка_Томми__статья_музыка_Томми_
                            _статья_музыка_Томми__статья_музыка_Томми__"""

    text_news_IT = """новость_IT_Фред__новость_IT_Фред__новость_IT_Фред__новость_IT_Фред__
                    новость_IT_Фред__новость_IT_Фред__новость_IT_Фред__новость_IT_Фред__"""

    article_jimmy = Post.objects.create(author=jimmy, post_type=Post.article, title="статья_спорт_кино_Джимми",
                                        text=text_article_sport_cinema)
    article_fred = Post.objects.create(author=fred, post_type=Post.article, title="статья_музыка_Фред",
                                        text=text_article_music)
    news_fred = Post.objects.create(author=fred, post_type=Post.news, title="новость_IT_Томми", text=text_news_IT)

    PostCategory.objects.create(post=article_jimmy, category=cat_sport)
    PostCategory.objects.create(post=article_jimmy, category=cat_cinema)
    PostCategory.objects.create(post=article_fred, category=cat_music)
    PostCategory.objects.create(post=news_fred, category=cat_IT)

    comment1 = Comment.objects.create(post=article_jimmy, user=fred.user, text="коммент Томми №1 к статье Джимми")
    comment2 = Comment.objects.create(post=article_fred, user=jimmy.user, text="коммент Джимми №2 к статье Томми")
    comment3 = Comment.objects.create(post=news_fred, user=fred.user, text="коммент Томми №3 к новости Томми")
    comment4 = Comment.objects.create(post=news_fred, user=jimmy.user, text="коммент Джимми №4 к новости Томми")

    list_for_like = [article_jimmy,
                     article_fred,
                     news_fred,
                     comment1,
                     comment2,
                     comment3,
                     comment4]

    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()

    rating_jimmy = (sum([post.rating * 3 for post in Post.objects.filter(author=jimmy)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=jimmy.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=jimmy)]))
    jimmy.update_rating(rating_jimmy)

    rating_fred = (sum([post.rating * 3 for post in Post.objects.filter(author=fred)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=fred.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=fred)]))
    fred.update_rating(rating_fred)

    best_author = Author.objects.all().order_by('-rating')[0]

    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")

    best_article = Post.objects.filter(post_type=Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.created)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")

    print("Комментарии к ней")
    for comment in Comment.objects.filter(post=best_article):
        print("Дата:", comment.created)
        print("Автор:", comment.user.username)
        print("Рейтинг:", comment.rating)
        print("Комментарий:", comment.text)
        print("")
