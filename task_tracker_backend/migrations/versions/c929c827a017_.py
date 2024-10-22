"""empty message

Revision ID: c929c827a017
Revises: 0f8d5828d227
Create Date: 2024-10-22 18:41:52.279577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c929c827a017'
down_revision = '0f8d5828d227'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skills',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('skill_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('priority', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('skill_match', sa.Boolean(), nullable=True),
    sa.Column('assigned_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('assignment')
    op.drop_table('task')
    op.drop_table('skill')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skill',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('skill_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='skill_pkey')
    )
    op.create_table('task',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('task_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('priority', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
    sa.Column('deadline', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='task_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('assignment',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('skill_match', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('assigned_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('completed_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], name='assignment_task_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='assignment_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='assignment_pkey')
    )
    op.drop_table('assignments')
    op.drop_table('tasks')
    op.drop_table('skills')
    # ### end Alembic commands ###
