import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

CONST_EXP = "Hr hospital constant example"


class HrHospitalLibraryDoctor(models.Model):
    _name = 'hr.hospital.library.doctor'
    _description = 'Doctor'

    name = fields.Char()

    active = fields.Boolean(
        default=True, )
    description = fields.Text()

    date_of_birth = fields.Date(
        string="Date of Birth",
    )

    phone = fields.Char(
        string="Phone Number",
    )
