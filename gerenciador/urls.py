from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    # PÁGINAS
    path("", views.home_page, name="home"),  # página inicial (criar escola)
    path("escolas/<int:escola_id>/", views.escola_page, name="escola_page"),  # página da escola / lista de turmas
    path("escolas/<int:escola_id>/turmas/<int:turma_id>/", views.turma_page, name="turma_page"),  # página da turma

    # API ESCOLAS
    path("api/escolas/", views.lista_escolas, name="lista_escolas"),  # GET lista / POST criar escola
    path("api/escolas/<int:escola_id>/", views.deletar_escola, name="deletar_escola"),  # DELETE escola / GET detalhes escola

    # API TURMAS
    path("api/escolas/<int:escola_id>/turmas/", views.lista_turmas, name="lista_turmas"),  # GET lista / POST criar turma
    path("api/escolas/<int:escola_id>/turmas/<int:pk>/", views.deletar_turma, name="deletar_turma"),  # DELETE turma / GET detalhes turma

    # API ALUNOS
    path("api/alunos/", views.lista_alunos, name="lista_alunos"),          # GET lista / POST criar aluno
    path("api/alunos/<int:pk>/", views.detalhe_aluno, name="detalhe_aluno"),  # GET detalhes / DELETE aluno

    # API MATRICULAS
    path("api/turmas/<int:turma_id>/matriculas/", views.lista_matriculas, name="lista_matriculas"),
    path("api/turmas/<int:turma_id>/matriculas/<int:matricula_id>/", views.deletar_matricula, name="deletar_matricula"),

]
