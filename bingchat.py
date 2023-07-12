from EdgeGPT.EdgeUtils import Query, Cookie
import os

Cookie.dir_path = os.getcwd() + "/bing_cookies"

q = Query(
  "hello",
  style="creative",  # or: 'balanced', 'precise'
  ignore_cookies=True
)

for stuff in [q.output, q.sources, q.sources_dict, q.suggestions, q.code, q.code_block_formats]:
    print(stuff)
