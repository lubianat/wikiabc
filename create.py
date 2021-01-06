import pandas as pd 
from scrape_abc import utils
import pywikibot
from datetime import date, datetime

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

print(f"https://www.google.com/search?q={name.replace(' ', '_')}")

qid = input("Enter Wikidata QID for " + name + ": " )
abc_page.print_qs(qid, woman=False)


####### Pywikibot integration #######

print("===== Starting pywikibot =====")

def convert_date_to_pywiki(date):
    datetime_object = datetime.strptime(date,"%d/%m/%Y")

    y = datetime_object.strftime("%Y")
    m = datetime_object.strftime("%m")
    d = datetime_object.strftime("%d")
    py_date = pywikibot.WbTime(year=int(y), month=int(m), day=int(d))
    return py_date

woman = False # Already added the women to Wiki

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
item = pywikibot.ItemPage(repo, qid)


data = [{'site':'ptwiki', 'title': name}]
item.setSitelinks(data)

data = {"labels": {"en": abc_page.name, "de": abc_page.name, "pt": abc_page.name, "fr": abc_page.name }}
item.editEntity(data, summary=u'Edited item: set labels, descriptions, aliases')

ref_url = pywikibot.Claim(repo, u'P854')
ref_url.setTarget(abc_page.url)


print("===== Adding birth date =====")

try:
    dateclaim = pywikibot.Claim(repo, u'P569')
    dateclaim.setTarget(convert_date_to_pywiki(abc_page.birth_date))
    item.addClaim(dateclaim, summary=u'Adding dateOfBirth')

    dateclaim.addSources([ref_url], summary=u'Adding source')
except Exception as e:
  print(e)
finally:
    pass


print("===== Adding membership of ABC =====")
ref_url = pywikibot.Claim(repo, u'P854')
ref_url.setTarget(abc_page.url)
try:
    claim_member = pywikibot.Claim(repo, u'P463')
    target = pywikibot.ItemPage(repo, u"Q2497232") # ABC
    claim_member.setTarget(target) #Set the target value in the local object.
    item.addClaim(claim_member, summary=u'Adding claim') 

    qualifier = pywikibot.Claim(repo, u'P580')
    qualifier.setTarget(convert_date_to_pywiki(abc_page.member_date))
    claim_member.addQualifier(qualifier, summary=u'Adding a qualifier.')

    claim_member.addSources([ref_url], summary=u'Adding source')
except Exception as e:
  print(e)
finally:
    pass


print("===== Adding National Order of Scientific Merit award =====")
try:
    claim_order = pywikibot.Claim(repo, u'P166')
    target = pywikibot.ItemPage(repo, u"Q3132815") # ABC
    claim_order.setTarget(target) #Set the target value in the local object.
    item.addClaim(claim_order, summary=u'Adding claim')     
except Exception as e:
  print(e)
finally:
    pass


print("===== Adding gender =====")
ref_url = pywikibot.Claim(repo, u'P854')
ref_url.setTarget(abc_page.url)
try:
    gender_claim = pywikibot.Claim(repo, u'P21')

    if woman == True:
        gender_claim.setTarget(pywikibot.ItemPage(repo, u"Q6581072"))

    else:
        gender_claim.setTarget(pywikibot.ItemPage(repo, u"Q6581097"))

    item.addClaim(gender_claim, summary=u'Adding gender')
    gender_claim.addSources([ref_url], summary=u'Adding source')
except Exception as e:
  print(e)
finally:
    pass


print("===== Adding Lattes URL =====")
ref_url = pywikibot.Claim(repo, u'P854')
ref_url.setTarget(abc_page.url)
try:
    if hasattr(abc_page, "lattes_url"):
        lattes_claim = pywikibot.Claim(repo, u'P1007')
        lattes_claim.setTarget(f"{abc_page.lattes_url.split('/')[-1]}")
        item.addClaim(lattes_claim, summary=u'Adding Lattes URL')
        lattes_claim.addSources([ref_url], summary=u'Adding source')
except Exception as e:
  print(e)
finally:
    pass



print("===== Adding nationality =====")
ref_url = pywikibot.Claim(repo, u'P854')
ref_url.setTarget(abc_page.url)
try:
    if abc_page.nacionality == "Brasileira":
        nationality_claim = pywikibot.Claim(repo, u'P27')
        brazil = pywikibot.ItemPage(repo, u"Q155") # ABC
        nationality_claim.setTarget(brazil)
        item.addClaim(nationality_claim, summary=u'Adding nationality')
        nationality_claim.addSources([ref_url], summary=u'Adding source')
except Exception as e:
  print(e)
finally:
    pass

print("===== Done =====")

man_abc_onc_df = man_abc_onc_df.reset_index(drop=True).drop(0)
man_abc_onc_df.head()
man_abc_onc_df.to_csv("man_to_create.csv")