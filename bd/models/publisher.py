from odoo import api, fields, models, _


class Publisher(models.Model):
    _name = 'bd.publisher'
    _description = 'Publisher of comic book'

    name = fields.Char('Name', 
        help='Name of the publisher.')
        