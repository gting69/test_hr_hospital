from odoo import models, fields

class ContactPerson(models.Model):
    _name = 'contact.person'
    _description = 'Contact Person'
    _inherit = ['abstract.person']

    relation = fields.Char(string='Relation to Patient')