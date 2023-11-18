from datetime import UTC, datetime, time, timedelta, timezone

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from icalendar import Calendar, Event

from kb_2315.backend.crud import crud_session, crud_shoe
from kb_2315.backend.models import Session
from kb_2315.backend.weather.code2icon import weather_code2icon


router = APIRouter()


@router.get("/")
def get_calendar(shoe_id: int | None = None) -> PlainTextResponse:
    JST = timezone(timedelta(hours=+9), "JST")
    sessions: list[Session] = crud_session.search_session_by(shoe_id=shoe_id)

    shoe_names: dict[int, str] = {}

    def _search_shoes(shoe_id: int | None) -> str:
        if shoe_id is None:
            return "靴"
        elif shoe_id in shoe_names.keys():
            return shoe_names[shoe_id]
        else:
            shoe_names[shoe_id] = crud_shoe.search_shoe_by(shoe_id=shoe_id)[0].name
            return shoe_names[shoe_id]

    cal: Calendar = Calendar()
    cal["summary"] = f"{_search_shoes(shoe_id=shoe_id)} の乾燥記録"
    cal["scale"] = "GREGORIAN"
    cal["method"] = "PUBLISH"
    cal["X-WR-CALNAME"] = f"{_search_shoes(shoe_id=shoe_id)} の乾燥記録"
    cal["X-WR-TIMEZONE"] = "Asia/Tokyo"

    for s in sessions:
        try:
            last_time: datetime = s.created_at

            e: Event = Event(
                SUMMARY=f"天気: { weather_code2icon(s.weather_code)}, {_search_shoes(shoe_id=s.shoe_id)} を履いた",
                DTSTART=datetime(
                    last_time.year, last_time.month, last_time.day, time(7, 0).hour, time(7, 0).minute, tzinfo=JST
                )
                .astimezone(UTC)
                .strftime("%Y%m%dT%H%M%SZ"),
                DTEND=last_time.strftime("%Y%m%dT%H%M%SZ"),
            )
            cal.add_component(e)
        except IndexError:
            pass

    ical_data: str = cal.to_ical().decode("utf-8")

    response = PlainTextResponse(content=ical_data, media_type="text/calendar")
    response.headers["Content-Disposition"] = "attachment; filename=event.ics"

    return response
