from odoo import api, fields, models, _


class Publisher(models.Model):
    _name = 'bd.publisher'
    _description = 'Publisher of comic book'

    name = fields.Char('Name', help='Name of the publisher.')


class PublisherAlias(models.Model):
    _name = 'bd.publisher.alias'
    _description = 'Publisher alias'

    name = fields.Char('Name', help='Name of the publisher.')
    publisher_id = fields.Many2one('bd.publisher', string='Publisher')