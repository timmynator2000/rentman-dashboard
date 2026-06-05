import sys
import json

token = sys.argv[1]
with open('config.js', 'w') as f:
    f.write('window.RENTMAN_API_TOKEN=' + json.dumps(token) + ';\n')

print('  Token saved to config.js (' + str(len(token)) + ' chars)')
