"""analysis_natures

Revision ID: 3a36ba91e12c
Revises: 31d59e7965ee
Create Date: 2015-08-06 14:07:57.357228

"""

# revision identifiers, used by Alembic.
revision = '3a36ba91e12c'
down_revision = '31d59e7965ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('analysis_natures', sa.Column('nature', sa.Enum('anchor', 'elections', 'children'), nullable=True))

    op.execute("UPDATE analysis_natures SET nature = 'elections' WHERE id = 1")
    op.execute("UPDATE analysis_natures SET nature = 'children' WHERE id = 2")
    op.execute("UPDATE analysis_natures SET nature = 'anchor' WHERE id = 3")

    op.alter_column('analysis_natures', 'nature', nullable=False, existing_type=sa.Enum('anchor', 'elections', 'children'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('analysis_natures', 'nature')
    ### end Alembic commands ###
