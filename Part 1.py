import requests, re
from time import sleep
from bs4 import BeautifulSoup
#the function to remove links within parentheses, but keep the other text within parentheses
#this is necessary because parentheses can exist within links
#you can use regular expressions for that, but the problem arises with nested parentheses
def remove_nested_parentheses(s):
    ret = ''
    skip = 0
    open_pars = []
    close_pars = []
    for i in range(len(s)):
        if s[i] == '(':
            skip += 1
            open_pars.append(i)
        elif s[i] == ')' and skip > 0:
            skip -= 1
            close_pars.append(i)
        if skip == 0:
            if len(open_pars) != 0 and len(close_pars) != 0:
                first_open_par = min(open_pars)
                last_close_par = max(close_pars)
                if s.find("href", first_open_par, last_close_par) == -1:
                    ret += s[first_open_par:last_close_par+1]
                else:
                    ret += s[i+1]
                open_pars.clear()
                close_pars.clear()
            else:
                ret += s[i]
    return ret

def getting_to_philosophy(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    #if achieved Philosophy -> stop
    if soup.find(id='firstHeading').text == 'Philosophy':
        return 'You achieved Philosophy'
    else:
        content = soup.find(id='mw-content-text')
        # remove internal links within article, footnotes, italics, tables
        for s in content.find_all(['span', 'small', 'sup,', 'i', 'table']): 
            s.replace_with("")     
        #remove only links within parentheses - ensures that parentheses within link remain intact
        content=BeautifulSoup(remove_nested_parentheses(str(content)))
        #content=BeautifulSoup(content)
        first_link=None

        #look at paragraphs and stop when a link is found
        for par in content.find_all('p'):
            if first_link is None:
                for link in par.find_all('a'):
                    if link.get('href').startswith('/wiki/'):
                        first_link=link.get('href')
                        break

        if first_link is None:
            return 'No way out'
        elif first_link in history:
            return 'Stuck in a loop'
        else:
            url = 'http://en.wikipedia.org' + first_link
            print(url)
            history.append(first_link)
            sleep(0.5)
            return getting_to_philosophy(url)
history=[]
url="https://en.wikipedia.org/wiki/Special:Random"
getting_to_philosophy(url)
