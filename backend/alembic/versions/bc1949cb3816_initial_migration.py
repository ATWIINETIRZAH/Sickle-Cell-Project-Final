# """Initial migration

# Revision ID: bc1949cb3816
# Revises: 
# Create Date: 2025-03-31 16:40:18.726757

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision: str = 'bc1949cb3816'
# down_revision: Union[str, None] = None
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     # ### commands auto generated by Alembic - please adjust! ###
#     pass
#     # ### end Alembic commands ###


# def downgrade() -> None:
#     """Downgrade schema."""
#     # ### commands auto generated by Alembic - please adjust! ###
#     pass
#     # ### end Alembic commands ###


"""Initial migration

Revision ID: bc1949cb3816
Revises: 
Create Date: 2025-03-31 16:40:18.726757
"""

# revision identifiers, used by Alembic.
revision = 'bc1949cb3816'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime, String, Integer, Float
from datetime import datetime

def upgrade():
    # Create 'patients' table
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('contact', sa.String(), nullable=False),
        sa.Column('next_appointment', sa.DateTime(), default=datetime.utcnow),
    )

    # Create 'cbc_reports' table
    op.create_table(
        'cbc_reports',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('patient_id', sa.Integer, sa.ForeignKey('patients.id')),
        sa.Column('rbc', sa.Float()),
        sa.Column('hgb', sa.Float()),
        sa.Column('wbc', sa.Float()),
        sa.Column('plt', sa.Float()),
        sa.Column('neutp', sa.Float()),
        sa.Column('uploaded_at', sa.DateTime(), default=datetime.utcnow),
    )

def downgrade():
    # Drop the 'cbc_reports' and 'patients' tables in case of a downgrade
    op.drop_table('cbc_reports')
    op.drop_table('patients')
