#!/usr/local/bin/python3
import json, pickle
import datetime
from pylatex import Document, Section, Subsection, Command, Itemize, MiniPage, LineBreak, VerticalSpace, PageStyle, Head, StandAloneGraphic, MediumText
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape, bold
from pathlib import Path

MAX_YEAR_LIMIT = 20     # more recent years (with compact flag)
NARRATIVE      = False # disable narrative by default (compact==true)
ENCODING       ='utf8' # encoding for writing/readiing json files
DATE           = datetime.date.today().ctime().split(' ')
YEAR           = DATE[-1]
AUTHOR         = "Federico Cámara Halac"
def phone_format(p):
    return f"+ {p[0]} ({p[1]}) {p[2]}-{p[3]}"

class Itemize(Environment):
    escape = True
    content_separator = "\n"

class Resume(Environment):
    escape = True
    content_separator = "\n"

class Quote(Environment):
    escape = True
    content_separator = "\n"

def comment(doc, s=''):
    doc.append(NoEscape("%" + "-"*78 + "\n"))
    doc.append(NoEscape("% "+s+" \n"))
    doc.append(NoEscape("%" + "-"*78 + "\n"))

def writeEntry(doc, item, curr, prev):

    e = curr
    if prev:
        # this selects which repeated keys to be removed:
        if curr['employer'] == prev['employer']:
            e['employer'] = ''
        if curr['location'] == prev['location']:
            e['location'] = ''
            
        # # this removes all repeated. comment-out if wanted
        # for (c_k, c_v), (p_k, p_v) in zip(curr.items(),prev.items()):
        #     if c_v == p_v:
        #         e[c_k] = ''
    
    dates=e['dates']
    title=e['title']
    employer=e['employer']
    description=e['description']
    location=e['location']
    year=e['year']
    subheader=e['subheader']
    narrative=e['narrative']
        
    if title and title[-1] == ".":
        title[:-2]
    if employer and  employer[-1] == ".":
        employer[:-2]
    if description and description[-1] == ".":
        description[:-2]
    if location and location[-1] == ".":
        location[:-2]

    with doc.create(Itemize(options=[ 
        'align=parleft',
        'leftmargin=2.25cm',
        'labelwidth=2cm' ]
        )):
        doc.append(NoEscape("\\item["+item+"]"))

        if 'ongoing' in dates:
            doc.append(bold(title))
            doc.append("(ongoing). ")
        else:
            doc.append(bold(title+"."))
        
        if employer and subheader != employer:
            doc.append(employer+". ")
        
        if description:
            # remove my name from the description if i'm the only one there...
            fd="Federico Camara Halac"
            if fd != description and len(description) != len(fd):
                doc.append(description+". ")
        
        if location:
            doc.append(location+". ")
        
        if 'ongoing' not in dates and dates != year:
            doc.append(dates+".")

        if NARRATIVE and narrative:
            with doc.create(Quote()):
                doc.append(narrative)


def make_personal(doc, image=False):
    """Write up the personal data header
    """
        
        
    # doc.append(Command('hrule'))
    # doc.append(VerticalSpace("-5pt"))
    if image:
        with doc.create(MiniPage(width=r"0.45\textwidth")):
            # with doc.create(Figure()) as profil:
            doc.append(Command("centering"))
            doc.append(Command("includegraphics", PROFIL,"width=200pt"))

    with doc.create(MiniPage(width=r"0.6\textwidth")):
        with doc.create(Section(data['personal']['name'])):
            # doc.append(VerticalSpace("-3pt"))
            with doc.create(Itemize(options=[ 
                            'align=parleft',
                            'leftmargin=2.25cm',
                            'labelwidth=2cm' ]
                            )):
                # doc.append(Command("hrule"))
                doc.append(NoEscape("\\item[Phone]"))
                doc.append(phone_format(data['personal']['phone']))
                doc.append(NoEscape("\\item[Email]"))
                doc.append(Command("url",data['personal']['email'][0]))
                # doc.append(Command("url",data['personal']['email'][1]))
                doc.append(NoEscape("\\item[Website]"))
                doc.append(Command("url",data['personal']['website']))
                doc.append(NoEscape("\\item[Address]"))
                doc.append(NoEscape(",\\\\".join(data['personal']['address'])))
                doc.append(NoEscape("\\item[Birth]"))
                b=data['personal']['birth']
                birth=f"{b['day']} {b['month']['name']} {b['year']}"
                doc.append(NoEscape(birth+f", {b['city']}, {b['country']}"))

    # doc.append(Command('hrule'))
    doc.append(Command("hfill"))
    # doc.append(LineBreak())
 
def make_doc(file, 
            title, 
            author, 
            geometry_options = {"margin": "1.15cm"}, 
            options=""):
    """ Create and return a formatted Pylatex Document with my data
    
    Parameters
    ----------
    file = Path() (from pathlib) to ifentify the tex and pdf output files
    
    Returns
    ----------
    The document class

    """
    
    # geometry_options = {"tmargin": "1.5cm", "lmargin": "2.5cm"},

    doc = Document(
        default_filepath = file.as_posix(),
        documentclass    = 'article',
        document_options = ['12pt', 'titlepage' ] + options,
        fontenc          = "T1",
        inputenc         = ENCODING,
        font_size        = "normalsize",
        lmodern          = True,
        page_numbers     = False,
        indent           = False,
        geometry_options = geometry_options
    )
    doc.change_document_style("empty")
    date = str(datetime.datetime.date(datetime.datetime.now()))
    comment(doc.preamble, "Automatically generated by make on " + date)

    doc.preamble.append(Command("usepackage","graphicx"))
    doc.preamble.append(Command("usepackage","enumitem"))
    doc.preamble.append(Command("usepackage","url"))
    doc.preamble.append(NoEscape("\\setcounter{secnumdepth}{0}"))
    doc.preamble.append(Command("usepackage","titlesec"))
    doc.preamble.append(NoEscape("\\titlespacing\\section{0pt}{12pt}{12pt}"))
    doc.preamble.append(NoEscape("\\titlespacing\\subsection{0pt}{12pt}{12pt}"))
    doc.preamble.append(Command("title", title.title()))
    doc.preamble.append(Command("author", author.title()))
    doc.preamble.append(Command("date", NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    return doc

if __name__ == '__main__':
    
    import argparse

    parser  = argparse.ArgumentParser()
    
    parser.add_argument("-d", '--datadir',
        help="Local data files.", 
        type=str,
        default="./data")
    
    parser.add_argument("-cl", '--cover',
        help="Output Cover Letter with data from given path", 
        type=str)

    parser.add_argument("-u", '--update',
        help="Update local sheet data with google sheet data.", 
        action="store_true")

    parser.add_argument("-c", '--compact',
        help="Make a compact version of the cv by setting max year limit", 
        type=int,
        default=MAX_YEAR_LIMIT)
    
    parser.add_argument("-cv", '--cv',
        help="Make the cv file", 
        action="store_true")
    
    parser.add_argument("-rs", '--refselect',
        help="Pass an array of indices to select references.", 
        type=str,
        default="0 1 2")

    parser.add_argument("-r", '--references',
        help="Make only the references file.", 
        action="store_true")

    parser.add_argument("-T", '--translate',
        help="Translate the file (applying sheet offset to download.py).", 
        action="store_true")

    parser.add_argument("-p", '--parse',
        help="Parse the local data without fetching it again.", 
        action="store_true")

    args = parser.parse_args()
    
    DATADIR = Path(args.datadir)

    PROFIL  = Path("img") / "profil.jpg"
    # sheeti  = DATADIR / "sheet_id.pkl"
    sheetj  = DATADIR / "sheet_data.json"
    sheetp  = DATADIR / "sheets_english-parsed-test.json"
    sheetg  = DATADIR / "sheets_german-parsed-test.json"
    sheett  = DATADIR / "cv_tree.json"
    sheettg = DATADIR / "cv_tree_german.json"
    sheetr  = DATADIR / "references.json"
    texfile = DATADIR / "temp_trans" if args.translate else DATADIR / "temp"
    reffile = DATADIR / "references"
    datafile= DATADIR / "data.json"
    logoimg = DATADIR / "logo.jpg"
    sigimg  = DATADIR / "signature.jpg"

    with datafile.open(mode='r', encoding=ENCODING) as f:
        data = json.load(f)

    if args.compact:
        # reset the max year limit global
        MAX_YEAR_LIMIT = args.compact
    
    ###
    ### UPDATE
    ###
    
    if args.update:

        sheet_id = "1vViMWDsMRnbGUgP44XNDlQrLQ3MsdgO9W91mM4MxJtw"

        import download
        download.downloadSheet(sheet_id, sheetj, offset=args.translate)
    
    ###
    ### PARSE
    ###

    if args.update or args.parse:
        
        import parser
        parser.parseSheet(sheetj,sheetp)
    
    ###
    ### CV
    ###

    if args.cv:
        if args.translate:
          with sheetg.open(mode='r', encoding=ENCODING) as f:
              sheet_data = json.load(f)
          
          with sheettg.open(mode='r', encoding=ENCODING) as f:
              cv_tree = json.load(f)

        else:
          with sheetp.open(mode='r', encoding=ENCODING) as f:
              sheet_data = json.load(f)
          
          with sheett.open(mode='r', encoding=ENCODING) as f:
              cv_tree = json.load(f)

        doc = make_doc(texfile, 
            title="Curriculum Vitae", 
            author=data['personal']['name'],
            options=['ngerman']
        )
        if args.translate:
          doc.preamble.append(Command("usepackage", "babel"))
          doc.preamble.append(Command("usepackage", "csquotes"))
          doc.preamble.append(Command("MakeOuterQuote", NoEscape("\"")))

        PROFIL = PROFIL.resolve().as_posix()
        doc.append(Command("raggedright"))

        make_personal(doc, image=True)

        for section in cv_tree['sections']:
            sheet=section['sheet']
            doc.append(VerticalSpace(NoEscape("-6pt")))
            with doc.create(Section(sheet_data[sheet]['section'])):
                doc.append(VerticalSpace(NoEscape("-8pt")))
                doc.append(Command('hrule'))
                for v in section['order']:
                    v = v.replace(" ","_")
                    subheader=sheet_data[sheet]['subcategories'][v]["subsection"]
                    # doc.append(NoEscape("\\noindent\\rule{\\textwidth}{0.4pt}"))
                    # doc.append(Command('hrule'))
                    p_y=''
                    p_m=''
                    monthit=len(sheet_data[sheet]['subcategories'][v]['data'])
                    p_title=''
                    p_entry={}
                    p_subheader=''
                    merge=0
                    entryBuffer = []                    
                    for i in sheet_data[sheet]['subcategories'][v]['data']:

                        c_y = i['year'].replace(" ","").replace(".","")
                        c_m = i['month'].replace(" ","")
                        # this accounts for year/month repetition
                        if p_y != c_y and p_m != c_m:
                            # year and month changed, display full date
                            dateit=i['year'].replace(".","")
                            if monthit > 1:
                                dateit+=" | " +i['month'][:3]

                        elif p_y == c_y and p_m != c_m:
                            # only month changed, display month only
                            dateit=i['month']
                        elif p_y != c_y and p_m == c_m:
                            # only year changed, display year only
                            dateit=i['year'].replace(".","")
                        else:
                            # no change, no date display
                            dateit=''

                        p_y=c_y
                        p_m=c_m

                        # the current entry object
                        c_entry = {
                            "dates":i['dates'],
                            "title":i['title'],
                            "employer":i['employer'],
                            "description":i['description'],
                            "narrative":i['narrative'],
                            "location":i['location'],
                            "subheader":subheader,
                            "year":i['year'].replace(".","")
                        }
                        p_entry = c_entry
                        within = abs(int(c_y)-int(YEAR)) <= MAX_YEAR_LIMIT
                        if within or "education" in sheet:
                            e = {
                                "data":[dateit,c_entry,p_entry],
                            }
                            if p_subheader is not subheader:
                                c_subheader = subheader
                                e.update({"title":c_subheader})
                            else:
                                e.update({"title":None})
                            p_subheader = c_subheader
                            entryBuffer.append(e)

                    for e in entryBuffer:
                        d = e['data']
                        if e['title'] is not None:
                            doc.append(VerticalSpace(NoEscape("-2pt")))
                            doc.append(Command("subsection",e['title']))
                            doc.append(VerticalSpace(NoEscape("-8pt")))
                        writeEntry(doc, d[0], d[1], d[2])
                        doc.append(VerticalSpace(NoEscape("-2pt")))
                
                if "education" in sheet:
                    with doc.create(Section("Research Interests")):
                        doc.append(Command('hrule'))
                        with doc.create(Quote()):
                            doc.append(". ".join(data["research"]))
                    doc.append(Command("pagebreak"))
                # end subsection loop
                doc.append(VerticalSpace(NoEscape("-2pt")))
            # end subsections
        # end sections
        with doc.create(Section("Other Skills")):
            doc.append(Command('hrule'))

            for k,v in data['skills'].items():
                with doc.create(MiniPage(
                        width=NoEscape(r"0.33\textwidth"),
                        pos='t', align='l'
                    )) as mp:
                    with mp.create(Subsection(k.title())):
                        # mp.append(VerticalSpace(NoEscape("-2pt")))
                        with mp.create(Itemize()):
                            for i in v:
                                mp.append(Command('item'))
                                if 'Latex' in i['item']:
                                    mp.append(Command("LaTeX"))
                                else:
                                    mp.append(bold(i['item']))
                                if i['description']:
                                    mp.append(": "+i['description'])
                                # mp.append(VerticalSpace(NoEscape("-2pt")))
                            mp.append(LineBreak())


            # with doc.create(Subsection("Languages")):
            #     with doc.create(Itemize(options=[ 
            #             'align=parleft',
            #             'leftmargin=2.25cm',
            #             'labelwidth=2cm' ]
            #             )):
            #         for i in data["languages"]:
            #             doc.append(Command("item"))
            #             doc.append(Command("textbf", i['item']))
            #             doc.append(" ("+i['description']+") ")

            # with doc.create(Subsection("Code")):
            #     with doc.create(Itemize(options=[ 
            #             'align=parleft',
            #             'leftmargin=2.25cm',
            #             'labelwidth=2cm' ]
            #             )):
            #         for i in data["code"]:
            #             doc.append(Command("item"))
            #             doc.append(Command("textbf", i['item']))
            #             doc.append(" ("+i['description']+") ")

            # with doc.create(Subsection("Software")):
            #     with doc.create(Itemize(options=[ 
            #             'align=parleft',
            #             'leftmargin=2.25cm',
            #             'labelwidth=2cm' ]
            #             )):

            #         for i in data["software"]:
            #             doc.append(Command("item"))
            #             doc.append(Command("textbf", i+"."))

        print("Compiling CV PDF file")
        doc.generate_pdf(clean_tex=True)

        doc.generate_tex()

    ###
    ### REFERENCES
    ###

    if args.references:

        with sheetr.open(mode='r', encoding=ENCODING) as f:
            ref_data = json.load(f)

        doc = make_doc(reffile, 
            title="References", 
            author=data['personal']['name']
        )

        make_personal(doc,image=False)

        doc.append(Command("raggedright"))
        splitter=Command("par")# ". "

        selection = [ ref_data[int(i)] for i in args.refselect.split(" ") ]


        with doc.create(Section("References")):
            for i in selection:
                with doc.create(Subsection(i['name'])):
                    phone = phone_format(i['phone'])
                    address = ", ".join(i['address'])
                    doc.append(Command('hrule'))
                    doc.append(bold("Affiliation: "))
                    doc.append(i['affiliation'])
                    doc.append(VerticalSpace(NoEscape("-10pt")))
                    doc.append(splitter)
                    doc.append(bold("Department: "))
                    doc.append(i['department'])
                    doc.append(VerticalSpace(NoEscape("-10pt")))
                    doc.append(splitter)
                    doc.append(bold("Title: "))
                    doc.append(i['title'])
                    doc.append(VerticalSpace(NoEscape("-10pt")))
                    doc.append(splitter)
                    doc.append(bold("Phone: "))
                    doc.append(phone)
                    doc.append(VerticalSpace(NoEscape("-10pt")))
                    doc.append(splitter)
                    doc.append(bold("Address: "))
                    doc.append(address)
                    doc.append(VerticalSpace(NoEscape("-10pt")))
                    doc.append(splitter)
                    doc.append(VerticalSpace(NoEscape("10pt")))

        print("Compiling References PDF file")
        doc.generate_pdf(clean_tex=True)

        doc.generate_tex()
    
    ###
    ### COVER LETTER
    ###

    if args.cover:
        
        date = f"{DATE[2]} {DATE[1]} {DATE[-1] }"
        
        
        import importlib

        covername = args.cover.replace('.py','').split("/")[-1]

        print("Making Cover Letter for ", covername)

        coverfile = DATADIR / covername

        m = importlib.import_module("calls." + covername)
        u = m.post
        f = m.fede

        geometry_options = {
            "head": "40pt",
            "margin": "0.5in",
            "bottom": "0.6in",
            "includeheadfoot": True
        }

        doc = make_doc(coverfile, 
            title="Cover Letter", 
            author=data['personal']['name'],
            geometry_options=geometry_options
        )

        first_page = PageStyle("firstpage")

        with first_page.create(Head("R")) as h:

            with h.create(MiniPage(width=NoEscape(r"\textwidth"),
                                     pos='r', align='r')) as w:
                w.append(VerticalSpace(NoEscape("-10pt")))
                w.append(MediumText(bold(data['personal']['name'])))
                w.append(LineBreak())
                w.append(phone_format(data['personal']['phone'])+" ")
                w.append(Command("url",data['personal']['email'][0]))
                w.append(VerticalSpace('2pt'))
                w.append(Command("hrule"))


        address = [u['department'], u['university']]+[i for i in u['contact']['address']]
        
        with first_page.create(Head("L")) as h:
            # h.append(VerticalSpace(NoEscape('-30pt')))
            h.append(StandAloneGraphic(
                image_options=[
                "height=1cm", 
                "keepaspectratio=true"],
                filename=logoimg.resolve().as_posix()))
   
            with h.create(MediumText()):
                doc.append(MediumText(m.addressee))
                doc.append(LineBreak())
            
                for i in address:
                    doc.append(MediumText(i))
                    doc.append(LineBreak())

        doc.preamble.append(Command('raggedright'))
        doc.preamble.append(first_page)
        doc.change_document_style("firstpage")
        doc.append(LineBreak())
        doc.append(VerticalSpace(NoEscape('-120pt')))
        doc.append(Command("flushright"))
        doc.append(MediumText(date))
        doc.append(LineBreak())
        
        # opening
        doc.append(VerticalSpace('60pt'))
        doc.append(Command("flushleft"))
        doc.append(m.paragraphs[0])

        # paragraphs
        doc.append(Command("justify"))
        for i in m.paragraphs[1:5]:
            doc.append(NoEscape(i))
            doc.append(Command("par"))
        
        # projects
        with doc.create(Itemize()):
            for i in f['projects']:
                doc.append(Command('item'))
                doc.append(i)
        doc.append(Command("pagebreak"))
        # paragraphs
        for i in m.paragraphs[5:]:
            doc.append(NoEscape(i))
            doc.append(Command("par"))
        
        # signature
        doc.append(Command("centering"))
        doc.append(StandAloneGraphic(
            image_options=[
                "height=4cm", 
                "keepaspectratio=true"
            ],
            filename=sigimg.resolve().as_posix()))
        doc.append(Command("par"))
        doc.append(VerticalSpace(NoEscape('-20pt')))
        doc.append(data['personal']['name'])

        doc.generate_pdf(clean_tex=True)

        doc.generate_tex()
