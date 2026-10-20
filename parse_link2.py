import json
import re

with open("chat_link2.html", "r", encoding="utf-8") as f:
    text = f.read()

decoder = json.JSONDecoder()
# Find start of enqueue("
pos = 0
found_arrays = []
while True:
    idx = text.find('window.__reactRouterContext.streamController.enqueue(', pos)
    if idx == -1:
        break
    start_quote = text.find('"', idx)
    if start_quote != -1:
        try:
            val, end_idx = decoder.raw_decode(text[start_quote:])
            # val is a json string that contains the array
            parsed_inner = json.loads(val)
            print("Successfully decoded stream array, len:", len(parsed_inner))
            found_arrays.append(parsed_inner)
            pos = start_quote + end_idx
        except Exception as e:
            print("Error decoding:", e)
            pos = idx + 50
    else:
        break

all_interesting = []
for arr in found_arrays:
    for idx, item in enumerate(arr):
        if isinstance(item, str) and len(item) > 20:
            if any(k in item for k in ["class", "Class", "tier", "Tier", "forecast", "Forecast", "waste", "Waste", "Low", "Moderate", "High", "Critical", "Category", "category", "Table", "table", "Risk", "risk"]):
                all_interesting.append((idx, item))

print(f"Total interesting strings: {len(all_interesting)}")
with open("chat_link2_output.txt", "w", encoding="utf-8") as out:
    for idx, s in all_interesting:
        out.write(f"\n================ Index {idx} ================\n")
        out.write(s + "\n")
print("Saved to chat_link2_output.txt")

