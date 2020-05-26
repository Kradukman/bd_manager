#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests as req
import json
from isbnlib import meta, canonical
from isbnlib.registry import bibformatters, set_cache
from isbnlib_bnf._bnf import query

class BdBd(models.Model):
    _name = 'bd.bd'
    _description = 'Model for comic book'
    _order = 'tome'

    name = fields.Char('isbn', required=True, help='ISBN. ISBN10 and ISBN13 will be converted into EAN13')
    title = fields.Char('Title')
    year = fields.Char('Year')
    tome = fields.Integer('Tome')
    author_ids = fields.Many2many('bd.author', string='Authors', readonly=True)
    author_alias_ids = fields.Many2many('bd.author.alias', string='Authors alias')
    location_id = fields.Many2one('res.partner', string='Where is the comic')
    publisher_id = fields.Many2one('bd.publisher', string='Publisher', related='publisher_alias_id.publisher_id', readonly=True)
    publisher_alias_id = fields.Many2one('bd.publisher.alias', string='Publisher alias')
    serie_id = fields.Many2one('bd.serie', string='Serie')
    status = fields.Selection(string='Status', related='serie_id.status')
    cover = fields.Binary('cover', store=True)
    comment = fields.Char('Comment')
    service = fields.Selection(
        string='Service', 
        selection=[('bnf', 'BNF'), ('goob', 'Google Book'), ('openl', 'Open Library')], 
        default='bnf', 
        required=True)

    @api.onchange('name', 'service')
    def _onchange_name(self):
        if self.name:
            set_cache(None)
            isbn = canonical(self.name)
            bookdata = meta(isbn, self.service)
            if bookdata:
                authors_alias = []
                self.title = bookdata['Title']
                self.year = bookdata['Year']
                publisher_alias_id = self.env['bd.publisher.alias'].search([('name', '=',  bookdata['Publisher'])], limit=1)
                if not publisher_alias_id:
                    publisher_alias_id = self.env['bd.publisher'].create({
                        'name': bookdata['Publisher'],
                    })
                self.publisher_alias_id = publisher_alias_id
                for author_alias in bookdata['Authors']:
                    author_alias_id = self.env['bd.author.alias'].search([('name', '=', author_alias)], limit=1)
                    if not author_alias_id:
                        author_alias_id = self.env['bd.author.alias'].create({
                            'name': author_alias,})
                    authors_alias.append(author_alias_id.id)
                if authors_alias:
                    self.author_alias_ids = [(6, 0, authors_alias)]

    @api.onchange('author_alias_ids')
    def _onchange_author_alias_ids(self):
        for bd in self:
            bd.author_ids = [(6, 0, (alias_id.author_id.id for alias_id in bd.author_alias_ids))]