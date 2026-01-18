from odoo import models, fields


class ContactPerson(models.Model):
    """
    Модель для зберігання інформації про контактних осіб пацієнтів.
    Наслідує базові персональні дані з абстрактної моделі осіб.
    """
    _name = 'contact.person'
    _description = 'Contact Person'
    _inherit = ['abstract.person']

    relation = fields.Char()
