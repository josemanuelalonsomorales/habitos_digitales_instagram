import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.io as pio

from utils.data_loader import (
    load_liked_posts,
    load_liked_comments,
    load_relationships,
    load_login_activity
)

from utils.metrics import (
    calculate_time_metrics,
    calculate_density_metrics,
    calculate_network_advanced_metrics,
    calculate_security_metrics
)

st.set_page_config(
    page_title="Hábitos Digitales: Instagram",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"], [data-testid="stApp"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    letter-spacing: -0.4px;
}

[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stDataFrame"] {
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

pio.templates["instagram_theme"] = pio.templates["plotly_dark"]
pio.templates["instagram_theme"].layout.font.family = "Inter, sans-serif"
pio.templates["instagram_theme"].layout.title.font.family = "Inter, sans-serif"
pio.templates.default = "instagram_theme"

st.title("Hábitos Digitales: Instagram")
st.markdown("Análisis exploratorio de interacción, patrones temporales, relaciones de red y seguridad digital.")

try:
    df_posts = load_liked_posts()
    df_comments = load_liked_comments()
    rel_data, followers, following, close_friends = load_relationships()
    df_logins = load_login_activity()

    time_metrics = calculate_time_metrics(df_posts, df_comments)
    density_metrics = calculate_density_metrics(df_posts, df_comments)
    net_metrics = calculate_network_advanced_metrics(followers, following, close_friends)
    sec_metrics = calculate_security_metrics(df_logins)
    data_loaded = True
except Exception as e:
    st.error(f"Error al cargar o procesar los datos JSON desde la carpeta 'data/': {e}")
    data_loaded = False

if data_loaded:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "¿Cuándo soy más activo?",
        "Interacciones Densas y Bajas",
        "Relaciones e Interacciones Sociales",
        "Logins y Privacidad Digital",
        "Resumen de Métricas EDA"
    ])

    with tab1:
        st.header("¿Cuándo soy más activo?")
        st.markdown("Análisis de patrones de actividad por hora del día, hábitos nocturnos e interacción en fines de semana.")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Interacciones Totales", time_metrics.get("total_interactions", 0))
        c2.metric("Hora Pico de Actividad", f"{time_metrics.get('peak_hour', 0)}:00 hrs")

        day_translation = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo",
            "Lunes": "Lunes",
            "Martes": "Martes",
            "Miércoles": "Miércoles",
            "Jueves": "Jueves",
            "Viernes": "Viernes",
            "Sábado": "Sábado",
            "Domingo": "Domingo"
        }

        raw_peak_day = time_metrics.get("peak_day", "")
        peak_day_display = day_translation.get(raw_peak_day, raw_peak_day or "N/A")
        c3.metric("Día Más Activo", peak_day_display)
        c4.metric("Actividad Nocturna (00-06 hrs)", f"{time_metrics.get('night_interactions_pct', 0)}%")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Distribución de Actividad por Hora del Día")
            df_hourly_list = []

            if not df_posts.empty and "hour" in df_posts.columns:
                df_posts_h = df_posts["hour"].value_counts().reset_index()
                df_posts_h.columns = ["hour", "count"]
                df_posts_h["Tipo"] = "Likes en Posts"
                df_hourly_list.append(df_posts_h)

            if not df_comments.empty and "hour" in df_comments.columns:
                df_comments_h = df_comments["hour"].value_counts().reset_index()
                df_comments_h.columns = ["hour", "count"]
                df_comments_h["Tipo"] = "Likes en Comentarios"
                df_hourly_list.append(df_comments_h)

            if df_hourly_list:
                df_hourly = pd.concat(df_hourly_list, ignore_index=True)
                fig_hourly = px.bar(
                    df_hourly,
                    x="hour",
                    y="count",
                    color="Tipo",
                    barmode="group",
                    labels={
                        "hour": "Hora (0-23 hrs)",
                        "count": "Cantidad de Interacciones"
                    },
                    title="Volumen de Interacciones por Hora"
                )
                st.plotly_chart(fig_hourly, use_container_width=True)
            else:
                st.info("No hay suficientes datos de hora para mostrar el gráfico.")

        with col_right:
            st.subheader("Distribución: Entre Semana vs. Fin de Semana")

            if not df_posts.empty and "is_weekend" in df_posts.columns:
                df_posts_copy = df_posts.copy()
                df_posts_copy["day_type"] = df_posts_copy["is_weekend"].map({
                    True: "Fin de Semana",
                    False: "Entre Semana"
                })

                fig_weekend = px.pie(
                    df_posts_copy,
                    names="day_type",
                    title="Proporción de Interacciones",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_weekend, use_container_width=True)
            else:
                st.info("No hay suficientes datos para la proporción de días.")

        st.subheader("Detalle de Actividad por Día de la Semana")
        daily_dist = time_metrics.get("daily_distribution", {})

        if daily_dist:
            days_order = [
                "Lunes",
                "Martes",
                "Miércoles",
                "Jueves",
                "Viernes",
                "Sábado",
                "Domingo"
            ]

            normalized_dist = {day: 0 for day in days_order}

            for day, count in daily_dist.items():
                translated_day = day_translation.get(day, day)

                if translated_day in normalized_dist:
                    normalized_dist[translated_day] += count

            df_daily = pd.DataFrame({
                "Día": days_order,
                "Interacciones": [
                    normalized_dist[day] for day in days_order
                ]
            })

            fig_daily = px.line(
                df_daily,
                x="Día",
                y="Interacciones",
                markers=True,
                title="Tendencia Semanal de Interacciones",
                category_orders={"Día": days_order}
            )

            fig_daily.update_xaxes(
                type="category",
                categoryorder="array",
                categoryarray=days_order
            )

            st.plotly_chart(fig_daily, use_container_width=True)
        else:
            st.info("No hay datos diarios para desplegar la tendencia semanal.")

    with tab2:
        st.header("¿Cuáles son mis interacciones más y menos densas?")
        st.markdown("Identificación de las cuentas y autores con mayor concentración de likes.")

        c1, c2 = st.columns(2)
        c1.metric(
            "Cuentas Únicas con Likes en Posts",
            density_metrics.get("unique_post_accounts_count", 0)
        )
        c2.metric(
            "Concentración Top 10 Cuentas",
            f"{density_metrics.get('top10_posts_concentration_pct', 0)}%"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Interacciones Más Densas (Top 10 Cuentas)")
            top_posts = density_metrics.get("top_post_accounts", {})

            if top_posts:
                top_posts_df = pd.DataFrame(
                    list(top_posts.items()),
                    columns=["Cuenta", "Likes"]
                ).sort_values("Likes", ascending=True)

                fig_top_p = px.bar(
                    top_posts_df,
                    x="Likes",
                    y="Cuenta",
                    orientation="h",
                    title="Top 10 Cuentas con Más Likes en Posts"
                )
                st.plotly_chart(fig_top_p, use_container_width=True)
            else:
                st.info("Sin datos de cuentas para posts.")

        with col2:
            st.subheader("Autores de Comentarios Más Likeados")
            top_comments = density_metrics.get("top_comment_authors", {})

            if top_comments:
                top_comm_df = pd.DataFrame(
                    list(top_comments.items()),
                    columns=["Autor", "Likes"]
                ).sort_values("Likes", ascending=True)

                fig_top_c = px.bar(
                    top_comm_df,
                    x="Likes",
                    y="Autor",
                    orientation="h",
                    title="Top 10 Autores de Comentarios Likeados"
                )
                st.plotly_chart(fig_top_c, use_container_width=True)
            else:
                st.info("Sin datos de autores para comentarios.")

        st.subheader("Interacciones Menos Densas")
        st.info("Cuentas a las que solo se les ha dado 1 o 2 likes en todo el periodo analizado.")

        if not df_posts.empty and "owner" in df_posts.columns:
            low_density_count = (df_posts["owner"].value_counts() == 1).sum()
            st.metric("Cuentas con Solo 1 Like (Baja Interacción)", low_density_count)

    with tab3:
        st.header("Análisis de Red, Cobertura y Reciprocidad")
        st.markdown("Estructura de seguidores, cuentas seguidas, relaciones unilaterales y círculos cercanos.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Seguidores (Followers)", net_metrics.get("followers_count", 0))
        m2.metric("Seguidos (Following)", net_metrics.get("following_count", 0))
        m3.metric("Tasa de Reciprocidad", f"{net_metrics.get('reciprocity_rate_pct', 0)}%")
        m4.metric(
            "Close Friends en Following",
            f"{net_metrics.get('close_friends_coverage_in_following_pct', 0)}%"
        )

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Composición General de la Red")

            net_df = pd.DataFrame({
                "Tipo de Relación": [
                    "Mutuos (Recíprocos)",
                    "Seguidos Unilaterales",
                    "Seguidores Unilaterales"
                ],
                "Cantidad": [
                    net_metrics.get("mutual_count", 0),
                    net_metrics.get("unilateral_following_count", 0),
                    net_metrics.get("unilateral_followers_count", 0)
                ]
            })

            fig_net = px.bar(
                net_df,
                x="Tipo de Relación",
                y="Cantidad",
                color="Tipo de Relación",
                title="Desglose de Relaciones"
            )
            st.plotly_chart(fig_net, use_container_width=True)

        with col_b:
            st.subheader("Estructura de Close Friends")
            total_cf = net_metrics.get("close_friends_count", 0)
            purity_pct = net_metrics.get("close_friends_purity_pct", 0)
            mutuos_cf = int(total_cf * (purity_pct / 100))
            no_mutuos_cf = total_cf - mutuos_cf

            cf_df = pd.DataFrame({
                "Estado": ["Close Friends Mutuos", "Close Friends No Mutuos"],
                "Cuentas": [mutuos_cf, no_mutuos_cf]
            })

            fig_cf = px.pie(
                cf_df,
                names="Estado",
                values="Cuentas",
                title="Relación de Reciprocidad en Close Friends",
                hole=0.3
            )
            st.plotly_chart(fig_cf, use_container_width=True)

    with tab4:
        st.header("Inicios de Sesión, Dispositivos y Privacidad Digital")
        st.markdown("Supervisión de seguridad, huella de accesos y dispersión de logins.")

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Inicios de Sesión", sec_metrics.get("total_logins", 0))
        s2.metric("Dispositivos Únicos", sec_metrics.get("unique_devices_count", 0))
        s3.metric("Direcciones IP Únicas", sec_metrics.get("unique_ips_count", 0))
        s4.metric(
            "Frecuencia Promedio de Login",
            f"{sec_metrics.get('avg_hours_between_logins', 0)} hrs"
        )

        col_x, col_y = st.columns(2)

        with col_x:
            st.subheader("Dispositivos Utilizados para Login")
            devices = sec_metrics.get("device_breakdown", {})

            if devices:
                dev_df = pd.DataFrame(
                    list(devices.items()),
                    columns=["Dispositivo", "Logins"]
                )

                fig_dev = px.pie(
                    dev_df,
                    names="Dispositivo",
                    values="Logins",
                    title="Distribución por Sistema Operativo/Navegador"
                )
                st.plotly_chart(fig_dev, use_container_width=True)
            else:
                st.info("Sin registros de dispositivos.")

        with col_y:
            st.subheader("Inicios de Sesión por Hora del Día")

            if not df_logins.empty and "hour" in df_logins.columns:
                fig_log_h = px.histogram(
                    df_logins,
                    x="hour",
                    nbins=24,
                    labels={"hour": "Hora (0-23 hrs)"},
                    title="Horarios Frecuentes de Login"
                )
                st.plotly_chart(fig_log_h, use_container_width=True)
            else:
                st.info("Sin registros de horarios de inicio de sesión.")

    with tab5:
        st.header("Resumen Consolidado de Métricas (EDA)")
        st.markdown("Tabla resumen con los indicadores procesados para exportación o análisis del informe.")

        summary_data = {
            "Categoría": [
                "Hábitos Temporales",
                "Hábitos Temporales",
                "Hábitos Temporales",
                "Densidad de Interacción",
                "Densidad de Interacción",
                "Análisis de Red",
                "Análisis de Red",
                "Análisis de Red",
                "Seguridad y Privacidad",
                "Seguridad y Privacidad"
            ],
            "Métrica": [
                "Total Interacciones",
                "Hora Pico de Actividad",
                "Porcentaje Actividad Nocturna",
                "Cuentas Únicas Interactuadas",
                "Concentración Top 10 Cuentas",
                "Total Seguidores",
                "Total Seguidos",
                "Tasa de Reciprocidad",
                "Total Inicios de Sesión",
                "Dispositivos Únicos Usados"
            ],
            "Valor": [
                str(time_metrics.get("total_interactions", 0)),
                f"{time_metrics.get('peak_hour', 0)}:00 hrs",
                f"{time_metrics.get('night_interactions_pct', 0)}%",
                str(density_metrics.get("unique_post_accounts_count", 0)),
                f"{density_metrics.get('top10_posts_concentration_pct', 0)}%",
                str(net_metrics.get("followers_count", 0)),
                str(net_metrics.get("following_count", 0)),
                f"{net_metrics.get('reciprocity_rate_pct', 0)}%",
                str(sec_metrics.get("total_logins", 0)),
                str(sec_metrics.get("unique_devices_count", 0))
            ]
        }

        st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
