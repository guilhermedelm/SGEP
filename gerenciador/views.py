from django.shortcuts import render,redirect,get_object_or_404
from .models import Aluno,Turma
from rest_framework import viewsets
from .serializers import AlunoSerializer

# Create your views here.


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


def alunos_page(request):
    return render(request, "alunos.html")



