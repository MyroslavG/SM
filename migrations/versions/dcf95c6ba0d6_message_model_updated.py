"""message model updated

Revision ID: dcf95c6ba0d6
Revises: c13d0c493036
Create Date: 2023-08-09 17:03:56.349076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcf95c6ba0d6'
down_revision = 'c13d0c493036'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['recipient_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('recipient_id')

    # ### end Alembic commands ###
