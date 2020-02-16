"""create cities table

Revision ID: 9dd7cc79ee85
Revises: 
Create Date: 2020-01-01 12:19:57.153901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd7cc79ee85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('city', sa.String(50), nullable=False),
        sa.Column('sw_latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('sw_longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('ne_latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('ne_longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP,
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text(
            'now()'), server_onupdate=sa.text('now()'), nullable=False),
    )
    op.create_unique_constraint('city', 'cities', ['city'])


def downgrade():
    op.drop_table('cities')
