from datetime import timedelta, timezone

from uuid import UUID

import plotly.graph_objects as go
import streamlit as st

from kb_2315.backend.crud import crud_sensor, crud_session, crud_shoe
from kb_2315.backend.models import Sensor


st.set_page_config(layout="wide")

# Parameter
try:
    current_shoe_id: int | None = int(st.experimental_get_query_params().get("shoe_id", None)[0])  # type:ignore
    if current_shoe_id == 0:
        current_shoe_id = None
except Exception:
    current_shoe_id = None

try:
    current_session_id: str | None = st.experimental_get_query_params().get("session_id", None)[0]  # type:ignore
except Exception:
    current_session_id = None


# Sidebar

st.sidebar.title("Analyze")

# # Shoe

shoes: dict[int, str] = {0: " All"} | {i.id: f"{i.id} {i.name}" for i in crud_shoe.search_shoe_by()}

current_shoe_index: int | None = list(shoes.keys()).index(current_shoe_id) if current_shoe_id is not None else None


try:
    st.session_state.shoe_id = int(
        st.sidebar.selectbox(
            label="Select a Shoe", options=shoes.values(), index=current_shoe_index, placeholder="靴を選んでください"
        ).split(  # type:ignore
            " "
        )[
            0
        ]
    )

except Exception:
    st.session_state.shoe_id = None

# # Session

sessions: list[str] = [str(i.session_id) for i in crud_session.search_session_by(shoe_id=st.session_state.shoe_id)]

try:
    currennt_session_index: int | None = sessions.index(current_session_id)  # type:ignore
    # if current_session_id is not None else None
except Exception:
    currennt_session_index = None

st.session_state.session_id = st.sidebar.selectbox(
    label="Select a Session", options=sessions, index=currennt_session_index
)


# Main Page

if st.session_state.session_id is not None:
    sensors: list[Sensor] = crud_sensor.search_sensor_by(session_id=st.session_state.session_id)

    JST = timezone(timedelta(hours=+9), "JST")
    timeseries: list[str] = [s.time.astimezone(JST).strftime("%H時%M分%S秒") for s in sensors]

    external_temperatures: list[float] = [s.external_temperature for s in sensors]
    external_humidities: list[float] = [s.external_humidity for s in sensors]
    internal_temperatures: list[float] = [s.internal_temperature for s in sensors]
    internal_humidities: list[float] = [s.internal_humidity for s in sensors]

    st.subheader("温度")
    figT = go.Figure(
        data=[
            go.Scatter(
                x=timeseries,
                y=external_temperatures,
                name="外気温度",
                mode="lines+markers",
            ),
            go.Scatter(
                x=timeseries,
                y=internal_temperatures,
                name="内気温度",
                mode="lines+markers",
            ),
        ]
    )
    st.plotly_chart(figT)

    st.subheader("湿度")
    figH = go.Figure(
        data=[
            go.Scatter(
                x=timeseries,
                y=external_humidities,
                name="外気温度",
                mode="lines+markers",
            ),
            go.Scatter(
                x=timeseries,
                y=internal_humidities,
                name="内気温度",
                mode="lines+markers",
            ),
        ]
    )
    st.plotly_chart(figH)
