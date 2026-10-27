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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --accent: #E1306C;
    --accent-light: #F77737;
    --text-main: #F5F5F7;
    --text-muted: #A7A9B4;
    --border: rgba(255, 255, 255, 0.09);
    --surface: rgba(255, 255, 255, 0.035);
    --surface-hover: rgba(255, 255, 255, 0.065);
}

html, body, [class*="st-"], [data-testid="stApp"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6,
[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif;
}

h1 {
    font-size: 2.65rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px !important;
    line-height: 1.2 !important;
    padding-bottom: 0.35rem;
}

h2 {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px !important;
    margin-top: 0.5rem !important;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.35px !important;
}

p, li, label, [data-testid="stMarkdownContainer"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] .main .block-container {
    padding-top: 2.5rem;
    padding-bottom: 3.5rem;
    max-width: 1500px;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stCaptionContainer"] {
    color: var(--text-muted);
}

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    transition: border-color 0.2s ease, background 0.2s ease;
}

[data-testid="stMetric"]:hover {
    background: var(--surface-hover);
    border-color: rgba(225, 48, 108, 0.4);
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-main) !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px;
}

[data-testid="stMetricDelta"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stTabs"] {
    margin-top: 1.6rem;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 16px;
    height: auto;
    transition: all 0.2s ease;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: var(--surface-hover);
    border-color: rgba(225, 48, 108, 0.35);
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(225, 48, 108, 0.12) !important;
    border-color: rgba(225, 48, 108, 0.55) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background-color: var(--accent);
    height: 3px;
}

[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none;
}

[data-testid="stPlotlyChart"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 10px;
    overflow: hidden;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid var(--border);
}

[data-testid="stMarkdownContainer"] a {
    color: #F77737;
}

hr {
    border-color: var(--border);
    margin: 1.5rem 0;
}

[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
}

@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        padding: 1.5rem 1rem 2rem;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        padding: 8px 10px;
    }
}
</style>
""", unsafe_allow_html=True)

pio.templates["instagram_theme"] = pio.templates["plotly_dark"]
pio.templates["instagram_theme"].layout.font.family = "Inter, sans-serif"
pio.templates["instagram_theme"].layout.font.size = 12
pio.templates["instagram_theme"].layout.title.font.family = "Manrope, sans-serif"
pio.templates["instagram_theme"].layout.title.font.size = 17
pio.templates["instagram_theme"].layout.title.font.color = "#F5F5F7"
pio.templates["instagram_theme"].layout.paper_bgcolor = "rgba(0,0,0,0)"
pio.templates["instagram_theme"].layout.plot_bgcolor = "rgba(0,0,0,0)"
pio.templates["instagram_theme"].layout.font.color = "#D8D9E0"
pio.templates["instagram_theme"].layout.colorway = [
    "#E1306C",
    "#F77737",
    "#833AB4",
    "#4F9DDE",
    "#38BFA7",
    "#F2C14E",
    "#A78BFA"
]
pio.templates["instagram_theme"].layout.margin = dict(l=20, r=20, t=65, b=25)
pio.templates["instagram_theme"].layout.autosize = True
pio.templates["instagram_theme"].layout.xaxis = dict(
    showgrid=False,
    zeroline=False,
    linecolor="rgba(255,255,255,0.12)",
    tickfont=dict(color="#A7A9B4", size=11),
    title_font=dict(color="#D8D9E0")
)
pio.templates["instagram_theme"].layout.yaxis = dict(
    showgrid=True,
    gridcolor="rgba(255,255,255,0.07)",
    zeroline=False,
    linecolor="rgba(255,255,255,0.12)",
    tickfont=dict(color="#A7A9B4", size=11),
    title_font=dict(color="#D8D9E0")
)
pio.templates["instagram_theme"].layout.legend = dict(
    bgcolor="rgba(0,0,0,0)",
    borderwidth=0,
    font=dict(size=11, color="#D8D9E0")
)
pio.templates.default = "instagram_theme"

st.title("Hábitos Digitales: Instagram")
st.markdown(
    "Explora tus patrones de actividad, interacciones, relaciones sociales y seguridad digital."
)

st.markdown(
    "<div style='height:1px;background:linear-gradient(90deg,#E1306C,rgba(247,119,55,0.25),transparent);margin:1.2rem 0 1.5rem 0;'></div>",
    unsafe_allow_html=True
)

try:
    df_posts = load_liked_posts()
    df_comments = load_liked_comments()
    rel_data, followers, following, close_friends = load_relationships()
    df_logins = load_login_activity()

    time_metrics = calculate_time_metrics(df_posts, df_comments)
    density_metrics = calculate_density_metrics(df_posts, df_comments)
    net_metrics = calculate_network_advanced_metrics(
        followers,
        following,
        close_friends
    )
    sec_metrics = calculate_security_metrics(df_logins)
    data_loaded = True
except Exception as e:
    st.error(
        f"Error al cargar o procesar los datos JSON desde la carpeta 'data/': {e}"
    )
    data_loaded = False

if data_loaded:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Actividad",
        "Interacciones",
        "Relaciones",
        "Seguridad",
        "Resumen EDA"
    ])

    with tab1:
        st.header("¿Cuándo soy más activo?")
        st.markdown(
            "Descubre tus horarios de mayor actividad, hábitos nocturnos y diferencias entre días laborales y fines de semana."
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Interacciones totales",
            f"{time_metrics.get('total_interactions', 0):,}"
        )
        c2.metric(
            "Hora pico de actividad",
            f"{time_metrics.get('peak_hour', 0):02d}:00 hrs"
        )

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
        peak_day_display = day_translation.get(
            raw_peak_day,
            raw_peak_day or "N/A"
        )

        c3.metric("Día más activo", peak_day_display)
        c4.metric(
            "Actividad nocturna",
            f"{time_metrics.get('night_interactions_pct', 0)}%",
            help="Porcentaje de interacciones registradas entre las 00:00 y las 06:00."
        )

        st.divider()

        col_left, col_right = st.columns(2, gap="large")

        with col_left:
            st.subheader("Actividad por hora del día")

            df_hourly_list = []

            if not df_posts.empty and "hour" in df_posts.columns:
                df_posts_h = df_posts["hour"].value_counts().reset_index()
                df_posts_h.columns = ["hour", "count"]
                df_posts_h["Tipo"] = "Likes en posts"
                df_hourly_list.append(df_posts_h)

            if not df_comments.empty and "hour" in df_comments.columns:
                df_comments_h = df_comments["hour"].value_counts().reset_index()
                df_comments_h.columns = ["hour", "count"]
                df_comments_h["Tipo"] = "Likes en comentarios"
                df_hourly_list.append(df_comments_h)

            if df_hourly_list:
                df_hourly = pd.concat(
                    df_hourly_list,
                    ignore_index=True
                )

                fig_hourly = px.bar(
                    df_hourly,
                    x="hour",
                    y="count",
                    color="Tipo",
                    barmode="group",
                    labels={
                        "hour": "Hora del día",
                        "count": "Interacciones",
                        "Tipo": "Tipo de interacción"
                    },
                    title="Volumen de interacciones",
                    color_discrete_sequence=["#E1306C", "#F77737"]
                )

                fig_hourly.update_xaxes(
                    tickmode="linear",
                    dtick=2,
                    range=[-0.5, 23.5]
                )

                fig_hourly.update_traces(
                    marker_line_width=0,
                    opacity=0.9
                )

                st.plotly_chart(
                    fig_hourly,
                    use_container_width=True
                )
            else:
                st.info("No hay suficientes datos horarios para mostrar el gráfico.")

        with col_right:
            st.subheader("Entre semana vs. fin de semana")

            if not df_posts.empty and "is_weekend" in df_posts.columns:
                df_posts_copy = df_posts.copy()
                df_posts_copy["day_type"] = df_posts_copy["is_weekend"].map({
                    True: "Fin de semana",
                    False: "Entre semana"
                })

                fig_weekend = px.pie(
                    df_posts_copy,
                    names="day_type",
                    title="Distribución de likes en posts",
                    hole=0.62,
                    color="day_type",
                    color_discrete_map={
                        "Entre semana": "#833AB4",
                        "Fin de semana": "#F77737"
                    }
                )

                fig_weekend.update_traces(
                    textposition="outside",
                    textinfo="percent+label",
                    marker=dict(
                        line=dict(
                            color="rgba(0,0,0,0)",
                            width=2
                        )
                    ),
                    hovertemplate="%{label}<br>Interacciones: %{value}<br>Porcentaje: %{percent}<extra></extra>"
                )

                st.plotly_chart(
                    fig_weekend,
                    use_container_width=True
                )
            else:
                st.info("No hay suficientes datos para comparar los días.")

        st.divider()
        st.subheader("Tu ritmo de actividad semanal")

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
                title="Tendencia semanal de interacciones",
                category_orders={"Día": days_order},
                color_discrete_sequence=["#E1306C"]
            )

            fig_daily.update_traces(
                line=dict(width=3),
                marker=dict(size=9, line=dict(width=2, color="#191923")),
                fill="tozeroy",
                fillcolor="rgba(225,48,108,0.10)",
                hovertemplate="%{x}<br>Interacciones: %{y}<extra></extra>"
            )

            fig_daily.update_xaxes(
                type="category",
                categoryorder="array",
                categoryarray=days_order
            )

            st.plotly_chart(
                fig_daily,
                use_container_width=True
            )
        else:
            st.info("No hay datos diarios para mostrar la tendencia semanal.")

    with tab2:
        st.header("¿Dónde se concentran mis interacciones?")
        st.markdown(
            "Identifica las cuentas y los autores que reciben más likes, y observa qué tan concentrada está tu actividad."
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Cuentas únicas con likes",
            f"{density_metrics.get('unique_post_accounts_count', 0):,}"
        )
        c2.metric(
            "Concentración del top 10",
            f"{density_metrics.get('top10_posts_concentration_pct', 0)}%",
            help="Porcentaje de likes en posts concentrado en las diez cuentas principales, según las métricas calculadas."
        )

        st.divider()

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.subheader("Cuentas con más likes")

            top_posts = density_metrics.get("top_post_accounts", {})

            if top_posts:
                top_posts_df = pd.DataFrame(
                    list(top_posts.items()),
                    columns=["Cuenta", "Likes"]
                ).sort_values(
                    "Likes",
                    ascending=True
                ).tail(10)

                fig_top_p = px.bar(
                    top_posts_df,
                    x="Likes",
                    y="Cuenta",
                    orientation="h",
                    title="Top 10 cuentas",
                    color="Likes",
                    color_continuous_scale=["#833AB4", "#E1306C", "#F77737"],
                    labels={
                        "Likes": "Cantidad de likes",
                        "Cuenta": "Cuenta"
                    }
                )

                fig_top_p.update_layout(
                    coloraxis_showscale=False,
                    yaxis=dict(
                        categoryorder="total ascending",
                        showgrid=False
                    )
                )

                fig_top_p.update_traces(
                    marker_line_width=0,
                    opacity=0.95,
                    hovertemplate="%{y}<br>Likes: %{x}<extra></extra>"
                )

                st.plotly_chart(
                    fig_top_p,
                    use_container_width=True
                )
            else:
                st.info("No hay datos de cuentas para posts.")

        with col2:
            st.subheader("Autores con más likes en comentarios")

            top_comments = density_metrics.get(
                "top_comment_authors",
                {}
            )

            if top_comments:
                top_comm_df = pd.DataFrame(
                    list(top_comments.items()),
                    columns=["Autor", "Likes"]
                ).sort_values(
                    "Likes",
                    ascending=True
                ).tail(10)

                fig_top_c = px.bar(
                    top_comm_df,
                    x="Likes",
                    y="Autor",
                    orientation="h",
                    title="Top 10 autores",
                    color="Likes",
                    color_continuous_scale=["#4F9DDE", "#833AB4", "#E1306C"],
                    labels={
                        "Likes": "Cantidad de likes",
                        "Autor": "Autor"
                    }
                )

                fig_top_c.update_layout(
                    coloraxis_showscale=False,
                    yaxis=dict(
                        categoryorder="total ascending",
                        showgrid=False
                    )
                )

                fig_top_c.update_traces(
                    marker_line_width=0,
                    opacity=0.95,
                    hovertemplate="%{y}<br>Likes: %{x}<extra></extra>"
                )

                st.plotly_chart(
                    fig_top_c,
                    use_container_width=True
                )
            else:
                st.info("No hay datos de autores para comentarios.")

        st.divider()
        st.subheader("Interacciones de baja frecuencia")
        st.markdown(
            "Cuentas con las que tu actividad ha sido puntual durante el periodo analizado."
        )

        if not df_posts.empty and "owner" in df_posts.columns:
            low_density_count = (
                df_posts["owner"].value_counts() == 1
            ).sum()

            metric_col, info_col = st.columns([1, 2])

            metric_col.metric(
                "Cuentas con un solo like",
                f"{low_density_count:,}"
            )

            with info_col:
                st.markdown(
                    "<div style='background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.09);border-radius:14px;padding:18px 20px;margin-top:4px;'>"
                    "<div style='font-family:Manrope,sans-serif;font-weight:700;margin-bottom:6px;'>Interacciones puntuales</div>"
                    "<div style='color:#A7A9B4;font-size:0.9rem;line-height:1.6;'>Este indicador contabiliza las cuentas que aparecen exactamente una vez en los likes de posts del periodo analizado.</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No hay datos de cuentas para analizar las interacciones puntuales.")

    with tab3:
        st.header("Mi red social y reciprocidad")
        st.markdown(
            "Explora el equilibrio entre seguidores y seguidos, las relaciones mutuas y la presencia de Close Friends en tu red."
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric(
            "Seguidores",
            f"{net_metrics.get('followers_count', 0):,}"
        )
        m2.metric(
            "Seguidos",
            f"{net_metrics.get('following_count', 0):,}"
        )
        m3.metric(
            "Tasa de reciprocidad",
            f"{net_metrics.get('reciprocity_rate_pct', 0)}%"
        )
        m4.metric(
            "Close Friends en seguidos",
            f"{net_metrics.get('close_friends_coverage_in_following_pct', 0)}%"
        )

        st.divider()

        col_a, col_b = st.columns(2, gap="large")

        with col_a:
            st.subheader("Composición de la red")

            net_df = pd.DataFrame({
                "Tipo de relación": [
                    "Mutuos",
                    "Seguidos unilaterales",
                    "Seguidores unilaterales"
                ],
                "Cantidad": [
                    net_metrics.get("mutual_count", 0),
                    net_metrics.get("unilateral_following_count", 0),
                    net_metrics.get("unilateral_followers_count", 0)
                ]
            })

            fig_net = px.bar(
                net_df,
                x="Tipo de relación",
                y="Cantidad",
                color="Tipo de relación",
                title="Desglose de relaciones",
                color_discrete_sequence=[
                    "#38BFA7",
                    "#833AB4",
                    "#F77737"
                ],
                labels={
                    "Tipo de relación": "Tipo de relación",
                    "Cantidad": "Número de cuentas"
                }
            )

            fig_net.update_layout(
                showlegend=False,
                xaxis=dict(
                    tickangle=-12,
                    showgrid=False
                )
            )

            fig_net.update_traces(
                marker_line_width=0,
                opacity=0.9,
                hovertemplate="%{x}<br>Cuentas: %{y}<extra></extra>"
            )

            st.plotly_chart(
                fig_net,
                use_container_width=True
            )

        with col_b:
            st.subheader("Tu círculo de Close Friends")

            total_cf = net_metrics.get("close_friends_count", 0)
            purity_pct = net_metrics.get("close_friends_purity_pct", 0)
            mutuos_cf = int(total_cf * (purity_pct / 100))
            no_mutuos_cf = total_cf - mutuos_cf

            cf_df = pd.DataFrame({
                "Estado": [
                    "Close Friends mutuos",
                    "Close Friends no mutuos"
                ],
                "Cuentas": [
                    mutuos_cf,
                    no_mutuos_cf
                ]
            })

            fig_cf = px.pie(
                cf_df,
                names="Estado",
                values="Cuentas",
                title="Reciprocidad dentro de Close Friends",
                hole=0.62,
                color="Estado",
                color_discrete_map={
                    "Close Friends mutuos": "#38BFA7",
                    "Close Friends no mutuos": "#833AB4"
                }
            )

            fig_cf.update_traces(
                textposition="outside",
                textinfo="percent+label",
                marker=dict(
                    line=dict(
                        color="rgba(0,0,0,0)",
                        width=2
                    )
                ),
                hovertemplate="%{label}<br>Cuentas: %{value}<br>Porcentaje: %{percent}<extra></extra>"
            )

            st.plotly_chart(
                fig_cf,
                use_container_width=True
            )

        st.divider()

        st.subheader("Lectura de tus relaciones")

        r1, r2 = st.columns(2)

        with r1:
            st.markdown(
                "<div style='background:rgba(56,191,167,0.07);border:1px solid rgba(56,191,167,0.22);border-radius:14px;padding:18px 20px;'>"
                "<div style='font-family:Manrope,sans-serif;font-weight:700;margin-bottom:6px;'>Relaciones recíprocas</div>"
                "<div style='color:#A7A9B4;font-size:0.9rem;line-height:1.6;'>Cuentas que aparecen tanto entre tus seguidores como entre las personas que sigues.</div>"
                "</div>",
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(
                "<div style='background:rgba(131,58,180,0.08);border:1px solid rgba(131,58,180,0.25);border-radius:14px;padding:18px 20px;'>"
                "<div style='font-family:Manrope,sans-serif;font-weight:700;margin-bottom:6px;'>Relaciones unilaterales</div>"
                "<div style='color:#A7A9B4;font-size:0.9rem;line-height:1.6;'>Cuentas en las que el seguimiento no es mutuo. Distingue entre quienes sigues y quienes te siguen.</div>"
                "</div>",
                unsafe_allow_html=True
            )

    with tab4:
        st.header("Seguridad y privacidad digital")
        st.markdown(
            "Revisa los registros de acceso, los dispositivos utilizados y la distribución temporal de tus inicios de sesión."
        )

        s1, s2, s3, s4 = st.columns(4)

        s1.metric(
            "Inicios de sesión",
            f"{sec_metrics.get('total_logins', 0):,}"
        )
        s2.metric(
            "Dispositivos únicos",
            f"{sec_metrics.get('unique_devices_count', 0):,}"
        )
        s3.metric(
            "Direcciones IP únicas",
            f"{sec_metrics.get('unique_ips_count', 0):,}"
        )
        s4.metric(
            "Intervalo promedio",
            f"{sec_metrics.get('avg_hours_between_logins', 0)} hrs",
            help="Tiempo promedio entre inicios de sesión, según los registros disponibles."
        )

        st.divider()

        col_x, col_y = st.columns(2, gap="large")

        with col_x:
            st.subheader("Dispositivos y navegadores")

            devices = sec_metrics.get("device_breakdown", {})

            if devices:
                dev_df = pd.DataFrame(
                    list(devices.items()),
                    columns=["Dispositivo", "Logins"]
                ).sort_values(
                    "Logins",
                    ascending=False
                )

                fig_dev = px.pie(
                    dev_df,
                    names="Dispositivo",
                    values="Logins",
                    title="Distribución por dispositivo",
                    hole=0.62,
                    color_discrete_sequence=[
                        "#E1306C",
                        "#833AB4",
                        "#F77737",
                        "#4F9DDE",
                        "#38BFA7",
                        "#F2C14E"
                    ]
                )

                fig_dev.update_traces(
                    textposition="outside",
                    textinfo="percent+label",
                    marker=dict(
                        line=dict(
                            color="rgba(0,0,0,0)",
                            width=2
                        )
                    ),
                    hovertemplate="%{label}<br>Inicios de sesión: %{value}<br>Porcentaje: %{percent}<extra></extra>"
                )

                st.plotly_chart(
                    fig_dev,
                    use_container_width=True
                )
            else:
                st.info("No hay registros de dispositivos.")

        with col_y:
            st.subheader("Horarios de acceso")

            if not df_logins.empty and "hour" in df_logins.columns:
                fig_log_h = px.histogram(
                    df_logins,
                    x="hour",
                    nbins=24,
                    labels={
                        "hour": "Hora del día",
                        "count": "Inicios de sesión"
                    },
                    title="Frecuencia de inicios de sesión",
                    color_discrete_sequence=["#833AB4"]
                )

                fig_log_h.update_xaxes(
                    tickmode="linear",
                    dtick=2,
                    range=[-0.5, 23.5]
                )

                fig_log_h.update_traces(
                    marker_line_width=0,
                    opacity=0.9,
                    hovertemplate="Hora: %{x}<br>Registros: %{y}<extra></extra>"
                )

                st.plotly_chart(
                    fig_log_h,
                    use_container_width=True
                )
            else:
                st.info("No hay registros horarios de inicios de sesión.")

        st.divider()

        st.subheader("Indicadores de seguridad")

        sec_col1, sec_col2 = st.columns(2)

        with sec_col1:
            st.markdown(
                "<div style='background:rgba(79,157,222,0.07);border:1px solid rgba(79,157,222,0.23);border-radius:14px;padding:18px 20px;'>"
                "<div style='font-family:Manrope,sans-serif;font-weight:700;margin-bottom:6px;'>Diversidad de dispositivos</div>"
                "<div style='color:#A7A9B4;font-size:0.9rem;line-height:1.6;'>Compara los dispositivos y navegadores registrados para reconocer patrones habituales de acceso.</div>"
                "</div>",
                unsafe_allow_html=True
            )

        with sec_col2:
            st.markdown(
                "<div style='background:rgba(225,48,108,0.07);border:1px solid rgba(225,48,108,0.23);border-radius:14px;padding:18px 20px;'>"
                "<div style='font-family:Manrope,sans-serif;font-weight:700;margin-bottom:6px;'>Huella de acceso</div>"
                "<div style='color:#A7A9B4;font-size:0.9rem;line-height:1.6;'>Los cambios de dispositivo, IP u horario pueden servir como puntos de revisión, pero no demuestran por sí solos un acceso no autorizado.</div>"
                "</div>",
                unsafe_allow_html=True
            )

    with tab5:
        st.header("Resumen de métricas EDA")
        st.markdown(
            "Consulta los indicadores principales de tu actividad digital en una sola tabla, lista para revisar o utilizar en tu informe."
        )

        summary_data = {
            "Categoría": [
                "Hábitos temporales",
                "Hábitos temporales",
                "Hábitos temporales",
                "Densidad de interacción",
                "Densidad de interacción",
                "Análisis de red",
                "Análisis de red",
                "Análisis de red",
                "Seguridad y privacidad",
                "Seguridad y privacidad"
            ],
            "Métrica": [
                "Total de interacciones",
                "Hora pico de actividad",
                "Actividad nocturna",
                "Cuentas únicas interactuadas",
                "Concentración del top 10",
                "Total de seguidores",
                "Total de seguidos",
                "Tasa de reciprocidad",
                "Total de inicios de sesión",
                "Dispositivos únicos"
            ],
            "Valor": [
                str(time_metrics.get("total_interactions", 0)),
                f"{time_metrics.get('peak_hour', 0):02d}:00 hrs",
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

        summary_df = pd.DataFrame(summary_data)

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
            height=390,
            column_config={
                "Categoría": st.column_config.TextColumn(
                    "Categoría",
                    width="medium"
                ),
                "Métrica": st.column_config.TextColumn(
                    "Indicador",
                    width="large"
                ),
                "Valor": st.column_config.TextColumn(
                    "Resultado",
                    width="medium"
                )
            }
        )

        st.divider()

        st.subheader("Distribución de indicadores")

        category_counts = summary_df["Categoría"].value_counts().reset_index()
        category_counts.columns = ["Categoría", "Indicadores"]

        fig_summary = px.bar(
            category_counts,
            x="Categoría",
            y="Indicadores",
            color="Categoría",
            title="Indicadores por área de análisis",
            color_discrete_sequence=[
                "#E1306C",
                "#833AB4",
                "#F77737",
                "#4F9DDE"
            ],
            labels={
                "Categoría": "Área de análisis",
                "Indicadores": "Número de indicadores"
            }
        )

        fig_summary.update_layout(
            showlegend=False,
            xaxis=dict(
                tickangle=-12,
                showgrid=False
            )
        )

        fig_summary.update_traces(
            marker_line_width=0,
            opacity=0.9,
            hovertemplate="%{x}<br>Indicadores: %{y}<extra></extra>"
        )

        st.plotly_chart(
            fig_summary,
            use_container_width=True
        )

        st.caption(
            "Los resultados dependen de los registros disponibles en los archivos JSON de la carpeta data."
        )

    st.markdown(
        "<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(225,48,108,0.5),transparent);margin:2rem 0 1rem 0;'></div>"
        "<div style='text-align:center;color:#858794;font-family:Inter,sans-serif;font-size:0.78rem;padding:0.5rem 0 1rem 0;'>"
        "HÁBITOS DIGITALES · INSTAGRAM"
        "<div style='margin-top:5px;'>Análisis personal de actividad e interacciones digitales</div>"
        "</div>",
        unsafe_allow_html=True
    )