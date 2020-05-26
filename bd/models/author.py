from odoo import api, fields, models, _


class Author(models.Model):
    _name = 'bd.author'
    _description = 'Author of comic book'

    name = fields.Char('Name', help='Name of the author')
    bd_ids = fields.Many2many('bd.bd', string='Albums')


class AuthorAlias(models.Model):
    _name = 'bd.author.alias'
    _description = 'Alias for Author'
    '''Since all services do not use the same standard name. Or Opencl sometimes has several ways to write author '''

    name = fields.Char('Name')
    author_id = fields.Many2one('bd.author', string='Author')
    bd_ids = fields.Many2many('bd.bd', string='Albums')

    def write(self, vals):
        res = super(AuthorAlias, self).write(vals)
        if ('author_id' in vals):
            self.bd_ids.write({'author_ids': [[6, False, (author_alias.author_id.id for author_alias in self.bd_ids.author_alias_ids)]]})
        return res