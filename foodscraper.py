import urllib2
import json
from bs4 import BeautifulSoup
from urlparse import urljoin
import csv

def getrestaurants():

    siteurl = "http://rocwiki.org/"
    url = "http://rocwiki.org/Restaurants/Areas"

    html = urllib2.urlopen(url).read()
    htmlparts = html.split('<span id="head-')

    ignores = [
        'Copyrights',
    ]

    restaurants = []
    for i in range(1,len(htmlparts)):
        
        htmlparts[i] = "<span id={0}".format(htmlparts[i])
        soup = BeautifulSoup(htmlparts[i])
        atags = soup.findAll('a',href=True)
        h3s = soup.findAll('h3')        

        # gross ...
        for h in h3s:
            town = h.string
            break

        for t in atags:
            atag = t

            if atag.string == None or atag.string in ignores:
                continue

            name = '{0}'.format(atag.string.strip().encode('utf-8'))

            rawhref = atag['href']
        
            if rawhref[0] == '/':
                abslink = urljoin(siteurl,rawhref)
                restaurant = {
                    'town': town,
                    'name': name,
                    'url': abslink,
                }
                restaurants.append(restaurant)    

    return restaurants

def getaddress(url):

    """ pulls address of the restaurant """

    #
    # BROKEN
    #

    replaces = [
        ['&amp','&'],
        ['&lt;','<'],
        ['&gt;','>'],
        ['&nbsp;',' '],
    ]

    html = urllib2.urlopen(url)

    soup = BeautifulSoup(html)

    divs = soup.findAll('div', {'class': 'wikitable'})

    address = str(divs[0].findAll('td')[1]).split('<a')[0]

    address = address.replace('<td>','').replace('</td>','').strip()

    for item in replaces:
        address = address.replace(item[0],item[1])

    print address

    return address

if __name__ == '__main__':

    print "Getting Restaurant List ..."

    items = getrestaurants()

    print " ... Done"

    print "Getting Restaurant Addresses ..."

    restaurants = []
    for item in items:
        print item
        #item['address'] = getaddress(item['url'])
        restaurants.append(item)

    with open('restaurants.json','w') as f:
        f.write(json.dumps(restaurants))

    with open('restaurants.csv','w') as f:
        w = csv.DictWriter(f,restaurants[0])
        w.writeheader()
        for restaurant in restaurants:
            w.writerow(restaurant)

    print " ... Done"


