"""second

Revision ID: d9be2a6c59a0
Revises: bee4880ef588
Create Date: 2023-06-15 16:42:15.483861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9be2a6c59a0'
down_revision = 'bee4880ef588'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("my_table", sa.Column("title", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("my_table", "title")
