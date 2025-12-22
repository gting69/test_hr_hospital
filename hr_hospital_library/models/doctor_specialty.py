from odoo import models, fields


class DoctorSpecialty(models.Model):
    _name = 'doctor.specialty'
    _description = 'Doctor Specialty'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Specialty Code',
        size=10,
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.library.doctor',
        inverse_name='specialty_id',
        string='Doctors',
    )