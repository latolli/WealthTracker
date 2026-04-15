import numpy as np

graph_colors = {
    'rose_1': "#cf7680",   # gentle rose pink
    'blue_1': "#5497c4",   # muted cool blue
    'gold_1': "#ccba78",   # soft gold
    'purple_1': "#866cb6", # muted lavender
    'green_1': "#6ca06b",  # sage green
    'slate_1': "#4f6e86",  # soft slate
}

def plot_common_activities(ax, title, y_label):
    """ Function for doing common plotting tasks """
    ax.set_title(title, color='white', 
        fontdict={
            "family": "Arial",
            "size": 12,
            "weight": "bold"})
    ax.set_ylabel(y_label, color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True)
    ax.set_facecolor("#222222")
    return ax

def mouse_hover_annotation(event):
    """Handle mouse hover events to show data values."""
    if event.inaxes is None or event.xdata is None or event.ydata is None:
        return
    
    ax = event.inaxes
    
    # Find the closest data point to the mouse cursor
    closest_dist = float('inf')
    closest_point = None
    closest_label = None
    
    for line in ax.get_lines():
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        
        if len(xdata) == 0:
            continue
        
        # Calculate distances from cursor to all points on this line
        for i, (x, y) in enumerate(zip(xdata, ydata)):
            # Calculate Euclidean distance in axes coordinate space
            x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
            y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
            
            # Normalize distances
            try:
                x_dist = abs(float(x) - event.xdata) / x_range if x_range != 0 else 0
            except (ValueError, TypeError):
                # If x is not numeric (e.g., string), use index position
                x_dist = abs(i - event.xdata) / x_range if x_range != 0 else 0
            
            y_dist = abs(y - event.ydata) / y_range if y_range != 0 else 0
            distance = np.sqrt(x_dist**2 + y_dist**2)
            
            if distance < closest_dist:
                closest_dist = distance
                closest_point = (x, y, i)
                closest_label = line.get_label()

    # Only show annotation if cursor is close enough
    draw_new = closest_dist < 0.1 and closest_point is not None
    if draw_new:
        x, y, idx = closest_point
        
        # Create new annotation
        label_text = f'{closest_label}\nX: {x}\nY: {y:.2f}'
        annotation = ax.annotate(label_text,
                                xy=(idx, y),
                                xytext=(10, 10),
                                textcoords='offset points',
                                bbox=dict(boxstyle='round,pad=0.7', 
                                            fc='#1a1d21', 
                                            ec='#4a90e2',
                                            alpha=0.95,
                                            linewidth=2),
                                arrowprops=dict(arrowstyle='->', 
                                                connectionstyle='arc3,rad=0',
                                                color='#4a90e2',
                                                lw=1.5),
                                fontsize=9,
                                color='white',
                                zorder=10)
        return annotation
    # Return None if no annotation was drawn
    return None
