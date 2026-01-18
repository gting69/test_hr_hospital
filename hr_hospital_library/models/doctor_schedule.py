from odoo import models, fields


class DoctorSchedule(models.Model):
    """
    Модель для планування робочого часу лікарів.
    Дозволяє фіксувати робочі години, відпустки та лікарняні з перевіркою коректності часу.
    """
    _name = 'doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.library.doctor',
        required=True,
    )
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string='Day of Week',
    )
    date = fields.Date()
    start_hour = fields.Float(
        string='Start Time',
    )
    end_hour = fields.Float(
        string='End Time',
    )
    schedule_type = fields.Selection(
        selection=[
            ('work', 'Work Day'),
            ('vacation', 'Vacation'),
            ('sick', 'Sick Leave'),
            ('conference', 'Conference'),
        ],
        string='Type',
        default='work',
    )
    notes = fields.Char()

    _sql_constraints = [
        (
            'check_schedule_time',
            'CHECK(end_hour > start_hour)',
            'End time must be greater than start time!'
        ),
    ]
