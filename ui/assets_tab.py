from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ui.ui_utils import mouse_hover_annotation, plot_common_activities, graph_colors

class AssetsTab(QWidget):
    def __init__(self, business_logic):
        super().__init__()
        self.business_logic = business_logic
        self.annotations = {}   # Store annotations for each canvas
        self.canvases = {}      # Store canvases for each graph
        self.figures = {}       # Store figures for each graph
        self.assets_data_months, self.assets_data_values = self.business_logic.prepare_assets_data_for_plotting()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Investments Graph
        self.investments_figure = Figure()
        self.investments_figure.patch.set_facecolor('#202124')
        self.investments_canvas = FigureCanvas(self.investments_figure)
        layout.addWidget(self.investments_canvas)
        self.investments_canvas.mpl_connect('motion_notify_event', 
                                      lambda event: self.on_hover(event, 'investments'))
        self.canvases['investments'] = self.investments_canvas
        self.figures['investments'] = self.investments_figure
        self.plot_graph_by_type("investments")
        #self.plot_investments()

        # House Value Graph
        self.house_value_figure = Figure()
        self.house_value_figure.patch.set_facecolor('#202124')
        self.house_value_canvas = FigureCanvas(self.house_value_figure)
        layout.addWidget(self.house_value_canvas)
        self.house_value_canvas.mpl_connect('motion_notify_event',
                                               lambda event: self.on_hover(event, 'house'))
        self.canvases['house'] = self.house_value_canvas
        self.figures['house'] = self.house_value_figure
        self.plot_graph_by_type("house")
        #self.plot_house_value()

        # Bank Value Graph
        self.bank_value_figure = Figure()
        self.bank_value_figure.patch.set_facecolor('#202124')
        self.bank_value_canvas = FigureCanvas(self.bank_value_figure)
        layout.addWidget(self.bank_value_canvas)
        self.bank_value_canvas.mpl_connect('motion_notify_event',
                                             lambda event: self.on_hover(event, 'bank'))
        self.canvases['bank'] = self.bank_value_canvas
        self.figures['bank'] = self.bank_value_figure
        self.plot_graph_by_type("bank")
        #self.plot_bank_value()

        self.setLayout(layout)
    
    def refresh_assets(self):
        # Clear and redraw all canvases and graphs
        self.assets_data_months, self.assets_data_values = self.business_logic.prepare_assets_data_for_plotting()
        asset_graph_colors = {
            'investments': graph_colors['gold_1'],
            'house': graph_colors['green_1'],
            'bank': graph_colors['blue_1']
        }
        for graph_type in asset_graph_colors.keys():
            self.figures[graph_type].clear()
            self.plot_graph_by_type(graph_type, asset_graph_colors[graph_type])

    def plot_graph_by_type(self, graph_type, graph_color=graph_colors['rose_1']):
        # Draw the specified graph type (investments, house, or bank)
        if self.assets_data_months:
            avg_growth = (self.assets_data_values[graph_type][-1] - self.assets_data_values[graph_type][0]) / (len(self.assets_data_months) - 1) if len(self.assets_data_months) > 1 else 0
            title = f'{graph_type.capitalize()} || Avg growth: {avg_growth:.2f}/M'
            ax = self.figures[graph_type].add_subplot(111)
            ax.clear()
            ax.plot(self.assets_data_months, self.assets_data_values[graph_type], marker='.', label=graph_type.capitalize(), color=graph_color)
            ax = plot_common_activities(ax, title, 'Amount')
            self.canvases[graph_type].draw()

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
