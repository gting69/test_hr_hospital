from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date

class TestHospital(TransactionCase):

    def setUp(self):
        """ Підготовка початкових даних для кожного тесту """
        super(TestHospital, self).setUp()
        self.Doctor = self.env['hr.hospital.library.doctor']
        self.Patient = self.env['hr.hospital.library.patient']

    def test_01_doctor_mentor_self_constraint(self):
        """ Тест 1: Перевірка, що лікар не може бути ментором самому собі """
        doctor = self.Doctor.create({
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
        })
        # Очікуємо помилку ValidationError при спробі призначити себе ментором
        with self.assertRaises(ValidationError):
            doctor.mentor_id = doctor.id

    def test_02_patient_future_birth_date(self):
        """ Тест 2: Перевірка, що дата народження не може бути в майбутньому """
        with self.assertRaises(ValidationError):
            self.Patient.create({
                'first_name': 'Petro',
                'last_name': 'Petrenko',
                'birth_date': date(2030, 1, 1), # Майбутня дата
            })

    def test_03_doctor_rating_limit(self):
        """ Тест 3: Перевірка обмеження рейтингу лікаря (не більше 5) """
        doctor = self.Doctor.create({
            'first_name': 'Olena',
            'last_name': 'Kovalenko',
        })
        with self.assertRaises(ValidationError):
            doctor.rating = 10.0 # Невалідний рейтинг