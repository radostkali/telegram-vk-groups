#!/usr/bin/env python3
import typer

import os
import logging
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from telegram_service.bot import TgBot
from database.services.tables_control_service import DBTablesControlService
from database.daos.last_refresh_dao import LastRefreshDAO
from database.utils import db_session

import settings


app = typer.Typer()
db_tables_control_service = DBTablesControlService()


DEBUG_LAST_REFRESH_UPDATE_DELTA = timedelta(hours=5)


def update_last_refresh():
    with db_session() as session:
        last_refresh = LastRefreshDAO._get_or_create_last_refresh(session)
        datetime_to_set = datetime.utcnow() - DEBUG_LAST_REFRESH_UPDATE_DELTA
        last_refresh.timestamp = int((datetime_to_set - datetime(1970, 1, 1)).total_seconds())


@app.command()
def run(
        recreate_db: bool = typer.Option(
            False, '--recreate-db', '-r', help='Drop and create DB tables', show_default=True
        ),
):
    """
    Run telegram bot.
    """
    typer.echo('Starting telegram bot...')

    if recreate_db:
        typer.echo('Recreating database...')
        db_tables_control_service.recreate_tables()
        typer.secho('SUCCESS', fg=typer.colors.GREEN)
    else:
        db_tables_control_service.create_tables()

    debug_mode_msg = typer.style(f'{settings.DEBUG}', fg=typer.colors.RED, bold=True)
    typer.echo('Debug mode on: ' + debug_mode_msg)

    if settings.DEBUG:
        update_last_refresh()
        logging.basicConfig(
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.CRITICAL,
        )
    else:
        log_filepath = os.path.join(settings.BASEDIR, 'logs', 'tg_bot.log')
        handler = RotatingFileHandler(
            filename=log_filepath,
            maxBytes=1024 * 1024 * 50,  # 50 mb
            backupCount=3,
        )
        logging.basicConfig(
            handlers=[handler],
            format='[%(name)s %(levelname)s] %(asctime)s: %(message)s',
            level=logging.DEBUG,
        )

    bot = TgBot()
    bot.start()


if __name__ == "__main__":
    app()
