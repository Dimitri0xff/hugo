import os
import urllib.request


def download_file(url, out_path):
    request = urllib.request.urlopen(url)
    data = request.read()
    request.close()

    with open(out_path, "wb") as file:
        file.write(data)
    print('Downloaded {}'.format(out_path))

if __name__ == '__main__':
    # Create token file
    token = os.environ.get('HUGO_TOKEN')
    if token:
        with open('token.txt', 'w') as token_file:
            token_file.write(token)
        print('Done writing token file')
    else:
        print('Warning: token environment variable not set')

    # Download conifg files
    download_file('https://www.dropbox.com/s/633or3g69zeon5a/commands.xml?dl=1', 'config/bot/commands.xml')
