import pypdf, re
from argparse import ArgumentParser
def font_index_is_switched(font_index, font_index_prev, newline):
    if font_index != font_index_prev:
        return newline
    else:
        return ""
class OrganisationObject:
    re_empty_str = re.compile(r"^[ \t\n\s0-9,.-]*$") # match if "empty" string
    re_extract_info = re.compile(r".*?(\([0-9]{3}\)\s[0-9]{3}-[0-9]{2}-[0-9]{2}[\s,]*)+")
    # settings variables
    header_pos = 9.5 # x coordinate of text relative to each page
    body_pos = 9.0
    def __init__(self):
        self.name = ""
        self.description = ""
        self.info = ""
        self.ok = False
    def is_ok(self):
        return self.ok
    def is_empty_str(string):
        # matches: "" | " " | "\t" | "\n" | "123"
        return OrganisationObject.re_empty_str.match(string) is not None
    def to_str(self):
        return f"Name:\n{self.name}\nDescr:\n{self.description}\n"
    def to_csv(self, delim):
        lines = self.description.split("\n")
        lines = [line for line in lines if line != ""]
        description = "".join([line for line in lines if line[0] != '\t'])
        info = delim.join([" " + line[2:] for line in lines if line[0] == '\t'])
        phones = delim.join(
                [num.group().replace("|", ";")
                for num in OrganisationObject.re_extract_info.finditer(info)])
        urls = OrganisationObject.re_extract_info.split(info)[-1]
        return f"{self.name}{delim}{description}{delim}{phones}{urls}\n
def visitor_body_fonts(text, cm, tm, font_dict, font_size):
    # do once, create list of fonts
    global font_list, font_count
    if (not font_dict is None and text):
        # skip page numbers and "empty" strings
        if OrganisationObject.is_empty_str(text):
            return
        if font_dict["/BaseFont"] not in font_list:
            # add new font
            font_list.append(font_dict["/BaseFont"])
def visitor_body_text(text, cm, tm, font_dict, font_size):
    # do for all pages, extract text according to
    # positions of fonts in font_list
    font = font_dict["/BaseFont"] if font_dict is not None else False
    if (not OrganisationObject.is_empty_str(text)
            and font in font_list):
        font_index = font_list.index(font)
        xpos = tm[3]
        #ypos = tm[4]

        # organisation header
        if xpos == OrganisationObject.header_pos:
            if font_index != font_index_prev:
                organisation_list.append(organisation) # save previous organisation object
                organisation = OrganisationObject() # create new organisation object
            organisation.name += text + " "
        # organisation body
        elif xpos == OrganisationObject.body_pos:
            if font_index == 0: # sub organisation header
                organisation.description += (
                    font_index_is_switched(
                        font_index, font_index_prev, "\n\t" # insert prefix
                    ) + text + " ")
            elif font_index == 1: # organisation body
                organisation.description += (
                    font_index_is_switched(
                        font_index, font_index_prev, "\n"
                    ) + text + " ")
            elif font_index == 2: # organisation info
                organisation.description += "\n\t\t" + text
                 
        font_index_prev = font_index
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("pdf_file", action="store", help="string: path to pdf file to parse")
    parser.add_argument("-p", action="store", default=0,
help="int: page number from pdf file at which the organisations are printed (1st page is '0'); default is '0';")
    args = parser.parse_args()

    reader = pypdf.PdfReader(args.pdf_file)
    pages = reader.pages[int(args.p):]
    # global vars; modified only in visitor_body() methods
    font_list = []
    font_index_prev = 0
    organisation = OrganisationObject()
    organisation_list = []

    # populate font_list
    pages[0].extract_text(visitor_text=visitor_body_fonts)
    # 1st font: header (organisation name)
    # 2nd font: organisation description (plain text)
    # 3rd font: organisation info (addresses, phone numbers)
    font_list = font_list[-3:] # keep 3 last, important fonts

    for page in pages:
        # populate organisation_list
        page.extract_text(visitor_text=visitor_body_text2)

    for org in organisation_list:
#        print(org.to_str())   
        print(org.to_csv("|"), end="")
