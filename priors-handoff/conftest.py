# Placing an (empty) conftest.py at the priors-handoff root makes pytest add
# this directory to sys.path, so `from app.priors... import ...` resolves the
# same way `python -m app.priors.demo_combine` does. No fixtures needed yet.
