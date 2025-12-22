import re
import logging
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    old_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='Old Doctor',
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='New Doctor',
        required=True,
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.library.patient',
        string='Patients',
        required=True,
    )
    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.today,
    )
    reason = fields.Text(
        string='Reason for Change',
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'hr.hospital.library.patient':
            active_ids = self.env.context.get('active_ids')
            res.update({
                'patient_ids': [(6, 0, active_ids)]
            })
        return res

    def action_reassign(self):
        for patient in self.patient_ids:
            patient.write({
                'personal_doctor_id': self.new_doctor_id.id
            })
        return {'type': 'ir.actions.act_window_close'}


class RescheduleVisitWizard(models.TransientModel):
    _name = 'reschedule.visit.wizard'
    _description = 'Reschedule Visit Wizard'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.library.visit',
        string='Current Visit',
        readonly=True,
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='New Doctor',
    )
    new_date = fields.Date(
        string='New Date',
        required=True,
    )
    new_time = fields.Float(
        string='New Time',
        required=True,
    )
    reason = fields.Text(
        string='Reason for Reschedule',
        required=True,
    )

    def action_reschedule(self):
        self.visit_id.state = 'cancelled'

        new_datetime = (
            fields.Datetime.to_datetime(self.new_date) +
            timedelta(hours=self.new_time)
        )

        self.env['hr.hospital.library.visit'].create({
            'name': _("Rescheduled: %s") % self.visit_id.name,
            'patient_id': self.visit_id.patient_id.id,
            'doctor_id': self.new_doctor_id.id or self.visit_id.doctor_id.id,
            'planned_datetime': new_datetime,
            'visit_type': self.visit_id.visit_type,
        })
        return {'type': 'ir.actions.act_window_close'}


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.library.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease.type',
        string='Diseases',
    )
    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Countries',
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
    )
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
        string='Group By',
    )

    def action_generate_report(self):
        self.ensure_one()
        domain = [
            ('visit_id.planned_datetime', '>=', self.start_date),
            ('visit_id.planned_datetime', '<=', self.end_date),
        ]
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        return {
            'name': _('Disease Analysis Result'),
            'type': 'ir.actions.act_window',
            'res_model': 'medical.diagnosis',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {
                'group_by': self.group_by or 'disease_id',
            },
        }


class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        string='Doctor',
        required=True,
    )
    start_week = fields.Date(
        string='Start Week',
        required=True,
    )
    weeks_count = fields.Integer(
        string='Weeks Count',
        default=1,
        required=True,
    )
    monday = fields.Boolean(string='Mon')
    tuesday = fields.Boolean(string='Tue')
    wednesday = fields.Boolean(string='Wed')
    thursday = fields.Boolean(string='Thu')
    friday = fields.Boolean(string='Fri')
    saturday = fields.Boolean(string='Sat')
    sunday = fields.Boolean(string='Sun')
    start_hour = fields.Float(
        string='Start Hour',
    )
    end_hour = fields.Float(
        string='End Hour',
    )

    def action_generate_schedule(self):
        self.ensure_one()
        days_map = {
            '0': self.monday,
            '1': self.tuesday,
            '2': self.wednesday,
            '3': self.thursday,
            '4': self.friday,
            '5': self.saturday,
            '6': self.sunday,
        }
        selected_days = [day for day, active in days_map.items() if active]

        for week in range(self.weeks_count):
            for day_code in selected_days:
                schedule_date = (
                    self.start_week +
                    timedelta(weeks=week, days=int(day_code))
                )
                self.env['doctor.schedule'].create({
                    'doctor_id': self.doctor_id.id,
                    'day_of_week': day_code,
                    'date': schedule_date,
                    'start_hour': self.start_hour,
                    'end_hour': self.end_hour,
                    'schedule_type': 'work',
                })
        return {'type': 'ir.actions.act_window_close'}


class PatientCardExportWizard(models.TransientModel):
    _name = 'patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.library.patient',
        string='Patient',
        required=True,
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )
    include_diagnoses = fields.Boolean(
        string='Include Diagnoses',
        default=True,
    )
    include_recommendations = fields.Boolean(
        string='Include Recommendations',
        default=True,
    )
    export_format = fields.Selection(
        selection=[
            ('json', 'JSON'),
            ('csv', 'CSV'),
        ],
        string='Export Format',
        default='json',
        required=True,
    )

    def action_export(self):
        return True