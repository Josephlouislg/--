"""update

Revision ID: 497179c940f7
Revises: cf902fa0741d
Create Date: 2019-05-29 14:47:31.696346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497179c940f7'
down_revision = 'cf902fa0741d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('type', sa.SmallInteger(), nullable=False, server_default='1'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'type')
    # ### end Alembic commands ###
