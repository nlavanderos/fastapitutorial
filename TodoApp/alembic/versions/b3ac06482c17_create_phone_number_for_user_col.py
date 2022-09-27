"""create phone number for user col

Revision ID: b3ac06482c17
Revises: 
Create Date: 2022-09-26 14:42:33.983399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3ac06482c17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number',sa.String(),nullable=True))


def downgrade():

    # TABLE,COLUMN
    op.drop_column('users','phone_number')
 