import logging
from odoo import models, fields, _

_logger = logging.getLogger(__name__)


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many('hr.hospital.library.doctor')
    disease_ids = fields.Many2many('hr.hospital.disease.type')

    country_ids = fields.Many2many('res.country', string='Countries')
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    report_type = fields.Selection(
        selection=[
            ('detail', 'Detailed'),
            ('summary', 'Summary'),
        ],
        default='detail',
    )
    group_by = fields.Selection(
        selection=[
            ('doctor', 'By Doctor'),
            ('disease', 'By Disease'),
        ],
        default='disease',
    )

    def action_generate_report(self):
        self.ensure_one()
        domain = [
            ('approval_date', '>=', self.start_date),
            ('approval_date', '<=', self.end_date),
        ]
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        return {
            'name': _('Disease Analysis Result'),
            'type': 'ir.actions.act_window',
            'res_model': 'medical.diagnosis',
            'view_mode': 'tree,form,pivot',
            'domain': domain,
            'context': {
                'group_by': self.group_by or 'disease_id',
                'expand': 1,
            },
        }
