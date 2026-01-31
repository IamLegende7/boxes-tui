import toml, sys


with open("pyproject.toml", 'r') as f:
    p = toml.load(f)

p.setdefault("project", {})
p["project"]["version"] = sys.argv[1]

with open("pyproject.toml", "w") as f:
    toml.dump(p, f)