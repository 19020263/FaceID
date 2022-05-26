# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Face(models.Model):
    _name = 'face'
    _description = 'face'

    name = fields.Char(string="Name")
    img = fields.Binary(string="Image")
    time = fields.Datetime(string="Time", default = lambda self: fields.datetime.today())
