# Since the mermaid service is having connectivity issues, let's create a Plotly-based deployment flow diagram
import plotly.graph_objects as go
import plotly.express as px

# Create a figure for the deployment flow
fig = go.Figure()

# Define the steps and their positions
steps = [
    {"name": "Start Setup", "x": 5, "y": 10, "color": "#B3E5EC"},
    {"name": "Check Prereq", "x": 5, "y": 9, "color": "#FFEB8A"},
    {"name": "Install Missing", "x": 2, "y": 8.5, "color": "#FFCDD2"},
    {"name": "Download Files", "x": 5, "y": 8, "color": "#B3E5EC"},
    {"name": "Create Venv", "x": 5, "y": 7, "color": "#B3E5EC"},
    {"name": "Activate Env", "x": 5, "y": 6, "color": "#B3E5EC"},
    {"name": "Install Deps", "x": 5, "y": 5, "color": "#B3E5EC"},
    {"name": "Check Install", "x": 5, "y": 4, "color": "#FFEB8A"},
    {"name": "Resolve Issues", "x": 8, "y": 4.5, "color": "#FFCDD2"},
    {"name": "Generate Data", "x": 5, "y": 3, "color": "#B3E5EC"},
    {"name": "Train Models", "x": 5, "y": 2, "color": "#B3E5EC"},
    {"name": "Launch Server", "x": 5, "y": 1, "color": "#B3E5EC"},
    {"name": "System Ready", "x": 5, "y": 0, "color": "#A5D6A7"}
]

# Add rectangles for each step
for step in steps:
    fig.add_shape(
        type="rect",
        x0=step["x"]-0.8, y0=step["y"]-0.3,
        x1=step["x"]+0.8, y1=step["y"]+0.3,
        fillcolor=step["color"],
        line=dict(color="black", width=1)
    )
    
    # Add text labels
    fig.add_annotation(
        x=step["x"], y=step["y"],
        text=step["name"],
        showarrow=False,
        font=dict(size=10, color="black"),
        xanchor="center", yanchor="middle"
    )

# Add time estimates as annotations
time_estimates = [
    {"x": 6.5, "y": 10, "text": "0 min"},
    {"x": 6.5, "y": 9, "text": "2-5 min"},
    {"x": 6.5, "y": 8, "text": "1-3 min"},
    {"x": 6.5, "y": 7, "text": "30 sec"},
    {"x": 6.5, "y": 6, "text": "5 sec"},
    {"x": 6.5, "y": 5, "text": "3-8 min"},
    {"x": 6.5, "y": 3, "text": "2-5 min"},
    {"x": 6.5, "y": 2, "text": "5-15 min"},
    {"x": 6.5, "y": 1, "text": "10 sec"},
    {"x": 6.5, "y": 0, "text": "Ready!"}
]

for est in time_estimates:
    fig.add_annotation(
        x=est["x"], y=est["y"],
        text=est["text"],
        showarrow=False,
        font=dict(size=8, color="gray"),
        xanchor="left"
    )

# Add arrows for main flow
arrows = [
    {"x0": 5, "y0": 9.7, "x1": 5, "y1": 9.3},  # Start to Check
    {"x0": 5, "y0": 8.7, "x1": 5, "y1": 8.3},  # Check to Download
    {"x0": 5, "y0": 7.7, "x1": 5, "y1": 7.3},  # Download to Create
    {"x0": 5, "y0": 6.7, "x1": 5, "y1": 6.3},  # Create to Activate
    {"x0": 5, "y0": 5.7, "x1": 5, "y1": 5.3},  # Activate to Install
    {"x0": 5, "y0": 4.7, "x1": 5, "y1": 4.3},  # Install to Check
    {"x0": 5, "y0": 3.7, "x1": 5, "y1": 3.3},  # Check to Generate
    {"x0": 5, "y0": 2.7, "x1": 5, "y1": 2.3},  # Generate to Train
    {"x0": 5, "y0": 1.7, "x1": 5, "y1": 1.3},  # Train to Launch
    {"x0": 5, "y0": 0.7, "x1": 5, "y1": 0.3},  # Launch to Ready
]

# Add decision branches
decision_arrows = [
    {"x0": 4.2, "y0": 9, "x1": 2.8, "y1": 8.5},  # Check to Install Missing
    {"x0": 2, "y0": 8.2, "x1": 4.2, "y1": 8},     # Install Missing to Download
    {"x0": 5.8, "y0": 4, "x1": 7.2, "y1": 4.5},   # Check Install to Resolve
    {"x0": 8, "y0": 4.2, "x1": 5.8, "y1": 5},     # Resolve back to Install
]

# Add all arrows
for arrow in arrows + decision_arrows:
    fig.add_annotation(
        x=arrow["x1"], y=arrow["y1"],
        ax=arrow["x0"], ay=arrow["y0"],
        xref="x", yref="y",
        axref="x", ayref="y",
        arrowhead=2, arrowsize=1,
        arrowcolor="black",
        arrowwidth=1.5
    )

# Update layout
fig.update_layout(
    title="MineGuard 3D Setup Flow",
    xaxis=dict(range=[0, 10], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[-0.5, 10.5], showgrid=False, showticklabels=False, zeroline=False),
    showlegend=False,
    plot_bgcolor="white"
)

# Save the chart
fig.write_image("deployment_flow.png")
fig.write_image("deployment_flow.svg", format="svg")
print("Deployment flow chart created successfully!")