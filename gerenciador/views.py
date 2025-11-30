from django.db import connection

from django.shortcuts import render,redirect,get_object_or_404
from .models import Aluno,Turma
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import AlunoSerializer, EscolaSerializer

# Create your views here.

def dict_fetchall(cursor):
    """
    Função auxiliar para converter resultado do cursor em lista de dicionários
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    """
    Função auxiliar para converter resultado do cursor em um dicionário
    """
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))




@api_view(['GET','POST'])
def lista_escolas(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT escola_id,nome,cnpj,telefone,email,cep FROM app.escola 
                    ORDER BY nome ASC
                ''')
                escolas = dict_fetchall(cursor)

                return Response(escolas,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'Erro ao buscar escolas{e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif request.method == 'POST':
        try:
            campo_obrigatorio = ['nome','cnpj','cep']
            for campo in campo_obrigatorio:
                if campo not in request.data:
                    return Response({'erro':f'Campo {campo} obrigatório'}, status = status.HTTP_400_BAD_REQUEST)
            
            with connection.cursor() as cursor:
                cursor.execute('''
                INSERT INTO app.escola (nome,cnpj,telefone,email,cep)
                VALUES (%s,%s,%s,%s,%s)
                ''', [request.data['nome'],request.data['cnpj'],request.data.get('telefone',''),request.data.get('email',''),request.data['cep']
                ])
                escola_id = cursor.lastrowid
                cursor.execute('''
                    SELECT escola_id,nome,cnpj,telefone,email,cep FROM app.escola
                    WHERE escola_id = %s
                    ''',[escola_id])
                escola = dict_fetchone(cursor)
                
            return Response(escola,status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'erro':f'Erro ao criar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
                





@api_view(['GET','DELETE'])
def deletar_escola(request, pk):

    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                        SELECT escola_id,nome,cnpj,telefone,email,cep 
                        FROM app.escola
                        WHERE escola_id = %s
                                ''' ,[pk])
                escola = dict_fetchone(cursor)
                return Response(escola, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'Erro ao achar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    DELETE FROM app.escola WHERE escola_id = %s
                        ''', [pk])
                
                if cursor.rowcount == 0:
                    return Response({'erro': 'Escola não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar escola: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ... Mantenha o restante do views.py

'''

CRUD TURMAS

'''

@api_view(['GET','POST'])
def lista_turmas(request,escola_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT nome, data_inicio, data_fim, periodo, capacidade, capacidade_max FROM app.turma
                        ORDER BY periodo ASC
                    ''')
                turmas = dict_fetchall(cursor)
                
                return Response(turmas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'erro ao dicionar turma{str(e)}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            campo_obrigatorio = ['nome','periodo','data_inicio','capacidade_max']    
            for campo in campo_obrigatorio:
                if campo not in request.data:
                    return Response({'campo:{campo} obrigatório'}, status=status.HTTP_400_INTERNAL_SERVER_ERROR)
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.turma (nome,data_inicio,data_fim,periodo,escola_id,capacidade,capacidade_max)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                ''', [request.data['nome'],
                      request.data['data_inicio'],
                      request.data.get('data_fim',None),
                      request.data['periodo'],
                      escola_id,
                      request.data.get('capacidade',0),
                      request.data['capacidade_max']
                               ])
                turma_id = cursor.lastrowid 
                cursor.execute('''
                    SELECT turma_id,nome,data_inicio,data_fim,periodo,escola_id, capacidade, capacidade_max FROM app.turma
                    WHERE turma_id = %s
                    ''',[turma_id])
                turma = dict_fetchone(cursor)
                return Response(turma, status=status.HTTP_201_CREATED)
        except Exception as e:
                        return Response({'erro':f'Erro ao criar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','DELETE'])
def deletar_turma(request,pk):

    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                        SELECT escola_id,nome,cnpj,telefone,email,cep,endereco 
                        FROM app.escola
                        WHERE escola_id = %s
                               ''' ,[pk])
                escola = dict_fetchone(cursor)
                return Response(escola, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'Erro ao achar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)




    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute(''' DELETE FROM app.turma WHERE turma_id = %s''', [pk])

                if cursor.rowcount == 0:
                    return Response({'erro': 'Turma não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar escola: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



'''CRUD DISCIPLINA'''

@api_view(['GET','POST'])
def listar_disciplina(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute(''' 
                    SELECT nome
                    FROM  app.disciplina
                    ORDER BY ASC
                    ''')
            disciplinas = dict_fetchall(cursor)
            return Response(disciplinas, status = status)
        except Exception as e:
            return Response({'erro':f'Erro ao buscar disciplinas{str(e)}',status: status.HTTP_500_INTERNAL_SERVER_ERROR})

    elif request.method == 'POST':
        try:
            campo_obrigatorio = ['nome']
            for campo in campo_obrigatorio:
                if campo not in request.data:
                    return Response({'campo:{campo} obrigatório'}, status=status.HTTP_400_INTERNAL_SERVER_ERROR)
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.disciplina (nome)
                    VALUES (%s)  
                            ''',[request.data['nome']])
                disciplina_id = cursor.lastrowid
                cursor.execute('''
                    SELECT disciplina_id, nome
                    FROM app.disciplina
                    WHERE turma_id = %s
                        ''', [disciplina_id])
                disciplina = dict_fetchone

                return Response(disciplina,status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro':f'Erro ao achar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)










class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


def escolas_page(request):
    return render(request, "escolas.html")

def turmas_page(request,escola_id):
    return render(request, "turmas.html")




