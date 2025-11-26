from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Aluno, Avaliacao, Disciplina, Endereco, Escola, Matricula,
    Presenca, Professor, Turma, TurmaDisciplina, TurmaProfessor
)

admin.site.register(Aluno)
admin.site.register(Avaliacao)
admin.site.register(Disciplina)
admin.site.register(Endereco)
admin.site.register(Escola)
admin.site.register(Matricula)
admin.site.register(Presenca)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(TurmaDisciplina)
admin.site.register(TurmaProfessor)