from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class GraphsTab(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.annotations = {}   # Store annotations for each canvas
        self.canvases = {}      # Store canvases for each graph
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Total Wealth Graph
        self.wealth_figure = Figure()
        self.wealth_figure.patch.set_facecolor('#202124')
        self.wealth_canvas = FigureCanvas(self.wealth_figure)
        layout.addWidget(self.wealth_canvas)
        self.wealth_canvas.mpl_connect('motion_notify_event', 
                                      lambda event: self.on_hover(event, 'wealth'))
        self.canvases['wealth'] = self.wealth_canvas
        self.plot_total_wealth()

        # Income vs Expenses Graph
        self.income_expenses_figure = Figure()
        self.income_expenses_figure.patch.set_facecolor('#202124')
        self.income_expenses_canvas = FigureCanvas(self.income_expenses_figure)
        layout.addWidget(self.income_expenses_canvas)
        self.income_expenses_canvas.mpl_connect('motion_notify_event',
                                               lambda event: self.on_hover(event, 'income_expenses'))
        self.canvases['income_expenses'] = self.income_expenses_canvas
        self.plot_income_vs_expenses()

        # Expense Types Graph
        self.expense_types_figure = Figure()
        self.expense_types_figure.patch.set_facecolor('#202124')
        self.expense_types_canvas = FigureCanvas(self.expense_types_figure)
        layout.addWidget(self.expense_types_canvas)
        self.expense_types_canvas.mpl_connect('motion_notify_event',
                                             lambda event: self.on_hover(event, 'expense_types'))
        self.canvases['expense_types'] = self.expense_types_canvas
        self.plot_expense_types()

        self.setLayout(layout)
    
    def refresh_graphs(self):
        # Clear and redraw all canvases and graphs
        self.wealth_figure.clear()
        self.income_expenses_figure.clear()
        self.expense_types_figure.clear()
        self.plot_total_wealth()
        self.plot_income_vs_expenses()
        self.plot_expense_types()

    def plot_total_wealth(self):
        months, wealth_data, _, _, _ = self.business_logic.prepare_data_for_plotting()
        if months:
            avg_growth = (wealth_data[-1] - wealth_data[0]) / (len(months) - 1) if len(months) > 1 else 0
            title = f'Total Wealth || Avg growth: {avg_growth:.2f}/M'
            ax = self.wealth_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, wealth_data, marker='o', label='Total Wealth')
            ax = self.plot_common_activities(ax, title, 'Wealth')
            self.wealth_canvas.draw()

    def plot_income_vs_expenses(self):
        months, _, income_data, expenses_data, _ = self.business_logic.prepare_data_for_plotting()
        if months:
            avg_income = (sum(income_data)) / (len(months))
            title = f'Income & Expenses || Avg income: {avg_income:.2f}/M'
            ax = self.income_expenses_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, income_data, marker='o', label='Income', color='blue')
            ax.plot(months, expenses_data, marker='o', label='Expenses', color='red')
            ax = self.plot_common_activities(ax, title, 'Amount')
            self.income_expenses_canvas.draw()

    def plot_expense_types(self):
        months, _, _, _, expense_types_data = self.business_logic.prepare_data_for_plotting()
        if months:
            avg_expenses = 0
            ax = self.expense_types_figure.add_subplot(111)
            ax.clear()
            colors = ['blue', 'green', 'orange', 'purple', 'brown', 'yellow']
            for idx, (expense_type, values) in enumerate(expense_types_data.items()):
                ax.plot(months, values, marker='o', label=expense_type.replace('_', ' ').title(), color=colors[idx])
                avg_expenses += sum(values)
            avg_expenses = avg_expenses / (len(months))
            title = f'Expense Types || Avg expenses: {avg_expenses:.2f}/M'
            ax = self.plot_common_activities(ax, title, 'Amount')
            self.expense_types_canvas.draw()

    def plot_common_activities(self, ax, title, y_label):
        # Function for doing common plotting tasks
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
        ax.set_facecolor('#353535')
        return ax

    def on_hover(self, event, graph_type):
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

        # Remove all previous annotations
        for g_type in list(self.annotations.keys()):
            if self.annotations[g_type] is not None:
                self.annotations[g_type].remove()
                del self.annotations[g_type]
                self.canvases[g_type].draw_idle()
            
        # Draw the new annotation if applicable
        if draw_new:
            self.annotations[graph_type] = annotation
            self.canvases[graph_type].draw_idle()
