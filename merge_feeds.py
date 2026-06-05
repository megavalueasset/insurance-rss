name: Merge RSS Feeds
on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:

jobs:
  merge:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests
      - run: mkdir -p docs && python merge_feeds.py
      - run: |
          git config user.email "bot@github.com"
          git config user.name "RSS Bot"
          git add docs/feed.xml
          git diff --staged --quiet || git commit -m "Update RSS feed"
          git push
