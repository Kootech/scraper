from bs4 import BeautifulSoup
import requests
import csv 

import psycopg2



URL = 'https://www.ebay.com/'

class ParseFile:
    def __init__(self, url = URL) -> None:
        self.url = url


    def loadWeb(self):
        try:
            rq = requests.get(self.url)
        except:
            print('cannot load')
        soup = BeautifulSoup(rq.content, 'html5lib')
        return soup 
    
    def saveToFile(self):
        soup = self.loadWeb()
        with open('links.txt', 'w') as f:
            for link in soup.find_all('a'):
                words = link.string
                if words == None:
                    words == 'none'
                f.write("Name: " + str(words) + ' Link: ' + link.get('href') + "\n")

    
    def saveToCsv(self):
        header = ['name', 'link']
        soup = self.loadWeb()
        with open('links.csv', 'w') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            for link in soup.find_all("a"):
                csvwriter.writerow([str(link.string), link.get('href')])
        


    def readCsv(self):
        fields = []
        rows = []
        with open('links.csv', 'r') as f:
            csvreader = csv.reader(f)
            fields = next(csvreader)

            for row in csvreader:
                rows.append(row)
        
        for row in rows[:5]:
            # parsing each column of a row
            for col in row:
                print("%10s"%col,end=" "),
            print('\n')

    def saveToDatabase(self):
        soup = self.loadWeb()
        #database connection
        try:
            test_database = psycopg2.connect('dbname=test host=localhost user=postgres password=kelvin')
        except:
            print("database cannot connect")
        
        cur = test_database.cursor()
        try:
            cur.execute("CREATE TABLE tlinks(name varchar, link varchar)")
        except:
            print("database already exist")
        for link in soup.find_all('a'):
            name = str(link.string)
            link = link.get('href')

            if name == None:
                name = "none"

            cur.execute("INSERT INTO tlinks(name, link) VALUES(%s, %s)", (name, link))

        test_database.commit()
        cur.close()
        test_database.close()
        

    def readDatabase(self):
        try:
            test_database = psycopg2.connect('dbname=test host=localhost user=postgres password=kelvin')
        except:
            print("database cannot connect")
        
        cur = test_database.cursor()
        cur.execute("SELECT * FROM tlinks")
        print(cur.fetchall())

        cur.close()
        test_database.close()
        

if __name__ == '__main__':
    parsefile = ParseFile()
    # parsefile.saveToFile()
    # parsefile.saveToCsv()
    # parsefile.readCsv()
    # parsefile.saveToDatabase()
    parsefile.readDatabase()