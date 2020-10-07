from datetime import datetime, date

import click

from mta_tracker.app import create_app
from mta_tracker.extensions import db
from mta_tracker.models import Lines, Delays

app = create_app()
db.app = app

@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass

@click.command()
def init():
    """
    Initialize the database.

    :return: None
    """

    db.drop_all()
    db.create_all()

    return None

@click.command()
def seed():
    """
    Seed the database with inital data.

    :return: 
    """

    # All subway lines
    num_lines = ['1','2','3','4','5','6','7']
    letter_lines = ['A','C','E','B','D','F','M','G','J','Z','N','Q','R','W','L']
    other_lines = ['SIR','S']

    lines = []
    lines.extend(num_lines)
    lines.extend(letter_lines)
    lines.extend(other_lines)

    # Add each line to db
    for line in lines:
        kwargs = {
                "line": line,
                "current_status": 'On-time',
                "total_min_delayed": 0,
                "created": datetime.now(),
                "last_updated": datetime.now()
                }
        new_line = Lines(**kwargs)
        new_line.add_line()
    
    return None

@click.command()
@click.pass_context
def reset(ctx):
    """
    Init and seed automatically.

    :return: None
    """
    ctx.invoke(init)
    ctx.invoke(seed)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)