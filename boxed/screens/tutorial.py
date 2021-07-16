# import boxed
# from boxed.border import draw_boundary

#Gets the content of tutorial.txt and give you back a dict --> dict[heading, content_list]
def get_pages_content(file_location : str):
    heading_content_kvp = {}
    with open(file_location,"rt") as tutf:
        sections = tutf.read().split("\n\n\n")
        for mashed_content in sections:
            mashed_content_lines = mashed_content.split("\n")
            header = mashed_content_lines[0][1:-2]
            content = mashed_content_lines[1:]
            heading_content_kvp[header] = content
    return heading_content_kvp

# print(get_pages_content("../../tutorial.txt"))

"""
I couldn't write any tui code because the env didnt set up properly for me no matter what I tried (;-;)
Provided function gets you a dict which you can just call shove content into boiler plate code taken from credits.py
"""