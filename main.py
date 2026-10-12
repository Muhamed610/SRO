from models import StandardPolicy, LenientPolicy
from logic import generate_initial_data, filter_risk_group, get_attendance_report_generator

def main():
    print("Инициализация системы контроля посещаемости...")
    students, journal = generate_initial_data()
    
    total_classes = 10
    standard_policy = StandardPolicy(total_classes, max_absent_percent=30.0)
    
    while True:
        print("\n=== МЕНЮ СИСТЕМЫ ПОСЕЩАЕМОСТИ ===")
        print("1. Показать общий отчёт по посещаемости (через генератор)")
        print("2. Вывести список студентов группы риска")
        print("3. Сравнить политику доступа (Стандартная vs Лояльная)")
        print("4. Выход")
        
        choice = input("Выберите пункт меню (1-4): ").strip()
        
        if choice == '1':
            print("\n--- ОБЩИЙ ОТЧЁТ ---")
            report_gen = get_attendance_report_generator(students, journal)
            for line in report_gen:
                print(line)
                
        elif choice == '2':
            print("\n--- ГРУППА РИСКА (Не допущены) ---")
            risks = filter_risk_group(students, journal, standard_policy)
            if not risks:
                print("Студентов в группе риска нет.")
            else:
                for student, pct in risks:
                    print(f"⚠️ {student.full_name} — Посещаемость ниже нормы ({pct}%)")
                    
        elif choice == '3':
            print("\n--- СРАВНЕНИЕ ПОЛИТИК ДОПУСКА ---")
            lenient_policy = LenientPolicy(total_classes, max_penalty_percent=30.0)
            
            std_fails = len(filter_risk_group(students, journal, standard_policy))
            len_fails = len(filter_risk_group(students, journal, lenient_policy))
            
            print(f"Не допущено по Стандартной политике (строгий подсчет пропусков): {std_fails} студ.")
            print(f"Не допущено по Лояльной политике (с учетом опозданий): {len_fails} студ.")
            print("Вывод: Лояльная политика мягче учитывает статус 'опоздал', что снижает число ложно-отрицательных решений.")
            
        elif choice == '4':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Ошибка: неверный выбор. Введите число от 1 до 4.")

if __name__ == '__main__':
    main()