# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class OlxPipeline(object):
    def process_item(self, item, spider):
        return item

class CSVPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open('%s_items.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = [
        'id', 'data', 'tipo', 'preco', 'area_util', 
        'area_construida', 'n_quartos', 'vagas_garagem', 
        'titulo', 'bairro', 'municipio', 'cep', 
        'descricao', 'url'
    ]
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
