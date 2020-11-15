
from datetime import date, datetime
import requests
from bs4 import BeautifulSoup

class AbcPage:
    """
    Loads and process info for a member of the brazilian academy of sciences.
    
    
    """
    def __init__(self, url):
        self.url = url
    
    
    def get_info(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        self.birth_date = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(1) > span")[0].text

        self.member_date = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(3) > span")[0].text

        self.nacionality = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.excerpt > div:nth-child(2) > span")[0].text

        self.name = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > h2 """)[0].text

        self.field = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.details > strong """)[0].text

        self.title = soup.select("head > title")[0].text

        self.membership = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div.details """)[0].text.split(" | ")[-1].lower()

        self.lattes_url = soup.select("#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page > div > \
                                    div:nth-child(5) > a """)[0].get('href')


    def print_qs(self, wikidata_id):
        birth_object = datetime.strptime(self.birth_date,"%d/%m/%Y")
        birth_date_wiki = birth_object.strftime("+%Y-%m-%dT00:00:00Z/11")

        member_object = datetime.strptime(self.member_date,"%d/%m/%Y")
        member_date_wiki = member_object.strftime("+%Y-%m-%dT00:00:00Z/11")

        print(f'{wikidata_id}|P463|Q2497232|P580|{member_date_wiki}|S854|"{self.url}"')
        print(f'{wikidata_id}|P569|{birth_date_wiki}|S854|"{self.url}"')
        print(f'{wikidata_id}|P1007|"{self.lattes_url.split("/")[-1]}"|S854|"{self.url}"')

        if self.nacionality == "Brasileira":
            print(f'{wikidata_id}|P27|Q155|S854|"{self.url}"')
    
    def write_wikipage(self, filepath="wikipage"):

            today = date.today()
            d1 = today.strftime("%Y-%m-%d")

            wiki_page = """{{Info/Biografia/Wikidata}}

""" + f"""{self.name} ({self.birth_date}) é uma pesquisadora brasileira, {self.membership} da [[Academia Brasileira de Ciências]] na área de {self.field} desde {self.member_date}.""" \
+ "<ref>{{Citar web |url=" + self.url + f"/ |titulo={self.title} |acessodata={d1} |lingua=pt-BR" + "}}</ref>" + f"""


== Links externos ==

* [{self.url}/ Página na Academia Brasileira de Ciências]
* [{self.lattes_url} Currículo na Plataforma Lattes]

""" + """

{{Referencias}}

{{Esboço-cientista}}{{Controle de autoridade}}
[[Categoria:Membros da Academia Brasileira de Ciências]]

            """

            with open(filepath, "w+") as f:
                f.write(wiki_page)





