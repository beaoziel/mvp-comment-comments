from pydantic import BaseModel
from typing import List
from model.comments import Comments


class CommentSchema(BaseModel):
    """ Define como um novo comentario a ser inserido deve ser representado
    """
    id: int = 1
    user: int = 1
    title: str = "Assunto"
    emoji: str = "U+1F917"
    text: str = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's"

class CommentTittleSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base titulo do comentário.
    """
    title: str = "Assunto"

class CommentUserSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    id: int = 1
    user: int = 1
    title: str = "Assunto"
    emoji: str = "U+1F917"
    text: str = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's"

class ListCommentsSchema(BaseModel):
    """ Define como uma listagem de comentários será retornada.
    """
    name:List[CommentSchema]

def show_comments(comments: List[Comments]):
    """ Retorna uma representação do usuario seguindo o schema definido em
        CommentViewSchema.
    """
    result = []
    for c in comments:
        result.append({
            "id": c.id,
            "user": c.user,
            "title": c.title,
            "emoji": c.emoji,
            "text": c.text
        })

    return {"comments": result}

class CommentDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    title: str = "Assunto"

class CommentUserDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    title: str = "Assunto"
    user: int = 1

class CommentViewSchema(BaseModel):
    """ Define como um comentário será retornado: id + nome + título.
    """
    id: int = 1
    user: int = 1
    title: str = "Assunto"

def show_comment(comment: Comments):
    """ Retorna uma representação do comentário seguindo o schema definido em
        CommentSchema.
    """
    return {
        "user": comment.user,
        "title": comment.title,
        "emoji": comment.emoji,
        "text": comment.text
    }

class CommentIDSearchSchema(BaseModel):
    """ Define como um comentário será retornado: id
    """
    id: int = 1