{
    'name': 'HR Employee Job Department Domain',
    'version': '17.0.1.0.0',
    'summary': 'Restrict job positions to those belonging to the selected department in HR.',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': [
        'hr',  
    ],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'application': False,
}
