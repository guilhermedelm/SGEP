from rest_framework import serializers
from .models import Aluno,Escola

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola 
        fields = "__all__"
