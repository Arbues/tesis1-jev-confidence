import urllib.parse, urllib.request, xml.etree.ElementTree as ET, time
ns = {'a': 'http://www.w3.org/2005/Atom'}
ids = ["2602.12430","2601.10338","2603.28815","2604.02837","2608.10906","2607.13987","2604.25109",
"2603.16572","2606.15899","2606.03024","2605.23951","2605.11770","2606.00925","2602.06547",
"2608.11888","2602.20156","2607.01136","2608.08453","2607.01456","2512.15144","2606.11671",
"2605.00314","2604.06550","2603.27204","2605.11418","2604.16911","2606.15242","2604.04989",
"2606.14154","2608.09577","2605.14460","2609.17274","2608.29596","2607.10113","2606.20631",
"2607.12340","2609.10962","2605.10990","2604.01687","2605.03353","2606.19191","2609.14079",
"2609.13353","2605.28588","2606.01494","2603.22447","2607.18970","2607.27309","2603.15401","2607.22520"]
out=[]
for i in range(0, len(ids), 15):
    chunk = ids[i:i+15]
    url = "https://export.arxiv.org/api/query?id_list=" + ",".join(chunk) + "&max_results=50"
    try:
        with urllib.request.urlopen(url, timeout=45) as r:
            root = ET.fromstring(r.read())
    except Exception as e:
        print("ERR", e); time.sleep(5); continue
    for e in root.findall('a:entry', ns):
        aid = e.find('a:id', ns).text.strip().split('/abs/')[-1]
        title = ' '.join(e.find('a:title', ns).text.split())
        pub = e.find('a:published', ns).text[:10]
        summ = ' '.join(e.find('a:summary', ns).text.split())
        auth = ', '.join(a.find('a:name', ns).text for a in e.findall('a:author', ns)[:4])
        cmt = e.find('{http://arxiv.org/schemas/atom}comment')
        out.append({'id': aid, 'title': title, 'year': int(pub[:4]), 'pub': pub, 'authors': auth,
                    'comment': (cmt.text if cmt is not None else ''), 'abstract': summ})
    time.sleep(3.5)
import json
json.dump(out, open('audit/key_papers.json','w'), indent=1)
for p in out:
    print(f"### [{p['id']}] {p['year']} | {p['title']}")
    print(f"AUTH: {p['authors']}")
    print(f"ABS: {p['abstract'][:700]}")
    print()
