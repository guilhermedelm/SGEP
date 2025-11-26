


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aluno(models.Model):
    aluno_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=120, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    telefone_pai = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aluno'


class Avaliacao(models.Model):

    matricula_id = models.ForeignKey('Matricula', models.DO_NOTHING)
    avaliacao = models.CharField(max_length=20)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data_avaliacao = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'avaliacao'
        unique_together =(('matricula_id', 'avaliacao'),)


class Disciplina(models.Model):
    disciplina_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'disciplina'


class Endereco(models.Model):
    endereco_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, models.DO_NOTHING)
    estado = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.CharField(max_length=60, blank=True, null=True)
    bairro = models.CharField(max_length=70, blank=True, null=True)
    rua = models.CharField(max_length=70, blank=True, null=True)
    casa = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'endereco'


class Escola(models.Model):
    escola_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(unique=True, max_length=14)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    cep = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escola'


class Matricula(models.Model):
    matricula_id = models.AutoField(primary_key=True)
    turma = models.ForeignKey('Turma', models.DO_NOTHING)
    aluno = models.ForeignKey(Aluno, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'matricula'


class Presenca(models.Model):
    matricula = models.ForeignKey('Matricula', models.DO_NOTHING)
    disciplina = models.ForeignKey('Disciplina', models.DO_NOTHING)
    data_aula = models.DateField()
    presente = models.BooleanField(blank=True, null=True)
    justificada = models.BooleanField(blank=True, null=True)
    justificativa = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'presenca'
        unique_together = (('matricula', 'disciplina', 'data_aula'),)


class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    cpf = models.CharField(unique=True, max_length=11)
    nome = models.CharField(max_length=30)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=120, blank=True, null=True)
    endereco = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'professor'


class Turma(models.Model):
    turma_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20, blank=True, null=True)
    data_inicio = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    periodo = models.CharField(max_length=20, blank=True, null=True)
    escola = models.ForeignKey(Escola, models.DO_NOTHING)
    capacidade = models.SmallIntegerField(blank=True, null=True)
    capacidade_max = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'turma'


class TurmaDisciplina(models.Model):
    disciplina = models.ForeignKey('Disciplina', models.DO_NOTHING)
    turma = models.ForeignKey('Turma', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'turma_disciplina'
        unique_together = (('turma', 'disciplina'),)


class TurmaProfessor(models.Model):
    turma = models.ForeignKey(Turma, models.DO_NOTHING)
    professor = models.ForeignKey(Professor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'turma_professor'
        unique_together = (('turma', 'professor'))
