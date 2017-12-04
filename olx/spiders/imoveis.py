# -*- coding: utf-8 -*-
import scrapy
import re

from olx.items import OlxItem
from datetime import date


class ImoveisSpider(scrapy.Spider):
    name = 'imoveis'
    allowed_domains = ['pb.olx.com.br']
    #start_urls = ['http://pb.olx.com.br/']
    start_urls = ['http://pb.olx.com.br/paraiba/joao-pessoa/imoveis/aluguel']

    converteMes = {
        "Janeiro":   1,
        "Fevereiro": 2,
        "Março":     3,
        "Abril":     4,
        "Maio":      5,
        "Junho":     6,
        "Julho":     7,
        "Agosto":    8,
        "Setembro":  9,
        "Outubro":   10,
        "Novembro":  11,
        "Dezembro":  12,
    }

    def parse(self, response):
        items = response.xpath(
            '//div[contains(@class,"section_OLXad-list")]//li[contains(@class,"item") and not(contains(@class, "list_native"))]'
        )

        for i, item in enumerate(items):
            url = item.xpath(".//a[contains(@class,'OLXad-list-link')]/@href").extract_first()
            
            #if i == 0:
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()

        if next_page:
            #self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        #self.log(u'Imóvel URL: {0}'.format(response.url))
        
        imovel = OlxItem()

        imovel['url']       = response.url
        imovel['titulo']    = response.xpath('normalize-space(//h1[contains(@id,"ad_title")]//.)').extract_first()

        data                = response.xpath('normalize-space(//div[contains(@class,"OLXad-date")]//p)').re("Inserido em: (\d*) (\w*)")
        imovel['data']      = date(date.today().year, self.converteMes[data[1]], int(data[0]))

        preco               = response.xpath('normalize-space(//span[contains(@class,"actual-price")])').re("R\$ (.*)")
        preco               = (preco and preco[0]) or 0
        if preco != 0:
            imovel['preco']     = int(re.sub('[^0-9]', '', preco))
        else:
            imovel['preco']     = preco


        imovel['descricao'] = response.xpath('normalize-space(//div[contains(@class,"OLXad-description")]//p)').extract_first()

        detalhes = response.xpath('//div[contains(@class, "OLXad-details")]//li[contains(@class, "item")]')

        atributo = None
        valor    = None
        for i, detalhe in enumerate(detalhes):
            atributo = detalhe.xpath('normalize-space(.//span[contains(@class, "term")]/text())').extract_first()
            valor    = detalhe.xpath('normalize-space(.//strong[contains(@class, "description")]/text())').extract_first()
            
            if (atributo == 'Tipo:'):
                imovel['tipo'] = valor
            elif (atributo == 'Área útil:'):
                area = int(re.sub('[^0-9]', '', valor))
                imovel['area_util'] = area
            elif (atributo == 'Área construída:'):
                area = int(re.sub('[^0-9]', '', valor))
                imovel['area_construida'] = area
            elif (atributo == 'Quartos:'):
                imovel['n_quartos'] = valor
            elif (atributo == 'Vagas na garagem:'):
                imovel['vagas_garagem'] = valor
            elif (atributo == 'Condomínio:'):
                imovel['condominio'] = valor

        localizacao = response.xpath('//div[contains(@class, "OLXad-location")]//li[contains(@class, "item")]')

        atributo = None
        valor    = None
        for i, loc in enumerate(localizacao):
            atributo = loc.xpath('normalize-space(.//span[contains(@class, "term")]/text())').extract_first()
            valor    = loc.xpath('normalize-space(.//strong[contains(@class, "description")]/text())').extract_first()
            
            if (atributo == 'Município:'):
                imovel['municipio'] = valor
            elif (atributo == 'CEP do imóvel:'):
                imovel['cep'] = valor
            elif (atributo == 'Bairro:'):
                imovel['bairro'] = valor
            
        imovel['id'] = response.xpath('normalize-space(//div[contains(@class, "OLXad-id")]//p//strong)').extract_first()

        yield imovel
