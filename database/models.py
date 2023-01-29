from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship


from database.db import engine


Base = declarative_base()


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime)
    email = Column(String(50))
    address = Column(String(250))


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    phone = Column(String(12))
    person_id = Column(Integer, ForeignKey("persons.id", ondelete="CASCADE"))


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(String(1024), nullable=False)
    created = Column(DateTime)
    tags = relationship('Tag', secondary='notes_to_tags', back_populates='notes')


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False)
    notes = relationship('Note', secondary='notes_to_tags', back_populates='tags')


class Notes2Tags(Base):
    __tablename__ = "notes_to_tags"
    id = Column(Integer, primary_key=True)
    note_id = Column('note_id', ForeignKey('notes.id', ondelete='CASCADE'))
    tag_id = Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'))


if __name__ == "__main__":
    Base.metadata.create_all(engine)
