
import json
import pandas as pd
import streamlit as st

DIAS_ES = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

MESES_ES = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}


def add_calendar_columns(df, include_weekend=False):
    if not df.empty and "timestamp" in df.columns:
        df["hour"] = df["timestamp"].dt.hour
        df["day_name"] = df["timestamp"].dt.day_name().map(DIAS_ES)
        df["month_name"] = df["timestamp"].dt.month_name().map(MESES_ES)

        if include_weekend:
            df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5

    return df


@st.cache_data
def load_liked_posts(filepath="data/liked_posts.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []

        for item in data:
            ts = item.get("timestamp", 0)
            labels = {
                lv.get("label"): lv.get("value")
                for lv in item.get("label_values", [])
                if "label" in lv
            }

            owner = None

            for lv in item.get("label_values", []):
                if lv.get("title") == "Propietario":
                    dicts = lv.get("dict", [])

                    if dicts and "dict" in dicts[0]:
                        for inner in dicts[0]["dict"]:
                            if inner.get("label") == "Nombre de usuario":
                                owner = inner.get("value")

            records.append({
                "timestamp": pd.to_datetime(ts, unit="s"),
                "url": labels.get("URL", ""),
                "description": labels.get("Descripción", ""),
                "owner": owner
            })

        df = pd.DataFrame(records)
        return add_calendar_columns(df, include_weekend=True)

    except (FileNotFoundError, json.JSONDecodeError):
        return pd.DataFrame()


@st.cache_data
def load_liked_comments(filepath="data/liked_comments.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []

        for item in data.get("likes_comment_likes", []):
            author = item.get("title", "")

            for sub in item.get("string_list_data", []):
                ts = sub.get("timestamp", 0)

                records.append({
                    "timestamp": pd.to_datetime(ts, unit="s"),
                    "comment_author": author,
                    "url": sub.get("href", "")
                })

        df = pd.DataFrame(records)
        return add_calendar_columns(df, include_weekend=True)

    except (FileNotFoundError, json.JSONDecodeError):
        return pd.DataFrame()


@st.cache_data
def load_relationships(
    followers_path="data/followers_1.json",
    following_path="data/following.json",
    close_path="data/close_friends.json"
):
    followers, following, close_friends = set(), set(), set()

    try:
        with open(followers_path, "r", encoding="utf-8") as f:
            f_data = json.load(f)

        for item in f_data:
            for s in item.get("string_list_data", []):
                if s.get("value"):
                    followers.add(s.get("value"))

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    try:
        with open(following_path, "r", encoding="utf-8") as f:
            fg_data = json.load(f)

        for item in fg_data.get("relationships_following", []):
            if item.get("title"):
                following.add(item.get("title"))

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    try:
        with open(close_path, "r", encoding="utf-8") as f:
            cf_data = json.load(f)

        for item in cf_data:
            for lv in item.get("label_values", []):
                if lv.get("label") == "Nombre de usuario":
                    close_friends.add(lv.get("value"))

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    mutual = followers.intersection(following)
    unilateral_following = following - followers

    metrics = {
        "total_followers": len(followers),
        "total_following": len(following),
        "total_close_friends": len(close_friends),
        "mutual_count": len(mutual),
        "unilateral_following_count": len(unilateral_following),
        "reciprocity_rate": round(
            len(mutual) / len(following) * 100, 2
        ) if following else 0,
        "close_friends_in_following_rate": round(
            len(close_friends.intersection(following)) / len(following) * 100, 2
        ) if following else 0
    }

    return metrics, followers, following, close_friends


@st.cache_data
def load_login_activity(filepath="data/login_activity.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        records = []

        for item in data.get("account_history_login_history", []):
            string_map = item.get("string_map_data", {})
            ts = string_map.get("Fecha y hora", {}).get("timestamp", 0)
            user_agent = string_map.get("Agente del usuario", {}).get("value", "")
            ip = string_map.get("Dirección IP", {}).get("value", "")

            device = "Desconocido"

            if "Windows" in user_agent:
                device = "Windows PC"
            elif "Macintosh" in user_agent:
                device = "Mac / macOS"
            elif "iPhone" in user_agent or "iPad" in user_agent:
                device = "Dispositivo iOS"
            elif "Android" in user_agent:
                device = "Dispositivo Android"

            records.append({
                "timestamp": pd.to_datetime(ts, unit="s"),
                "device": device,
                "ip": ip
            })

        df = pd.DataFrame(records)
        return add_calendar_columns(df)

    except (FileNotFoundError, json.JSONDecodeError):
        return pd.DataFrame()
