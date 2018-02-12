"""FDI Additions

Revision ID: 294efa8baade
Revises: 322e97ee8bc8
Create Date: 2017-10-13 11:41:42.587849

"""

# revision identifiers, used by Alembic.
revision = '294efa8baade'
down_revision = '322e97ee8bc8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('involvements1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_involvements1_name'), 'involvements1', ['name'], unique=True)
    op.create_table('involvements2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_involvements2_name'), 'involvements2', ['name'], unique=True)
    op.create_table('involvements3',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_involvements3_name'), 'involvements3', ['name'], unique=True)
    op.create_table('provinces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provinces_name'), 'provinces', ['name'], unique=True)
    op.drop_constraint(u'investments_ibfk_9', 'investments', type_='foreignkey')
    op.drop_index('ix_investments_involvement_id', table_name='investments')
    op.drop_table('involvements')
    op.add_column(u'investments', sa.Column('gov_programs', sa.String(length=1024), nullable=True))
    op.add_column(u'investments', sa.Column('involvement_id1', sa.Integer(), nullable=True))
    op.add_column(u'investments', sa.Column('involvement_id2', sa.Integer(), nullable=True))
    op.add_column(u'investments', sa.Column('involvement_id3', sa.Integer(), nullable=True))
    op.add_column(u'investments', sa.Column('mot_investment', sa.String(length=1024), nullable=True))
    op.add_column(u'investments', sa.Column('phase_date', sa.Date(), nullable=True))
    op.add_column(u'investments', sa.Column('province_id', sa.Integer(), nullable=True))
    op.add_column(u'investments', sa.Column('soc_programs', sa.String(length=1024), nullable=True))
    op.add_column(u'investments', sa.Column('target_market', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_investments_involvement_id1'), 'investments', ['involvement_id1'], unique=False)
    op.create_index(op.f('ix_investments_involvement_id2'), 'investments', ['involvement_id2'], unique=False)
    op.create_index(op.f('ix_investments_involvement_id3'), 'investments', ['involvement_id3'], unique=False)
    op.create_index(op.f('ix_investments_phase_date'), 'investments', ['phase_date'], unique=False)
    op.create_index(op.f('ix_investments_province_id'), 'investments', ['province_id'], unique=False)
    op.create_foreign_key(None, 'investments', 'involvements1', ['involvement_id1'], ['id'])
    op.create_foreign_key(None, 'investments', 'involvements3', ['involvement_id3'], ['id'])
    op.create_foreign_key(None, 'investments', 'provinces', ['province_id'], ['id'])
    op.create_foreign_key(None, 'investments', 'involvements2', ['involvement_id2'], ['id'])
    op.drop_column(u'investments', 'involvement_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'investments', sa.Column('involvement_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(u'investments_ibfk_12', 'investments', type_='foreignkey')
    op.drop_constraint(u'investments_ibfk_13', 'investments', type_='foreignkey')
    op.drop_constraint(u'investments_ibfk_14', 'investments', type_='foreignkey')
    op.drop_constraint(u'investments_ibfk_15', 'investments', type_='foreignkey')
    op.drop_index(op.f('ix_investments_province_id'), table_name='investments')
    op.drop_index(op.f('ix_investments_phase_date'), table_name='investments')
    op.drop_index(op.f('ix_investments_involvement_id3'), table_name='investments')
    op.drop_index(op.f('ix_investments_involvement_id2'), table_name='investments')
    op.drop_index(op.f('ix_investments_involvement_id1'), table_name='investments')
    op.drop_column(u'investments', 'target_market')
    op.drop_column(u'investments', 'soc_programs')
    op.drop_column(u'investments', 'province_id')
    op.drop_column(u'investments', 'phase_date')
    op.drop_column(u'investments', 'mot_investment')
    op.drop_column(u'investments', 'involvement_id3')
    op.drop_column(u'investments', 'involvement_id2')
    op.drop_column(u'investments', 'involvement_id1')
    op.drop_column(u'investments', 'gov_programs')
    op.create_table('involvements',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    op.create_foreign_key(u'investments_ibfk_9', 'investments', 'involvements', ['involvement_id'], ['id'])
    op.create_index('ix_investments_involvement_id', 'investments', ['involvement_id'], unique=False)
    op.drop_index(op.f('ix_provinces_name'), table_name='provinces')
    op.drop_table('provinces')
    op.drop_index(op.f('ix_involvements3_name'), table_name='involvements3')
    op.drop_table('involvements3')
    op.drop_index(op.f('ix_involvements2_name'), table_name='involvements2')
    op.drop_table('involvements2')
    op.drop_index(op.f('ix_involvements1_name'), table_name='involvements1')
    op.drop_table('involvements1')
    ### end Alembic commands ###