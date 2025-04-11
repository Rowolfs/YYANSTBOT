from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, Boolean, Integer
from config import Base, get_db, logger



class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=True)

    def __repr__(self):
        return f"UserBase(id={self.id}, name={self.name})"


class ChatBase(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    def __repr__(self):
        return f"ChatBase(id={self.id}, name={self.name})"


class ChatUserBase(Base):
    __tablename__ = "chat_users"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



def chat_user_registration(chatId, userId,isAdmin):
    db = next(get_db())
    chat_user = ChatUserBase(chat_id = chatId, user_id = userId,is_admin = isAdmin)
    db.add(chat_user)
    try:
        db.commit()
    except Exception as e:
        logger.warning(f"{e}")

    


def user_registration(user_id: int, full_name,user_name ) -> bool:
    db = next(get_db())
    if(user_name is not None):
        user = UserBase(id = user_id,name = full_name,username = user_name )
    else:
        user = UserBase(id = user_id,name = full_name)
    db.add(user)
    try:
        db.commit()
    except Exception as e:
        logger.warning(f"{e}")
    
    


def chat_registration(chat_id: int,chat_name):
    db = next(get_db())
    chat = ChatBase(id = chat_id, name = chat_name)
    db.add(chat)
    try:
        db.commit()
    except Exception as e:
        logger.warning(f"{e}")
