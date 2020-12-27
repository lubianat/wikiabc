import pandas as pd 
from scrape_abc import utils

man_abc_onc_df = pd.read_csv("man_to_create.csv")

for i, row in man_abc_onc_df.iterrows():
    url = row["url_x"]
    name = row["name"]
    abc_page = utils.AbcPage(url)
    abc_page.get_info()
    abc_page.write_wikipage(onmc=True, woman=False) 
    
    break
    
    
print(f"Creating page for {name}")

print(f"https://author-disambiguator.toolforge.org/names_oauth.php?precise=0&name={name.replace(' ', '+')}&doit=Look+for+author&limit=500&filter=")

print(f"https://pt.wikipedia.org/wiki/{name.replace(' ', '_')}")

print(f'https://www.google.com/search?q="{name.replace(' ', '_')}"')

qid = input("Enter Wikidata QID for " + name + ": " )
abc_page.print_qs(qid, woman=False)
print(f'{qid}|P166|Q3132815|P580|+1994-04-08T00:00:00Z/11|S854|"https://web.archive.org/web/20070213055821/http://www.mct.gov.br/index.php/content/view/11199.html?area=allAreas&categoria=allMembros"')

man_abc_onc_df = man_abc_onc_df.reset_index(drop=True).drop(0)
man_abc_onc_df.head()
man_abc_onc_df.to_csv("man_to_create.csv")