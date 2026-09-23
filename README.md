synthetic Northwind conversations.

command python dialogue_ops/dialogue_stats.py data/sample.json, run from this folder.

the first four results are 
conversation count, fallback count, handoff count, and the intent dict.



curl.exe --% -i -X POST http://127.0.0.1:8000/score-turn -H "Content-Type: application/json" -d "{\"utterance\":\"I lost my card\"}"