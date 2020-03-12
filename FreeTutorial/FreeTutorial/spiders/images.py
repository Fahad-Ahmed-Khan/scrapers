# -*- coding: utf-8 -*-
import scrapy
import MySQLdb
import urllib.request

class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['freetutorialsus.com']
    start_urls = ['http://freetutorialsus.com/']

    def parse(self, response):
        conn = MySQLdb.connect('localhost', 'root', '', 
                                    'tutorialsdb', charset="utf8",
                                    use_unicode=True)
        cursor = conn.cursor()
        
            
            
        cursor.execute("Select * from courses order by CID")
        courses = cursor.fetchall()
    
        for course in courses[1:10]:
            fullname = str(course[0])+".jpg"
            urllib.request.urlretrieve(course[2].decode('utf8'),fullname)     
    
        pass
