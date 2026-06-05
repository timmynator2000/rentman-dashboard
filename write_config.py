import sys
import json
import os

# Read token from environment variable to avoid command-line truncation issues
token = os.environ.get('RENTMAN_TOKEN', '')

if not token and len(sys.argv) > 1:
    token = sys.argv[1]

if not token:
    print('  ERROR: No token provided')
    sys.exit(1)

# Strip any surrounding quotes
token = token.strip().strip('"').strip("'")

with open('config.js', 'w') as f:
    f.write('window.RENTMAN_API_TOKEN=' + json.dumps(token) + ';\n')

print('  Token saved to config.js (' + str(len(token)) + ' chars)')
print('  First 10 chars: ' + token[:10] + '...')
