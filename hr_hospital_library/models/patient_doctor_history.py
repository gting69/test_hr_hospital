from odoo import models, fields, api

class PatientDoctorHistory(models.Model):
    _name = 'patient.doctor.history'
    _description = 'Patient Doctor History'
    _order = 'appointment_date desc'

    patient_id = fields.Many2one('hr.hospital.library.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hr.hospital.library.doctor', string='Doctor', required=True)
    appointment_date = fields.Date(string='Appointment Date', required=True, default=fields.Date.today)
    change_date = fields.Date(string='Change Date')
    reason = fields.Text(string='Reason for Change')
    is_active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        if vals.get('patient_id'):
            prev_history = self.search([
                ('patient_id', '=', vals['patient_id']),
                ('is_active', '=', True)
            ])
            if prev_history:
                prev_history.write({
                    'is_active': False,
                    'change_date': fields.Date.today()
                })
        return super(PatientDoctorHistory, self).create(vals)