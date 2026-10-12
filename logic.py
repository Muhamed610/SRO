from models import Student, AttendanceJournal, AccessPolicy
import random

# Лекция 2 & 3: Процедурное программирование и функции с явными параметрами
def calculate_attendance_percentage(attendance_list: list[str]) -> float:
    """Вычисляет процент успешного присутствия (present + late)"""
    if not attendance_list:
        return 0.0
    effective = attendance_list.count('present') + attendance_list.count('late') + attendance_list.count('excused')
    return round((effective / len(attendance_list)) * 100, 2)


def generate_initial_data() -> tuple[list[Student], AttendanceJournal]:
    """Генерация начального набора из 20+ записей (Требование №3)"""
    students = [
        Student(f"ST-{i:03d}", name) for i, name in enumerate([
            "Алихан М.", "Дильназ Б.", "Тимур К.", "Аружан С.", "Нурсултан Ж.",
            "Камила Т.", "Максим В.", "Елена П.", "Дамир Р.", "Адель Ш.",
            "Руслан Т.", "Мадина О.", "Санжар Б.", "Амина Н.", "Илья Р.",
            "Зарина К.", "Артур М.", "Диана С.", "Евгений Л.", "Томирис А."
        ], start=1)
    ]
    
    journal = AttendanceJournal()
    statuses = ['present', 'present', 'present', 'late', 'absent', 'excused']
    
    # Заполняем историю на 10 занятий для каждого студента детерминировано
    random.seed(42)
    for student in students:
        for _ in range(10):
            status = random.choice(statuses)
            journal.add_record(student.student_id, status)
            
    return students, journal


# Лекция 7: Чистые функции (не изменяющие исходные коллекции)
def filter_risk_group(students: list[Student], journal: AttendanceJournal, policy: AccessPolicy) -> list[tuple[Student, float]]:
    """Возвращает чистый список студентов, не прошедших по политике (группа риска)"""
    risk_list = []
    for student in students:
        records = journal.get_records(student.student_id)
        is_passed = policy.check_access(records)
        if not is_passed:
            pct = calculate_attendance_percentage(records)
            risk_list.append((student, pct))
    return risk_list


# Лекция 8: Функции высшего порядка, map и генераторы
def get_attendance_report_generator(students: list[Student], journal: AttendanceJournal):
    """Ленивый генератор строк отчёта по посещаемости"""
    for student in students:
        records = journal.get_records(student.student_id)
        pct = calculate_attendance_percentage(records)
        yield f"Студент: {student.full_name} ({student.student_id}) — Успешность: {pct}%"