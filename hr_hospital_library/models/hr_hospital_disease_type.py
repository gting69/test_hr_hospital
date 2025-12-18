from odoo import models, fields

class HrHospitalDiseaseType(models.Model):
    _name = 'hr.hospital.disease.type'
    _description = 'Disease Type'
    _parent_name = "parent_id"

    name = fields.Char(string='Disease Name', required=True)

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease.type',
        string='Parent Disease',
        ondelete='cascade')

    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease.type',
        inverse_name='parent_id',
        string='Child Diseases')

    icd_10_code = fields.Char(string='ICD-10 Code', size=10)

    severity_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity Level', default='low')

    is_contagious = fields.Boolean(string='Is Contagious', default=False)
    symptoms = fields.Text(string='Symptoms')

    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Spread Regions')