import sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET, time, json

ns = {'a': 'http://www.w3.org/2005/Atom'}

def search(q, max_results=100, sort='relevance'):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q) +
           f"&max_results={max_results}&sortBy={sort}&sortOrder=descending")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                data = r.read()
            break
        except Exception as e:
            print("ERR", e, file=sys.stderr); time.sleep(4)
    else:
        return []
    root = ET.fromstring(data)
    out = []
    for e in root.findall('a:entry', ns):
        aid = e.find('a:id', ns).text.strip().split('/abs/')[-1]
        title = ' '.join(e.find('a:title', ns).text.split())
        pub = e.find('a:published', ns).text[:10]
        summ = ' '.join(e.find('a:summary', ns).text.split())
        out.append({'id': aid, 'title': title, 'published': pub, 'year': int(pub[:4]), 'summary': summ[:400]})
    return out

queries = {
 'agent_skills_sec': 'all:"agent skills" AND all:security',
 'skill_md': 'all:"SKILL.md"',
 'mcp_security': 'all:"Model Context Protocol" AND all:security',
 'mcp_server': 'all:"MCP server"',
 'tool_poisoning': 'all:"tool poisoning"',
 'prompt_injection_tools': 'all:"prompt injection" AND all:tool',
 'skill_verification': 'all:"skill" AND all:"verification" AND all:"LLM agent"',
 'plugin_vuln': 'all:"LLM agent" AND all:"plugin" AND all:vulnerabilit',
 'tool_use_security': 'all:"tool use" AND all:"LLM" AND all:"security"',
 'capability_permissions': 'all:"capability" AND all:"permissions" AND all:"LLM agent"',
 'mcp_registry': 'all:"MCP" AND all:"registry"',
 'agent_supply_chain': 'all:"supply chain" AND all:"LLM agent"',
}

res = {}
for k, q in queries.items():
    r = search(q, 200)
    res[k] = r
    print(f"=== {k}: {len(r)} ===")
    for x in r[:25]:
        print(f"  [{x['id']}] {x['year']} {x['title']}")
    print()
    time.sleep(3.5)

json.dump(res, open('audit/arxiv_results.json','w'), indent=1)
