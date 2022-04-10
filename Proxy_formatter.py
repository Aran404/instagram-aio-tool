import os

def format_proxy(proxy, format):
    if format == 'user:pass:host:port':
        return str(proxy.split(':')[0]) + ':' + str(proxy.split(':')[1]) + '@' + str(proxy.split(':')[2]) + ':' + str(proxy.split(':')[3])
    elif format == 'host:port':
        return f'_:_:{proxy}'
    elif format == 'host:port@user:pass':
        return str(proxy.split('@')[1]) + '@' + str(proxy.split('@')[0])

os.system('cls' if os.name=='nt' else 'clear')

proxy_type = int(input('''
[1] user:pass:host:port
[2] host:port
[3] host:post@user:pass

[>>>] '''))

proxies = open('Proxies.txt','r').read().splitlines()

if proxy_type in [1,2,3]:
    open('Proxies.txt','w').truncate()

if proxy_type == 1:
    for proxy in proxies:
        formatted_proxy = format_proxy(proxy, 'user:pass:host:port')
        with open('Proxies.txt','a') as new_proxies:
            new_proxies.write(formatted_proxy + '\n')

elif proxy_type == 2:
    for proxy in proxies:
        formatted_proxy = format_proxy(proxy, 'host:port')
        with open('Proxies.txt','a') as new_proxies:
            new_proxies.write(formatted_proxy + '\n')

elif proxy_type == 3:
    for proxy in proxies:
        formatted_proxy = format_proxy(proxy, 'host:port@user:pass')
        with open('Proxies.txt','a') as new_proxies:
            new_proxies.write(formatted_proxy + '\n')

else:
    print('That is not a format!')
