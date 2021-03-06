import datetime
import logging

from dynaconf import settings
from ics import Calendar
from utils.ics_calendar import lhc_ics

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("joker")


def quando(update, context):
    with open(settings.ICS_LOCATION, "r") as ics_file:
        calendar = Calendar(ics_file.read())

    future_events = list(
        {
            event
            for event in calendar.events
            if event.begin.date() >= datetime.date.today()
        }
    )
    next_event = min(future_events, key=lambda e: e.begin)
    event = {
        "title": next_event.name,
        "date": next_event.begin.strftime("%d/%m/%Y"),
        "url": next_event.url,
    }
    next_event_msg = f"Vai rolar \"{event['title']}\" em {event['date']}. Mais informações em {event['url']}."
    context.bot.send_message(update.message.chat_id, text=next_event_msg)


def generate_ics(context):
    logger.info("Generating new ICS file.")
    lhc_ics(settings.ICS_LOCATION)
