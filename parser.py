from bs4 import BeautifulSoup

class AmazonParser:
    def __init__(self, source):
        self.source = source
        self.soup = BeautifulSoup(self.source, 'lxml')

    def update_source(self, source):
        """Updates HTML source and soup"""
        self.source = source
        self.soup = BeautifulSoup(self.source, 'lxml')

    def get_product_links(self) -> list:
        """Extracts product links from a search result page and returns a list of links."""
        links = []
        image_elements = self.soup.find_all("span", {"data-component-type":"s-product-image"})
        for elem in image_elements:
            link = elem.find("a")['href']
            links.append(link)
        return links

    def get_product_info(self) -> dict:
        """Extracts product info from a product page."""
        title = self.soup.find("span", {"id":"productTitle"}).text.strip()

        price_symbol = self.soup.find("span", {"class":"a-price-symbol"}).text
        price = self.soup.find("span", {"class":"a-price-whole"}).text.strip()

        # customer ratings is present in the format of 3 out of 5 starts \n total_reviews,
        # for now we don't want the number of total_reviews, so we split it.        
        customer_rating = self.soup.find("div", {"id":"averageCustomerReviews"})        
        if customer_rating == None:
            customer_rating == ""
        else:
            customer_rating = customer_rating.text.strip().split("\n")[0].strip()

        # Image list for product is present as a key value pair in data-a-dynamic-image attribute
        # We will get that attribute data and evaluate it to make it a python dict
        # then we create a list from the keys of that dict, the dict contains image url and their resolution
        # we just need the image url which is present in key. We will only select 1st image.
        img_li = self.soup.find("li", {"class":"image"})
        disp_img_attr_str = img_li.find("img")['data-a-dynamic-image']
        disp_img_attr = eval(disp_img_attr_str)
        disp_img_list = list(disp_img_attr.keys())
        product_image_url = disp_img_list[0]

        info = {
            "title":title,
            "currency":price_symbol,
            "price":price,
            "customer_ratings":customer_rating,
            "image_url":product_image_url
        }
        return info
