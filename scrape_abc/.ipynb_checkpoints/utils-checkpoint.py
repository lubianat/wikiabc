


class AbcPage:
    """
    
    
    
    """
    def __init__(self, url):
        self.url = url
    
    
    def get_info(self):

        birth_date = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(1) > span")[0].text

        member_date = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(3) > span")[0].text

        nacionality = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(2) > span")[0].text

        name = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > h2 """)[0].text

        field = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.details > strong """)[0].text

        title = soup.select("head > title")[0].text

        membership = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.details """)[0].text.split(" | ")[-1].lower()

        lattes_url = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div:nth-child(5) > a """)[0].get('href')


