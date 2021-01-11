import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class AbcPage:
    """
    Loads and process info for a member of the brazilian academy of sciences.
    
    
    """
    def __init__(self, url):
        """Inits AbcPage with member URL."""
        self.url = url
    
    
    def get_info(self):
        """Scrapes the Academia Brasileira de Ciencias website for info."""
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        box_pointer = "#page > div.page-content > \
                                    div > div > div > div:nth-child(1) > \
                                    div.col-lg-6.profile-page >  div > "

        self.birth_date = soup.select(box_pointer + " \
                                    div.excerpt > div:nth-child(1) > span")[0].text

        self.member_date = soup.select(box_pointer + " \
                                    div.excerpt > div:nth-child(3) > span")[0].text

        self.nacionality = soup.select(box_pointer + " \
                                    div.excerpt > div:nth-child(2) > span")[0].text

        self.name = soup.select(box_pointer + "h2 ")[0].text

        self.field = soup.select(box_pointer + " \
                                    div.details > strong """)[0].text

        self.title = soup.select("head > title")[0].text

        self.membership = soup.select(box_pointer + "\
                                    div.details """)[0].text.split(" | ")[-1].lower()
        try:
            self.lattes_url = soup.select(box_pointer + "\
                                    div:nth-child(5) > a """)[0].get('href')
        except:
            print("No lattes URL.")


    def print_qs(self, wikidata_id, woman=True):
        birth_object = datetime.strptime(self.birth_date,"%d/%m/%Y")
        birth_date_wiki = birth_object.strftime("+%Y-%m-%dT00:00:00Z/11")

        member_object = datetime.strptime(self.member_date,"%d/%m/%Y")
        member_date_wiki = member_object.strftime("+%Y-%m-%dT00:00:00Z/11")

        print(f'{wikidata_id}|Lpt|"{self.name}"')
        print(f'{wikidata_id}|Len|"{self.name}"')
        print(f'{wikidata_id}|Les|"{self.name}"')
        print(f'{wikidata_id}|Lde|"{self.name}"')
        print(f'{wikidata_id}|Lfr|"{self.name}"')

        print(f'{wikidata_id}|P463|Q2497232|P580|{member_date_wiki}|S854|"{self.url}"')
        print(f'{wikidata_id}|P569|{birth_date_wiki}|S854|"{self.url}"')
        if hasattr(self, "lattes_url"):
            print(f'{wikidata_id}|P1007|"{self.lattes_url.split("/")[-1]}"|S854|"{self.url}"')

        if self.nacionality == "Brasileira":
            print(f'{wikidata_id}|P27|Q155|S854|"{self.url}"')
        
        if woman == True:
            print(f'{wikidata_id}|P21|Q6581072|S854|"{self.url}"')       
        else:
            print(f'{wikidata_id}|P21|Q6581097|S854|"{self.url}"')
            print(f'{wikidata_id}|Dpt|"pesquisador"')
            print(f'{wikidata_id}|Den|"researcher"')

    

    def write_wikipage(self, filepath="wikipage", onmc="", woman=True):
        """
            onmc: String of the class in the National Order of Scientific Merit. 
            Can be either "great-cross", "comendador" or "".
        """

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        
        if hasattr(self, "lattes_url"):       
            link_lattes = f"* [{self.lattes_url} Currículo na Plataforma Lattes]"
        else:
            link_lattes = ""
        

        if onmc == "great-cross":
            onmc_complement = "com a Grã-Cruz da"
            onmc_categoria = "[[Categoria:Grã-Cruz_da_Ordem_Nacional_do_Mérito_Científico]]"
            onmc = get_onmctext(woman, onmc_complement)
            onmc_see_also= """
== Veja também ==
* [[Lista de agraciados com a Grã-Cruz da Ordem Nacional do Mérito Científico]]
            """
        elif onmc == "comendador": 
            onmc_complement = "com a comenda da"
            onmc_categoria = "[[Categoria:Ordem_Nacional_do_Mérito_Científico]]"
            onmc = get_onmctext(woman, onmc_complement)
            onmc_see_also= """
== Veja também ==
* [[Lista de agraciados na Ordem Nacional do Mérito Científico - Comendador]]
            """

        else:
            onmc_complement = ""
            onmc = ""
            onmc_categoria = ""
            onmc_see_also= ""

        if woman == True:
            desinence = "a";
            adding_desinence = "a"
        else:
            desinence = "o"
            adding_desinence = ""
        



        wiki_page = """{{Info/Biografia/Wikidata}}

""" + f"""'''{self.name}''' ({self.birth_date}) é um{adding_desinence} pesquisador{adding_desinence} brasileir{desinence}, {self.membership} da [[Academia Brasileira de Ciências]] na área de {self.field} desde {self.member_date}.""" \
+ "<ref>{{Citar web |url=" + self.url + f"/ |titulo={self.title} |acessodata={d1} |lingua=pt-BR" + "}}</ref>" + f"""

{onmc}

{onmc_see_also}
== Links externos ==
* [{self.url}/ Página na Academia Brasileira de Ciências]
{link_lattes}
""" + """
{{Referencias}}

{{Esboço-cientista}}{{Controle de autoridade}}
[[Categoria:Membros da Academia Brasileira de Ciências]]
""" + onmc_categoria 

             
                
                
        with open(filepath, "w+") as f:
            f.write(wiki_page)
        
        print(wiki_page)


        print("/n")


def get_onmctext(woman,onmc_complement):
    if woman == True:
        desinence = "a";
    if woman == False:
        desinence = "o"
        
    return(f"""Foi condecorad{desinence} {onmc_complement} [[Ordem Nacional do Mérito Científico]]. <ref>"""+"""{{Citar web |url=https://canalciencia.ibict.br/noticias/item/237-ordem-nacional-do-merito-cientifico |titulo=Ordem Nacional do Mérito Científico |acessodata=2021-01-10}}</ref>   
    """)
    
         
                
                
                

def get_members(url):
    """
    Extract members from an ABC page.
    
    Args:
        An ABC search result URL. 
        
    Returns:

      members: A dict of ABC members and their URLs in ABC

    """
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'lxml')
    link_urls = [a.get('href') for a in soup.find_all('a', href=True)]
    
    member_urls = []
    member_urls = [link for link in link_urls if "http://www.abc.org.br/membro/" in link]
    
    headers = [a.text for a in  soup.find_all('h2')]
    members = {}
    
    for i, value in enumerate(headers):
        members[value] = member_urls[i]
    
    
    return(members)

def get_all_woman_at_abc():
    all_members = {}
    for i in range(1,13):
        print(i)
        url = f'http://www.abc.org.br/membros/page/{str(i)}/?busca_membro_nome&busca_membro_genero=Feminino&busca_membro_datanascimento_mes&busca_membro_datanascimento_ano&busca_membro_areapesquisa&busca_membro_membrodesde_mes&busca_membro_membrodesde_ano&busca_membro_nacionalidade&busca_membro_regiao&busca_membro_categoria=titular' 
        members = get_members(url)
        all_members.update(members)
    
    return(all_members)
    

    
def get_all_men_at_abc():
    all_members = {}
    for i in range(1,59):
        print(i)
        url = f'http://www.abc.org.br/membros/page/{str(i)}/?busca_membro_nome&busca_membro_genero=Masculino&busca_membro_datanascimento_mes&busca_membro_datanascimento_ano&busca_membro_areapesquisa&busca_membro_membrodesde_mes&busca_membro_membrodesde_ano&busca_membro_nacionalidade&busca_membro_regiao&busca_membro_categoria=titular' 
        members = get_members(url)
        all_members.update(members)
    
    return(all_members)  


def save_all_men_at_abc(file="men_at_ABC_30_11_2020.csv"):

    all_members = get_all_men_at_abc()
    s = pd.Series(all_members, name = "url")

    s.index.name = "name"

    members_df = s.reset_index()

    members_df.to_csv(file)
    

def save_all_women_at_abc(file="women_at_ABC_25_11_2020.csv"):

    all_members = get_all_woman_at_abc()
    s = pd.Series(all_members, name = "url")

    s.index.name = "name"

    members_df = s.reset_index()

    members_df.to_csv(file)


def save_all_onmc_awards(file="people_at_onmc_in_2007_25_11_2020.csv"):
    driver = webdriver.Firefox()
    ordem_url = "https://web.archive.org/web/20070213055821/http://www.mct.gov.br/index.php/content/view/11199.html?area=allAreas&categoria=allMembros"

    driver.get(ordem_url)
    table_selector = "#layerConteudo > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2)"
    elem = driver.find_element_by_css_selector(table_selector)
    soup = BeautifulSoup(elem.get_attribute('innerHTML'))
    links = soup.find_all('a')

    driver.close()
    
    ordem_nacional_member_urls = {}

    for link in links:
        ordem_nacional_member_urls[link.text] = link["href"]
        
    s = pd.Series(ordem_nacional_member_urls, name = "url")

    s.index.name = "name"

    members_onmc_df = s.reset_index()

    members_onmc_df.to_csv(file)