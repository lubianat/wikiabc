import pandas as pd 
from scrape_abc import utils

url = "http://www.abc.org.br/membro/renato-de-azevedo-tribuzy/"

abc_page = utils.AbcPage(url)
abc_page.get_info()
abc_page.write_wikipage(onmc=True, woman=False) 
    
name = "Renato de Azevedo Tribuzy"
    
print(f"Creating page for {name}")

print(f"https://author-disambiguator.toolforge.org/names_oauth.php?precise=0&name={name.replace(' ', '+')}&doit=Look+for+author&limit=500&filter=")

print(f"https://pt.wikipedia.org/wiki/{name.replace(' ', '_')}")

print(f"https://www.google.com/search?q={name.replace(' ', '_')}")

qid = input("Enter Wikidata QID for " + name + ": " )
abc_page.print_qs(qid, woman=False)
print(f'{qid}|P166|Q3132815|P580|+1994-04-08T00:00:00Z/11|S854|"https://web.archive.org/web/20070213055821/http://www.mct.gov.br/index.php/content/view/11199.html?area=allAreas&categoria=allMembros"')


import pywikibot

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, "Q102225626")

data = [{'site':'ptwiki', 'title': name}]

item.setSitelinks(data)
