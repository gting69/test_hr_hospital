from odoo import models, fields


class DoctorSpecialty(models.Model):
    _name = 'doctor.specialty'
    _description = 'Doctor Specialty'

    name = fields.Char(
        required=True,
    )
    code = fields.Char(
        string='Specialty Code',
        size=10,
        required=True,
    )
    description = fields.Text()
    active = fields.Boolean(
        default=True,
    )

    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.library.doctor',
        inverse_name='specialty_id',
        string='Doctors',
    )
