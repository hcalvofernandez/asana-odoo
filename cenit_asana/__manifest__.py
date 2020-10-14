# -*- coding: utf-8 -*-
################################################################################
# Author      : Hanoi Calvo Fernandez
# Copyright(c): 2020-Present HanoiCalvo Fernandez hanoi.calvo@uic.cu
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Asana Integration',
    'version': '1.0.0',
    'author': 'NeoHan-Solutions',
    'website': 'https://asana.odooexperts.com.mx',
    # ~ 'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': "Asana Integration",
    'description': "Asana Integration",
    'depends': ['cenit_base'],
    'data': [
        'security/ir.model.access.csv',
        'view/config.xml',
        'view/wizard.xml'
    ],
    'images': ['static/images/banner.jpg'],
    'installable': True
}
