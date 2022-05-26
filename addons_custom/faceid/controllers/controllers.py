#-*- coding: utf-8 -*-
from turtle import ht
from odoo import http


class Ooad(http.Controller):

    @http.route(route='/faceid/create', method='get', auth='public', type='json')
    def create_faceid(self, name, img):
        http.request.env['face'].create({
            'name': name,
            'img': str.encode(img)
        })