"""media column added to the post model

Revision ID: b8c2d024f9e0
Revises: 4cd22f6e8a56
Create Date: 2023-08-14 23:29:05.345219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b8c2d024f9e0'
down_revision = '4cd22f6e8a56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media', sa.String(length=200), nullable=True))
        batch_op.drop_constraint('post_ibfk_2', type_='foreignkey')
        batch_op.drop_column('media_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('post_ibfk_2', 'file', ['media_id'], ['id'])
        batch_op.drop_column('media')

    # ### end Alembic commands ###
