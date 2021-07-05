from datetime import datetime
from datetime import timedelta
from typing import Optional


class Record:
    def __init__(self, amount: int, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = datetime.now().date()
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
        current_day = datetime.now().date()
        today_stats = 0
        for record in self.records:
            if record.date == current_day:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self) -> int:
        """Метод считает за последние 7 дней,
        сколько денег потрачено/сколько калорий получено"""
        last_week = datetime.now().date() - timedelta(weeks=1)
        today = datetime.now().date()
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

    def get_today_cash_remained(self, currency: str) -> str:
        """Метод определяет, сколько ещё денег можно
        потратить сегодня в рублях, долларах или евро"""
        cur = {'rub': ('руб', 1),
               'usd': ('USD', CashCalculator.USD_RATE),
               'eur': ('Euro', CashCalculator.EURO_RATE)}
        cash_remained = self.get_remained_amount()

        if currency in cur.keys():
            cash_remained_cur = \
                abs(round((cash_remained / cur[currency][1]), 2))
            if cash_remained > 0:
                return (f'На сегодня осталось {cash_remained_cur} '
                        f'{cur[currency][0]}')
            elif cash_remained == 0:
                return 'Денег нет, держись'
            else:
                return('Денег нет, держись: твой долг -'
                       f' {cash_remained_cur} {cur[currency][0]}')
        else:
            return 'Невалидная валюта. Валидная валюта - "rub", "usd", "eur"'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        """Метод определяет, сколько ещё
        калорий можно/нужно получить сегодня"""
        calories_remained = self.get_remained_amount()
        if self.get_remained_amount() > 0:
            return('Сегодня можно съесть что-нибудь ещё, но с '
                   f'общей калорийностью не более {calories_remained} кКал')
        else:
            return 'Хватит есть!'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др', date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('eur'))
# должно напечататься
# На сегодня осталось 555 руб
