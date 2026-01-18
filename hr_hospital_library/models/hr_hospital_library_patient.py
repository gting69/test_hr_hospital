import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HrHospitalLibraryPatient(models.Model):
    """
    Модель для обліку пацієнтів медичного закладу.
    Наслідує базову інформацію про особу та додає медичні дані: групу крові,
    алергії, страхову інформацію, а також автоматично відстежує історію
    зміни особистого лікаря та встановлених діагнозів.
    """
    _name = 'hr.hospital.library.patient'
    _description = 'Patient'
    _inherit = ['abstract.person']
    _rec_name = 'display_name'

    active = fields.Boolean(default=True)
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='Personal Doctor',
    )
    passport_data = fields.Char(size=10)
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
    )
    blood_rh = fields.Selection(
        selection=[
            ('+', 'Rh+'),
            ('-', 'Rh-'),
        ],
        string='Rh Factor',
    )
    allergies = fields.Text()
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance Company',
        domain=[('is_company', '=', True)],
    )
    insurance_policy_number = fields.Char()

    doctor_history_ids = fields.One2many(
        comodel_name='patient.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )

    phone = fields.Char()

    diagnosis_history_ids = fields.Many2many(
        comodel_name='medical.diagnosis',
        string='Diagnosis History',
        compute='_compute_diagnosis_history',
        help="All diagnoses from all visits of this patient"
    )

    display_name = fields.Char(
        string='Patient Name',
        compute='_compute_display_name',
        search='_search_display_name',
    )

    user_id = fields.Many2one(
        'res.users',
        string='Related User',
        help='User account connected to this patient'
    )

    user_id = fields.Many2one('res.users', string='Related User')

    def _compute_diagnosis_history(self):
        for rec in self:
            visits = self.env['hr.hospital.library.visit'].search([
                ('patient_id', '=', rec.id)
            ])
            rec.diagnosis_history_ids = visits.mapped('diagnosis_ids')

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
        res = super(HrHospitalLibraryPatient, self).write(vals)
        if 'personal_doctor_id' in vals:
            for rec in self:
                if rec.personal_doctor_id:
                    self.env['patient.doctor.history'].create({
                        'patient_id': rec.id,
                        'doctor_id': rec.personal_doctor_id.id,
                        'appointment_date': fields.Date.today(),
                        'is_active': True,
                    })
        return res
