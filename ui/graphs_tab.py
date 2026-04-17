from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.ui_utils import plot_common_activities, mouse_hover_annotation, graph_colors
from ui.setting import global_settings

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
            avg_growth = f'{(wealth_data[-1] - wealth_data[0]) / (len(months) - 1) if len(months) > 1 else 0:.2f}/M'
            if global_settings["private_mode"]["value"]:
                avg_growth = "Hidden"
            title = f'Total Wealth || Avg growth: {avg_growth}'
            ax = self.wealth_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, wealth_data, marker='.', label='Total Wealth', color=graph_colors['gold_1'])
            ax = plot_common_activities(ax, title, 'Wealth')
            self.wealth_canvas.draw()

    def plot_income_vs_expenses(self):
        months, _, income_data, expenses_data, _ = self.business_logic.prepare_data_for_plotting()
        if months:
            avg_income = f'{(sum(income_data)) / (len(months)):.2f}/M'
            if global_settings["private_mode"]["value"]:
                avg_income = "Hidden"
            title = f'Income & Expenses || Avg income: {avg_income}'
            ax = self.income_expenses_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, income_data, marker='.', label='Income', color=graph_colors['rose_1'])
            ax.plot(months, expenses_data, marker='.', label='Expenses', color=graph_colors['blue_1'])
            ax = plot_common_activities(ax, title, 'Amount')
            self.income_expenses_canvas.draw()

    def plot_expense_types(self):
        months, _, _, _, expense_types_data = self.business_logic.prepare_data_for_plotting()
        if months:
            avg_expenses = 0
            ax = self.expense_types_figure.add_subplot(111)
            ax.clear()
            colors = [val for val in graph_colors.values()]
            for idx, (expense_type, values) in enumerate(expense_types_data.items()):
                ax.plot(months, values, marker='.', label=expense_type.replace('_', ' ').title(), color=colors[idx])
                avg_expenses += sum(values)
            avg_expenses = f'{avg_expenses / (len(months)):.2f}/M'
            if global_settings["private_mode"]["value"]:
                avg_expenses = "Hidden"
            title = f'Expense Types || Avg expenses: {avg_expenses}'
            ax = plot_common_activities(ax, title, 'Amount')
            self.expense_types_canvas.draw()

    def on_hover(self, event, graph_type):
        # Handle mouse hover event on graphs
        new_annotation = mouse_hover_annotation(event)

        # Remove all previous annotations
        for g_type in list(self.annotations.keys()):
            if self.annotations[g_type] is not None:
                self.annotations[g_type].remove()
                del self.annotations[g_type]
                self.canvases[g_type].draw_idle()
            
        # Draw the new annotation if applicable
        if new_annotation is not None:
            self.annotations[graph_type] = new_annotation
            self.canvases[graph_type].draw_idle()
