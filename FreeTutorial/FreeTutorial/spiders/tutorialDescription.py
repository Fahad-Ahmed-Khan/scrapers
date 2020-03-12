# -*- coding: utf-8 -*-
import scrapy
import MySQLdb
import urllib.request

class TutorialdescriptionSpider(scrapy.Spider):
    name = 'tutorialDescription'
    allowed_domains = ['freecoursesite.us']
    start_urls = ['https://freecoursesite.us/']
    index = 0;
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', '', 
                                    'tutorialdb', charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        
    def parse(self, response):
        
        print("----------( Scraper Started )------------")
        for course in response.css('div.row.herald-posts.row-eq-height article'):
            courseUrl = course.css('div.herald-post-thumbnail.herald-format-icon-middle > a::attr(href)').extract_first()
            yield scrapy.Request(url=courseUrl, callback=self.GetData)
        next_url = response.css('a.next.page-numbers::attr(href)').extract_first()
        yield scrapy.Request(url=next_url, callback=self.parse)
    def GetData(self, response):
        print("-----( Inside Page )-----")
        Title = response.css('h1.entry-title::text').extract_first()        
        SubTitle = response.css('div.entry-content.herald-entry-content h3::text').extract_first()
        ImageUrl = response.css('div.herald-post-thumbnail.herald-post-thumbnail-single > span > img::attr(src)').extract_first()
        Description = response.css('div.description  p').extract();
        Learning = response.css('ul.what-you-get__items').extract_first()
        Requirements = response.css('ul.requirements__list').extract_first()
        Audience = response.css('ul.audience__list').extract_first()
        Size = response.css('a.mks_button::text').extract_first()

        download_url = response.css('a.mks_button::attr(href)').extract_first()
        
        
        if Learning is None:
            Learning = "To much to learn in this course."
            
        if Requirements is None:
            Requirements = "Computer/Laptop"
        
        if Audience is None:
            Audience = "Anyone can join, because its free :)"

        print(Title)

        print("++++++++++++++++++++++++("+str(self.index)+")+++++++++++++++++++++++++++++")
        self.index = self.index + 1
        fullname = "courseImages/"+str(self.index)+".jpg"
        urllib.request.urlretrieve(ImageUrl,fullname)
        try:
            self.cursor.execute("""INSERT INTO Courses(title, sub_title, learning, Requirements, 
                                    Audience, description, size, download_url, img_url)  
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                       (str(Title), 
                        str(SubTitle), 
                        str(Learning), 
                        str(Requirements), 
                        str(Audience), 
                        str(Description),
                        str(Size), 
                        str(download_url),
                        str(self.index)))            
            self.conn.commit()

        except MySQLdb.Error as e:
                print ("Error %d: %s" % (e.args[0], e.args[1]))
          