# Google Play Heatmap Dashboard

import pandas as pd
import altair as alt


# Load and clean the data
gps_apps_df = pd.read_csv('googleplaystore.csv')

gps_apps_df = gps_apps_df.dropna(
      subset = ["Content Rating", "Category", "Reviews", "Installs", "Rating"]
)

# convert installs like 1,000,000 -> 1000000
def parse_installs(s):
    s = str(s).replace('+', '').replace(',','')
    return int(s) if s.isdigit() else 0


# Convert numeric feilds
gps_apps_df["Reviews"] = pd.to_numeric(gps_apps_df["Reviews"], errors = "coerce")
gps_apps_df["Rating"] = pd.to_numeric(gps_apps_df["Rating"], errors = "coerce")
gps_apps_df["Installs"] = gps_apps_df["Installs"].map(parse_installs)


# Legend filtering off content rating
content_selector = alt.selection_point(
      fields = ["Content Rating"],
      bind = "legend",
      name = "content_selector",
)

# Brush selection on heatmap, filter by category
category_brush = alt.selection_interval(
      encodings = ["x"],
      name = "category_brush",
)

# Slider for installs
install_slider = alt.param(
      "min_installs",
      value = 0,
      bind = alt.binding_range(
            min = 0,
            max = 1200000000,
            step = 100,
            name = "min installs",
      ),
)

# Filter for all charts
install_filter = alt.datum.Installs >= install_slider

# KPI, number of apps after all filters
kpi = (
    alt.Chart(gps_apps_df)
    .mark_text(align = "left", baseline = "top", fontSize = 20)
    .encode(
          text = alt.Text("count():Q", format = ",.0f"),
    )
    .transform_filter(install_filter)
    .transform_filter(category_brush)
    .transform_filter(content_selector)
    .properties(
        width = 200,
        height = 80,
        title = "Apps after Filters"
    )
    # add in parameters so the KPI updates
    .add_params(install_slider, category_brush, content_selector)
)

# Heatmap, category x binned rating (binned)
heatmap = (
    alt.Chart(gps_apps_df)
    .mark_rect()
    .encode(
        x = alt.X("Category:N", title = "Category"),
        y = alt.Y(
            "Rating:Q",
            bin = alt.Bin(step = 0.5),
            title = "Rating (binned)",
            axis = alt.Axis(
                values = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
            ),
        ),

        # green blue gradient based off number of apps in the bin
        color = alt.Color("count():Q", title = "Apps", scale = alt.Scale(scheme = "greenblue")), 
        tooltip = [
            alt.Tooltip("Category:N", title = "Category"),
            alt.Tooltip("count():Q", title = "Apps in bin"),
        ],
    )
    .transform_filter(install_filter)
    .transform_filter(content_selector)
    .properties(
        width = 800,
        height = 270,
        title = "Category x Rating (binned)",
    )
    .add_params(category_brush, install_slider)
)

# Bar chart, apps per content rating
bar = (
    alt.Chart(gps_apps_df)
    .mark_bar()
    .encode(
        x = alt.X("Content Rating:N", title = "Content Rating"),
        y = alt.Y("count():Q", title = "Apps"),

        # opacity lowers on unselected values
        opacity = alt.condition(
            content_selector,
            alt.value(1.0),
            alt.value(0.2),
        ),

        # Color applied when selected 
        color = alt.condition(
              content_selector,
              alt.Color(
                  "Content Rating:N",
                  legend = alt.Legend(title = "Content Rating"),
              ),
              alt.value("lightgrey"),
        ),
        tooltip = [
            alt.Tooltip("Content Rating:N", title = "Content Rating"),
            alt.Tooltip("count():Q", title = "# Apps"),
        ],
    )
    .transform_filter(install_filter)
    .transform_filter(category_brush)
    .properties(
          width = 150,
          height = 270,
          title = "Apps by Content Rating")
    .add_params(content_selector)
)


# Scatter plot, reviews (log) vs rating
scatter = (
    alt.Chart(gps_apps_df)
    .mark_circle(size = 30, opacity = 0.6, color = "steelblue")
    .encode(
        x = alt.X(
            "Reviews:Q",
            scale = alt.Scale(type = "log"),
            title = "Reviews (log)",
        ),
        y = alt.Y("Rating:Q", title = "Rating", axis = alt.Axis(values = [1, 2, 3, 4, 5]),),
        tooltip = [
            alt.Tooltip("App:N", title = "App"),
            alt.Tooltip("Category:N", title = "Category"),
            alt.Tooltip("Content Rating:N", title = "Content Rating"),
            alt.Tooltip("Rating:Q", title = "Rating"),
            alt.Tooltip("Reviews:Q", title = "Reviews"),
            alt.Tooltip("Installs:Q", title = "Installs"),
        ],
    )
    # Respond to all filters
    .transform_filter(install_filter)
    .transform_filter(category_brush)
    .transform_filter(content_selector)
    .properties(
        width = 1200,
        height = 300,
        title = "Reviews vs Rating",
    )
)

# Set up final layout
overview = alt.hconcat(kpi, heatmap, bar)

# Full dashboard
dashboard = alt.vconcat(overview, scatter).properties(
    title = "Google Play Store - Heatmap Linked Dashboard"
)

# Save HTML
dashboard.save("visuals/google_play_heatmap_dashboard.html")