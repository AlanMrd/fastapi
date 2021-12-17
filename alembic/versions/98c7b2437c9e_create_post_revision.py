"""create post revision

Revision ID: 98c7b2437c9e
Revises: 
Create Date: 2021-12-12 14:25:26.504136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98c7b2437c9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
