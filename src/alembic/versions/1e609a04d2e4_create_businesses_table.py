"""create businesses table

Revision ID: 1e609a04d2e4
Revises: 420a63a01ca7
Create Date: 2020-01-07 21:49:02.334228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e609a04d2e4'
down_revision = '420a63a01ca7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'businesses',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('category', sa.String(80)),
        sa.Column('phone', sa.String(20)),
        sa.Column('website', sa.String(255)),
        sa.Column('claimed_business', sa.BOOLEAN, default=False),
        sa.Column('rating', sa.Float),
        sa.Column('reviews', sa.Integer),
        sa.Column('image', sa.String(500)),
        sa.Column('latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('full_address', sa.String(150)),
        sa.Column('address', sa.String(50)),
        sa.Column('city', sa.String(50)),
        sa.Column('zipcode', sa.String(15)),
        sa.Column('country', sa.String(50)),
        sa.Column('created_at', sa.TIMESTAMP,
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text(
            'now()'), server_onupdate=sa.text('now()'), nullable=False),
    )
    op.create_unique_constraint('url', 'businesses', ['url'])


def downgrade():
    op.drop_table('businesses')
