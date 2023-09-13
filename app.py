from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from model import Session, Comments
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API Comment!", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
comments_tag = Tag(name="Comentario", description="Adição, visualização e remoção de comentários à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#1 Adicionar comentário
@app.post('/comment/new', tags=[comments_tag],
          responses={"200": CommentViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_comment(form: CommentSchema):
    """Adiciona um novo Usuário à base de dados

    Retorna uma representação dos usuários associados.
    """

    session = Session()
    titles = []
    titles_all = session.query(Comments).all()

    for t in titles_all:
        titles.append(t.title)

    if form.title in titles:
        error_msg = "Comentário de mesmo título já salvo na base :/"
        logger.warning(f"Erro ao adicionar comentário, {error_msg}")
        return {"mesage": error_msg}, 409
    
    else:
        comment = Comments(
            user=form.user,
            title=form.title,
            emoji=form.emoji,
            text=form.text)
        logger.debug(f"Adicionando um novo comentario: '{comment.title}'")
        try:
                session = Session()
                session.add(comment)
                session.commit()
                logger.debug(f"Adicionando um novo comentário: '{comment.title}'")
                return show_comment(comment), 200
            
        except IntegrityError as e:
                # como a duplicidade do nome é a provável razão do IntegrityError
                error_msg = "Comentário de mesmo nome já salvo na base :/"
                logger.warning(f"Erro ao adicionar comentário, {error_msg}")
                return {"mesage": error_msg}, 409

        except Exception as e:
                # caso um erro fora do previsto
                error_msg = "Não foi possível salvar nova comentrário :/"
                logger.warning(f"Erro ao adicionar comentário, {error_msg}")
                return {"mesage": error_msg}, 400

#2 Pegar todos os comentários
@app.get('/comment/all', tags=[comments_tag],
         responses={"200": ListCommentsSchema, "404": ErrorSchema})
def get_all_comments():
    """Faz a busca por todos os comentários publicados

    Retorna uma representação da listagem de usuários.
    """
    logger.debug(f"Coletando todos os usuários")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    comments = session.query(Comments).all()

    if not comments:
        # se não há produtos cadastrados
        return {"comentários": []}, 200
    else:
        logger.debug(f"%d comentários econtrados" % len(comments))
        # retorna a representação de produto
        print(comments)
        return show_comments(comments), 200

#3 Deletar cometário
@app.delete('/comment/delete', tags=[comments_tag],
            responses={"200": CommentDelSchema, "404": ErrorSchema})
def del_comment(query: CommentTittleSearchSchema):
    """Deleta um Usuário a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    title = unquote(unquote(query.title))
    print(title)
    logger.debug(f"Deletando comentário: #{title}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Comments).filter(Comments.title == title).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado comentário #{title}")
        return {"mesage": "Comentário deletado"}
    else:
        # se o usuário não foi encontrado
        error_msg = "Título não encontrada na base :/"
        logger.warning(f"Erro ao deletar comentário #'{title}', {error_msg}")
        return {"mesage": error_msg}, 404

#4 Pegar todos os comentários de um usuário específico
@app.get('/comment/user', tags=[comments_tag],
         responses={"200": CommentUserSearchSchema, "404": ErrorSchema})
def get_comments_user(query: CommentSchema):
    """Faz a busca por nome do usuário
        Retorna uma representação de um comentario
    """
    user_id = unquote(unquote(query.user))
    logger.debug(f"Coletando usuário {user_id}")
    # criando conexão com a base
    session = Session()
    #Fazendo busca geral
    stmt=(f'SELECT * FROM comments WHERE user = "{user_id}"')
    comments_user = session.execute(stmt)

    if comments_user:
        return f"Nenhum comentário encontrado para o usuário {user_id}", 200
    else:
        return show_comments(comments_user), 200

#5 Update no comentário
@app.put('/comment/update', tags=[comments_tag],
            responses={"200": CommentSchema, "404": ErrorSchema})
def update_comment(query: CommentTittleSearchSchema, form: CommentSchema):
    """
    Faz update dos valores de um usuário
    """
    title = unquote(unquote(query.title))
    logger.debug(f"Coletando comentário {title}")
    # criando conexão com a base
    session = Session()
    #Fazendo busca
    comment = session.query(Comments).filter(Comments.title == title).first()
    comments = session.query(Comments).all()
    all_comments = []

    for c in comments:
        all_comments.append(c.title)

    if not comment:
        return "Nenhum comentário encointrado", 200
    else:
         if form.title in all_comments:
            return "Título já existente", 200
         else:
            try:
                comment.user = form.user
                comment.title = form.title
                comment.emoji = form.emoji
                comment.text = form.text
                session.commit()
                logger.debug(f"Editando comentário: '{comment.title}'")
                return show_comment(comment), 200

            except Exception as e:
                # caso um erro fora do previsto
                error_msg = "Não foi possível editar comentário :/"
                logger.warning(f"Erro ao editar comentário, {error_msg}")
                return {"mesage": error_msg}, 400