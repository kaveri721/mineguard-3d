import plotly.graph_objects as go
import plotly.express as px

# Create MineGuard 3D System Architecture using Plotly
fig = go.Figure()

# Define layer colors from the brand palette
colors = {
    'data': '#B3E5EC',      # Light cyan for Data Layer
    'process': '#A5D6A7',   # Light green for Processing Layer
    'app': '#FFEB8A',       # Light yellow for Application Layer
    'external': '#FFCDD2'   # Light red for External Interfaces
}

# Define positions for each layer and component
layers = {
    'External Interfaces': {'y': 4, 'components': [
        {'name': 'Real-time\nMonitoring', 'x': 1, 'icon': '📊'},
        {'name': 'Safety\nRecommendations', 'x': 2, 'icon': '⚠️'},
        {'name': 'Alert\nNotifications', 'x': 3, 'icon': '🔔'}
    ]},
    'Application Layer': {'y': 3, 'components': [
        {'name': 'Streamlit Web\nInterface', 'x': 0.5, 'icon': '🌐'},
        {'name': '3D Digital Twin\nVisualization', 'x': 1.5, 'icon': '🎮'},
        {'name': 'Interactive\nDashboard', 'x': 2.5, 'icon': '📈'},
        {'name': 'What-if Scenario\nSimulation', 'x': 3.5, 'icon': '🔮'}
    ]},
    'Processing Layer': {'y': 2, 'components': [
        {'name': 'Data Processing\nModule', 'x': 0.5, 'icon': '🔄'},
        {'name': 'AI/ML Prediction\nEngine', 'x': 1.5, 'icon': '🧠'},
        {'name': 'Real-time\nInference', 'x': 2.5, 'icon': '⚡'},
        {'name': 'Alert Generation\nSystem', 'x': 3.5, 'icon': '🚨'}
    ]},
    'Data Layer': {'y': 1, 'components': [
        {'name': 'Sensor Data\n(Displacement,\nStrain, Vibration,\nGas, Seismic)', 'x': 1, 'icon': '📡'},
        {'name': 'CSV Data\nFiles', 'x': 2, 'icon': '📊'},
        {'name': 'Trained ML\nModels\n(.pkl files)', 'x': 3, 'icon': '🤖'}
    ]}
}

# Color mapping for layers
layer_colors = {
    'Data Layer': colors['data'],
    'Processing Layer': colors['process'],
    'Application Layer': colors['app'],
    'External Interfaces': colors['external']
}

# Add rectangles for each component
for layer_name, layer_data in layers.items():
    for comp in layer_data['components']:
        # Add component box
        fig.add_shape(
            type="rect",
            x0=comp['x']-0.3, y0=layer_data['y']-0.3,
            x1=comp['x']+0.3, y1=layer_data['y']+0.3,
            line=dict(color="black", width=1),
            fillcolor=layer_colors[layer_name],
            opacity=0.8
        )
        
        # Add component text with icon
        fig.add_annotation(
            x=comp['x'], y=layer_data['y'],
            text=f"{comp['icon']}<br>{comp['name']}",
            showarrow=False,
            font=dict(size=10, color="black"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        )

# Define data flow connections
connections = [
    # Data to Processing
    (1, 1, 0.5, 2),  # Sensor Data to Data Processing
    (2, 1, 0.5, 2),  # CSV to Data Processing
    (3, 1, 1.5, 2),  # ML Models to AI/ML Engine
    
    # Within Processing Layer
    (0.5, 2, 1.5, 2),  # Data Processing to AI/ML
    (0.5, 2, 2.5, 2),  # Data Processing to Real-time Inference
    (1.5, 2, 2.5, 2),  # AI/ML to Real-time Inference
    (2.5, 2, 3.5, 2),  # Real-time Inference to Alert Generation
    
    # Processing to Application
    (0.5, 2, 0.5, 3),  # Data Processing to Streamlit
    (2.5, 2, 0.5, 3),  # Real-time Inference to Streamlit
    (3.5, 2, 0.5, 3),  # Alert Generation to Streamlit
    
    # Within Application Layer
    (0.5, 3, 1.5, 3),  # Streamlit to 3D Twin
    (0.5, 3, 2.5, 3),  # Streamlit to Dashboard
    (0.5, 3, 3.5, 3),  # Streamlit to What-if
    
    # Application to External
    (3.5, 2, 1, 4),    # Alert Generation to Real-time Monitoring
    (2.5, 2, 2, 4),    # Real-time Inference to Safety Recommendations
    (3.5, 2, 3, 4),    # Alert Generation to Alert Notifications
    (1.5, 3, 1, 4),    # 3D Twin to Real-time Monitoring
    (2.5, 3, 1, 4),    # Dashboard to Real-time Monitoring
    (3.5, 3, 2, 4),    # What-if to Safety Recommendations
]

# Add arrows for connections
for x1, y1, x2, y2 in connections:
    fig.add_annotation(
        x=x2, y=y2,
        ax=x1, ay=y1,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="#333333",
        opacity=0.7
    )

# Add layer labels
layer_positions = [
    ('🗄️ Data Layer', 0, 1),
    ('⚙️ Processing Layer', 0, 2),
    ('💻 Application Layer', 0, 3),
    ('📤 External Interfaces', 0, 4)
]

for label, x, y in layer_positions:
    fig.add_annotation(
        x=x, y=y,
        text=f"<b>{label}</b>",
        showarrow=False,
        font=dict(size=12, color="black"),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="black",
        borderwidth=1
    )

# Update layout
fig.update_layout(
    title="MineGuard 3D System Architecture",
    xaxis=dict(
        range=[-0.5, 4],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0.5, 4.5],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save the chart
fig.write_image("mineguard_architecture.png")
fig.write_image("mineguard_architecture.svg", format="svg")

print("MineGuard 3D System Architecture diagram created successfully!")
print("Files saved: mineguard_architecture.png and mineguard_architecture.svg")