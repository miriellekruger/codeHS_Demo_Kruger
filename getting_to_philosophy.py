"""
getting_to_philosophy.py Mirielle Kruger for CodeHS

Given a Wikipedia article url, this script will hop from article to article within Wikipedia until reaching the article "Philosophy", 
    using the first link in each article, printing each article url and the final number of hops taken. 

Command: 
python getting_to_philosophy.py "https://en.wikipedia.org/wiki/Elizabeth_I"

Optional arguments: 
    -mh or --max-hops: Sets the maximum number of hops to prevent getting stuck in a loop
        Default 100 
    -n or --no-alt-namespaces: Optional argument to exclude links that start with Wikipedia namespaces that are not main articles (e.g.,"Help:", "Talk:"). 
        See: https://en.wikipedia.org/wiki/Wikipedia:Namespace
        Test with: https://en.wikipedia.org/wiki/Referent 
        
Result: 
A printed list of all the links that are on the path to the Philosophy Wikipedia page 
    and a printed count of the number of hops made to reach the Philosophy Wikipedia page 
        
Read more at http://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy

"""
import urllib.request # opens url and provides html
from bs4 import BeautifulSoup # processes html based on tags
import argparse # grabs arguments from terminal command

def getFirstUrl(url, alt_namespaces):
    """
    Process a url to get the first link in the main content of the url's page

    Inputs: 
        url (string): an input url to be processed
        alt_namespaces (boolean): if true, includes links that start with alternative namespaces like "Help:" 
            Default True

    NOTE: Assume that the first url is not a footnote.
    """

    # fetch html of the url
    html = urllib.request.urlopen(url)

    # parse through html to find the first link 
    soup = BeautifulSoup(html, "html.parser")

    # content of wikipedia page found in div with class "mw-content-ltr" 
    div_with_content = soup.find("div",{"class": "mw-content-ltr"})

    # main content is found in p or paragraph tags
    content = div_with_content.find_all("p", recursive=False)

    # find first p with a link (aka "a" or anchor tag) that isn't a footnote (recursive=True would find footnotes as well)
    for p in content: 
        links = p.find_all("a", recursive=False)
        if links: 
            ind = 0
            # arg alt_namespaces determines whether or not we want links with alternative namespaces like "Help:"
            if not alt_namespaces:
                namespaces = ["Help:", "User:", "Wikipedia:", "Project:", "WP:", "File:", "Image:", "MediaWiki:", "Template:", "TM:", "Category:", "Portal:", "Draft:", "TimedText:", "Module:"]
                while any(namespace in links[ind]['href'] for namespace in namespaces):
                    ind += 1
            
            relative_path = links[ind]['href']
            break
    
    # build url, hrefs are given in relative paths
    base_url = "https://en.wikipedia.org"
    next_url = base_url + relative_path
    return next_url

def isPhilosophy(url): 
    """
    Determine whether the current page is the "Philosophy" page.

    Input: 
        url: a string containing a url for testing

    Output: 
        a boolean that is True if the topic of the page is "Philosophy"

    """

    # identify topic of url
    split_url = url.split("/")
    topic = split_url[-1]

    # return if topic is Philosophy
    return topic == "Philosophy"

def hopUrls(url, max_hops, alt_namespaces):
    """
    Hops urls until reaches Philosophy or maximum hops. 

    Input: 
        url (string): an input url to be processed
        alt_namespaces (boolean): if true, includes links that start with alternative namespaces like "Help:" 
            Default True
        max_hops (int): 
        alt_namespaces (boolean): 

    Output: (via Terminal)
        Printed List of Urls
        Printed Number of Hops
    """

    hop_count = 0
    
    # iterate until reach "Philosophy" or max_hops
    for i in range(max_hops):
        # test if url is "Philosophy"
        if isPhilosophy(url):
            # searcch complete
            print(f"{hop_count} hops")
            break

        # keep searching
        url = getFirstUrl(url, alt_namespaces)
        print(url)
        hop_count += 1
    
def main():
    """
    Function that receives the arguments from the terminal and runs hopUrls accordingly.
    """
    parser = argparse.ArgumentParser(description="Getting to Philosophy Wikipedia Page")
    parser.add_argument("url")
    parser.add_argument("-mh", "--max-hops", help="Set max hops until termination.", default=100, dest="max_hops")
    parser.add_argument("-n", "--no-alt-namespaces", help="Get first nonfootnote links excluding links to non-main Wikipedia pages.", action=argparse.BooleanOptionalAction, dest="alt_namespaces")

    args = parser.parse_args()
    url = args.url
    alt_namespaces = not args.alt_namespaces
    max_hops = int(args.max_hops)
    hopUrls(url, max_hops, alt_namespaces)

if __name__ == '__main__':
    main()