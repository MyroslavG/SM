"""file model added + bugs fixed

Revision ID: 45838db44288
Revises: beec80995fef
Create Date: 2023-08-10 19:51:42.590582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45838db44288'
down_revision = 'beec80995fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_filename', sa.String(length=100), nullable=True),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('bucket', sa.String(length=100), nullable=True),
    sa.Column('region', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('media_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'file', ['media_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('media_id')

    op.drop_table('file')
    # ### end Alembic commands ###
