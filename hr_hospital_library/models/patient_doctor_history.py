from odoo import models, fields, api


class PatientDoctorHistory(models.Model):
    _name = 'patient.doctor.history'
    _description = 'Patient Doctor History'
    _order = 'appointment_date desc'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.library.patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        required=True,
    )
    appointment_date = fields.Date(
        required=True,
        default=fields.Date.today,
    )
    change_date = fields.Date()
    reason = fields.Text(
        string='Reason for Change',
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('patient_id'):
            prev_history = self.search([
                ('patient_id', '=', vals['patient_id']),
                ('is_active', '=', True),
            ])
            if prev_history:
                prev_history.write({
                    'is_active': False,
                    'change_date': fields.Date.today(),
                })
        return super(PatientDoctorHistory, self).create(vals)
