import plotly.graph_objects as go

def create_range_chart(species, parameter, overlap):

    fig = go.Figure()

    for fish in species:
        minimum = getattr(fish, f"{parameter}_min")
        maximum = getattr(fish, f"{parameter}_max")

        fig.add_trace(go.Bar(
                      y=[fish.common_name],
                      x=[maximum - minimum],
                      base=minimum,
                      orientation='h',
                      name=fish.common_name))

    if overlap["compatible"]:
        fig.add_trace(go.Bar(
            y=["Community Range"],
            x=[overlap["max"] - overlap["min"]],
            base=overlap["min"],
            orientation='h',
            name="Community"
        ))

    fig.update_layout(height=500, showlegend=False)

    return fig.to_html(full_html=False)