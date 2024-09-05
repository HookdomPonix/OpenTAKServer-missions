"""Added packages table

Revision ID: 04d5dc15acab
Revises: d91957bb59a0
Create Date: 2024-09-04 14:13:49.055298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04d5dc15acab'
down_revision = 'd91957bb59a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(), nullable=False),
    sa.Column('plugin_type', sa.String(), nullable=False),
    sa.Column('package_name', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('revision_code', sa.Integer(), nullable=True),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.Column('apk_hash', sa.Integer(), nullable=True),
    sa.Column('os_requirement', sa.Integer(), nullable=True),
    sa.Column('tak_prereq', sa.Integer(), nullable=True),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('icon', sa.BLOB(), nullable=True),
    sa.Column('icon_filename', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('package_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('packages')
    # ### end Alembic commands ###
