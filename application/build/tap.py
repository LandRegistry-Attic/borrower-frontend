import requests
from os import path, makedirs
from subprocess import call


def thisDir():
    return path.dirname(path.realpath(__file__))


def latest_release():
    url = 'https://api.github.com/repos/alphagov/govuk_template/releases'
    response = requests.get(url)
    return response.json()[0]


def mustache_asset(release):
    assets_url = release['assets_url']
    response = requests.get(assets_url)
    response.json
    mustache_assets = []
    for asset in response.json():
        if asset['name'].startswith('mustache_govuk_template'):
            mustache_assets.append(asset)

    return mustache_assets[0]


def jinja_asset(release):
    assets_url = release['assets_url']
    response = requests.get(assets_url)
    response.json
    mustache_assets = []
    for asset in response.json():
        if asset['name'].startswith('jinja_govuk_template'):
            mustache_assets.append(asset)

    return mustache_assets[0]


def download(asset):
    local_filepath = './zip/' + asset['name']
    response = requests.get(asset['browser_download_url'], stream=True)
    if not path.exists(path.dirname(local_filepath)):
        makedirs(path.dirname(local_filepath))
    with open(local_filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

    print('Downloaded ' + asset['name'] + ' to ' + local_filepath)

    return local_filepath


def download_mustache():
    release = latest_release()
    mustache = mustache_asset(release)
    path = download(mustache)
    copy_assets(path)
    copy_views(path, 'mustache')


def download_jinja():
    release = latest_release()
    jinja = jinja_asset(release)
    path = download(jinja)
    copy_assets(path)
    copy_views(path, 'jinja')


def unzip_path(tar_path):
    unzipped_folder = path.basename(tar_path).replace('.tgz', '')
    unzipped_path = thisDir() + "/zip/" + unzipped_folder
    return unzipped_path


def unzip(tar_path):
    target_path = thisDir() + "/zip"
    print('Unpacking ' + tar_path + ' to ' + target_path)
    call(["tar", "-xf", tar_path, "-C", target_path])


def copy_views(tar_path, name):
    unzipped_path = unzip_path(tar_path)
    source_view = unzipped_path + '/views/layouts/govuk_template.html'
    target_view = '../application/templates/base/govuk_base_template.html'

    if not path.exists(unzipped_path):
        unzip(tar_path)
    if not path.exists(path.dirname(target_view)):
        makedirs(path.dirname(target_view))

    call(["cp", "-f", source_view, target_view])
    print('Copied ' + source_view + ' to ' + target_view)


def copy_assets(tar_path):
    unzipped_path = unzip_path(tar_path)
    assets_path = '../application/static/govuk_template'

    if not path.exists(unzipped_path):
        unzip(tar_path)
    call(["cp", "-rf", unzipped_path + "/assets", assets_path])

    print('Copied ' + unzipped_path + '/assets to ' + assets_path)


download_jinja()
