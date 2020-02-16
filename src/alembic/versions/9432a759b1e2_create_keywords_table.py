"""create keywords table

Revision ID: 9432a759b1e2
Revises: 9dd7cc79ee85
Create Date: 2020-01-01 12:20:09.486903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9432a759b1e2'
down_revision = '9dd7cc79ee85'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'keywords',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('keyword', sa.String(50), nullable=False),
    )
    op.create_unique_constraint('keyword', 'keywords', ['keyword'])


def downgrade():
    op.drop_table('keywords')
