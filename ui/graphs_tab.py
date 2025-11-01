from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphsTab(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Total Wealth Graph
        self.wealth_figure = Figure()
        self.wealth_figure.patch.set_facecolor('#202124')
        self.wealth_canvas = FigureCanvas(self.wealth_figure)
        layout.addWidget(self.wealth_canvas)
        self.plot_total_wealth()

        # Income vs Expenses Graph
        self.income_expenses_figure = Figure()
        self.income_expenses_figure.patch.set_facecolor('#202124')
        self.income_expenses_canvas = FigureCanvas(self.income_expenses_figure)
        layout.addWidget(self.income_expenses_canvas)
        self.plot_income_vs_expenses()

        # Expense Types Graph
        self.expense_types_figure = Figure()
        self.expense_types_figure.patch.set_facecolor('#202124')
        self.expense_types_canvas = FigureCanvas(self.expense_types_figure)
        layout.addWidget(self.expense_types_canvas)
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
            ax = self.wealth_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, wealth_data, marker='o', label='Total Wealth')
            ax = self.plot_common_activities(ax, 'Total Wealth Over Time', 'Wealth')
            self.wealth_canvas.draw()

    def plot_income_vs_expenses(self):
        months, _, income_data, expenses_data, _ = self.business_logic.prepare_data_for_plotting()
        if months:
            ax = self.income_expenses_figure.add_subplot(111)
            ax.clear()
            ax.plot(months, income_data, marker='o', label='Income', color='blue')
            ax.plot(months, expenses_data, marker='o', label='Expenses', color='red')
            ax = self.plot_common_activities(ax, 'Income vs Expenses', 'Amount')
            self.income_expenses_canvas.draw()

    def plot_expense_types(self):
        months, _, _, _, expense_types_data = self.business_logic.prepare_data_for_plotting()
        if months:
            ax = self.expense_types_figure.add_subplot(111)
            ax.clear()
            colors = ['blue', 'green', 'orange', 'purple', 'brown', 'yellow']
            for idx, (expense_type, values) in enumerate(expense_types_data.items()):
                ax.plot(months, values, marker='o', label=expense_type.replace('_', ' ').title(), color=colors[idx])
            ax = self.plot_common_activities(ax, 'Expense Types Over Time', 'Amount')
            self.expense_types_canvas.draw()

    def plot_common_activities(self, ax, title, y_label):
        # Function for doing common plotting tasks
        ax.set_title(title, color='white')
        ax.set_ylabel(y_label, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True)
        ax.set_facecolor('#353535')
        return ax