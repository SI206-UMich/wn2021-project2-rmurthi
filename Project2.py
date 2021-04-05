# Name: Renuka Murthi
# Student ID: 16826716
# Email: rmurthi@umich.edu
# Partner: Annie Rauwerda

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), 'r') as f:
        fyle = f.read()
    soup = BeautifulSoup(fyle, 'html.parser')
    titles = soup.find_all('a', class_ = 'bookTitle')
    authors = soup.find_all('span', itemprop = 'author')
    t = []
    a = []
    for x in titles:
        t.append(x.text.strip())
    for x in authors:
        a.append(x.text.strip())
    
    # print(len(a))
    # print(a)
    tuplz = zip(t,a)
    tupls = list(tuplz)
    # print(tupls)
    return tupls

    

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".
    """
    

    lst = []
    r = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    soup = BeautifulSoup(r.text, 'html.parser')
    lst2 = soup.find('div', class_='leftContainer')
    lst3 = lst2.find_all('a', class_='bookTitle')

    for x in lst3:
        y = x.get('href')
        if y.startswith('/book/show'):
            lst.append('https://www.goodreads.com' + y)
    
    lst4 = lst[:10]
    return lst4


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    pass


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r', encoding="utf8") as f:
        fyle = f.read()
    soup = BeautifulSoup(fyle, 'html.parser')

    lst = []
    lst2 = soup.find_all('h4')
    
    for x in lst2:
        lst.append(x.text.strip())

    lst3 = []
    lst4 = soup.find_all('div', class_='category__winnerImageContainer') 
    for x in lst4:
        title = x.find('img')['alt']
        lst3.append(title)
    
    lst5 = []
    # lst6 = soup.find_all('a', href=True)
    # for a in lst6:
    #     if a.text:
    #         a = a.get('href')
    #         url = lst6[a]
    #         if url.find("https://www.goodreads.com/") >= 0:
    #             print(url)


    lst6 = soup.find_all('div', class_='category clearFix')
    lst7 = []
    for x in lst6:
        y = x.find('a')['href']
        lst5.append(y)

 
    for x, y, z in zip(lst, lst3, lst5):
        tupl = (x, y, z)
        lst7.append(tupl)
    return lst7


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """

    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), 'w', newline='', encoding='utf-8') as f:
        x = csv.writer(f, delimiter = ',')
        x.writerow(['Book Title', 'Author Name'])
        for y in data:
            x.writerow(y)

def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):
 
   # call get_search_links() and save it to a static variable: search_urls
   search_urls = get_search_links()
 
  
   def test_get_titles_from_search_results(self):
       # call get_titles_from_search_results() on search_results.htm and save to a local variable
       results = get_titles_from_search_results("search_results.htm")
       # check that the number of titles extracted is correct (20 titles)
       self.assertEqual(len(results), 20)
       # check that the variable you saved after calling the function is a list
       self.assertTrue(type(results) is list)
       # check that each item in the list is a tuple
       for x in results:
           self.assertTrue(type(x) is tuple)
       # check that the first book and author tuple is correct (open search_results.htm and find it)
       self.assertEqual(results[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
       # check that the last title is correct (open search_results.htm and find it)
       self.assertEqual(results[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))
  
  
   def test_get_search_links(self):
       # check that TestCases.search_urls is a list
       self.assertTrue(type(TestCases.search_urls) is list)
       # check that the length of TestCases.search_urls is correct (10 URLs)
       self.assertEqual(len(TestCases.search_urls), 10)
       # check that each URL in the TestCases.search_urls is a string
       for x in TestCases.search_urls:
           self.assertTrue(type(x) is str)
       # check that each URL contains the correct url for Goodreads.com followed by /book/show/
       for x in TestCases.search_urls:
           reg = 'https://www.goodreads.com/book/show'
           self.assertEqual(bool(re.match(reg, x)), True)
  
  
   def test_get_book_summary(self):
       # create a local variable – summaries – a list containing the results from get_book_summary()
       # for each URL in TestCases.search_urls (should be a list of tuples)
       lst = []
       for x in TestCases.search_urls:
           y = get_book_summary(x)
           lst.append(y)
       # check that the number of book summaries is correct (10)
       self.assertEqual(len(lst), 10)
       # check that each item in the list is a tuple
       for x in lst:
           self.assertTrue(type(x) is tuple)
       # check that each tuple has 3 elements
       for x in lst:
           self.assertEqual(len(x), 3)
       # check that the first two elements in the tuple are string
       for x in lst:
           self.assertTrue(type(x[0]) is str)
           self.assertTrue(type(x[1]) is str)
       # check that the third element in the tuple, i.e. pages is an int
       for x in lst:
           self.assertTrue(type(x[2]) is int)
       # check that the first book in the search has 337 pages
       firstbook = lst[0]
       self.assertTrue(firstbook[2] == 337)
  
  
   def test_summarize_best_books(self):
       # call summarize_best_books and save it to a variable
       bestbooks = summarize_best_books("best_books_2020.htm")
       # check that we have the right number of best books (20)
       self.assertEqual(len(bestbooks), 20)
       # assert each item in the list of best books is a tuple
       for book in bestbooks:
           self.assertIsInstance(book, tuple)
       # check that each tuple has a length of 3
       for book in bestbooks:
           self.assertEqual(len(book), 3)
       # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
           self.assertEqual(bestbooks[0], ('Fiction', 'The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
       # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
           self.assertEqual(bestbooks[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
   
   def test_write_csv(self):
       # call get_titles_from_search_results on search_results.htm and save the result to a variable
       var = get_titles_from_search_results('search_results.htm')
       # call write csv on the variable you saved and 'test.csv'
       write_csv(var, 'test.csv')
       # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
       csv_lines = []
       with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
           reader = csv.reader(f)
           for x in reader:
               csv_lines.append(x)
       # check that there are 21 lines in the csv
       self.assertEqual(len(csv_lines), 21)
       # check that the header row is correct
       self.assertEqual(csv_lines[0], ['Book Title','Author Name'])
       # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
       self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
       # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
       self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])
  
  
if __name__ == '__main__':
   #print(extra_credit("extra_credit.htm"))
   unittest.main(verbosity=2)
   # get_titles_from_search_results("search_results.htm")
