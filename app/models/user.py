from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

# from app.schemas.user import UserRole
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    role = Column(Integer, default=1)


#     movies = relationship("Movie_User", back_populates="movie", cascade="save-update, merge, delete", passive_deletes=True)


# class Movie_User(Base):
#     __tablename__ = "movies_users"

#     id = Column(Integer, primary_key=True)
#     movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     rating = Column(Float)

#     movie = relationship("User", back_populates="movies", cascade="save-update, merge, delete", passive_deletes=True)
#     user = relationship("Movie", back_populates="watchers", cascade="save-update, merge, delete", passive_deletes=True)


# # movie_genre = Table("movies_genres", Base.metadata,
# #                     Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE")),
# #                     Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"))
# #                     )


# # movie_castmember = Table("movies_castmembers", Base.metadata,
# #                     Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE")),
# #                     Column('castmember_id', Integer, ForeignKey('castmembers.id', ondelete="CASCADE"))
# #                     )


# class Movie(Base):
#     __tablename__ = "movies"

#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     country = Column(String)
#     budget = Column(String)
#     year = Column(Integer)
#     date_of_release = Column(Date, nullable=False)
#     path_to_file = Column(String, nullable=False)
#     watchers = relationship("Movie_User", back_populates="user", cascade="save-update, merge, delete", passive_deletes=True)
# genres = relationship("Movie_Genre", back_populates="genre")
# also we could make in User table: movies = relationship("Movie", secondary=movie_user, bachref="watchers")
#     # in case if there no extra data :
#     genres = relationship("Genre", secondary=movie_genre, back_populates="movies", cascade="save-update, merge, delete", passive_deletes=True)
#     castmembers = relationship("CastMember", secondary=movie_castmember, back_populates="movies", cascade="save-update, merge, delete", passive_deletes=True)

# class Genre(Base):
#     __tablename__ = "genres"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     movies = relationship("Movie", secondary=movie_genre, back_populates="genres", cascade="save-update, merge, delete", passive_deletes=True)


# class CastMember(Base):
#     __tablename__ = "castmembers"

#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(50), nullable=False)
#     last_name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     age = Column(Integer)
#     role = Column(String)
#     movies = relationship("Movie", secondary=movie_castmember, back_populates="castmembers", cascade="save-update, merge, delete", passive_deletes=True)
