import toml, sys

p = toml.load("pyproject.toml")
p.setdefault("project", {})
p["project"]["version"] = sys.argv[1]

with open("pyproject.toml", "w") as f:
    toml.dump(p, f)