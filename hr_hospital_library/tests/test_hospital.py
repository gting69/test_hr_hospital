from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date

class TestHospital(TransactionCase):

    def setUp(self):
        super(TestHospital, self).setUp()
        self.Doctor = self.env['hr.hospital.library.doctor']
        self.Patient = self.env['hr.hospital.library.patient']

    def test_01_doctor_mentor_self_constraint(self):
        doctor = self.Doctor.create({
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
        })
        with self.assertRaises(ValidationError):
            doctor.mentor_id = doctor.id


    def test_02_patient_future_birth_date(self):
        with self.assertRaises(ValidationError):
            self.Patient.create({
                'first_name': 'Petro',
                'last_name': 'Petrenko',
                'birth_date': date(2030, 1, 1), # Майбутня дата
            })

    def test_03_doctor_rating_limit(self):
        doctor = self.Doctor.create({
            'first_name': 'Olena',
            'last_name': 'Kovalenko',
        })
        with self.assertRaises(ValidationError):
            doctor.rating = 10.0