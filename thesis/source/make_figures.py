import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
D = json.load(open(os.path.join(HERE, "..", "..", "verification", "figure_data.json")))

ATT, SSM, GOOD, BAD, INK, MUTED, GRID = "#1F5FAD", "#D9622B", "#1B8A6B", "#C23B4E", "#1D2433", "#6B7280", "#E5E7EB"
plt.rcParams.update({
    "font.family": "Inter", "font.size": 9, "axes.edgecolor": "#9CA3AF", "axes.linewidth": 0.8,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
})


def panel(ax, letter, title):
    ax.set_title(f"({letter})  {title}", loc="left", fontsize=9.5, fontweight="bold", pad=10)


def fig_a():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.25, 1, 1]})
    ax = axs[0]
    pairs = D["pairs"]
    labels = ["160M / 130M", "410M / 370M", "1B / 790M", "1.4B / 1.4B", "2.8B / 2.8B"]
    for i, p in enumerate(pairs):
        a, m = 100 * p["pythia"] / p["n"], 100 * p["mamba"] / p["n"]
        y = len(pairs) - 1 - i
        ax.plot([m, a], [y, y], color="#CBD5E1", lw=3, solid_capstyle="round", zorder=1)
        ax.scatter([a], [y], s=46, color=ATT, zorder=3)
        ax.scatter([m], [y], s=46, color=SSM, zorder=3)
        ax.text(104, y, f"{p['pythia']}/{p['mamba']}", va="center", fontsize=7.2, color=MUTED)
    ax.set_yticks(range(len(pairs)))
    ax.set_yticklabels(labels[::-1], fontsize=8)
    ax.set_xlim(20, 122)
    ax.set_xticks([25, 50, 75, 100])
    ax.set_xlabel("planted false line repeated (% of 666)")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.scatter([], [], color=ATT, label="attention (Pythia)")
    ax.scatter([], [], color=SSM, label="state space (Mamba)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.3), fontsize=7, frameon=False, handletextpad=0.2, ncol=2, columnspacing=0.8)
    panel(ax, "a", "All conflict items")

    ax = axs[1]
    kn = [k for k in D["known"] if k["pair"] != "pythia-160m"]
    names = ["410M", "1B", "1.4B", "2.8B"]
    x = range(len(kn))
    pa = [100 * k["pythia"] / k["n"] for k in kn]
    ma = [100 * k["mamba"] / k["n"] for k in kn]
    ax.bar([i - 0.19 for i in x], pa, 0.36, color=ATT)
    ax.bar([i + 0.19 for i in x], ma, 0.36, color=SSM)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, fontsize=8)
    ax.set_ylim(0, 112)
    ax.set_ylabel("false line repeated (%)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    panel(ax, "b", "Facts both models knew")

    ax = axs[2]
    sp = [s for s in D["support"] if s["pair"] != "pythia-160m"]
    ps = [100 * s["pythia"][0] / s["pythia"][1] for s in sp]
    ms = [100 * s["mamba"][0] / s["mamba"][1] for s in sp]
    ax.bar([i - 0.19 for i in x], ps, 0.36, color=ATT)
    ax.bar([i + 0.19 for i in x], ms, 0.36, color=SSM)
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, fontsize=8)
    ax.set_ylim(0, 112)
    ax.set_ylabel("true line read correctly (%)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    panel(ax, "c", "Reading control")
    fig.tight_layout(w_pad=1.6)
    fig.savefig(os.path.join(OUT, "fig_study_a.pdf"))
    fig.savefig(os.path.join(OUT, "fig_study_a.png"), dpi=220)
    plt.close(fig)


def fig_b():
    b = D["studyB"]["A"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axs[0]
    names = {"allam-2-7b": "ALLaM-2-7B", "openai/gpt-oss-120b": "GPT-OSS-120B", "qwen/qwen3.6-27b": "Qwen3.6-27B"}
    ly = {"allam-2-7b": 56.0, "openai/gpt-oss-120b": 40.5, "qwen/qwen3.6-27b": 34.0}
    for m, (n, bef, aft) in b["per"].items():
        ax.plot([0, 1], [bef, aft], color="#94A3B8", lw=1.2, marker="o", ms=4)
        ax.plot([1.02, 1.1], [aft, ly[m]], color="#CBD5E1", lw=0.7)
        ax.text(1.12, ly[m], f"{names[m]}  {aft:.1f}%", va="center", fontsize=7, color=MUTED)
    ax.plot([0, 1], [b["before"], b["after"]], color=BAD, lw=2.6, marker="o", ms=6, zorder=3)
    ax.text(-0.05, b["before"], f"{b['before']:.1f}%", ha="right", va="center", fontsize=9, fontweight="bold", color=BAD)
    ax.plot([1.02, 1.1], [b["after"], 48.2], color=BAD, lw=0.7)
    ax.text(1.12, 48.2, f"all models  {b['after']:.1f}%", va="center", fontsize=7.5, fontweight="bold", color=BAD)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["original answer", "first wrong fact\nreplaced"], fontsize=8)
    ax.set_xlim(-0.35, 1.95)
    ax.set_ylim(30, 105)
    ax.set_ylabel("answers with a later error (%)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    panel(ax, "a", f"Repair halves later errors (n={b['n']})")

    ax = axs[1]
    vals = [b["bfree"], b["dfree"], 100 * b["iso"] / 111]
    cols = [GOOD, "#7C3AED", "#94A3B8"]
    lab = ["correct fact\ninserted", "different wrong\nfact inserted", "answered alone\n(no prefix)"]
    ax.bar(range(3), vals, 0.6, color=cols)
    txt = [f"{vals[0]:.1f}%", f"{vals[1]:.1f}%", f"{b['iso']} of 111"]
    for i, v in enumerate(vals):
        ax.text(i, v + 2.5, txt[i], ha="center", fontsize=8.5, fontweight="bold")
    ax.set_xticks(range(3))
    ax.set_xticklabels(lab, fontsize=7.5)
    ax.set_ylim(0, 80)
    ax.set_ylabel("error-free / correct (%)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    panel(ax, "b", "Any interruption works")
    fig.tight_layout(w_pad=1.8)
    fig.savefig(os.path.join(OUT, "fig_study_b.pdf"))
    fig.savefig(os.path.join(OUT, "fig_study_b.png"), dpi=220)
    plt.close(fig)


def fig_c():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1, 1.05, 1]})
    ax = axs[0]
    clear = [59.9, 38.5, 1.7]
    under = [31.8, 34.5, 33.7]
    cols = [GOOD, BAD, "#94A3B8"]
    names = ["answered correctly", "answered wrongly", "asked or declined"]
    for j, (vals) in enumerate([clear, under]):
        bottom = 0
        for k, v in enumerate(vals):
            ax.bar(j, v, 0.58, bottom=bottom, color=cols[k], label=names[k] if j == 0 else None)
            if v > 6:
                ax.text(j, bottom + v / 2, f"{v:.0f}", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
            bottom += v
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["fully\nspecified", "referent\nremoved"], fontsize=8)
    ax.set_ylim(0, 100)
    ax.set_ylabel("share of prompts (%)")
    ax.legend(fontsize=6.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=1)
    panel(ax, "a", "Missing information")

    ax = axs[1]
    groups = ["correct\nanswers", "wrong\nanswers"]
    clear_h = [8.2, 22.3]
    under_h = [16.4, 27.3]
    ax.bar([-0.19, 0.81], clear_h, 0.36, color="#64748B", label="fully specified")
    ax.bar([0.19, 1.19], under_h, 0.36, color=BAD, label="referent removed")
    for xx, v in zip([-0.19, 0.81, 0.19, 1.19], clear_h + under_h):
        ax.text(xx, v + 0.8, f"{v:.1f}", ha="center", fontsize=7.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(groups, fontsize=8)
    ax.set_ylim(0, 40)
    ax.set_ylabel("answers carrying a hedge (%)")
    ax.legend(fontsize=6.5, frameon=False, loc="upper left")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    panel(ax, "b", "Tone barely changes")

    ax = axs[2]
    fr = ["anonymous", "patient", "physician", "researcher"]
    fr_lab = ["anon.", "patient", "physician", "researcher"]
    ln = [188, 259, 268, 268]
    ax.bar(range(4), ln, 0.6, color=["#94A3B8", ATT, ATT, ATT])
    for i, v in enumerate(ln):
        ax.text(i, v + 6, str(v), ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(range(4))
    ax.set_xticklabels(fr_lab, fontsize=7, rotation=20)
    ax.set_ylim(0, 320)
    ax.set_ylabel("mean answer length (words)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    panel(ax, "c", "Who is asking")
    fig.tight_layout(w_pad=1.4)
    fig.savefig(os.path.join(OUT, "fig_study_c.pdf"))
    fig.savefig(os.path.join(OUT, "fig_study_c.png"), dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig_a()
    fig_b()
    fig_c()
