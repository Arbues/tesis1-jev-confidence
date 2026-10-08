import urllib.parse, urllib.request, xml.etree.ElementTree as ET, time
ns = {'a': 'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
def count(q):
    url = "https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q) + "&max_results=1"
    for _ in range(4):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                root = ET.fromstring(r.read())
            return int(root.find('o:totalResults', ns).text)
        except Exception as e:
            time.sleep(4)
    return -1

queries = {
 'agent skills (all)': 'all:"agent skills"',
 'agent skills + security': 'all:"agent skills" AND all:security',
 'agent skills + vulnerabilit': 'all:"agent skills" AND all:vulnerabilit',
 'SKILL.md': 'all:"SKILL.md"',
 'skill + malicious': 'all:"skill" AND all:malicious AND all:"LLM agent"',
 'skill + verification': 'all:"agent skill" AND all:verification',
 'skill + benchmark': 'all:"agent skill" AND all:benchmark',
 'MCP security': 'all:"Model Context Protocol" AND all:security',
 'MCP server': 'all:"MCP server"',
 'tool poisoning': 'all:"tool poisoning"',
 'capability permissions agent': 'all:"permission" AND all:"agent skill"',
 'skill + taxonomy/threat': 'all:"agent skill" AND all:"threat"',
}
print(f"{'query':42s} {'total':>7s}  " + "  ".join(f"{y:>6d}" for y in range(2023,2027)))
for k,q in queries.items():
    tot = count(q)
    row=[]
    for y in range(2023,2027):
        c = count(f'({q}) AND submittedDate:[{y}01010000 TO {y}12312359]')
        row.append(c); time.sleep(3.5)
    print(f"{k:42s} {tot:>7d}  " + "  ".join(f"{c:>6d}" for c in row))
    time.sleep(3.5)
