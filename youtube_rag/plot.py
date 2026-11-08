import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


def plot_podcast_details_as_heat_map(cc_details: list[dict]) -> go.Figure:

    durations = np.array([c['duration'] for c in cc_details if c['view_count'] is not None])  # Minutes
    views = np.array([c['view_count'] / 1e3 for c in cc_details if c['view_count'] is not None])

    # Bin boundaries
    duration_bins = np.linspace(0, durations.max() + 1, 10)
    positive_views = np.maximum(views, 1)
    log_views = np.log10(positive_views)
    view_bins = np.linspace(log_views.min(), log_views.max(), 10)

    # 2D histogram: count videos in each bin
    counts, x_edges, y_edges = np.histogram2d(
        durations,
        log_views,
        bins=[duration_bins, view_bins],
    )

    # Heatmap: median original view count per bin
    median_views = np.full(counts.shape, np.nan)

    x_idx = np.digitize(durations, duration_bins) - 1
    y_idx = np.digitize(log_views, view_bins) - 1

    for i in range(len(durations)):
        xi = min(x_idx[i], len(duration_bins) - 2)
        yi = min(y_idx[i], len(view_bins) - 2)

        # Store observations in each bin
        if np.isnan(median_views[xi, yi]):
            median_views[xi, yi] = views[i]
        else:
            median_views[xi, yi] = np.median(
                [median_views[xi, yi], views[i]]
            )

    # Plot both side by side
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "2D Histogram: Number of Videos",
            "Heatmap: Median Views"
        ),
        horizontal_spacing=0.15,
    )

    # Histogram
    fig.add_trace(
        go.Heatmap(
            x=(x_edges[:-1] + x_edges[1:]) / 2,
            y=(y_edges[:-1] + y_edges[1:]) / 2,
            z=counts.T,
            colorscale="Viridis",
            colorbar=dict(title="Video count", x=0.44),
            hovertemplate=(
                "Duration: %{x:.1f} min<br>"
                "Log10(views): %{y:.2f}<br>"
                "Video count: %{z}<extra></extra>"
            ),
        ),
        row=1,
        col=1,
    )

    # Median-view heatmap
    fig.add_trace(
        go.Heatmap(
            x=(x_edges[:-1] + x_edges[1:]) / 2,
            y=(y_edges[:-1] + y_edges[1:]) / 2,
            z=median_views.T,
            colorscale="Plasma",
            colorbar=dict(title="Median views"),
            hovertemplate=(
                "Duration: %{x:.1f} min<br>"
                "Log10(views): %{y:.2f}<br>"
                "Median views: %{z:,.0f}<extra></extra>"
            ),
        ),
        row=1,
        col=2,
    )

    fig.update_layout(
        title="YouTube Video Duration and View Count Analysis",
        template="plotly_white",
        height=550,
    )

    fig.update_xaxes(title_text="Duration (minutes)", row=1, col=1)
    fig.update_xaxes(title_text="Duration (minutes)", row=1, col=2)

    # Display actual view counts on both vertical axes
    tick_vals = np.arange(
        np.floor(log_views.min()),
        np.ceil(log_views.max()) + 1
    )

    tick_text = [
        f"{10 ** v:,.0f}" for v in tick_vals
    ]

    fig.update_yaxes(
        title_text="View count",
        tickmode="array",
        tickvals=tick_vals,
        ticktext=tick_text,
        row=1,
        col=1,
    )

    fig.update_yaxes(
        title_text="View count",
        tickmode="array",
        tickvals=tick_vals,
        ticktext=tick_text,
        row=1,
        col=2,
    )

    return fig


def plot__podcast_details_as_scatter(cc_details: list[dict]) -> go.Figure:
    durations = np.array([c['duration']/60 for c in cc_details if c['view_count'] is not None])  # Minutes
    views = np.array([c['view_count'] / 1e3 for c in cc_details if c['view_count'] is not None])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=durations,
            y=views,
            mode='markers',
            marker=dict(size=5, color='blue', opacity=0.6),
            hovertemplate=(
                "Duration: %{x:.1f} min<br>"
                "Views (thousands): %{y:,.0f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title="YouTube Video Duration vs View Count",
        xaxis_title="Duration (minutes)",
        yaxis_title="View count (thousands)",
        template="plotly_white",
        height=550,
    )

    return fig

def plot_podcast_details_as_histogram(cc_details: list[dict]) -> go.Figure:
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Video Duration", "Views"),
        shared_yaxes=False,
    )

    fig = fig.add_trace(
        go.Histogram(
            y = [c['duration'] for c in cc_details if c['view_count'] is not None], name='duration'
        ), row=1, col=1
    )

    fig = fig.add_trace(
        go.Histogram(
            x = [c['view_count']/1e3 for c in cc_details if c['view_count'] is not None], name='view counts'
        ), row=1, col=2
    )
    # First subplot: horizontal histogram
    fig.update_xaxes(title_text="Number of videos", row=1, col=1)
    fig.update_yaxes(title_text="Duration (seconds)", row=1, col=1)

    # Second subplot: vertical histogram
    fig.update_xaxes(title_text="Views (thousands)", row=1, col=2)
    fig.update_yaxes(title_text="Number of videos", row=1, col=2)

    return fig

