import urllib.parse, urllib.request, xml.etree.ElementTree as ET, time
ns = {'o':'http://a9.com/-/spec/opensearch/1.1/'}
def count(q):
    url = "https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q) + "&max_results=1"
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                root = ET.fromstring(r.read())
            return int(root.find('o:totalResults', ns).text)
        except Exception:
            time.sleep(3)
    return -1
queries = {
 'agent skills (all)': 'all:"agent skills"',
 'agent skills + security': 'all:"agent skills" AND all:security',
 'agent skills + vulnerab': 'all:"agent skills" AND all:vulnerabilit',
 'SKILL.md': 'all:"SKILL.md"',
 'MCP security': 'all:"Model Context Protocol" AND all:security',
 'tool poisoning': 'all:"tool poisoning"',
}
out=[]
for k,q in queries.items():
    tot = count(q); row=[]
    for y in range(2023,2027):
        c = count(f'({q}) AND submittedDate:[{y}01010000 TO {y}12312359]'); row.append(c); time.sleep(1)
    out.append((k,tot,row)); time.sleep(1)
    print(f"{k:26s} total={tot:5d} " + " ".join(f"{y}:{c}" for y,c in zip(range(2023,2027),row)), flush=True)
