import csv
import collections
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import binomtest, mannwhitneyu, chi2_contingency

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "..", "evidence")
A = os.path.join(EV, "study_A_attention_ablation")
B = os.path.join(EV, "study_B_commitment_repair")
C = os.path.join(EV, "study_C_confidence_and_identity")

ledger = []


def check(study, claim, thesis_value, computed, tol=0.0):
    ok = abs(float(thesis_value) - float(computed)) <= tol
    ledger.append((study, claim, thesis_value, computed, "PASS" if ok else "FAIL"))


def mcnemar_exact(b, c):
    return binomtest(min(b, c), b + c, 0.5).pvalue if b + c else 1.0


def kappa(x, y):
    x, y = np.asarray(x), np.asarray(y)
    cats = sorted(set(x) | set(y))
    po = np.mean(x == y)
    pe = sum(np.mean(x == k) * np.mean(y == k) for k in cats)
    return (po - pe) / (1 - pe)


def study_a():
    krows = list(csv.DictReader(open(os.path.join(A, "data", "model_key.csv"), encoding="utf-8")))
    key = {r["response_id"]: r["true_model"] for r in krows}
    kitem = {r["response_id"]: r["item_id"] for r in krows}
    an = {}
    for name in ("annotator_A", "annotator_B"):
        an[name] = {r["response_id"]: int(r["failure_type"]) for r in csv.DictReader(open(os.path.join(A, "data", name + ".csv"), encoding="utf-8"))}
    ids = sorted(an["annotator_A"])
    k = kappa([an["annotator_A"][i] for i in ids], [an["annotator_B"][i] for i in ids])
    agree = sum(an["annotator_A"][i] == an["annotator_B"][i] for i in ids)
    check("A", "Free recall: responses double-scored", 400, len(ids))
    check("A", "Free recall: raw agreement (of 400)", 395, agree)
    check("A", "Free recall: Cohen's kappa", 0.85, round(k, 2))
    item = collections.defaultdict(dict)
    for i in ids:
        item[kitem[i]][key[i]] = an["annotator_A"][i]
    P, M = "EleutherAI/pythia-2.8b", "state-spaces/mamba-2.8b-hf"
    check("A", "Free recall: Pythia-2.8B correct of 200", 3, sum(v[P] == 0 for v in item.values()))
    check("A", "Free recall: Mamba-2.8B correct of 200", 3, sum(v[M] == 0 for v in item.values()))
    po = sum(v[P] == 0 and v[M] != 0 for v in item.values())
    mo = sum(v[M] == 0 and v[P] != 0 for v in item.values())
    check("A", "Free recall: paired McNemar p on correctness", 1.0, round(mcnemar_exact(po, mo), 3))
    check("A", "Free recall: factual error on the same questions", 182, sum(v[P] == 1 and v[M] == 1 for v in item.values()))

    rows = list(csv.DictReader(open(os.path.join(A, "study1b", "results", "scored_items.csv"), encoding="utf-8")))
    by = collections.defaultdict(dict)
    for r in rows:
        by[r["model"]][r["item_id"]] = r
    check("A", "Context probe: models run", 14, len(by))
    check("A", "Context probe: items per model", 999, min(len(v) for v in by.values()))
    pairs = [("pythia-160m", "mamba-130m-hf"), ("pythia-410m", "mamba-370m-hf"), ("pythia-1b", "mamba-790m-hf"),
             ("pythia-1.4b", "mamba-1.4b-hf"), ("pythia-2.8b", "mamba-2.8b-hf")]
    fig = {"pairs": [], "known": [], "support": []}
    claims_all = {"pythia-410m": (646, 427), "pythia-1b": (653, 542), "pythia-1.4b": (648, 186), "pythia-2.8b": (650, 566), "pythia-160m": (312, 271)}
    base = {m: {r["fact_id"]: r["label"] == "correct" for r in d.values() if r["condition"] == "baseline"} for m, d in by.items()}
    for p, m in pairs:
        pm, mm = "EleutherAI/" + p, "state-spaces/" + m
        conf = [i for i, r in by[pm].items() if r["condition"] == "conflict"]
        fp = sum(by[pm][i]["label"] == "followed" for i in conf)
        fm = sum(by[mm][i]["label"] == "followed" for i in conf)
        a = sum(by[pm][i]["label"] == "followed" and by[mm][i]["label"] != "followed" for i in conf)
        b = sum(by[mm][i]["label"] == "followed" and by[pm][i]["label"] != "followed" for i in conf)
        pv = mcnemar_exact(a, b)
        check("A", f"Conflict items followed, {p}", claims_all[p][0], fp)
        check("A", f"Conflict items followed, {m}", claims_all[p][1], fm)
        kn = {f for f in base[pm] if base[pm][f] and base[mm][f]}
        ids = [i for i, r in by[pm].items() if r["condition"] == "conflict" and r["length"] == "long" and r["fact_id"] in kn]
        kp = sum(by[pm][i]["label"] == "followed" for i in ids)
        km = sum(by[mm][i]["label"] == "followed" for i in ids)
        ka = sum(by[pm][i]["label"] == "followed" and by[mm][i]["label"] != "followed" for i in ids)
        kb = sum(by[mm][i]["label"] == "followed" and by[pm][i]["label"] != "followed" for i in ids)
        sup = {}
        for mod in (pm, mm):
            s = [r for r in by[mod].values() if r["condition"] == "support" and r["length"] == "long"]
            sup[mod] = (sum(r["label"] == "correct" for r in s), len(s))
        fig["pairs"].append({"pair": p.replace("pythia-", "").upper() + " / " + m.replace("mamba-", "").replace("-hf", "").upper(),
                             "pythia": fp, "mamba": fm, "n": len(conf), "disc": [a, b], "p": pv})
        fig["known"].append({"pair": p, "n": len(ids), "pythia": kp, "mamba": km, "disc": [ka, kb], "p": mcnemar_exact(ka, kb)})
        fig["support"].append({"pair": p, "pythia": sup[pm], "mamba": sup[mm]})
        if p == "pythia-2.8b":
            check("A", "2.8B discordant (attention only)", 90, a)
            check("A", "2.8B discordant (state-space only)", 6, b)
            check("A", "2.8B McNemar p (x1e-20)", 2.5, round(pv / 1e-20, 1))
            check("A", "2.8B known facts, items", 279, len(ids))
            check("A", "2.8B known facts, Pythia followed", 264, kp)
            check("A", "2.8B known facts, Mamba followed", 210, km)
            check("A", "2.8B known facts McNemar p (x1e-13)", 9.0, round(mcnemar_exact(ka, kb) / 1e-13, 1))
            check("A", "2.8B support (true line) Mamba correct, long", 110, sup[mm][0])
        if p == "pythia-1.4b":
            check("A", "1.4B discordant (attention only)", 462, a)
            check("A", "1.4B discordant (state-space only)", 0, b)
    rate = lambda mod: 100 * np.mean([r["label"] == "followed" for r in by[mod].values() if r["condition"] == "conflict" and r["length"] == "long"])
    exp_disc = {"pythia-160m": (152, 111, 0.0135), "pythia-410m": (228, 9, 5.25e-56), "pythia-1b": (113, 2, 3.21e-31), "pythia-1.4b": (462, 0, 1.68e-139), "pythia-2.8b": (90, 6, 2.5e-20)}
    exp_known = {"pythia-410m": (87, 80, 28, 2.3e-13), "pythia-1b": (78, 73, 40, 2.3e-10), "pythia-1.4b": (243, 235, 63, 3.3e-52), "pythia-2.8b": (279, 264, 210, 9.0e-13), "pythia-160m": (15, 8, 14, 0.031)}
    for (p, m), f, k in zip(pairs, fig["pairs"], fig["known"]):
        e = exp_disc[p]
        check("A", f"{p}/{m}: discordant, attention only", e[0], f["disc"][0])
        check("A", f"{p}/{m}: discordant, state space only", e[1], f["disc"][1])
        check("A", f"{p}/{m}: McNemar p (mantissa)", float(f"{e[2]:.2e}".split("e")[0]), float(f"{f['p']:.2e}".split("e")[0]), tol=0.011)
        q = exp_known[p]
        check("A", f"{p}/{m}: known-fact items (long)", q[0], k["n"])
        check("A", f"{p}/{m}: known facts, attention followed", q[1], k["pythia"])
        check("A", f"{p}/{m}: known facts, state space followed", q[2], k["mamba"])
        check("A", f"{p}/{m}: known facts p (mantissa)", float(f"{q[3]:.1e}".split("e")[0]), float(f"{k['p']:.1e}".split("e")[0]), tol=0.11)
    sl = {}
    for L in ("short", "long"):
        ids = [i for i, r in by["EleutherAI/pythia-2.8b"].items() if r["condition"] == "conflict" and r["length"] == L]
        sl[L] = (sum(by["EleutherAI/pythia-2.8b"][i]["label"] == "followed" for i in ids), sum(by["state-spaces/mamba-2.8b-hf"][i]["label"] == "followed" for i in ids))
    check("A", "2.8B short texts: attention followed (of 333)", 332, sl["short"][0])
    check("A", "2.8B short texts: state space followed (of 333)", 312, sl["short"][1])
    check("A", "2.8B long texts: attention followed (of 333)", 318, sl["long"][0])
    check("A", "2.8B long texts: state space followed (of 333)", 254, sl["long"][1])
    prior = lambda mod: 100 * np.mean([r["label"] == "correct" for r in by[mod].values() if r["condition"] == "baseline"])
    check("A", "Pythia-2.8B knew fact without context (%)", 85.6, round(prior("EleutherAI/pythia-2.8b"), 1))
    check("A", "Mamba-2.8B knew fact without context (%)", 92.8, round(prior("state-spaces/mamba-2.8b-hf"), 1))
    fr = {"EleutherAI/pythia-2.8b": (187, 7, 3), "state-spaces/mamba-2.8b-hf": (195, 0, 2)}
    for mod, (fe, ab, dg) in fr.items():
        vals = [v[mod] for v in item.values()]
        check("A", f"Free recall {mod.split('/')[1]}: factual errors", fe, vals.count(1))
        check("A", f"Free recall {mod.split('/')[1]}: abstentions", ab, vals.count(2))
        check("A", f"Free recall {mod.split('/')[1]}: degenerate", dg, vals.count(3))
    check("A", "Free recall: McNemar p on factual error", 0.096, round(mcnemar_exact(5, 13), 3))
    check("A", "Free recall: factual error only Pythia", 5, sum(v[P] == 1 and v[M] != 1 for v in item.values()))
    check("A", "Free recall: factual error only Mamba", 13, sum(v[M] == 1 and v[P] != 1 for v in item.values()))
    others = ["Qwen/Qwen2.5-0.5B", "Qwen/Qwen2.5-1.5B", "Qwen/Qwen2.5-3B", "HuggingFaceTB/SmolLM2-1.7B"]
    check("A", "Other attention models: lowest long follow rate (%)", 98.8, round(min(rate(m) for m in others), 1))
    check("A", "Mamba long follow rate at 1.4B (%)", 29.4, round(rate("state-spaces/mamba-1.4b-hf"), 1))
    check("A", "Mamba long follow rate at 2.8B (%)", 76.3, round(rate("state-spaces/mamba-2.8b-hf"), 1))
    for p, m in pairs[1:]:
        f = next(x for x in fig["pairs"] if x["pair"].startswith(p.replace("pythia-", "").upper()))
        check("A", f"Attention model follows more, {p} (1 = yes)", 1, int(f["pythia"] > f["mamba"] and f["p"] < 1e-5))
    att = [m for m in by if not m.startswith("state-spaces")]
    ssm = [m for m in by if m.startswith("state-spaces")]
    ra, rs = [rate(x) for x in att], [rate(x) for x in ssm]
    check("A", "Group mean long follow rate, attention (%)", 91.1, round(np.mean(ra), 1))
    check("A", "Group mean long follow rate, state-space (%)", 52.9, round(np.mean(rs), 1))
    check("A", "Group Mann-Whitney p", 0.007, round(mannwhitneyu(ra, rs, alternative="two-sided").pvalue, 3))
    fig["group"] = {"attention": {m.split("/")[1]: round(rate(m), 1) for m in att}, "ssm": {m.split("/")[1]: round(rate(m), 1) for m in ssm}}
    return fig


def study_b():
    def load(path):
        it = collections.defaultdict(dict)
        for r in csv.DictReader(open(path, encoding="utf-8")):
            it[(r["item_id"], r["model"])][r["condition"]] = r
        return it

    def refused(r):
        return r["abstain"].strip() in ("1", "1.0")

    def err(r):
        if r["condition"] in ("b_substituted", "d_control") and refused(r):
            return None
        return int(float(r["n_downstream_failing"]) > 0)

    out = {}
    for tag, fname in (("A", "annotator_A.csv"), ("B", "annotator_B.csv")):
        it = load(os.path.join(B, "data", fname))
        pr = [(err(v["a_baseline"]), err(v["b_substituted"])) for v in it.values()]
        pr = [x for x in pr if x[1] is not None]
        before = np.mean([x[0] for x in pr])
        after = np.mean([x[1] for x in pr])
        fixed = sum(x == (1, 0) for x in pr)
        broken = sum(x == (0, 1) for x in pr)
        bd = [(err(v["b_substituted"]), err(v["d_control"])) for v in it.values()]
        bd = [x for x in bd if None not in x]
        bfree = np.mean([x[0] == 0 for x in bd])
        dfree = np.mean([x[1] == 0 for x in bd])
        bb = sum(x == (0, 1) for x in bd)
        db = sum(x == (1, 0) for x in bd)
        iso = sum(float(v["c_isolated"]["isolated_query_correct"] or 0) == 1 for v in it.values())
        per = {}
        for mod in sorted({k[1] for k in it}):
            q = [(err(v["a_baseline"]), err(v["b_substituted"])) for k, v in it.items() if k[1] == mod]
            q = [x for x in q if x[1] is not None]
            per[mod] = (len(q), 100 * np.mean([x[0] for x in q]), 100 * np.mean([x[1] for x in q]))
        out[tag] = dict(n=len(pr), before=100 * before, after=100 * after, fixed=fixed, broken=broken,
                        p=mcnemar_exact(fixed, broken), n_bd=len(bd), bfree=100 * bfree, dfree=100 * dfree,
                        bd_disc=[bb, db], p_bd=mcnemar_exact(bb, db), iso=iso, items=len(it), per=per)
    a = out["A"]
    rowsA = {(r["item_id"], r["model"], r["condition"]): r for r in csv.DictReader(open(os.path.join(B, "data", "annotator_A.csv"), encoding="utf-8"))}
    rowsB = {(r["item_id"], r["model"], r["condition"]): r for r in csv.DictReader(open(os.path.join(B, "data", "annotator_B.csv"), encoding="utf-8"))}
    dk = [k for k in rowsA if k[2] in ("a_baseline", "b_substituted", "d_control")]
    kd = kappa([int(float(rowsA[k]["n_downstream_failing"] or 0) > 0) for k in dk], [int(float(rowsB[k]["n_downstream_failing"] or 0) > 0) for k in dk])
    check("B", "Rows double-scored for downstream error", 333, len(dk))
    check("B", "Kappa, downstream error (dichotomised)", 0.94, round(kd, 2))
    ik = [k for k in rowsA if k[2] == "c_isolated"]
    check("B", "Kappa, isolated correctness", 1.0, round(kappa([rowsA[k]["isolated_query_correct"] for k in ik], [rowsB[k]["isolated_query_correct"] for k in ik]), 2))
    exp_per = {"allam-2-7b": (69, 94.2, 50.7), "openai/gpt-oss-120b": (18, 77.8, 44.4), "qwen/qwen3.6-27b": (19, 100.0, 42.1)}
    for mod, (n, bef, aft) in exp_per.items():
        check("B", f"{mod}: items", n, a["per"][mod][0])
        check("B", f"{mod}: later error before (%)", bef, round(a["per"][mod][1], 1))
        check("B", f"{mod}: later error after (%)", aft, round(a["per"][mod][2], 1))
    itA = collections.defaultdict(dict)
    for k, r in rowsA.items():
        itA[(k[0], k[1])][k[2]] = r
    succ = [v for v in itA.values() if int(float(v["a_baseline"]["n_downstream_failing"]) > 0) == 1 and not (v["b_substituted"]["abstain"].strip() in ("1", "1.0")) and float(v["b_substituted"]["n_downstream_failing"]) == 0]
    kn = sum(float(v["c_isolated"]["isolated_query_correct"] or 0) == 1 for v in succ)
    check("B", "Fully repaired items", 50, len(succ))
    check("B", "Fully repaired items known in isolation", 1, kn)
    refB = sum(v["b_substituted"]["abstain"].strip() in ("1", "1.0") for v in itA.values())
    refD = sum(v["d_control"]["abstain"].strip() in ("1", "1.0") for v in itA.values())
    check("B", "Refusals after correct fact", 5, refB)
    check("B", "Refusals after wrong fact", 12, refD)
    pr = [(float(v["a_baseline"]["n_downstream_failing"]), float(v["b_substituted"]["n_downstream_failing"])) for v in itA.values() if not v["b_substituted"]["abstain"].strip() in ("1", "1.0")]
    check("B", "Failing claims per answer before", 1.70, round(np.mean([x[0] for x in pr]), 2))
    check("B", "Failing claims per answer after", 0.75, round(np.mean([x[1] for x in pr]), 2))
    check("B", "Baseline answers that corrected themselves", 0, sum(float(v["a_baseline"]["spontaneous_correction"] or 0) == 1 for v in itA.values()))
    check("B", "Items analysed", 111, a["items"])
    check("B", "Paired items for repair test", 106, a["n"])
    check("B", "Downstream error before repair (%)", 92.5, round(a["before"], 1))
    check("B", "Downstream error after repair (%)", 48.1, round(a["after"], 1))
    check("B", "Items fixed by repair", 50, a["fixed"])
    check("B", "Items broken by repair", 3, a["broken"])
    check("B", "Repair McNemar p (x1e-12)", 5.5, round(a["p"] / 1e-12, 1))
    check("B", "Correct in isolation (of 111)", 2, a["iso"])
    check("B", "Control comparison, items", 97, a["n_bd"])
    check("B", "Error-free after correct fact (%)", 54.6, round(a["bfree"], 1))
    check("B", "Error-free after wrong fact (%)", 60.8, round(a["dfree"], 1))
    check("B", "Correct vs wrong fact McNemar p", 0.38, round(a["p_bd"], 2))
    b = out["B"]
    check("B", "Second annotator: before (%)", 97.2, round(b["before"], 1))
    check("B", "Second annotator: after (%)", 50.0, round(b["after"], 1))
    check("B", "Second annotator: McNemar p (x1e-14)", 2.35, round(b["p"] / 1e-14, 2))
    return out


def study_c_original_labels():
    s = pd.read_csv(os.path.join(C, "data", "scoring", "scoring_sadi_filled.csv"))
    t = pd.read_csv(os.path.join(C, "data", "scoring", "scoring_tasin_filled.csv"))
    key = pd.read_csv(os.path.join(C, "data", "scoring", "blind_key.csv"))
    ov = set(pd.read_csv(os.path.join(C, "data", "scoring", "kappa_overlap_uids.csv")).row_uid)
    d = pd.concat([s, t[~t.row_uid.isin(ov)]], ignore_index=True).merge(key, on="row_uid", how="left")
    check("C", "Responses in the scoring sheets", 5620, len(d))
    f = d[(d.tag == "main") & d.condition.isin(["C1", "C2", "C4", "C5"])]
    check("C", "Factual responses (142 items x 2 forms x 5 models)", 1420, len(f))
    f = f[f.correctness.isin(["correct", "incorrect"])]
    cl = f[f.condition.isin(["C1", "C2"])].correctness.eq("incorrect").mean()
    am = f[f.condition.isin(["C4", "C5"])].correctness.eq("incorrect").mean()
    check("C", "Original labels: error, clear wording (%)", 39.9, round(100 * cl, 1))
    check("C", "Original labels: error, underspecified wording (%)", 66.7, round(100 * am, 1))
    g = d[(d.tag == "main") & d.correctness.isin(["correct", "incorrect"])]
    g = g[g.confidence_tone.astype(str).isin(["1", "1.0", "2", "2.0", "3", "3.0"])]
    inc = g[g.correctness == "incorrect"]
    check("C", "Original labels: wrong answers without a hedge (%)", 77.4, round(100 * (inc.confidence_tone.astype(float) != 1).mean(), 1))
    au = d[d.tag == "auth"].copy()
    au["w"] = au.raw_output.fillna("").str.split().apply(len)
    for fr, v in (("anonymous", 188), ("patient", 259), ("physician", 268), ("researcher", 268)):
        check("C", f"Mean answer length, {fr} (words)", v, round(au[au.prompt_version == fr].w.mean()))


def main():
    fig = study_a()
    b = study_b()
    study_c_original_labels()
    fig["studyB"] = {k: {kk: (vv if not isinstance(vv, dict) else {m: list(x) for m, x in vv.items()}) for kk, vv in v.items()} for k, v in b.items()}
    out_json = os.path.join(HERE, "figure_data.json")
    json.dump(fig, open(out_json, "w"), indent=1, default=float)
    w = max(len(x[1]) for x in ledger)
    lines = [f"{'Study':5}  {'Claim':{w}}  {'Thesis':>10}  {'Recomputed':>11}  Result", "-" * (w + 45)]
    for st, cl, tv, cv, res in ledger:
        lines.append(f"{st:5}  {cl:{w}}  {str(tv):>10}  {str(cv):>11}  {res}")
    n_fail = sum(x[4] == "FAIL" for x in ledger)
    lines.append("-" * (w + 45))
    lines.append(f"{len(ledger)} checks, {len(ledger) - n_fail} passed, {n_fail} failed")
    report = "\n".join(lines)
    print(report)
    open(os.path.join(HERE, "verification_report.txt"), "w", encoding="utf-8").write(report + "\n")
    json.dump([{"study": a, "claim": b, "thesis": c, "recomputed": d, "result": e} for a, b, c, d, e in ledger], open(os.path.join(HERE, "ledger.json"), "w"), indent=1, default=float)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
