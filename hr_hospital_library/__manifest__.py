{
    'name': 'Hr Hospital Library',
    'summary': 'Hospital',
    'author': 'Hr Hospital',
    'website': 'https://hr.hospital/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '17.0.2.1.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [

        'security/ir.model.access.csv',

        'data/hr_hospital_disease_data.xml',

        'views/contact_person_views.xml',
        'views/doctor_specialty_views.xml',
        'views/doctor_schedule_views.xml',
        'views/hr_hospital_library_doctor_views.xml',
        'views/hr_hospital_library_patient_views.xml',
        'views/hr_hospital_library_visit_views.xml',
        'views/hr_hospital_disease_type_views.xml',
        'views/patient_doctor_history_views.xml',
        'views/mass_reassign_doctor_wizard_views.xml',

        'views/hr_hospital_library_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],

}