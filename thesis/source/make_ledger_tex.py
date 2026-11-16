import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "..", "..", "verification", "ledger.json")))


def esc(t):
    t = str(t)
    for a, b in (("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"), ("_", "\\_"), ("#", "\\#"), ("$", "\\$")):
        t = t.replace(a, b)
    return t


def fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


rows = []
for x in L:
    rows.append(f"{x['study']} & {esc(x['claim'])} & {esc(fmt(x['thesis']))} & {esc(fmt(x['recomputed']))} & \\textcolor{{okgreen}}{{\\textbf{{{x['result']}}}}} \\\\")
n = len(L)
ok = sum(x["result"] == "PASS" for x in L)
head = "{\\small\n\\setlength{\\tabcolsep}{4pt}\n\\begin{longtable}{@{}cp{8.2cm}rrc@{}}\n\\toprule\nStudy & Figure checked & Thesis & Recomputed & Result\\\\\n\\midrule\n\\endfirsthead\n\\toprule\nStudy & Figure checked & Thesis & Recomputed & Result\\\\\n\\midrule\n\\endhead\n"
tail = "\\bottomrule\n\\end{longtable}\n}\n"
open(os.path.join(HERE, "ledger_table.tex"), "w", encoding="utf-8").write(head + "\n".join(rows) + "\n" + tail)
open(os.path.join(HERE, "ledger_count.tex"), "w").write(f"\\newcommand{{\\ledgertotal}}{{{n}}}\\newcommand{{\\ledgerpass}}{{{ok}}}\n")
print(n, ok)
