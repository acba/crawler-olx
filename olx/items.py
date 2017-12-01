# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id              = scrapy.Field()
    data            = scrapy.Field()
    titulo          = scrapy.Field()
    preco           = scrapy.Field()
    tipo            = scrapy.Field()
    area_util       = scrapy.Field()
    area_construida = scrapy.Field()
    n_quartos       = scrapy.Field()
    vagas_garagem   = scrapy.Field()
    bairro          = scrapy.Field()
    municipio       = scrapy.Field()
    cep             = scrapy.Field()
    descricao       = scrapy.Field()
    url             = scrapy.Field()