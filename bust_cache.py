import time

p = 'templates/base.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Force browser to discard cached CSS by adding version timestamp
ts = int(time.time())
c = c.replace('style.css', f'style.css?v={ts}')

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print('>>> Cache Busted Successfully! <<<')