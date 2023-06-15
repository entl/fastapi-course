"""first

Revision ID: bee4880ef588
Revises: 
Create Date: 2023-06-15 16:39:45.330752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bee4880ef588'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("my_table", sa.Column("id", sa.Integer, primary_key=True, nullable=False))


def downgrade() -> None:
    op.drop_table("my_table")
