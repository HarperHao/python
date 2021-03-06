# -*- coding: utf-8 -*-
import scrapy
import json
import time


class MubanSpider(scrapy.Spider):
    name = 'muban'
    allowed_domains = ['data.stats.gov.cn/']
    area = [110000, 120000, 130000, 140000, 150000, 210000, 220000, 230000, 310000, 320000, 330000, 340000, 350000,
            360000, 370000, 410000, 420000, 430000, 440000, 450000, 460000, 500000, 510000, 520000, 530000, 540000,
            610000, 620000, 630000, 640000, 650000]

    start_urls = [
        'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22reg%22%2C%22valuecode%22%3A%22{}%22%7D%5D&dfwds={}&k1={}'.
            format(valuecode, '[{"wdcode":"zb","valuecode":"A0M01"}]', int(round(time.time() * 1000))) for valuecode in
        area]
    custom_settings = {
        'ITEM_PIPELINES': {'Demo3.pipelines.MuBanPipeline': 300},
    }


    def parse(self, response):
        text = json.loads(response.text, encoding='utf-8')
        datanodes = text.get('returndata').get('datanodes')
        dict1 = {}
        areas = {'110000': '北京市',
                 '120000': '天津市',
                 '130000': '河北省',
                 '140000': '山西省',
                 '150000': '内蒙古自治区',
                 '210000': '辽宁省',
                 '220000': '吉林省',
                 '230000': '黑龙江省',
                 '310000': '上海市',
                 '320000': '江苏省',
                 '330000': '浙江省',
                 '340000': '安徽省',
                 '350000': '福建省',
                 '360000': '江西省',
                 '370000': '山东省',
                 '410000': '河南省',
                 '420000': '湖北省',
                 '430000': '湖南省',
                 '440000': '广东省',
                 '450000': '广西壮族自治区',
                 '460000': '海南省',
                 '500000': '重庆市',
                 '510000': '四川省',
                 '520000': '贵州省',
                 '530000': '云南省',
                 '540000': '西藏自治区',
                 '610000': '陕西省',
                 '620000': '甘肃省',
                 '630000': '青海省',
                 '640000': '宁夏回族自治区',
                 '650000': '新疆维吾尔自治区'
                 }
        choice = {
            'A0M0101': '普通高等学校数(所)',
            'A0M0102': '普通高等学校招生数(万人)',
            'A0M0103': '普通高等学校本科招生数(万人)',
            'A0M0104': '普通高等学校专科招生数(万人)',
            'A0M0105': '普通高等学校在校学生数(万人)',
            'A0M0106': '普通高等学校本科在校学生数(万人)',
            'A0M0107': '普通高等学校专科在校学生数(万人)',
            'A0M0108': '普通高等学校预计毕业生数(万人)',
            'A0M0109': '普通高等学校本科预计毕业生数(万人)',
            'A0M010A': '普通高等学校专科预计毕业生数(万人)',
            'A0M010B': '普通高等学校毕(结)业生数(万人)',
            'A0M010C': '通高等学校本科毕(结)业生数(万人)',
            'A0M010D': '普通高等学校专科毕(结)业生数(万人)',
            'A0M010E': '普通高等学校本专科授予学位数(万人)'

        }
        code = datanodes[0].get("wds")[1].get("valuecode")
        area = areas.get(code)

        for node in datanodes:
            valuecode = node.get("wds")[0].get("valuecode")
            name = choice.get(valuecode)
            if name not in dict1.keys():
                dict1[name] = []
            data = node.get('data').get('data')
            dict1[name].append(data)
        for key, values in dict1.items():
            yield {
                "area": area,
                "指标": key,
                '2018年': values[1],
                '2017年': values[2],
                '2016年': values[3],
                '2015年': values[4],
                '2014年': values[5],
                '2013年': values[6],
                '2012年': values[7],
                '2011年': values[8],
                '2010年': values[9]
            }
