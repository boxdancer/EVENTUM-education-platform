"""create table users

Revision ID: 027f09ee3125
Revises: 
Create Date: 2024-10-24 21:20:05.778383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '027f09ee3125'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('surname', sa.String(length=150), nullable=False),
    sa.Column('class_number', sa.Integer(), nullable=True),
    sa.Column('exam_type', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('telegram', sa.String(length=150), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###