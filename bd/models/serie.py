from odoo import api, fields, models, _


class Serie(models.Model):
    _name = 'bd.serie'
    _description = 'Serie of comic book'

    name = fields.Char('Name', 
        help='Name of the serie.')
    status = fields.Selection(string='Status', selection=[('continue', 'En cours'), ('finished', 'Terminée')])
    author_ids = fields.Many2many('bd.author', compute='_compute_author')
    bd_ids = fields.One2many('bd.bd', 'serie_id', string='Albums')

    def _compute_author(self):
        for serie in self:
            serie.author_ids = serie.bd_ids.author_ids