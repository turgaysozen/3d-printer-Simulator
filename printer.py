from random import randint, uniform


class Printer:
    """ This is mock 3d printer class which simulates physical 3d printer realtime data """

    def __init__(self):
        self.printer_name = f'Printer_{randint(1, 10)}'
        self.temperature = randint(20, 80)  # °C
        self.status = 'Idle'
        self.fan_speed = randint(20, 70)  # percent
        self.print_progress = 0
        self.filament_usage = 0  # gram
        self.initial_filament = 1000  # gram
        self.is_paused = False
        self.is_stopped = False
        self.left_filament = self.initial_filament - self.filament_usage
        self.print_time = 0

    def simulate_changes(self):
        if self.is_stopped or self.is_paused:
            return

        if not self.is_paused:
            temperature_change = uniform(-5, 5)
            fan_speed_change = uniform(-10, 10)
            self.temperature = max(20, min(80, self.temperature + temperature_change))
            self.fan_speed = max(20, min(100, self.fan_speed + fan_speed_change))
            self.print_progress = min(100, self.print_progress + uniform(0.1, 0.5))
            self.filament_usage += uniform(0.3, 0.8)
            self.left_filament = max(0, self.initial_filament - self.filament_usage)
            self.print_time += 1 
            self.status = 'Printing'

    def pause_printer(self):
        if not self.is_paused and not self.is_stopped:
            self.is_paused = True
            self.status = 'Paused'
            print("Printer paused")

    def continue_printer(self):
        if self.is_paused and not self.is_stopped:
            self.is_paused = False
            self.status = 'Printing'
            print("Printer continued")

    def stop_printer(self):
        if not self.is_stopped:
            self.is_paused = False
            self.is_stopped = True
            self.status = 'Stopped'
            print("Printer stopped")

    def start_printer(self):
        if self.is_stopped:
            self.reset_printer() # self.__init__()
            self.is_stopped = False
            self.status = 'Printing'
            print("Printer restarted and reset")
            
    def is_printing_complete(self):
        return self.print_progress >= 100

    def mark_completed(self):
        self.status = 'Completed'
        self.is_stopped = True
            
    def reset_printer(self):
        self.temperature = randint(20, 80)
        self.status = 'Idle'
        self.fan_speed = randint(20, 70)
        self.print_progress = 0
        self.filament_usage = 0
        self.is_paused = False
        self.is_stopped = False
        self.left_filament = self.initial_filament - self.filament_usage
        self.print_time = 0

    def get_printer_data(self):
        left_filament_percentage = (self.left_filament / self.initial_filament) * 100

        print_time_seconds = self.print_time
        print_time_minutes = print_time_seconds // 60
        print_time_seconds %= 60
        print_time_hours = print_time_minutes // 60
        print_time_minutes %= 60

        if print_time_hours > 0:
            formatted_time = f'{print_time_hours}h {print_time_minutes}m {print_time_seconds}s'
        elif print_time_minutes > 0:
            formatted_time = f'{print_time_minutes}m {print_time_seconds}s'
        else:
            formatted_time = f'{print_time_seconds}s'

        return {
            'printer_name': self.printer_name,
            'temperature': round(self.temperature, 2),
            'status': self.status,
            'fan_speed': round(self.fan_speed, 2),
            'print_progress': round(self.print_progress, 2),
            'filament_usage': round(self.filament_usage, 2),
            'left_filament': round(left_filament_percentage, 2),
            'print_time': formatted_time,
        }
