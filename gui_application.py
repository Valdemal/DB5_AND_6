from datetime import datetime
from typing import List, Callable

from PyQt5.QtWidgets import (
    QWidget, QApplication, QTabWidget, QTableWidget,
    QVBoxLayout, QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton
)

from managers import HostelManager


class DBTableWidget(QTableWidget):
    def __init__(self, get_dataset_function: Callable[[], List[dict]]):
        super().__init__()

        # Делает ячейки неактивными
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Делает так, чтобы ячейки растягивались
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # функция получения данных
        self.__get_dataset = get_dataset_function

        self.fill_data()

    def fill_data(self):
        """Заполняет таблицу данными"""

        data = self.__get_dataset()

        if len(data):
            self.setRowCount(len(data))
            self.setColumnCount(len(data[0]))
            self.setHorizontalHeaderLabels(data[0].keys())
        else:
            self.setRowCount(0)
            self.setColumnCount(0)

        for i in range(len(data)):
            j = 0
            for item_value in data[i].values():
                item = QTableWidgetItem(str(item_value))
                self.setItem(i, j, item)
                j += 1


class HiledDiseasesForPeriodWidget(QWidget):
    def __init__(self, manager: HostelManager):
        super().__init__()

        self.__start_date = datetime.fromtimestamp(0)
        self.__end_date = datetime.now()

        self.__table = DBTableWidget(lambda: manager.get_hiled_diagnosis_for_period(
            self.__start_date, self.__end_date
        ))
        self.__input = self.Input(parent=self)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.__input)
        layout.addWidget(self.__table)

    def repaint(self) -> None:
        super().repaint()
        self.__table.repaint()

    def update_period(self, start: datetime, end: datetime):
        self.__start_date = start
        self.__end_date = end
        self.__table.fill_data()
        self.repaint()

    class Input(QWidget):
        DATE_FORMAT = '%d.%m.%Y'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.__start_label = QLabel(text='Начало периода')
            self.__start_input = QLineEdit()
            self.__end_label = QLabel(text='Конец периода')
            self.__end_input = QLineEdit()
            self.__submit_button = QPushButton(text='Получить данные')
            self.__submit_button.clicked.connect(self.on_submit)

            # Настройка компоновщика
            layout = QHBoxLayout()
            self.setLayout(layout)
            for widget in \
                    self.__start_label, self.__start_input, self.__end_label, self.__end_input, self.__submit_button:

                layout.addWidget(widget)

        def on_submit(self):
            start_time = datetime.strptime(
                self.__start_input.text(), self.DATE_FORMAT
            ) if self.__start_input.text() != '' else datetime.fromtimestamp(0)

            end_time = datetime.strptime(
                self.__end_input.text(), self.DATE_FORMAT
            ) if self.__end_input.text() != '' else datetime.now()

            self.parent().update_period(start_time, end_time)


class MainWidget(QWidget):
    MIN_WIDHT = 1000
    MIN_HEIGHT = 400

    def __init__(self):
        super().__init__()
        # Настройка окна
        self.setMinimumSize(self.MIN_WIDHT, self.MIN_HEIGHT)
        self.resize(self.MIN_WIDHT, self.MIN_HEIGHT)
        self.setWindowTitle('Лабораторная работа №6')

        # Настройка содержимого
        self.__content = QTabWidget()

        # Настройка компоновщика
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.__content)

        self.__init_tabs()

    def __init_tabs(self):
        manager = HostelManager()

        tabs = [
            (DBTableWidget(manager.get_service_report), 'Предоставленные услуги'),
            (DBTableWidget(manager.get_statistics_of_doctors_refferals), 'Количество направлений докторов'),
            (DBTableWidget(manager.get_count_all_cases_of_diagnosis), 'Статистика по заболеваниям'),
            (HiledDiseasesForPeriodWidget(manager), 'Вылеченные случаи')
        ]

        for widget, header in tabs:
            self.__content.addTab(widget, header)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWidget()

    window.show()
    app.exec_()
