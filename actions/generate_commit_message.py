import random

commit_types = [
    "feat",
    "fix",
    "chore",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
]

verbs = [
    "reticulated",
    "recalibrated",
    "aligned",
    "demagnetized",
    "tuned",
    "overclocked",
    "realigned",
    "reversed",
    "charged",
    "flattened",
    "boosted",
    "activated",
    "uncorked",
    "shuffled",
    "smoothed",
    "ignited",
    "reinforced",
    "randomized",
    "lubricated",
    "polished",
    "merged",
    "condensed",
    "frobnicated",
    "normalized",
    "deconflicted",
]

nouns = ["splines", "quantum stabilizer", "flux capacitors", "bitstream", "entropy harmonizer", "cache matrix", "magnetic dampeners", "RAM coils", "photon array", "quantum spaghetti", "time dilation buffer", "turbo encabulator", "data vortex", "entropy deck", "space-time interpolator", "authentication beacons", "neutron form fields", "hypertext membrane", "contextual noise filter", "dependency gears", "pixel buffer", "wormhole branches", "semantic soup", "opcode tree", "chaos engine", "asynchronous timeline"]

templates = [
    "{verb} {noun} heroically",
    "completely {verb} the {noun}",
    "accidentally {verb} the {noun}",
    "{verb} the {noun} with excessive confidence",
    "{verb} the {noun} using duct tape and magic",
    "{verb} the {noun} while ignoring the consequences",
    "almost {verb} the {noun}, but got distracted",
]


def generate_commit_message() -> str:
    commit_type = random.choice(commit_types)
    verb = random.choice(verbs)
    noun = random.choice(nouns)
    template = random.choice(templates)
    return f"{commit_type}: {template.format(verb=verb, noun=noun)}"
