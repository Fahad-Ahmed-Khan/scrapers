# -*- coding: utf-8 -*-
import scrapy
import MySQLdb

class TutorialSpider(scrapy.Spider):
    name = 'tutorial'
    allowed_domains = ['freetutorialsus.com']
    start_urls = ['https://www.freetutorialsus.com/']

    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '', 
                                    'tutorialsdb', charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        
    def parse(self, response):
        for course in response.css("article.post-box"):
            Image = course.css("div.post-img.small-post-img > a > img::attr(src)").extract_first()
            Title = course.css("h2.entry-title.post-title a::text").extract_first()
            Description = course.css("div.entry-content.post-excerpt::text").extract_first()
            DescriptionUrl = course.css("h2.entry-title.post-title a::attr(href)").extract_first()
            Category = course.css("div.post-img.small-post-img > span > a::text").extract_first()
            print("==========================================")
            print(Title)
            print(Image)
            print(Description)
            print(DescriptionUrl)
            print(Category)
            print("-------------------------------------------")
            try:
                self.cursor.execute("""INSERT INTO Courses (Title, ImageUrl, ShortDescription, DescriptionUrl, Category)  
                        VALUES (%s, %s, %s, %s, %s)""", 
                       (Title.encode('utf-8'), 
                        Image.encode('utf-8'), 
                        Description.encode('utf-8'), 
                        DescriptionUrl.encode('utf-8'), 
                        Category.encode('utf-8')))            
                self.conn.commit()            
            except MySQLdb.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
            
            
        NextPage = response.css("a.next.page-numbers::attr(href)").extract_first()
        yield scrapy.Request(url=NextPage, callback=self.parse)