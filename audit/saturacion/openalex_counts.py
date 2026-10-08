import urllib.parse, urllib.request, json, time

def oa(q, extra=""):
    url = ("https://api.openalex.org/works?filter=title_and_abstract.search:" + urllib.parse.quote(q) +
           extra + "&per-page=1&mailto=research@example.org")
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            d = json.load(r)
        return d['meta']['count']
    except Exception as e:
        return f"ERR {e}"

def oa_year(q):
    out = {}
    for y in range(2022, 2027):
        c = oa(q, f",publication_year:{y}")
        out[y] = c
        time.sleep(0.3)
    return out

qs = {
 'agent skill security': 'agent skill security',
 'MCP security': 'Model Context Protocol security',
 'tool poisoning LLM': 'tool poisoning LLM agent',
 'LLM agent plugin vulnerability': 'LLM agent plugin vulnerability',
 'agent skill verification': 'agent skill verification',
 'tool use LLM security': 'tool use LLM agent security',
 'prompt injection agent tool': 'prompt injection LLM agent tool',
 'MCP server': 'Model Context Protocol server',
 'skill benchmark LLM agent': 'skill benchmark LLM agent',
 'capability permission LLM agent': 'capability permission LLM agent',
}
for k, q in qs.items():
    total = oa(q)
    by = oa_year(q)
    print(f"{k!r}: total={total}  byyear={by}")
    time.sleep(0.3)
