# Google Play Dashboard


import pandas as pd
import altair as alt


# Load and clean the data
gps_apps_df = pd.read_csv('googleplaystore.csv')

gps_apps_df = gps_apps_df.dropna(
    subset = ["Category", "Content Rating", "Installs", "Reviews"]
)

# convert installs like 1,000,000 -> 1000000
def parse_installs(s):
    s = str(s).replace('+', '').replace(',','')
    return int(s) if s.isdigit() else 0

gps_apps_df["Installs"] = gps_apps_df["Installs"].map(parse_installs)

# Convert numeric feilds
gps_apps_df["Reviews"] = pd.to_numeric(gps_apps_df["Reviews"], errors = "coerce")
gps_apps_df["Rating"] = pd.to_numeric(gps_apps_df["Rating"], errors = "coerce")


# Legend filter by content rating
selection = alt.selection_point(
    fields = ["Content Rating"],
    bind = "legend",
    name = "rating_selector"
    )

# Brush selection for bar chart
brush = alt.selection_interval(
      encodings = ["x"],
      name = "category_brush",
)


# Set the max installs to use for slider
max_installs = gps_apps_df['Installs'].max()

# Installs slider, with steps of 10,000,000
installs = alt.param(
    "min_installs",
    value = 0,
    bind = alt.binding_range(
        min = 0,
        max = max_installs,
        step = 10000000,
        name = "min installs"
    )
)

# Filter for all charts
install_filter = alt.datum.Installs >= installs


# Category bar chart, apps per category
bar = (
      alt.Chart(gps_apps_df).mark_bar().encode(
        x = alt.X("Category:N", title = "Category"),
        y = alt.Y("count():Q", title = "Number of Apps"),
        
        tooltip = [
            alt.Tooltip("Category:N", title = "Category"),
            alt.Tooltip("count():Q", title = "# Apps"),
        ],
    )
    # Filter by slider
    .transform_filter(install_filter)

    .properties (
      width = 800,
      height = 200,
    )
    # Allow use of brush and slider
    .add_params(brush, installs)
)


# Scatter plot, rating vs reviews
scatter = (
    alt.Chart(gps_apps_df).mark_circle(fill = None).encode(
        x = alt.X("Rating:Q", title = "Rating"),
        y = alt.Y("Reviews:Q", title = "Reviews"),
        size = alt.Size("Installs:Q", title = "Installs", legend = None),
        color = alt.condition(
            selection,
            alt.Color(
                "Content Rating:N", legend = alt.Legend(title = "Content Rating"),
            ),
            alt.value("lightgrey"),
        ),

        stroke = alt.condition(
            selection,
            alt.Color("Content Rating:N"),
            alt.value("lightgrey")
        ),

        tooltip = [
            alt.Tooltip("App:N", title = "Apps"),
            alt.Tooltip("Category:N", title = "Category"),
            alt.Tooltip("Content Rating:N", title = "Content Rating"),
            alt.Tooltip("Rating:Q", title = "Rating"),
            alt.Tooltip("Reviews:Q", title = "Reviews"),
            alt.Tooltip("Installs:Q", title = "Installs"),
        ],
    )
    # Apply all filters
    .transform_filter(install_filter)
    .transform_filter(brush)
    .transform_filter(selection)
    .properties (
        width = 600,
        height = 300,
    )
    # Allow clicking the legend
    .add_params(selection)
)

# KPI, avg rating by content rating
kpi = (
    alt.Chart(gps_apps_df)
    .mark_bar()
    .encode(
        x = alt.X("Content Rating:N", title = "Content Rating"),
        y = alt.Y("mean(Rating):Q", title = "Avg Rating"),

        # Constant set color to avoid duplicate legend
        color = alt.value("steelblue"),
        tooltip = [
            alt.Tooltip("Content Rating:N", title = "Content Rating"),
            alt.Tooltip("mean(Rating):Q", title = "Avg Rating", format = ".2f"),
        ],
    )
    .transform_filter(install_filter) 
    .transform_filter(brush)
    .transform_filter(selection)     
    .properties(
        width = 250,
        height = 300,
    )
)


# Set up final layout
bottom = alt.hconcat(scatter, kpi)

# Full dashboard
dashboard = alt.vconcat(bar, bottom).properties(
    title = "Google Play Store - Linked Dashboard"
)

# Save to HTML
dashboard.save("visuals/google_play_dashboard.html")

