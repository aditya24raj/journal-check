import json
import re
from tabnanny import check
import urllib.request
from bs4 import BeautifulSoup
from datetime import date


class Journal:
    def __init__(self):
        self.month_regex = {
            1 : "[jJ][aA][nN]",
            2 : "[fF][eE][bB]",
            3 : "[mM][aA][rR]",
            4 : "[aA][pP][rR]",
            5 : "[mM][aA][yY]",
            6 : "[jJ][uU][nN]",
            7 : "[jJ][uU][lL]",
            8 : "[aA][uU][gG]",
            9 : "[sS][eE][pP]",
            10 : "[oO][cC][tT]",
            11 : "[nN][oO][vV]",
            12 : "[dD][eE][cC]"
        }

        with open('journals.json') as journal_JSON:
            self.journals = json.load(journal_JSON)
    
    def __download_HTML__(self, journal_URL):
        with urllib.request.urlopen(journal_URL) as url_handle:
            return url_handle.read()
    
    def __get_td_tags__(self, journal_URL):
        journal_HTML = self.__download_HTML__(journal_URL)
        soup = BeautifulSoup(journal_HTML, 'html.parser')
        print(soup.findAll("td", string=re.compile("^.*18.(.*8|.*[aA][uU][gG])(.*2022)")))
    
    def generate_date_regex(self, check_for_date=None):
        if not check_for_date:
            check_for_date = date.today()
        
        return re.compile(
          f"^.*{check_for_date.day}.(.*{check_for_date.month}|.*{self.month_regex[check_for_date.month]})(.*{check_for_date.year})"
        )

    def check(self):
        for i in self.journals:
            print(i, end=" ")
            self.__get_td_tags__(self.journals[i]);

if __name__ == "__main__":
    my_journal = Journal()
    my_journal.check();