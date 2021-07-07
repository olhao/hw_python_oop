import datetime as dt
from datetime import datetime
from datetime import timedelta
from typing import Optional


class Record:
    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = datetime.strptime(str(date), '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, record: object) -> None:
        """Метод сохраняет новую запись о расходах/приёме пищи"""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Метод считает на сегодня,
        сколько денег потрачено/калорий уже съедено"""
        current_day = dt.date.today()
        today_stats = sum([record.amount for record in self.records
                           if record.date == current_day])
        return today_stats

    def get_week_stats(self) -> int:
        """Метод считает за последние 7 дней,
        сколько денег потрачено/сколько калорий получено"""
        last_week = dt.date.today() - timedelta(weeks=1)
        today = dt.date.today()
        week_stats = 0
        for record in self.records:
            if last_week < record.date <= today:
                week_stats += record.amount
        return week_stats

    def get_remained_amount(self) -> int:
        remained_amount = self.limit - self.get_today_stats()
        return remained_amount


class CashCalculator(Calculator):
    USD_RATE = 70.0
    EURO_RATE = 85.0

    @property
    def settings(self):
        """Метод для инициализации данных о валютах"""
        return {'rub': ('руб', 1),
                'usd': ('USD', CashCalculator.USD_RATE),
                'eur': ('Euro', CashCalculator.EURO_RATE)}

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод определяет, сколько ещё денег можно
        потратить сегодня в рублях, долларах или евро"""
        if currency in self.settings.keys():
            cash_remained = self.get_remained_amount()
            if cash_remained == 0:
                return 'Денег нет, держись'
            currency_name, currency_rate = (
                self.settings[currency][0], self.settings[currency][1])
            cash_remained_cur = (
                abs(round((cash_remained / currency_rate), 2)))
            if cash_remained > 0:
                return (f'На сегодня осталось {cash_remained_cur} '
                        f'{currency_name}')
            return('Денег нет, держись: твой долг -'
                   f' {cash_remained_cur} {currency_name}')
        return 'Невалидная валюта. Валидная валюта - "rub", "usd", "eur"'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """Метод определяет, сколько ещё
        калорий можно/нужно получить сегодня"""
        calories_remained = self.get_remained_amount()
        if calories_remained > 0:
            return('Сегодня можно съесть что-нибудь ещё, но с '
                   f'общей калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


if __name__ == "__main__":
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)

    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=150, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=30, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=300,
                                      comment='бар в Танин др',
                                      date='08.11.2019'))

    print(cash_calculator.get_today_cash_remained('usd'))
    # должно напечататься
    # На сегодня осталось 11.71 USD
