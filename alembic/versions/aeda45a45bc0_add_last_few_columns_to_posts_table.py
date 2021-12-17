"""add last few columns to posts table

Revision ID: aeda45a45bc0
Revises: bce0e4a93d00
Create Date: 2021-12-12 18:21:27.881385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeda45a45bc0'
down_revision = 'bce0e4a93d00'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
