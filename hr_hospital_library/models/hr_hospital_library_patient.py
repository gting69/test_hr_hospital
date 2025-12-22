import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HrHospitalLibraryPatient(models.Model):
    _name = 'hr.hospital.library.patient'
    _description = 'Patient'
    _inherit = ['abstract.person']
    _rec_name = 'display_name'

    active = fields.Boolean(
        default=True,
    )
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='Personal Doctor',
    )
    passport_data = fields.Char(
        string='Passport Data',
        size=10,
    )
    contact_person_id = fields.Many2one(
        comodel_name='contact.person',
        string='Contact Person',
    )
    blood_group = fields.Selection(
        selection=[
            ('0', 'O(I)'),
            ('A', 'A(II)'),
            ('B', 'B(III)'),
            ('AB', 'AB(IV)'),
        ],
        string='Blood Group',
    )
    blood_rh = fields.Selection(
        selection=[
            ('+', 'Rh+'),
            ('-', 'Rh-'),
        ],
        string='Rh Factor',
    )
    allergies = fields.Text(
        string='Allergies',
    )
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance Company',
        domain=[('is_company', '=', True)],
    )
    insurance_policy_number = fields.Char(
        string='Insurance Policy Number',
    )
    doctor_history_ids = fields.One2many(
        comodel_name='patient.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            lang = self.env['res.lang'].search(
                [('code', 'ilike', self.country_id.code)],
                limit=1,
            )
            if lang:
                self.lang_id = lang

    @api.onchange('country_id')
    def _onchange_country_filter_doctors(self):
        domain = []
        if self.country_id:
            domain = [('education_country_id', '=', self.country_id.id)]
        return {'domain': {'personal_doctor_id': domain}}

    def write(self, vals):
        if 'personal_doctor_id' in vals:
            for rec in self:
                if rec.personal_doctor_id:
                    self.env['patient.doctor.history'].create({
                        'patient_id': rec.id,
                        'doctor_id': rec.personal_doctor_id.id,
                        'appointment_date': (
                            rec.create_date.date() if rec.create_date
                            else fields.Date.today()
                        ),
                        'change_date': fields.Date.today(),
                        'is_active': False,
                    })
        return super(HrHospitalLibraryPatient, self).write(vals)