import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import date


class Journal:
    def __init__(self):
        self.journals = {
            "Aditya_Raj": "https://aditya24raj.github.io/journal/",
            "Ajit_N_Ogale": "https://ajit1-mrk.github.io/Ajit_journal",
            "Anmol_Saxena": "https://anmol-mrk.github.io/Journal.html",
            "Ashutosh_P_Hore": "https://ashutosh-mrk.github.io/Journal.html",
            "Ashwini_V_Waghale": "https://programmash.github.io/Journal.html",
            "Ashwini_Dolli": "https://ashwinisdolli.github.io/journal.html",
            "Basavaraja_C": "https://basavaraj-mrk.github.io/Journal.html",
            "Bharti_C_Rahangdale": "https://bharti-mrk.github.io/journal.html",
            "Bhupati_Sneha" : "https://snehabhupati-mrk.github.io/journal.html",
            "Chetan_A_Tekam" : "https://chetan-mrk.github.io/Journal.html",
            "Deepika_A_Lohakare": "https://deepika-mrk.github.io/journal.html",
            "Ekta_Y_Suryawanshi": "https://ekta-mrk.github.io/Journal.html",
            "Gujjula_H_Bindu" : "https://bindugujjula-mrk.github.io/Journal.html",
            "Gangavarapu_Mahendra": "https://mahendra-mrk.github.io/Journal.html",
            "Himanshu_K_Tajne": "https://himanshu-mrk.github.io/Journal.html",
            "Jami_V_Sai" : "https://venkatsai-mrk.github.io/journal.html",
            "Kunal_P_Lambat": "https://kunal-mrk.github.io/journal.html",
            "Lokesh_R_Gaidhane": "https://lokesh-mrk.github.io/Journal.html",
            "Lucky_R_Rakhunde": "https://lucky-mrk.github.io/Journal.html",
            "Mahesh_R_Thakre": "https://mahesht-mrk.github.io/journal.html",
            "Manoj_R_Bankar" : "https://manoj-mrk.github.io/journal.html",
            "Neha_A_Upadhyaya": "https://neha-mrk.github.io/journal.html",
            "Nithin_E": "https://nithin-mrk.github.io/Journal.html",
            "Pankaj_Nagar" : "https://pankaj-mrk.github.io/journal.html",
            "Pawan_S_Dambhare" : "https://pawandambhare-mrk.github.io/journal.html",
            "Pratiksha_B_Gaidhane": "https://pratiksha-mrk.github.io/journal.html",
            "Praveen_Birader": "https://praveen-mrk.github.io/journal.html",
            "Rahul_R_Nashikkar": "https://rahul-mrk.github.io/Journal.html",
            "Ramya_H_S": "https://ramya-mrk.github.io/journal.html",
            "Rishabh_Jain": "https://rishabh-mrk.github.io/journal.html",
            "Sagili_S_Prasad" : "https://sivasai-mrk.github.io/journal.html",
            "Sagar_S_Jalageri": "https://sagar-mrk.github.io/journal.html",
            "Sanjay_B_S": "https://sanjay-mrk.github.io/journal.html",
            "Shivam_P_Bhankhede": "https://shivam-mrk.github.io/Journal.html",
            "Shubham_B_Ladase": "https://shubham-mrk.github.io/Journal.html",
            "Sneha_T_Malghate": "https://sneha-mrk.github.io/journal.html",
            "Suraj_S_Bhoskar": "https://suraj-mrk.github.io/Journal.html",
            "Swapnil_D_Pulate": "https://swapnil-mrk.github.io/journal.html",
            "Swastik_R_Katre": "https://swastikkatre.github.io/journal.html",
            "Swathi_R_Premar": "https://swathi-mrk.github.io/Journal.html",
            "Vemparala_V_N_S_Swaroop" : "https://swaroopvemparala.github.io/journal.html"
        }

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

    
    def __download_HTML__(self, journal_URL):
        try:
            with urllib.request.urlopen(journal_URL) as url_handle:
                return url_handle.read()
        except:
            return None
    
    def __has_updated_for_date__(self, journal_URL, check_for_date):
        journal_HTML = self.__download_HTML__(journal_URL)
        
        if not journal_HTML:
            print("problem loading this page- ", journal_URL)
            return

        soup = BeautifulSoup(journal_HTML, 'html.parser')
        
        required_date_element = soup.find(
            "td",
            string = re.compile(
                f"^.*{check_for_date.day}.(.*{check_for_date.month}|.*{self.month_regex[check_for_date.month]})(.*{check_for_date.year})"
            )
        )

        if not required_date_element:
            return "Not Updated"

        # determine readability of text using Coleman–Liau index
        # CLI = 0.0588L - 0.296S - 15.8
        #   L = my_letters / words * 100
        #   S = sentences / words * 100
        
        letters = 0
        words = 0
        sentences = 0
        try:
            for i in required_date_element.findNextSibling("td").childGenerator():

                if i.get_text(strip=True, separator=' '):
                    i_sentence = i.get_text(strip=True, separator=' ')
                    i_sentence_len = len(i_sentence)
                    #print(repr(i.get_text(strip=True, separator=' ')))
                else:
                    continue

                sentence_found = False
                for my_index, my_letter in enumerate(i_sentence):
                    if my_index == 0 or my_index == i_sentence_len:
                        words += 1

                    if my_letter in ['.', '!', '?']:
                        sentences += 1
                        sentence_found = True

                    elif my_letter == ' ':
                        words += 1
                    
                    else:
                        letters += 1
                    
                
                if not sentence_found:
                    # no sentence terminator was found, treat whole <li> as one sentence
                    sentences += 1
            
            #print(letters, words, sentences)
            L = letters / words * 100
            S = sentences / words * 100

            return round(0.0588 * L - 0.296 * S - 15.8)
            #return len(required_date_element) > 0
            
        except Exception as e:
            print(e)
            exit()

    def __get_check_for_date__(self):
        #return date(2022, 8, 18)
        choice = input(f"Check Journal for today's({date.today()}) entry [Y/n]: ")
        
        if choice.strip().lower() in ['y', 'yes', '']:
            return date.today();
        
        else:
            try:
                print("Enter date-")
                return date(
                    int(input("Year: ")),
                    int(input("Month: ").lstrip('0')),
                    int(input("Day: ").lstrip('0'))
                )

            except ValueError as e:
                print("Error:", e)
                print("dev is lazy, didn't implement loop till valid input!")
                exit()

    def check(self):
        check_for_date = self.__get_check_for_date__()

        print(f"{'Name'.rjust(25)}  Coleman–Liau index(<5 means not enough/very simple english)")
        for i in self.journals:
            print(i.rjust(25), end="  ")
            print(self.__has_updated_for_date__(self.journals[i], check_for_date))
    
 
if __name__ == "__main__":
    my_journal = Journal()
    my_journal.check()