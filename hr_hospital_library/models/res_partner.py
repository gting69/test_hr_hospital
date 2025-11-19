import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    hospital_doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.library.doctor',
        string='Assigned Doctors',
    )

    hospital_patient_ids = fields.Many2many(
        comodel_name='hr.hospital.library.patient',
        string='Related Patients',
    )