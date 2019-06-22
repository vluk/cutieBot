import bs4
import aiohttp
import random

async def get_amc(session):
    year = "201" + str(int(random.random() * 9))
    version = ["A", "B"][int(random.random() * 2)]
    problem_number = int(random.random() * 25)
    print({"year" : year, "version" : version, "problem": problem_number})
    problems_url = "https://artofproblemsolving.com/wiki/index.php?title={0}_AMC_12{1}_Problems".format(year, version)
    problem_soup = None
    async with session.get(problems_url) as resp:
        problem_soup = bs4.BeautifulSoup(await resp.text(), "html.parser")

    problem_page = problem_soup.find("div", {"id" : "mw-content-text"})
    problems = problem_page.find_all("h2")

    # remove false matches
    del problems[0]
    del problems[-1]

    problem = problems[problem_number]
    # go to section with raw text from header
    problem_part = problem.next_sibling.next_sibling
    problem_tex = await paragraphs(problem_part)


    answers_url = "https://artofproblemsolving.com/wiki/index.php?title={0}_AMC_12{1}_Answer_Key".format(year, version)
    answer_soup = None
    async with session.get(answers_url) as resp:
        answer_soup = bs4.BeautifulSoup(await resp.text(), "html.parser")
    answer_page = answer_soup.find("div", {"id" : "mw-content-text"})
    answers_list = [i.contents[0] for i in answer_page.find("ol").children if i != "\n"]

    answer = answers_list[problem_number].strip()

    return {"latex" : problem_tex, "answer" : answer, "year" : year, "version" : version, "problem": problem_number}

async def get_aime(session):
    year = "20{0}".format(str(random.randint(8, 18)).zfill(2))
    version = ["I", "II"][int(random.random() * 2)]
    problem_number = int(random.random() * 15)
    print({"year" : year, "version" : version, "problem": problem_number})

    problem_url = "https://artofproblemsolving.com/wiki/index.php?title={0}_AIME_{1}_Problems".format(year, version)
    problem_soup = None
    async with session.get(problem_url) as resp:
        problem_soup = bs4.BeautifulSoup(await resp.text(), "html.parser")

    problem_page = problem_soup.find("div", {"id" : "mw-content-text"})
    problems = problem_page.find_all("h2")

    # remove false matches
    del problems[0]
    del problems[-1]

    problem = problems[problem_number]
    # go to section with raw text from header
    problem_part = problem.next_sibling.next_sibling
    problem_tex = await paragraphs(problem_part)


    answers_url = "https://artofproblemsolving.com/wiki/index.php?title={0}_AIME_{1}_Answer_Key".format(year, version)
    answers_soup = None
    async with session.get(answers_url) as resp:
        answers_soup = bs4.BeautifulSoup(await resp.text(), "html.parser")
    answers_page = answers_soup.find("div", {"id" : "mw-content-text"})
    answers_list = [i.contents[0] for i in answers_page.find("ol").children if i != "\n"]

    answer = answers_list[problem_number].strip()

    return {"latex" : problem_tex, "answer" : answer, "year" : year, "version" : version, "problem": problem_number}

async def paragraphs(problem_part):
    """Parses the HTML to get the LaTeX for a problem."""
    # never tell me the odds
    problem_tex = ""
    while True:
        if isinstance(problem_part, bs4.element.Tag):
            for part in problem_part:
                if isinstance(part, bs4.element.Tag):
                    if part.name == "img":
                        problem_tex += part["alt"].replace("[asy]", "\n\\begin{center}\n\\begin{asy}\nimport graph; \nsize(5cm); defaultpen(gray(1.0));").replace("[/asy]", "\n\\end{asy}\n\\end{center}\n")
                    elif part.name == "a":
                        return problem_tex.replace("$$", "$\\$")
                    else:
                        print("oh no")
                else:
                    problem_tex += part.replace("%", "\\%")
        else:
            problem_tex += problem_part
        problem_part = problem_part.next_sibling
        problem_tex += "\n"
    print("whelp")

