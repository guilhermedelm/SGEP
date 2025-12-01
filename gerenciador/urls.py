from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


from SGEP import settings
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

    path("escolas/<int:escola_id>/turmas/<int:turma_id>/alunos/<int:aluno_id>/",views.aluno_page,name="aluno_page"),

    # API DISCIPLINAS
    path('api/disciplinas/', views.listar_disciplinas, name='listar_disciplinas'),

    # API AVALIAÇÕES
    path('api/avaliacoes/<int:matricula_id>/', views.lista_avaliacoes, name='lista_avaliacoes'),
    path('api/avaliacoes/<int:matricula_id>/<int:disciplina_id>/<str:avaliacao_nome>/', views.deletar_avaliacao, name='deletar_avaliacao'),

        # Endpoints de disciplinas
    path('api/listar_disciplinas/', views.listar_disciplinas, name='listar_disciplinas'),

    # Endpoints de disciplinas por turma
    path('api/turmas/<int:turma_id>/disciplinas/', views.turma_disciplinas, name='turma_disciplinas'),

    path('api/alunos/<int:aluno_id>/enderecos',views.lista_endereco, name = 'lista_enderecos'),
    path('api/alunos/<int:aluno_id>/enderecos/<int:endereco_id',views.deletar_endereco, name = 'apagar_enderecos')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
