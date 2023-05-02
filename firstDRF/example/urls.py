from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet

from example.views import HelloAPI, booksAPI, bookAPI, BooksAPIMixins, BookAPIMixins, BooksAPIGenerics, BookAPIGenerics

# ViewSet
router = routers.SimpleRouter()
router.register('books', BookViewSet)
urlpatterns = [
    path('', include(router.urls))
]


urlpatterns = [

    # FBV
    path('hello/', HelloAPI),
    path('fbv/books/', booksAPI),
    path('fbv/book/<int:bid>', bookAPI),

    # CBV
    # path('cbv/books/', BooksAPI.as_view()),
    # path('cbv/book/<int:bid>', BookAPI.as_view()),

    # mixins
    path('mixin/books/', BooksAPIMixins.as_view()),
    path('mixin/book/<int:bid>/', BookAPIMixins.as_view()),

    # generics
    path('mixin/books/', BooksAPIGenerics.as_view()),
    path('mixin/book/<int:bid>/', BookAPIGenerics.as_view()),
]

