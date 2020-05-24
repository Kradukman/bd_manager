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
    author_ids = fields.Many2many('bd.author', string='Authors')
    location_id = fields.Many2one('res.partner', string='Where is the comic')
    publisher_id = fields.Many2one('bd.publisher', string='Publisher')
    serie_id = fields.Many2one('bd.serie', string='Serie')
    status = fields.Selection(string='Status', related='serie_id.status')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            service = 'bnf'
            set_cache(None)
            isbn = canonical(self.name)
            bookdata = meta(isbn, service)
            if bookdata:
                authors = []
                if self.author_ids:
                    authors = self.author_ids.ids
                self.title = bookdata['Title']
                self.year = bookdata['Year']
                publisher_id = self.env['bd.publisher'].search([('name', '=',  bookdata['Publisher'])], limit=1)
                if not publisher_id:
                    publisher_id = self.env['bd.publisher'].create({
                        'name': bookdata['Publisher'],
                    })
                self.publisher_id = publisher_id
                for author in bookdata['Authors']:
                    author_id = self.env['bd.author'].search([('name', '=', author)], limit=1)
                    if not author_id:
                        author_id = self.env['bd.author'].create({
                            'name': author,})
                    authors.append(author_id.id)
                self.author_ids = [(6, 0, authors)]