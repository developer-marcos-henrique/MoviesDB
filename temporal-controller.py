import plugins.extractor.scrap_working
import plugins.extractor.pos_processing
import plugins.extractor.SQLDumper
import asyncio

loop = asyncio.new_event_loop()
x = loop.run_until_complete(plugins.extractor.scrap_working.scrap_handler(search="steins").run())

output = plugins.extractor.pos_processing.filters(x).process()
print(output)