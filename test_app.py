import unittest
from models import Student, AttendanceJournal, StandardPolicy, LenientPolicy
from logic import calculate_attendance_percentage, filter_risk_group

class TestAttendanceSystem(unittest.TestCase):
    
    def test_calculation_empty(self):
        self.assertEqual(calculate_attendance_percentage([]), 0.0)

    def test_calculation_normal(self):
        records = ['present', 'present', 'absent', 'late', 'excused']
        # Полезных (present, late, excused) = 4 из 5 = 80.0%
        self.assertEqual(calculate_attendance_percentage(records), 80.0)

    def test_standard_policy_pass(self):
        policy = StandardPolicy(total_classes=10, max_absent_percent=20.0)
        # 2 пропуска из 10 = 20% (допуск разрешен)
        records = ['present']*8 + ['absent']*2
        self.assertTrue(policy.check_access(records))

    def test_standard_policy_fail(self):
        policy = StandardPolicy(total_classes=10, max_absent_percent=20.0)
        # 3 пропуска из 10 = 30% (превышен лимит)
        records = ['present']*7 + ['absent']*3
        self.assertFalse(policy.check_access(records))

    def test_lenient_policy_logic(self):
        policy = LenientPolicy(total_classes=10, max_penalty_percent=30.0)
        # 2 опоздания ('late' дают по 0.5 балла штрафа) + 1 прогул ('absent' = 1) = 2 штрафных балла (20%)
        records = ['present']*7 + ['late', 'late', 'absent']
        self.assertTrue(policy.check_access(records))

    def test_journal_storage(self):
        journal = AttendanceJournal()
        journal.add_record("ST-001", "present")
        self.assertEqual(journal.get_records("ST-001"), ["present"])
        self.assertEqual(journal.get_records("ST-999"), [])

    def test_filter_risk_group_empty(self):
        students = [Student("ST-1", "Тест Тестов")]
        journal = AttendanceJournal()
        journal.add_record("ST-1", "present")
        policy = StandardPolicy(total_classes=1, max_absent_percent=20.0)
        risk = filter_risk_group(students, journal, policy)
        self.assertEqual(len(risk), 0)

    def test_boundary_exact_limit(self):
        policy = StandardPolicy(total_classes=10, max_absent_percent=30.0)
        records = ['present']*7 + ['absent']*3 # ровно 30%
        self.assertTrue(policy.check_access(records))

    def test_boundary_over_limit(self):
        policy = StandardPolicy(total_classes=10, max_absent_percent=30.0)
        records = ['present']*6 + ['absent']*4 # 40%
        self.assertFalse(policy.check_access(records))

    def test_all_absent(self):
        records = ['absent']*10
        self.assertEqual(calculate_attendance_percentage(records), 0.0)

    def test_all_present(self):
        records = ['present']*10
        self.assertEqual(calculate_attendance_percentage(records), 100.0)

    def test_multiple_students_isolation(self):
        journal = AttendanceJournal()
        journal.add_record("A", "present")
        journal.add_record("B", "absent")
        self.assertEqual(journal.get_records("A"), ["present"])
        self.assertEqual(journal.get_records("B"), ["absent"])

if __name__ == '__main__':
    unittest.main()