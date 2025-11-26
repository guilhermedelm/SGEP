from django import forms
from .models import Aluno, Turma

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = "__all__"

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = "__all__"