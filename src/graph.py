from datetime import timedelta, timezone
from uuid import UUID

import plotly.graph_objects as go
import streamlit as st

from kb_2315.backend.crud import crud_sensor, crud_session
from kb_2315.backend.models import Sensor


st.set_page_config(layout="wide")

# Sidebar

st.sidebar.title("Analyze")

st.sidebar.subheader("Select a Session")
sessions: list[UUID] = [i.session_id for i in crud_session.search_session_by()]

st.session_state.session_id = st.sidebar.selectbox("Session", sessions)


# Main Page

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
