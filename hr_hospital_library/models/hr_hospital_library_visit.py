import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HrHospitalLibraryVisit(models.Model):
    """
    Модель для реєстрації та управління візитами пацієнтів.
    Забезпечує контроль станів візиту, запобігає дублюванню записів на один день,
    реалізує захист даних завершених візитів та інтеграцію з історією діагнозів.
    """
    _name = 'hr.hospital.library.visit'
    _description = 'Patient Visit'
    _rec_name = 'planned_datetime'

    name = fields.Char(
        string='Visit Subject',
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.library.patient',
        string="Patient",
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        required=True,
        domain=[('license_number', '!=', False)],
    )
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ],
        default='planned',
        required=True,
    )
    visit_type = fields.Selection(
        selection=[
            ('primary', 'Primary'),
            ('follow_up', 'Follow-up'),
            ('preventive', 'Preventive'),
            ('urgent', 'Urgent'),
        ],
    )
    planned_datetime = fields.Datetime(
        string="Planned Date/Time",
        required=True,
    )
    actual_datetime = fields.Datetime()
    diagnosis_ids = fields.One2many(
        comodel_name='medical.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses',
    )
    diagnoses_count = fields.Integer(
        compute='_compute_diagnoses_count',
    )
    recommendations = fields.Html()
    visit_cost = fields.Monetary(
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    @api.depends('diagnosis_ids')
    def _compute_diagnoses_count(self):
        for rec in self:
            rec.diagnoses_count = len(rec.diagnosis_ids)

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': _("Patient Allergy Warning!"),
                    'message': self.patient_id.allergies,
                }
            }
        return {}

    @api.constrains('patient_id', 'doctor_id', 'planned_datetime')
    def _check_duplicate_visits(self):
        for rec in self:
            if not rec.planned_datetime:
                continue
            start_day = rec.planned_datetime.replace(
                hour=0, minute=0, second=0
            )
            end_day = rec.planned_datetime.replace(
                hour=23, minute=59, second=59
            )
            duplicate_count = self.search_count([
                ('id', '!=', rec.id),
                ('patient_id', '=', rec.patient_id.id),
                ('doctor_id', '=', rec.doctor_id.id),
                ('planned_datetime', '>=', start_day),
                ('planned_datetime', '<=', end_day),
            ])
            if duplicate_count > 0:
                raise ValidationError(_(
                    "This patient is already scheduled "
                    "for this doctor today!"
                ))

    @api.onchange('patient_id')
    def _onchange_patient_country_filter(self):
        if self.patient_id and self.patient_id.country_id:
            domain = [
                ('education_country_id', '=', self.patient_id.country_id.id)
            ]
            return {'domain': {'doctor_id': domain}}
        return {}

    def write(self, vals):
        protected_fields = ['doctor_id', 'patient_id', 'planned_datetime']
        for rec in self:
            if (rec.state == 'completed' and
                    any(f in vals for f in protected_fields)):
                raise ValidationError(
                    _("You cannot change parameters of a completed visit!")
                )
        return super(HrHospitalLibraryVisit, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.diagnosis_ids:
                raise ValidationError(
                    _("You cannot delete a visit that already has diagnoses!")
                )
        return super(HrHospitalLibraryVisit, self).unlink()
