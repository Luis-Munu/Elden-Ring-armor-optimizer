from typing import List, Tuple, Dict, Set
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QSpinBox,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
import itertools
from .armor_optimizer import ArmorOptimizer
from .utils import load_armor_data, get_armor_attributes


class ResultsWindow(QWidget):
    """
    A class to represent the results window of the application.

    Attributes
    ----------
    optimal_configuration : List[Tuple[str, str]]
        The optimal configuration of the armor.
    total_stats : Dict[str, float]
        The total stats of the armor.
    style_sheet : str
        The style sheet for the window.
    """

    def __init__(
        self,
        optimal_configuration: Set[Tuple[str, str]],
        total_stats: Dict[str, float],
        style_sheet: str,
    ):
        """
        Constructs all the necessary attributes for the ResultsWindow object.

        Parameters
        ----------
            optimal_configuration : Set[Tuple[str, str]]
                The optimal configuration of the armor.
            total_stats : Dict[str, float]
                The total stats of the armor.
            style_sheet : str
                The style sheet for the window.
        """
        super().__init__()

        self.setWindowTitle("Optimization Results")
        self.setWindowIcon(QIcon("data/img.ico"))
        self.layout = QVBoxLayout()
        self.create_armor_layout(optimal_configuration)
        self.layout.addItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        self.create_stats_layout(total_stats)
        self.create_exit_button()
        self.setLayout(self.layout)
        self.setStyleSheet(style_sheet)

    def create_armor_layout(self, optimal_configuration: Set[Tuple[str, str]]):
        """
        Creates the armor layout for the results window.

        Parameters
        ----------
            optimal_configuration : Set[Tuple[str, str]]
                The optimal configuration of the armor.
        """
        armor_layout = QGridLayout()
        order = {"Helmet": 0, "Chest": 1, "Gauntlet": 2, "Pant": 3}
        optimal_configuration = sorted(
            optimal_configuration, key=lambda armor: order.get(armor[0], 999)
        )

        for i, armor in enumerate(optimal_configuration):
            slot, name = armor
            label = QLabel(f"{slot}: {name.title()}")
            label.setStyleSheet("color: orange;")
            armor_layout.addWidget(label, i // 2, i % 2)
        self.layout.addLayout(armor_layout)

    def create_stats_layout(self, total_stats: Dict[str, float]):
        """
        Creates the stats layout for the results window.

        Parameters
        ----------
            total_stats : Dict[str, float]
                The total stats of the armor.
        """
        colors = itertools.cycle(
            [
                "#888",
                "#f00",
                "#0f0",
                "#00f",
                "#ff0",
                "#f0f",
                "#0ff",
                "#888",
                "#f88",
                "#8f8",
                "#88f",
                "#ff8",
                "#f8f",
                "#8ff",
            ]
        )

        stats_layout = QGridLayout()
        for i, (stat, value) in enumerate(total_stats.items()):
            color = next(colors)
            label = QLabel(f"{stat}: {round(value, 1)}")
            label.setStyleSheet(f"color: {color};")
            stats_layout.addWidget(label, i // 3, i % 3)
        self.layout.addLayout(stats_layout)

    def create_exit_button(self):
        """
        Creates the exit button for the results window.
        """
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)


class ArmorOptimizerGUI(QWidget):
    """
    A class to represent the main window of the application.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the ArmorOptimizerGUI object.
        """
        super().__init__()
        self.setWindowTitle("Armor Optimizer")
        self.setWindowIcon(QIcon("data/img.ico"))
        self.layout = QVBoxLayout()
        self.create_weight_cap_input()
        self.create_attribute_selection()
        self.create_run_button()
        self.setLayout(self.layout)
        self.setStyleSheet(self.get_style_sheet())
        self.setFixedWidth(900)

    def create_weight_cap_input(self):
        """
        Creates the weight cap input field for the main window.
        """
        self.weight_cap_label = QLabel("Enter the weight cap: ")
        self.layout.addWidget(self.weight_cap_label)

        self.weight_cap_entry = QSpinBox()
        self.weight_cap_entry.setRange(0, 1000)
        self.layout.addWidget(self.weight_cap_entry)

    def create_attribute_selection(self):
        """
        Creates the attribute selection field for the main window.
        """
        self.attribute_label = QLabel("Select attribute to optimize: ")
        self.layout.addWidget(self.attribute_label)

        self.attribute_combo = QComboBox()
        self.attribute_combo.addItems(get_armor_attributes(load_armor_data()))
        self.layout.addWidget(self.attribute_combo)

    def create_run_button(self):
        """
        Creates the run button for the main window.
        """
        self.run_button = QPushButton("Run Optimizer")
        self.run_button.clicked.connect(self.run_optimizer)
        self.layout.addWidget(self.run_button)

    def get_style_sheet(self) -> str:
        """
        Returns the style sheet for the main window.

        Returns
        -------
        str
            The style sheet for the main window.
        """
        return """
            QWidget {
                background-color: #333;
                color: #fff;
                font-size: 16px;
            }
            QPushButton {
                background-color: #555;
                border: 2px solid #888;
                border-radius: 6px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #888;
            }
            QComboBox, QDoubleSpinBox {
                background-color: #555;
                border: 2px solid #888;
                border-radius: 6px;
                padding: 5px;
            }
        """

    def run_optimizer(self):
        """
        Runs the armor optimizer and displays the results in a new window.
        """
        weight_cap = self.weight_cap_entry.value()
        selected_attribute = self.attribute_combo.currentText()
        armor_data = load_armor_data()
        optimizer = ArmorOptimizer(armor_data, weight_cap)
        optimal_configuration = optimizer.optimize_armor_configuration(
            selected_attribute
        )
        total_stats = optimizer.calculate_total_stats(optimal_configuration)
        self.results_window = ResultsWindow(
            optimal_configuration, total_stats, self.styleSheet()
        )
        self.results_window.show()


def run_gui():
    """
    Runs the GUI for the application.
    """
    app = QApplication([])
    gui = ArmorOptimizerGUI()
    gui.show()
    app.exec_()
