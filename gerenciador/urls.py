from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("alunos",views.AlunoViewSet)

urlpatterns = [
    path("", views.escolas_page),
    path('api/escolas/<int:pk>/', views.deletar_escola, name='deletar_escola'),
    path('api/escolas/', views.lista_escolas, name='lista_escolas'),


    path('api/escolas/<int:escola_id>/turmas/', views.lista_turmas, name='lista_turmas'),
    path('api/escolas/<int:escola_id>/turmas/<int:pk>/', views.deletar_turma, name='deletar_turma'),
    path("escolas/<int:escola_id>/turmas/", views.turmas_page)
    

]                                                                                                                                                   