try:
    from Bio import Entrez
    import pandas as pd
except Exception as e:
    print("Missing modules: ", e)

def get_abs(id, email="pearlmed15@gmail.com"):
    '''
    Get abstract from PMID ID
    :param id: (integer) PMID ID
    :return: (string) Abstract
    '''
    Entrez.email = email
    handle = Entrez.efetch(db='pubmed', id=id, rettype='', retmode='xml')
    record = Entrez.read(handle)
    handle.close()
    text_abs = ""

    if record['PubmedArticle'] == []:
        abs = record['PubmedBookArticle'][0]['BookDocument']['Abstract']['AbstractText']
        text_abs = text_abs + abs

    else:
        # if no abstract available
        if not('Abstract' in record['PubmedArticle'][0]['MedlineCitation']['Article']):
            text_abs = ""
        else:
            abs = record['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText']

            if len(abs) == 1:
                text_abs = text_abs + abs[0]
            else:
                for i in range(len(abs)):
                    if 'Label' in abs[i].attributes:
                        attr = abs[i].attributes['Label']
                        line_abs = str(abs[i])
                        text_abs = text_abs + attr + " : " + line_abs + "\n"
                    else:
                        text_abs = text_abs + abs[i] + '\n'
    return(text_abs)

def search_list(term, mindate, maxdate, email="pearlmed15@gmail.com"):
    '''
    Enter the search terms and extract all the data from PubMed, return csv file
    :param terms: (string) search terms
    :param mindate: (string) minimum date (format: 2021/09/10) #todo: Learn format
    :param maxdate: (string) maximum date
    :return: (list) idlist; (dataframe or csv file) outcome dataframe of search lists
    '''

    Entrez.email = email
    handle = Entrez.esearch(db='pubmed', term=term, datetype="pdat", mindate=mindate, maxdate=maxdate, retmax=10000)
    record = Entrez.read(handle)
    handle.close()
    idlist=record["IdList"]

    search_df = pd.DataFrame({"Author_year": [], "Title": [], "Id": [], "FirstAuthor": [],
                              "PubDate": [], 'AuthorList': [], 'Journal': [], 'DOI': [], 'Abstract': []})
    i = 0
    for id in idlist:
        print("Efetching %i / %i" % (i + 1, len(idlist)))

        fetch_handle = Entrez.efetch(db="pubmed", id=id, rettype="docsum")
        fetch_record = Entrez.read(fetch_handle)
        fetch_handle.close()

        Id = fetch_record[0]['Id']
        PubDate = fetch_record[0]['PubDate']
        AuthorList = fetch_record[0]['AuthorList']

        if len(AuthorList) > 0:
            FirstAuthor = AuthorList[0]
        else:
            FirstAuthor = ''

        new_AuthorList = str(AuthorList)[1:-1]
        Title = fetch_record[0]['Title']

        if 'DOI' in fetch_record[0]:
            DOI = fetch_record[0]['DOI']
        else:
            DOI = ''

        Journal = fetch_record[0]['FullJournalName']
        Abstract = get_abs(id)

        if len(AuthorList) > 1:
            author_year = FirstAuthor + " et al., " + PubDate[0:4]
        else:
            author_year = FirstAuthor + ", " + PubDate[0:4]

        print("Efetched %i / %i" % (i + 1, len(idlist)))
        i = i + 1

        temp_df = pd.Series([author_year, Title, Id, FirstAuthor, PubDate,
                             new_AuthorList, Journal, DOI, Abstract],
                            index=["Author_year", "Title", "Id", "FirstAuthor", "PubDate",
                                   "AuthorList", "Journal", "DOI", "Abstract"])

        search_df = search_df.append(temp_df, ignore_index=True)

    return idlist, search_df