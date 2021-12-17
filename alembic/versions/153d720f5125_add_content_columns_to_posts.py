"""add content columns to posts

Revision ID: 153d720f5125
Revises: 98c7b2437c9e
Create Date: 2021-12-12 14:41:15.256150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '153d720f5125'
down_revision = '98c7b2437c9e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content' , sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
