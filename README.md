# Datasets

### NYC Census Data
https://data.cccnewyork.org/data/download#0,8,10/66,97

Note: Fips codes represent location.

Critical Note: There are aggregate rows in the dataset. There is a row for NYC, but then there are also rows for each borough
and then also each community district in each borough. 

For Median Incomes, for example, you will want to look at Household Type, since there are multiple values for each location
based on the type of household. Similar problems exist for total population by age group and ethnicity.

### NYC Transit Data
https://www.mta.info/developers

### Community Districts
Community Districts
https://boundaries.beta.nyc/?map=cd&dist=208

GeoJSON: https://www.nyc.gov/content/planning/pages/resources/datasets/community-districts

# Development

Uses the uv python package manager to install the dependencies. 

Use `uv sync` to install the dependencies and create the virtual environment.

You can select the python interpreter from `.venv` in VSCode, and then run the code in the terminal.

Use `uv add <package>` to add a new package to the project. This is preferred to using pip directly.

# Usage

Run `uv run python main.py` to run the project. This will run the main.py file in the current directory.