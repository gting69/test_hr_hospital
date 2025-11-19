from odoo import models, fields


class HrHospitalLibraryVisit(models.Model):
    _name = 'hr.hospital.library.visit'
    _description = 'Patient Visit'

    name = fields.Char(
        string='Visit Subject',
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.library.patient',
        string="Patient",
        required=True,
        ondelete='restrict',
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string="Doctor",
        required=True,
        ondelete='restrict',
    )

    disease_type_id = fields.Many2one(
        comodel_name='hr.hospital.disease.type',
        string="Disease Type",
        ondelete='restrict',
    )

    visit_datetime = fields.Datetime(
        string="Visit Date and Time",
        required=True,
        default=fields.Datetime.now,
    )

    description = fields.Text(string='Visit Notes / Diagnosis')