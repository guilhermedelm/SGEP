from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register("alunos",views.AlunoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("alunos/",views.alunos_page,name = "alunos")
]                                                                                                                                                   