from odoo import api, fields, models, _


class Author(models.Model):
    _name = 'bd.author'
    _description = 'author of comic book'

    name = fields.Char('Name', 
        help='Name of the author. Since most of the data comes from BNF and there is no distinction between name and surname,'
        'it\'s best to merge the two.')
    bd_ids = fields.Many2many('bd.bd', string='Albums')