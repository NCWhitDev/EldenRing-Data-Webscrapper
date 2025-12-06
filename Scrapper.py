import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# https://eldenring.wiki.fextralife.com/Builds

# Set up the WebDriver (Make sure to have the appropriate driver installed and in PATH)
driver = webdriver.Firefox()

def get_number_after_link(link):
    raw = driver.execute_script(
        "return arguments[0].nextSibling && arguments[0].nextSibling.textContent;",
        link
    )
    if raw is None:
        return None
    # clean whitespace & non-breaking spaces
    return raw.replace('\xa0', ' ').strip().strip('"')


def spell_stats(driver, href):
    print(href)
    driver.get(href)
    time.sleep(3)

    containers = driver.find_elements(
    By.XPATH,
    "//div[@class='lineleft'"
    " and .//a[@title='Elden Ring Intelligence']"
    " and .//a[@title='Elden Ring Faith']"
    " and .//a[@title='Elden Ring Arcane']]"
    )
 
    try:
        for div in containers:
        # 2. Find the three specific links inside this div
            try:
                int_link   = div.find_element(By.XPATH, ".//a[@title='Elden Ring Intelligence']")
                intelligence = get_number_after_link(int_link)
                intellect = int(intelligence)
            except:
                intellect = 0

            try:
                faith_link = div.find_element(By.XPATH, ".//a[@title='Elden Ring Faith']")
                faith        = get_number_after_link(faith_link)
                fa = int(faith)
            except:
                fa = 0
            
            try:
                arc_link   = div.find_element(By.XPATH, ".//a[@title='Elden Ring Arcane']")
                arcane       = get_number_after_link(arc_link)
                arc = int(arcane)
            except:
                arc = 0
            
        # 'Required Intelligence': driver.find_element(By.XPATH, ReqI)
        # 'Required Faith': driver.find_element(By.XPATH, ReqF)
        # 'Required Arcane': driver.find_element(By.XPATH, ReqA)
        total = intellect + arc + fa
        Spellinfo = {
            "Name": driver.find_element(By.TAG_NAME, 'h2').text,
            'TotalReq': total,
            'Required Intelligence': intellect,
            'Required Faith': fa,
            'Required Arcane': arc,
        }
        # Write to JSON File
        file_path = "spells.json"
        json_line = json.dumps(Spellinfo)
        with open(file_path, 'a') as fp:
            fp.write(json_line + '\n')

    except:
        return

def weapon_stats(driver, href):
    driver.get(href)
    time.sleep(3)
    # Weapon stats
    Name = 0
    physical = 0
    magic = 0
    fire = 0
    lighting = 0
    holy = 0
    crit = 0
    # Weapon requirements
    strength = 0
    dexterity = 0
    intellect = 0
    faith = 0
    arcane = 0
    weight = 0

    Weaponsinfo = {
        'Title': Name,
        'Physical_DMG': physical,
        'Magic_DMG': magic,
        'Fire_DMG': fire,
        'Lighting_DMG': lighting,
        'Holy_DMG': holy,
        'Crit': crit,
        'Strength': strength,
        'Dexterity': dexterity,
        'Intellect': intellect,
        'Faith': faith,
        'Arcane': arcane,
        'Weight': weight
    }
    # Write to JSON File
    file_path = "weapons.json"
    json_line = json.dumps(Weaponsinfo)
    with open(file_path, 'a') as fp:
        fp.write(json_line + '\n')


def bosses(driver, href):
    driver.get(href)
    time.sleep(3)
    # Implment Boss stats
    Health = '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[1]/div/table/tbody/tr[5]/td[2]'
    StrongAgainst = '//*[@id="infobox"]/div/table/tbody/tr[6]/td[1]/div' # May need to change
    WeakAgainst = '//*[@id="infobox"]/div/table/tbody/tr[6]/td[2]/div' # May need to change
    Defense = '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/ul[2]/li[2]/span/strong' # Defense (Level of boss)

    Bossinfo = {
        "BossHealth" : driver.find_element(By.XPATH, Health).text,
        "Strength" : driver.find_element(By.XPATH, StrongAgainst).text,
        "Weakness" : driver.find_element(By.XPATH, WeakAgainst).text,
        "Resistance" : driver.find_element(By.XPATH, Defense).text,
    }
    # Write to JSON File
    file_path = "Bosses.json"
    json_line = json.dumps(Bossinfo)
    with open(file_path, 'a') as fp:
        fp.write(json_line + '\n')

def main():
    # 1. We need to get spells info from the Elden Ring Wiki
    URL = 'https://eldenring.wiki.fextralife.com/Spells'
    driver.get(URL)
    time.sleep(3)     
    spells = driver.find_elements(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[5]//a[@class='wiki_link wiki_tooltip']")
    print(spells)
    print(len(spells))
    spells = [x.get_attribute('href') for x in spells]
    print(spells)

    for spell_link in spells:
        if spell_link == 'https://eldenring.wiki.fextralife.com/Crystal+Barrage': continue # IDK spell broke
        if spell_link == "https://eldenring.wiki.fextralife.com/Scholar's+Armament": continue
        if spell_link == "https://eldenring.wiki.fextralife.com/Scholar's+Shield": continue
        spell_stats(driver, spell_link)
    
    # # 2. We need to get weapons info from the Elden Ring Wiki
    # URL = 'https://eldenring.wiki.fextralife.com/Weapons+Comparison+Tables'
    # driver.get(URL)
    # time.sleep(3)  # Wait for the page to load
    # # wiki_table sortable searchable wiki-static-text
    # weapon_index = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[3]/div[2]/table//a[@class='wiki_link wiki_tooltip']") # Finds all a tags at xpath
    # weapons = [elem.get_attribute('href') for elem in weapon_index] # Extract href attributes
    # set(weapons)  # Remove duplicates if any
    # for weapon in weapons:
    #     weapon_stats(driver, weapon)

    # # 4. Get Bosses, strengths and weaknesses. If they are higher end bosses we should have a lower success by default.
    # URL = 'https://eldenring.wiki.fextralife.com/Bosses'
    # driver.get(URL)
    # time.sleep(3) # Wait for the page to load
    # Boss_index = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div[1]/div[5]")
    # Bosses = [elem.get_attribute('href') for elem in Boss_index]
    # set(Bosses) # # Remove duplicates if any
    # for boss in Bosses:
    #     bosses(driver, boss)

    driver.quit() # Close the browser

    # JSon to CSV

if __name__ == "__main__":
    main()