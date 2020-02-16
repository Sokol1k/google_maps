"""create sectors table

Revision ID: 420a63a01ca7
Revises: 9432a759b1e2
Create Date: 2020-01-01 12:20:23.547712

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT


# revision identifiers, used by Alembic.
revision = '420a63a01ca7'
down_revision = '9432a759b1e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sectors',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('city_id', sa.Integer, nullable=False),
        sa.Column('keyword_id', sa.Integer, nullable=False),
        sa.Column('status', TINYINT, nullable=False, default=0),
        sa.Column('unique_center', sa.String(20), nullable=False),
        sa.Column('sw_latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('sw_longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('center_latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('center_longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('ne_latitude', sa.DECIMAL(8, 6), nullable=False),
        sa.Column('ne_longitude', sa.DECIMAL(9, 6), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP,
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.text(
            'now()'), server_onupdate=sa.text('now()'), nullable=False),
    )
    op.create_unique_constraint('unique_center', 'sectors', ['unique_center'])

def downgrade():
    op.drop_table('sectors')
