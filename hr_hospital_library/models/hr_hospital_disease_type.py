from odoo import models, fields

class HrHospitalDiseaseType(models.Model):
    _name = 'hr.hospital.disease.type'
    _description = 'Disease Type (Master Data)'

    name = fields.Char(
        string='Disease Name',
        required=True,
    )

    code = fields.Char(string='ICD Code / Internal Code')

    description = fields.Text(string='Detailed Description')