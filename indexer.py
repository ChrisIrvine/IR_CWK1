import sys
import re
import string
import json

# global declarations for doclist, postings, vocabulary
docids = []
postings = {}
vocab = []

# main is used for offline testing only
def main():
    # code for testing offline
    if len(sys.argv) != 2:
        print('usage: ./indexer.py file')
        sys.exit(1)
    filename = sys.argv[1]

    try:
        input_file = open(filename, 'r')
    except (IOError) as ex:
        print('Cannot open ', filename, '\n Error: ', ex)

    else:
        page_contents = input_file.read()  # read the input file
        url = 'http://www.' + filename + '/'
        print(url, page_contents)
        make_index(url, page_contents)

    finally:
        input_file.close()


def write_index():
    # declare refs to global variables
    global docids
    global postings
    global vocab

    # writes to index files: docids, vocab, postings
    outlist1 = open('docids_test.txt', 'w')
    outlist2 = open('vocab_test.txt', 'w')
    outlist3 = open('postings_test.txt', 'w')

    json.dump(docids, outlist1)
    json.dump(vocab, outlist2)
    json.dump(postings, outlist3)

    outlist1.close()
    outlist2.close()
    outlist3.close()

    return


def clean_html(page_contents):
    # function to clean html
    ##### your code here ######
    #No JavaScript
    cleantext = re.sub('<script[\s\S]+?/script>', '', page_contents)
    #No CSS
    cleantext = re.sub('<style[\s\S]+?/style>', '', cleantext)
    #No Comments
    cleantext = re.sub('<!--[\s\S]+?-->', '', cleantext)
    #No HTML
    cleantext = re.sub('<.*?>', '', cleantext)
    #No Dates
    cleantext = re.sub('(\d{2}-\w{3}-\d{4}\s\d{2}:\d{2})', '', cleantext)
    #No Links
    cleantext = re.sub('(lg\d{3}.html)', '', cleantext)
    #No Numbers
    cleantext = re.sub('(\d)', '', cleantext)
    #No HTML Special Characters
    cleantext = re.sub('&[^\s]*', '', cleantext)
    #No Abbreviations
    cleantext = re.sub('(n\'t\b)',' not', cleantext)
    cleantext = re.sub('(\'ll\b)',' will', cleantext)
    cleantext = re.sub('(I\'m)','I am', cleantext)
    cleantext = re.sub('(I\'ve)','I have', cleantext)
    cleantext = re.sub('(\w*\'\w*)', '', cleantext)
    #No Punctuation
    cleantext = re.sub('([\W]+)', ' ', cleantext)
    #Get rid of index and of
    cleantext = re.sub('Index', '', cleantext)
    cleantext = re.sub('of', '', cleantext)
    return cleantext
    ##### your code end  ######


def make_index(url, page_contents):
    # declare refs to global variables
    global docids
    global postings
    global vocab

    # first convert bytes to string if necessary
    if isinstance(page_contents, bytes):
        page_contents = page_contents.decode('utf-8')

    print('===============================================')
    print('make_index: url = ', url)
    print('===============================================')

    page_text = clean_html(page_contents)

    #### your code here ####
    docids.append(url)
    tokens = [t.lower() for t in page_text.split()]

    vocab.extend([t for t in tokens if t not in vocab])

    for tokenID, token in enumerate(vocab):
        if tokenID not in postings:
            postings[tokenID] = []
        freq = tokens.count(token)
        if freq != 0:
            postings[tokenID].append([docids.index(url), tokens.count(token)])
    #### end of your code ####
    return

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
