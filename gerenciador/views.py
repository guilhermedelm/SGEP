import base64
from django.db import connection
from django.core.files.storage import default_storage


from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
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
def deletar_escola(request, escola_id):

    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                        SELECT escola_id,nome,cnpj,telefone,email,cep 
                        FROM app.escola
                        WHERE escola_id = %s
                                ''' ,[escola_id])
                escola = dict_fetchone(cursor)
                return Response(escola, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'Erro ao achar escola: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    DELETE FROM app.escola WHERE escola_id = %s
                        ''', [escola_id])
                
                if cursor.rowcount == 0:
                    return Response({'erro': 'Escola não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar escola: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''

CRUD TURMAS

'''
@api_view(['GET','POST','PUT'])
def lista_turmas(request,escola_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''SELECT * FROM app.turma
                    WHERE escola_id = %s
                    ORDER BY periodo ASC
                    ''',[escola_id] )
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

@api_view(['GET','DELETE', 'PUT'])
def deletar_turma(request,escola_id,pk):

    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                        SELECT turma_id,nome,data_inicio,data_fim,periodo,escola_id,capacidade,capacidade_max
                        FROM app.turma
                        WHERE turma_id = %s
                                ''' ,[pk])
                turma = dict_fetchone(cursor)
                return Response(turma, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro':f'Erro ao achar turma: {str(e)}'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)


    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute(''' DELETE FROM app.turma WHERE turma_id = %s''', [pk])

                if cursor.rowcount == 0:
                    return Response({'erro': 'Turma não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar escola: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif request.method == 'PUT':
        try:
            nome = request.data.get('nome')
            periodo = request.data.get('periodo')
            data_inicio = request.data.get('data_inicio')
            data_fim = request.data.get('data_fim')
            capacidade = request.data.get('capacidade')
            capacidade_max = request.data.get('capacidade_max')

            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE app.turma
                    SET nome = %s,
                        periodo = %s,
                        data_inicio = %s,
                        data_fim = %s,
                        capacidade = %s,
                        capacidade_max = %s
                    WHERE turma_id = %s
                ''', [nome, periodo, data_inicio, data_fim, capacidade, capacidade_max, pk])

                if cursor.rowcount == 0:
                    return Response({'erro': 'Turma não encontrada'}, status=status.HTTP_404_NOT_FOUND)

                cursor.execute('''
                    SELECT turma_id, nome, data_inicio, data_fim, periodo, escola_id, capacidade, capacidade_max
                    FROM app.turma
                    WHERE turma_id = %s
                ''', [pk])
                turma_atualizada = dict_fetchone(cursor)

            return Response(turma_atualizada, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'erro': f'Erro ao atualizar turma: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




'''CRUD ALUNOS'''
@api_view(['GET', 'POST'])
def lista_alunos(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT aluno_id, nome, telefone, email, telefone_pai
                    FROM app.aluno
                    ORDER BY nome ASC
                ''')
                alunos = dict_fetchall(cursor)
            return Response(alunos, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'erro': f'Erro ao buscar alunos: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            # Campos obrigatórios
            nome = request.data.get('nome')
            if not nome:
                return Response({'erro': 'Campo nome obrigatório'},
                                status=status.HTTP_400_BAD_REQUEST)

            telefone = request.data.get('telefone', '')
            email = request.data.get('email', '')
            telefone_pai = request.data.get('telefone_pai', '')

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.aluno (nome, telefone, email, telefone_pai)
                    VALUES (%s, %s, %s, %s)
                    RETURNING aluno_id, nome, telefone, email, telefone_pai
                ''', [nome, telefone, email, telefone_pai])

                aluno = cursor.fetchone()
                aluno_dict = {
                    'aluno_id': aluno[0],
                    'nome': aluno[1],
                    'telefone': aluno[2],
                    'email': aluno[3],
                    'telefone_pai': aluno[4]
                }

            return Response(aluno_dict, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro': f'Erro ao criar aluno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'DELETE', 'PUT'])
def detalhe_aluno(request, pk):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT aluno_id, nome, telefone, email, telefone_pai
                    FROM app.aluno
                    WHERE aluno_id = %s
                ''', [pk])
                aluno = dict_fetchone(cursor)

            if aluno is None:
                return Response({'erro': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            return Response(aluno, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'erro': f'Erro ao buscar aluno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    elif request.method == 'PUT':
        try:
            nome = request.data.get('nome')
            telefone = request.data.get('telefone')
            email = request.data.get('email')
            telefone_pai = request.data.get('telefone_pai')

            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL app.atualizar_aluno(%s, %s, %s, %s, %s)",
                    [pk, nome, telefone, email, telefone_pai]
                )

                # Retornar dados atualizados
                cursor.execute('''
                    SELECT aluno_id, nome, telefone, email, telefone_pai
                    FROM app.aluno
                    WHERE aluno_id = %s
                ''', [pk])
                aluno_atualizado = dict_fetchone(cursor)

            return Response(aluno_atualizado, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'erro': f'Erro ao atualizar aluno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    DELETE FROM app.aluno WHERE aluno_id = %s
                ''', [pk])

                if cursor.rowcount == 0:
                    return Response({'erro': 'Aluno não encontrado'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar aluno: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



'''CRUD MATRICULAS'''
@api_view(['GET','POST'])
def lista_matriculas(request, turma_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT m.matricula_id, a.aluno_id, a.nome, a.telefone, a.email, a.telefone_pai
                    FROM app.matricula m
                    JOIN app.aluno a ON m.aluno_id = a.aluno_id
                    WHERE m.turma_id = %s
                    ORDER BY a.nome ASC
                ''', [turma_id])
                matriculas = dict_fetchall(cursor)
                return Response(matriculas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': f'Erro ao buscar matrículas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            aluno_id = request.data.get('aluno_id')
            if not aluno_id:
                return Response({'erro': 'Campo aluno_id obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.matricula (turma_id, aluno_id)
                    VALUES (%s, %s)
                ''', [turma_id, aluno_id])
                matricula_id = cursor.lastrowid

                cursor.execute('''
                    SELECT m.matricula_id, a.aluno_id, a.nome, a.telefone, a.email, a.telefone_pai
                    FROM app.matricula m
                    JOIN app.aluno a ON m.aluno_id = a.aluno_id
                    WHERE m.matricula_id = %s
                ''', [matricula_id])
                matricula = dict_fetchone(cursor)
                return Response(matricula, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro': f'Erro ao criar matrícula: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def deletar_matricula(request, turma_id, matricula_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM app.matricula
                WHERE matricula_id = %s AND turma_id = %s
            ''', [matricula_id, turma_id])
            if cursor.rowcount == 0:
                return Response({'erro': 'Matrícula não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'erro': f'Erro ao deletar matrícula: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET', 'POST'])
def lista_avaliacoes(request, matricula_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT av.matricula_id, av.disciplina_id, d.nome AS disciplina,
                           av.avaliacao, av.nota, av.data_avaliacao, av.prova
                    FROM app.avaliacao av
                    JOIN app.disciplina d ON av.disciplina_id = d.disciplina_id
                    WHERE av.matricula_id = %s
                    ORDER BY d.nome ASC
                ''', [matricula_id])
                
                avaliacoes_raw = [
                    dict(zip([col[0] for col in cursor.description], row))
                    for row in cursor.fetchall()
                ]

            avaliacoes = []
            for a in avaliacoes_raw:
                # Nota como float
                if isinstance(a["nota"], float):
                    nota = a["nota"]
                else:
                    nota = float(a["nota"])
                
                # Data como string ISO
                data_avaliacao = a["data_avaliacao"].isoformat() if a["data_avaliacao"] else None

                # PDF em Base64
                if a["prova"]:
                    if isinstance(a["prova"], memoryview):
                        pdf_bytes = a["prova"].tobytes()
                    elif isinstance(a["prova"], bytes):
                        pdf_bytes = a["prova"]
                    else:
                        pdf_bytes = bytes(a["prova"])
                    prova_pdf = "data:application/pdf;base64," + base64.b64encode(pdf_bytes).decode('utf-8')
                else:
                    prova_pdf = None

                avaliacoes.append({
                    "matricula_id": a["matricula_id"],
                    "disciplina_id": a["disciplina_id"],
                    "disciplina": a["disciplina"],
                    "avaliacao": a["avaliacao"],
                    "nota": nota,
                    "data_avaliacao": data_avaliacao,
                    "prova_pdf": prova_pdf
                })

            return Response(avaliacoes, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            disciplina_id = request.data.get('disciplina_id')
            avaliacao = request.data.get('avaliacao')
            nota = request.data.get('nota')
            data_avaliacao = request.data.get('data_avaliacao', None)
            pdf_file = request.FILES.get('prova')

            pdf_bytes = pdf_file.read() if pdf_file else None

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.avaliacao (matricula_id, disciplina_id, avaliacao, nota, data_avaliacao, prova)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', [matricula_id, disciplina_id, avaliacao, nota, data_avaliacao, pdf_bytes])

            return Response({"mensagem": "Avaliação criada com sucesso"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deletar_avaliacao(request, matricula_id, disciplina_id, avaliacao_nome):
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM app.avaliacao
                WHERE matricula_id=%s AND disciplina_id=%s AND avaliacao=%s
            ''', [matricula_id, disciplina_id, avaliacao_nome])

            if cursor.rowcount == 0:
                return Response({'erro': 'Avaliação não encontrada'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'erro': f'Erro ao deletar avaliação: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def baixar_prova(request, avaliacao_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT prova FROM app.avaliacao WHERE id = %s", [avaliacao_id])
        pdf = cursor.fetchone()[0]

    if not pdf:
        return Response({"erro": "Sem PDF"}, status=404)

    return HttpResponse(pdf, content_type="application/pdf")



@api_view(['GET', 'POST'])
def listar_disciplinas(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT disciplina_id, nome FROM app.disciplina ORDER BY nome ASC')
                disciplinas = dict_fetchall(cursor)
            return Response(disciplinas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': f'Erro ao buscar disciplinas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            nome = request.data.get('nome')
            if not nome:
                return Response({'erro': 'Campo nome obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
            
            with connection.cursor() as cursor:
                cursor.execute('SELECT disciplina_id FROM app.disciplina WHERE nome = %s', [nome])
                existing = cursor.fetchone()
                if existing:
                    disciplina_id = existing[0]
                    return Response({'disciplina_id': disciplina_id, 'nome': nome}, status=status.HTTP_200_OK)

                cursor.execute('INSERT INTO app.disciplina (nome) VALUES (%s) RETURNING disciplina_id', [nome])
                disciplina_id = cursor.fetchone()[0]

                return Response({'disciplina_id': disciplina_id, 'nome': nome}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro': f'Erro ao criar disciplina: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST'])
def turma_disciplinas(request, turma_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT td.turma_id, d.disciplina_id, d.nome
                    FROM app.turma_disciplina td
                    JOIN app.disciplina d ON td.disciplina_id = d.disciplina_id
                    WHERE td.turma_id = %s
                    ORDER BY d.nome
                ''', [turma_id])
                disciplinas = dict_fetchall(cursor)
            return Response(disciplinas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': f'Erro ao listar disciplinas: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        try:
            disciplina_id = request.data.get('disciplina_id')
            if not disciplina_id:
                return Response({'erro': 'Campo disciplina_id obrigatório'}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.turma_disciplina (turma_id, disciplina_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING turma_id, disciplina_id
                ''', [turma_id, disciplina_id])
                result = cursor.fetchone()

                if result is None:
                    cursor.execute('SELECT disciplina_id, nome FROM app.disciplina WHERE disciplina_id = %s', [disciplina_id])
                    disciplina = dict_fetchone(cursor)
                    return Response({'erro': 'Disciplina já cadastrada nesta turma', 'disciplina': disciplina}, status=status.HTTP_400_BAD_REQUEST)

                cursor.execute('SELECT disciplina_id, nome FROM app.disciplina WHERE disciplina_id = %s', [disciplina_id])
                disciplina = dict_fetchone(cursor)

            return Response({'turma_id': turma_id, 'disciplina': disciplina}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'erro': f'Erro ao adicionar disciplina: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


'''CRUD PROFESSOR'''
@api_view(['GET', 'POST'])
def lista_professores(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM professor ORDER BY nome;")
            professores = dict_fetchall(cursor)
            return Response(professores)

    elif request.method == 'POST':
        try:
            cpf = request.data.get('cpf')
            nome = request.data.get('nome')
            telefone = request.data.get('telefone')
            email = request.data.get('email')
            endereco = request.data.get('endereco')
            
            if not cpf or not nome:
                return Response({'erro': 'CPF e Nome são obrigatórios'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO app.professor(cpf, nome, telefone, email, endereco)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING professor_id
                """, [cpf, nome, telefone, email, endereco])
                professor_id = cursor.fetchone()[0]

            return Response({"mensagem": "Professor cadastrado com sucesso!", "professor_id": professor_id}, status=201)

        except Exception as e:
            return Response({'erro': str(e)}, status=500)
        

@api_view(['GET','POST'])
def turma_professores(request, turma_id):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.* FROM professor p
                INNER JOIN turma_professor tp ON tp.professor_id = p.professor_id
                WHERE tp.turma_id = %s;
            """, [turma_id])
            profs = dict_fetchall(cursor)
        return Response(profs)

    if request.method == 'POST':
        professor_id = request.data.get("professor_id")
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO turma_professor (turma_id, professor_id)
                    VALUES (%s, %s)
                """, [turma_id, professor_id])
            return Response({"status":"ok"}, status=201)
        except Exception as e:
            return Response({"erro": str(e)}, status=500)


@api_view(['DELETE'])
def remover_professor_turma(request, turma_id, professor_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM turma_professor
                WHERE turma_id = %s AND professor_id = %s
            """, [turma_id, professor_id])
        return Response(status=204)
    except Exception as e:
        return Response({'erro': str(e)}, status=500)





@api_view(['POST','GET'])
def lista_endereco(request,aluno_id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT endereco_id,aluno_id,estado,cidade,bairro,rua,casa 
                    FROM app.endereco
                    WHERE aluno_id = %s
                    ORDER BY estado ASC              
                    ''', [aluno_id])
                enderecos = dict_fetchall(cursor)
            return Response(enderecos, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'erro': f'Erro ao procurar enderecos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        try:
            campos_obrigatorios = ['estado','cidade','bairro','rua','casa']
            for campo in campos_obrigatorios:
                if campo not in request.data:
                    return Response({'erro':f'Campo {campo} obrigatório'}, status = status.HTTP_400_BAD_REQUEST)
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO app.endereco (aluno_id,estado,cidade,bairro,rua,casa)
                    VALUES (%s,%s,%s,%s,%s,%s)
                ''',[aluno_id,request.data['estado'], request.data['cidade'],request.data['bairro'],request.data['rua'],request.data['casa']])
                endereco_id = cursor.lastrowid
                cursor.execute('''
                    SELECT endereco_id,aluno_id,estado,cidade,bairro,rua,casa
                    FROM app.endereco
                    WHERE endereco_id = %s AND aluno_id = %s 
                        ''',[endereco_id,aluno_id])
                endereco = dict_fetchone(cursor)
            return Response(endereco,status = status.HTTP_201_CREATED)
        except Exception as e :
            return Response({'erro': f'Erro ao adicionar endereco: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE','PUT'])
def deletar_endereco(request,aluno_id,endereco_id):
    
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                        DELETE FROM app.endereco
                        WHERE aluno_id = %s AND endereco_id = %s
                               ''',[aluno_id,endereco_id])
                
                if cursor.rowcount == 0:
                    return Response({'erro': 'Avaliação não encontrada'}, status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'erro': f'Erro ao deletar avaliação: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            campos_obrigatorios = ['estado','cidade','bairro','rua','casa']
            for campo in campos_obrigatorios:
                    if campo not in request.data:
                        return Response({'erro':f'Campo {campo} obrigatório'}, status = status.HTTP_400_BAD_REQUEST)
            with connection.cursor() as cursor: 
                cursor.execute('''
                        UPDATE app.endereco
                        SET estado = %s, cidade = %s, bairro = %s, rua = %s, casa = %s
                        WHERE aluno_id = %s AND endereco = %s         
                                '''[request.data['estado'],
                                request.data['cidade'],
                                request.data['bairro'],
                                request.data['rua'],
                                request.data['casa'],
                                aluno_id,
                                endereco_id])    
                if cursor.rowcount == 0:
                    return Response("Endereço não encontrado",status = status.HTTP_404_NOT_FOUND) 
                cursor.execute('''
                        SELECT estado,cidade,bairro,rua,casa 
                        FROM app.endereco
                        WHERE aluno_id = %s AND endereco_id = %s
                                ''', [aluno_id,endereco_id])
                endereco = dict_fetchone(cursor)
            return Response(endereco,status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response('erro: erro ao atualizar endereco{e}', status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        


@api_view(['GET'])
def consulta_medias_escolas(request):
    try:
        disciplina_nome = request.GET.get('disciplina', None)

        if not disciplina_nome:
            return Response(
                {'erro': 'O parâmetro "disciplina" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT escola_id, escola_nome, disciplina_nome, media_notas
                FROM app.vw_media_notas_escolas
                WHERE disciplina_nome = %s
                ORDER BY media_notas DESC;
            ''', [disciplina_nome])

            resultado = dict_fetchall(cursor)

        return Response(resultado, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'erro': f'Erro ao consultar médias: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




                    


def home_page(request):
    return render(request, "home.html")

def escola_page(request,escola_id):
    return render(request, "escola.html")

def turma_page(request,escola_id,turma_id):
    return render(request, "turma.html")

def aluno_page(request, escola_id, turma_id, aluno_id):
    return render(request, "aluno.html", {
        "escola_id": escola_id,
        "turma_id": turma_id,
        "aluno_id": aluno_id
    })

def consultas_avancadas_page(request):
    return render(request, "consultas_avancadas.html")
