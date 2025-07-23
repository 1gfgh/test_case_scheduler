import unittest
from scheduler import Scheduler


class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler(
            url="https://ofc-test-01.tspb.su/test-task/")

    def test_get_busy_slots(self):
        result = self.scheduler.get_busy_slots("2025-02-15")
        expected = [("09:00", "12:00"), ("17:30", "20:00")]
        self.assertEqual(result, expected)

        result = self.scheduler.get_busy_slots("2025-02-18")
        expected = [("10:00", "11:00"), ("11:30", "14:00"),
                    ("14:00", "16:00"), ("17:00", "18:00")]
        self.assertEqual(result, expected)

        with self.assertRaises(ValueError):
            self.scheduler.get_busy_slots("2025-02-20")

    def test_get_free_slots(self):
        result = self.scheduler.get_free_slots("2025-02-15")
        expected = [("12:00", "17:30"), ("20:00", "21:00")]
        self.assertEqual(result, expected)

        result = self.scheduler.get_free_slots("2025-02-17")
        expected = [("09:00", "12:30")]
        self.assertEqual(result, expected)

        result = self.scheduler.get_free_slots("2025-02-19")
        expected = [("09:00", "18:00")]
        self.assertEqual(result, expected)

    def test_is_available(self):
        self.assertTrue(self.scheduler.is_available(
            "2025-02-15", "13:00", "14:00"))

        self.assertFalse(self.scheduler.is_available(
            "2025-02-15", "10:00", "11:00"))

        self.assertTrue(self.scheduler.is_available(
            "2025-02-15", "12:00", "12:30"))

        self.assertTrue(self.scheduler.is_available(
            "2025-02-15", "20:30", "21:00"))

        self.assertFalse(self.scheduler.is_available(
            "2025-02-15", "08:00", "09:00"))

    def test_find_slot_for_duration(self):
        result = self.scheduler.find_slot_for_duration(30)
        self.assertEqual(result, ("2025-02-15", "12:00", "12:30"))

        result = self.scheduler.find_slot_for_duration(180)
        self.assertEqual(result, ("2025-02-15", "12:00", "15:00"))

        result = self.scheduler.find_slot_for_duration(300)
        self.assertEqual(result, ("2025-02-15", "12:00", "17:00"))

        result = self.scheduler.find_slot_for_duration(1440)
        self.assertIsNone(result)

    def test_validate_date_and_time_format(self):
        try:
            self.scheduler.get_busy_slots("2025-02-15")
        except ValueError:
            self.fail("Valid date raised ValueError")

        with self.assertRaises(ValueError):
            self.scheduler.get_busy_slots("15-02-2025")

        with self.assertRaises(ValueError) as context:
            self.scheduler.is_available("2025-02-15", "13.00", "14:00")
            self.assertEqual(str(context.exception),
                             "Invalid time format. Expected '%H:%M'")

        with self.assertRaises(ValueError) as context:
            self.scheduler.is_available("2025-02-15", "14:00", "13:00")
            self.assertEqual(str(context.exception),
                             "Invalid time input, start must be earlier then end")


if __name__ == '__main__':
    unittest.main()
