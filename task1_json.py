import json
from datetime import datetime

class Car:
    def __init__(self, brand, model, year, color, mileage=0):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.engine_on = False
        self.service_history = []
    
    def start_engine(self):
        if not self.engine_on:
            self.engine_on = True
            return f"Двигатель {self.brand} {self.model} запущен"
        return "Двигатель уже работает"
    
    def stop_engine(self):
        if self.engine_on:
            self.engine_on = False
            return f"Двигатель {self.brand} {self.model} остановлен"
        return "Двигатель уже выключен"
    
    def drive(self, distance):
        if self.engine_on:
            self.mileage += distance
            return f"Проехали {distance} км. Общий пробег: {self.mileage} км"
        return "Сначала запустите двигатель"
    
    def add_service_record(self, service_type, date=None, cost=0):
        record = {
            'type': service_type,
            'date': date or datetime.now().strftime("%Y-%m-%d"),
            'cost': cost
        }
        self.service_history.append(record)
        return f"Добавлена запись о ТО: {service_type}"
    
    # Метод для преобразования объекта в словарь
    def to_dict(self):
        return {
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'mileage': self.mileage,
            'engine_on': self.engine_on,
            'service_history': self.service_history
        }
    
    # Сериализация в JSON
    def to_json(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
            return f"Данные сохранены в {filename}"
        except Exception as e:
            return f"Ошибка при сохранении: {str(e)}"
    
    # Десериализация из JSON
    @classmethod
    def from_json(cls, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            car = cls(
                data['brand'],
                data['model'],
                data['year'],
                data['color'],
                data['mileage']
            )
            car.engine_on = data['engine_on']
            car.service_history = data['service_history']
            return car
        except Exception as e:
            print(f"Ошибка при загрузке: {str(e)}")
            return None
    
    def __str__(self):
        status = "заведен" if self.engine_on else "заглушен"
        return (f"{self.brand} {self.model} {self.year} ({self.color}), "
                f"пробег: {self.mileage} км, двигатель: {status}, "
                f"записей ТО: {len(self.service_history)}")


# Пример использования
if __name__ == "__main__":
    # Создаем автомобиль
    car = Car("Toyota", "Camry", 2022, "синий", 15000)
    car.start_engine()
    car.drive(250)
    car.add_service_record("Замена масла", cost=3500)
    car.add_service_record("Ротация шин")
    
    print("Создан автомобиль:")
    print(car)
    
    # Сохраняем в JSON
    json_file = "car_data.json"
    print("\n" + car.to_json(json_file))
    
    # Загружаем из JSON
    loaded_car = Car.from_json(json_file)
    if loaded_car:
        print("\nЗагруженный автомобиль:")
        print(loaded_car)
        
        # Проверка истории обслуживания
        print("\nИстория обслуживания:")
        for record in loaded_car.service_history:
            print(f"- {record['type']}, дата: {record['date']}, стоимость: {record.get('cost', 0)} руб.")