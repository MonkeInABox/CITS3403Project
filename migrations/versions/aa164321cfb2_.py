"""empty message

Revision ID: aa164321cfb2
Revises: e884b9085afe
Create Date: 2024-05-12 09:53:29.150645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa164321cfb2'
down_revision = 'e884b9085afe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dislike',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('dislike', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_dislike_author_id'), ['author_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_dislike_post_id'), ['post_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_dislike_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dislike', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_dislike_timestamp'))
        batch_op.drop_index(batch_op.f('ix_dislike_post_id'))
        batch_op.drop_index(batch_op.f('ix_dislike_author_id'))

    op.drop_table('dislike')
    # ### end Alembic commands ###