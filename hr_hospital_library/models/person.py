import re
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AbstractPerson(models.Model):
    _name = 'abstract.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    last_name = fields.Char(
        string='Last Name',
        required=True,
    )
    first_name = fields.Char(
        string='First Name',
        required=True,
    )
    middle_name = fields.Char(
        string='Middle Name',
    )
    display_name = fields.Char(
        compute='_compute_display_name',
        store=True,
    )
    phone = fields.Char(
        string='Phone',
    )
    email = fields.Char(
        string='Email',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender',
        default='other',
    )
    birth_date = fields.Date(
        string='Date of Birth',
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship',
    )
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Language',
    )

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_display_name(self):
        for rec in self:
            name_parts = [rec.last_name, rec.first_name, rec.middle_name]
            rec.display_name = " ".join(filter(None, name_parts))

    @api.depends('birth_date')
    def _compute_experience(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = (
                    today.year - rec.birth_date.year - (
                        (today.month, today.day) <
                        (rec.birth_date.month, rec.birth_date.day)
                    )
                )
            else:
                rec.age = 0

    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and not re.match(r'^\+?[\d\s\-()]{7,20}$', rec.phone):
                raise ValidationError(_("Invalid phone format!"))

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and not re.match(r"[^@]+@[^@]+\.[^@]+", rec.email):
                raise ValidationError(_("Invalid email format!"))

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date > fields.Date.today():
                raise ValidationError(_("Birth date cannot be in the future!"))
            if rec.age < 0:
                raise ValidationError(_("Patient age must be greater than 0!"))