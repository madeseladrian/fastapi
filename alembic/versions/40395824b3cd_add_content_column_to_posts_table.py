"""add content column to posts table

Revision ID: 40395824b3cd
Revises: 9e0ea885a880
Create Date: 2022-07-24 18:17:39.753366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40395824b3cd'
down_revision = '9e0ea885a880'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
