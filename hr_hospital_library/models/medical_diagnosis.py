from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MedicalDiagnosis(models.Model):
    _name = 'medical.diagnosis'
    _description = 'Medical Diagnosis'

    visit_id = fields.Many2one('hr.hospital.library.visit', string='Visit', ondelete='cascade')
    disease_id = fields.Many2one(
        'hr.hospital.disease.type',
        string='Disease',
        required=True,
        domain=[('is_contagious', '=', True), ('severity_level', 'in', ['high', 'critical'])]
    )

    description = fields.Text(string='Diagnosis Description')
    treatment = fields.Html(string='Treatment Prescribed')
    is_approved = fields.Boolean(string='Approved', default=False)
    approved_by_doctor_id = fields.Many2one('hr.hospital.library.doctor', string='Approved By', readonly=True)
    approval_date = fields.Datetime(string='Approval Date', readonly=True)
    severity = fields.Selection([
        ('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe'), ('critical', 'Critical')
    ], string='Severity')

    @api.constrains('approval_date', 'visit_id')
    def _check_approval_date(self):
        for rec in self:
            if rec.approval_date and rec.visit_id.planned_datetime:
                if rec.approval_date < rec.visit_id.planned_datetime:
                    raise ValidationError("Дата затвердження не може бути раніше дати візиту!")

    def action_approve(self):
        for rec in self:
            approver = rec.visit_id.doctor_id.mentor_id or rec.visit_id.doctor_id
            rec.write({
                'is_approved': True,
                'approved_by_doctor_id': approver.id,
                'approval_date': fields.Datetime.now(),
            })