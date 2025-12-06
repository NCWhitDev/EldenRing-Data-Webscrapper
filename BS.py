import json
import time
import requests
from protego import Protego
from bs4 import BeautifulSoup

# one line for constant global headers (fix its value)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0'
HEADERS = {'user-agent': user_agent}

def robot_parser(domain_name):
    robots = requests.get(domain_name + '/robots.txt', headers=HEADERS)
    rp = Protego.parse(robots.text)
    return rp

def helper_scrape(url, crawl_delay):
    # Will download a page, scrape it for data and return.
    response = requests.get(url, headers=HEADERS)
    time.sleep(crawl_delay)
    soup = BeautifulSoup(response.text, 'html.parser')
    attk = soup.find('a', title="Elden Ring Physical Damage").next_sibling.strip()
    crit = soup.find('a', string='Crit').parent.next_sibling.strip()
    magic = soup.find('a', string='Mag').next_sibling.text.strip()
    fire = soup.find('a', string='Fire').parent.next_sibling.text.strip()
    lighting = soup.find('a', string='Ligt').parent.next_sibling.text.strip()
    holy = soup.find('a', title="Elden Ring Holy Damage").parent.next_sibling.text.strip()
    weight = soup.find('a', title='Elden Ring Weight').find_next('span').text
    # try:
    #     strength = soup.find_all('Elden Ring Strength')[0].next_sibling.text.strip()
    #     if(strength == '0'):
    #         strength = soup.find_all('Elden Ring Strength')[1].next_sibling.text.strip()
    #     if(strength.isalpha() == True):
    #        strength = soup.find_all('Elden Ring Strength')[2].next_sibling.text.strip()
    # except:
    #     strength = 0

    # try:
    #     dex = soup.find_all('Elden Ring Dexterity')[0].next_sibling.text.strip()
    #     if(dex == '0'):
    #         dex = soup.find_all('Elden Ring Dexterity')[1].next_sibling.text.strip()
    #     if(dex.isalpha() == True):
    #        dex = soup.find_all('Elden Ring Dexterity')[2].next_sibling.text.strip()
    # except:
    #     dex = 0

    # try:
    #     faith = soup.find_all('Elden Ring Faith')[0].next_sibling.text.strip()
    #     if(faith == '0'):
    #         faith = soup.find_all('Elden Ring Faith')[1].next_sibling.text.strip()
    #     if(faith.isalpha() == True):
    #        faith = soup.find_all('Elden Ring Faith')[2].next_sibling.text.strip()
    # except:
    #     faith = 0
    
    # try:
    #     intellect = soup.find_all('Elden Ring Intellect')[0].next_sibling.text.strip()
    #     if(intellect == '0'):
    #         intellect = soup.find_all('Elden Ring Intellect')[1].next_sibling.text.strip()
    #     if(intellect.isalpha() == True):
    #        intellect = soup.find_all('Elden Ring Intellect')[2].next_sibling.text.strip()
    # except:
    #     intellect = 0
        
    # try:
    #     arc = soup.find_all('Elden Ring Arcane')[0].next_sibling.text.strip()
    #     if(arc == '0'):
    #         arc = soup.find_all('Elden Ring Arcane')[1].next_sibling.text.strip()
    #     if(arc.isalpha() == True):
    #        arc = soup.find_all('Elden Ring Arcane')[2].next_sibling.text.strip()
    # except:
    #     arc = 0


    dictionary = {
        'Title': soup.find('title').text.strip(),
        'AttDMG': attk,
        'Crit': crit,
        'Magic_DMG': magic,
        'Fire_DMG': fire,
        'Lighting_DMG' : lighting,
        'Holy_DMG': holy,
        'Weight': weight,
        # 'ReqStrength': strength,
        # 'ReqDexterity': dex,
        # 'ReqFaith': faith,
        # 'ReqArcane': arc,
        # 'ReqIntllect': intellect
    }

    json_line = json.dumps(dictionary)
    file_path = 'weapons.json'
    with open(file_path, 'a') as fp:
        fp.write(json_line + '\n')


# =========================================================
def main(domain_link):
    # download url and get all links that we want to request + scrape from.
    links = []
    index_link = domain_link + '/Weapons'
    robot = robot_parser(domain_link)
    crawl_delay = robot.crawl_delay('*') or 0
    response = requests.get(index_link, headers=HEADERS)
    time.sleep(crawl_delay)
    if robot.can_fetch(index_link, '*'):
        soup = BeautifulSoup(response.text, 'html.parser')

        i = soup.find_all('a', class_ = 'wiki_link wiki_tooltip')
        for each in i:
            links.append(each['href'])

        # No dups
        links = set(links)
        print(links)
        print(len(links))

        counts = 0
        for each in links:
            # DONT GET https://eldenring.wiki.fextralife.com/Upgrades <1-409>
            if each == '/Upgrades': continue

            item = domain_link + each
            if robot.can_fetch(item, '*'):
                try:
                    if "'" in each: pass
                    helper_scrape(item,crawl_delay)
                    print(item)
                    counts += 1
                except:
                    print("\n This item did not work " + item + "\n")
                    continue
        print(counts)

if __name__ == '__main__':
    main('https://eldenring.wiki.fextralife.com')
    # Sources:
    # https://github.com/scrapy/protego
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#Tag