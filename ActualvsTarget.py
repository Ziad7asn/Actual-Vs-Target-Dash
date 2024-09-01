import dash
from dash import dcc, html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = dash.Dash(title="Actual VS Target")

# Function Definitions
def create_gauge_chart(month, actual, target, max_value):
    """Creates a gauge chart for a given month."""
    return go.Indicator(
        mode="gauge+number+delta",
        value=actual,
        delta={'reference': target},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "rgba(54, 162, 235, 0.7)"},
            'steps': [
                {'range': [0, target], 'color': "rgba(255, 99, 132, 0.5)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.75,
                'value': target}
        },
        title={'text': f"{month}"},
    )

def create_bar_chart(months, actual_sales, target_sales):
    """Creates a bar chart comparing actual vs target sales."""
    return [
        go.Bar(
            x=months,
            y=actual_sales,
            name='Actual Sales',
            marker_color='rgba(54, 162, 235, 0.7)',  # Soft blue
            showlegend=False
        ),
        go.Bar(
            x=months,
            y=target_sales,
            name='Target Sales',
            marker_color='rgba(255, 99, 132, 0.7)',  # Soft red
            showlegend=False
        )
    ]

def create_dashboard(months, target_sales, actual_sales):
    """Creates a composite dashboard with gauge and bar charts."""
    max_target = max(target_sales) + 2000  # Adjust the maximum range for gauges

    # Create subplots
    fig = make_subplots(
        rows=2, cols=4,
        row_heights=[0.5, 0.5],
        subplot_titles=("", "", "", "",
                        "Actual VS Target", "", "", ""),
        specs=[
            [{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}],  # Gauges
            [{"type": "xy", "colspan": 4}, None, None, None]  # Bar Chart
        ],
        vertical_spacing=0.15
    )

    # Add Gauge Charts
    for i, month in enumerate(months):
        fig.add_trace(create_gauge_chart(month, actual_sales[i], target_sales[i], max_target),
                      row=1, col=i+1)

    # Add Bar Charts
    for trace in create_bar_chart(months, actual_sales, target_sales):
        fig.add_trace(trace, row=2, col=1)

    # Layout settings
    fig.update_layout(
        title='',
        height=800,
        template='plotly_dark',
        title_font=dict(size=24, family='Arial, sans-serif', color='white'),
        showlegend=False,
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e'
    )

    return fig

# Data
months = ["September", "October", "November", "December"]
target_sales = [5000, 7000, 10000, 12000]  # Target sales
actual_sales = [4800, 7500, 9500, 13000]   # Actual sales

# Create the figure using the function
dashboard_figure = create_dashboard(months, target_sales, actual_sales)

# Define the layout of the Dash app
app.layout = html.Div(
    style={'backgroundColor': '#1e1e1e', 'padding': '20px'},
    children=[
        html.H1(
            children='Actual VS Target',
            style={'textAlign': 'center', 'color': 'white'}
        ),
        dcc.Graph(
            id='sales-dashboard',
            figure=dashboard_figure
        )
    ]
)

# Run the app
app = app.server
