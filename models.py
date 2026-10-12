from abc import ABC, abstractmethod

class Student:
    """Субъект: Студент"""
    def __init__(self, student_id: str, full_name: str):
        self.student_id = student_id
        self.full_name = full_name

    def __repr__(self):
        return f"Student({self.student_id}, {self.full_name})"


class AttendanceJournal:
    """Журнал посещаемости (инкапсуляция состояния)"""
    def __init__(self):
        # Словарь: student_id -> список статусов ('present', 'late', 'absent', 'excused')
        self._records: dict[str, list[str]] = {}

    def add_record(self, student_id: str, status: str):
        if student_id not in self._records:
            self._records[student_id] = []
        self._records[student_id].append(status)

    def get_records(self, student_id: str) -> list[str]:
        return self._records.get(student_id, [])

    def get_all(self) -> dict[str, list[str]]:
        return self._records


# Лекция 6: Общий интерфейс и полиморфизм
class AccessPolicy(ABC):
    """Абстрактная политика допуска к зачёту/экзамену"""
    @abstractmethod
    def check_access(self, attendance_list: list[str]) -> bool:
        pass


class StandardPolicy(AccessPolicy):
    """Стандартная политика: пропусков (absent) должно быть не более 20%"""
    def __init__(self, total_classes: int, max_absent_percent: float = 20.0):
        self.total_classes = total_classes
        self.max_absent_percent = max_absent_percent

    def check_access(self, attendance_list: list[str]) -> bool:
        if not self.total_classes:
            return True
        absent_count = attendance_list.count('absent')
        percent = (absent_count / self.total_classes) * 100
        return percent <= self.max_absent_percent


class LenientPolicy(AccessPolicy):
    """Лояльная политика: учитываются также опоздания (late считаются как 0.5 пропуска)"""
    def __init__(self, total_classes: int, max_penalty_percent: float = 30.0):
        self.total_classes = total_classes
        self.max_penalty_percent = max_penalty_percent

    def check_access(self, attendance_list: list[str]) -> bool:
        if not self.total_classes:
            return True
        penalty_points = attendance_list.count('absent') + (attendance_list.count('late') * 0.5)
        percent = (penalty_points / self.total_classes) * 100
        return percent <= self.max_penalty_percent