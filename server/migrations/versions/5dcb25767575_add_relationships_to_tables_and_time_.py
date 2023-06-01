"""Add relationships to tables and time column to signups

Revision ID: 5dcb25767575
Revises: 6bbc545b0d61
Create Date: 2023-05-31 15:46:20.321865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dcb25767575'
down_revision = '6bbc545b0d61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('activity_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('camper_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_signups_camper_id_campers'), 'campers', ['camper_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_signups_activity_id_activities'), 'activities', ['activity_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_signups_activity_id_activities'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_signups_camper_id_campers'), type_='foreignkey')
        batch_op.drop_column('camper_id')
        batch_op.drop_column('activity_id')
        batch_op.drop_column('time')

    # ### end Alembic commands ###
