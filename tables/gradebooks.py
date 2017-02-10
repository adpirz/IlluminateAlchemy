from __future__ import print_function
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from base import Base, base_table_args
from utils import merge_dicts, foreignkey
from users import Users
from students import Students, StudentMixin


class GradebookSchemaMixin(object):

    __table_args__ = merge_dicts(base_table_args, {'schema': 'gradebook'})


class Gradebooks(GradebookSchemaMixin, Base):
    created_by = foreignkey(Users.user_id)
    user = relationship("Users", backref='gradebook')
    scores = relationship("OverallScoreCache", backref='gradebook')
    assignments = relationship("Assignments", backref='gradebook')

Users.gradebooks = relationship("Gradebooks", backref='staff')


class GradebookMixin(object):

    @declared_attr
    def gradebook_id(self):
        return foreignkey(Gradebooks.gradebook_id)


class GradebookSchemaAndMixin(GradebookMixin, GradebookSchemaMixin):
    pass


class OverallScoreCache(GradebookSchemaAndMixin, StudentMixin, Base):
    pass


class Categories(GradebookSchemaAndMixin, Base):
    pass

Categories.assignments = relationship("Assignments", backref='category')


class CategoryMixin(object):

    @declared_attr
    def category_id(self):
        return foreignkey(Categories.category_id)


class Assignments(GradebookSchemaAndMixin, CategoryMixin, Base):
    pass


class AssignmentMixin(object):

    @declared_attr
    def assignment_id(self):
        return foreignkey(Assignments.assignment_id)


class CategoryScoreCache(GradebookSchemaAndMixin, StudentMixin, Base):
    pass


class Scores(GradebookSchemaAndMixin, AssignmentMixin, StudentMixin, Base):
    pass


class ScoreCache(GradebookSchemaAndMixin, StudentMixin, AssignmentMixin, CategoryMixin, Base):
    pass
