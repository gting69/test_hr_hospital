import logging
from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class HrHospitalLibraryDoctor(models.Model):
    _name = 'hr.hospital.library.doctor'
    _description = 'Doctor'
    _inherit = ['abstract.person']

    active = fields.Boolean(default=True)
    description = fields.Text()
    user_id = fields.Many2one('res.users', string='System User')
    specialty_id = fields.Many2one('doctor.specialty', string='Specialty')
    is_intern = fields.Boolean(string='Is Intern', default=False)
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor', string='Mentor', domain=[('is_intern', '=', False)])
    license_number = fields.Char(string='License Number', required=True, copy=False)
    license_date = fields.Date(string='License Issue Date')
    experience = fields.Integer(string='Experience (years)', compute='_compute_experience', store=True)
    rating = fields.Float(string='Rating', digits=(3, 2))
    education_country_id = fields.Many2one('res.country', string='Education Country')
    schedule_ids = fields.One2many(comodel_name='doctor.schedule', inverse_name='doctor_id', string='Work Schedule')

    _sql_constraints = [
        ('license_number_unique', 'UNIQUE(license_number)', 'The license number must be unique!'),
        ('rating_check', 'CHECK(rating >= 0 AND rating <= 5)', 'Rating must be between 0 and 5!')
    ]

    @api.depends('last_name', 'first_name', 'specialty_id')
    def _compute_display_name(self):
        for rec in self:
            name = f"{rec.last_name or ''} {rec.first_name or ''}".strip()
            rec.display_name = f"{name} ({rec.specialty_id.name})" if rec.specialty_id else name

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if self.is_intern and not self.mentor_id:
            mentor = self.env['hr.hospital.library.doctor'].search([('is_intern', '=', False)], limit=1)
            self.mentor_id = mentor

    @api.depends('license_date')
    def _compute_experience(self):
        today = date.today()
        for rec in self:
            if rec.license_date:
                rec.experience = today.year - rec.license_date.year - (
                        (today.month, today.day) < (rec.license_date.month, rec.license_date.day)
                )
            else: rec.experience = 0

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for rec in self:
            if rec.mentor_id:
                if rec.mentor_id == rec: raise ValidationError("A doctor cannot be their own mentor!")
                if rec.mentor_id.is_intern: raise ValidationError("An intern cannot be chosen as a mentor!")

    @api.constrains('rating')
    def _check_rating_value(self):
        for rec in self:
            if rec.rating < 0 or rec.rating > 5: raise ValidationError("The rating must be between 0.00 and 5.00!")

    def toggle_active(self):
        for rec in self:
            if rec.active:
                active_visits = self.env['hr.hospital.library.visit'].search_count([
                    ('doctor_id', '=', rec.id), ('state', '=', 'planned')])
                if active_visits > 0: raise ValidationError("Cannot archive a doctor with planned visits!")
        return super().toggle_active()

    mentor_id = fields.Many2one(
        'hr.hospital.library.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )