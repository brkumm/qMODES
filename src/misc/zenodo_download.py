'''
Script from Valentino with no major modifications.

Script downloads all datasets listed in 'urlDOI' by their DOI.

Put the cript in to the directory where you would like to download the data and run it.
Make sure that you have approximately 200GB of free space.
'''
import requests
import json
import hashlib
import os
from pathlib import Path


def check_hash(filename, checksum):
    algorithm, value = checksum.split(':')
    if not os.path.exists(filename):
        return value, 'invalid'
    h = hashlib.new(algorithm)
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)
    digest = h.hexdigest()
    return value, digest



# DOIs of all data sets from Zenodo
urlDOI = {'vsf':'https://doi.org/10.5281/zenodo.12726172',
          #'scripts':'',
          'coef':'https://doi.org/10.5281/zenodo.12724196',
          'hough1':'https://doi.org/10.5281/zenodo.12749244',
          'hough2':'https://doi.org/10.5281/zenodo.12749316',
          'hough3':'https://doi.org/10.5281/zenodo.12749407',
          'hough4':'https://doi.org/10.5281/zenodo.12749482',
          'hough5':'https://doi.org/10.5281/zenodo.12751158',
          'hough6':'https://doi.org/10.5281/zenodo.12751242',
          'hough7':'https://doi.org/10.5281/zenodo.12751345',
          'hough8':'https://doi.org/10.5281/zenodo.12751416'}


# General url
url = 'https://zenodo.org/api/records/'

# Different directories
dirs = ['vsf','coef','hough1','hough2','hough3','hough4','hough5','hough6','hough7','hough8']

for i in dirs:
    # Get the information on the dataset
    response = requests.get(urlDOI[i])

    # Get the record ID
    recordID = response.url.split('/')[-1]
    recordID = recordID.strip()

    # Get the list of all files in the dataset
    r = requests.get(url + recordID)
    js = json.loads(r.text)
    files = js['files']

    # Computing total size of the dataset
    total_size = sum(f['size'] for f in files)

    # Printing some informations of the dataset
    print('Title: {}'.format(js['metadata']['title']))
    print('DOI: ' + js['metadata']['doi'])
    print('Total size: {:.1f} MB'.format(total_size / 2 ** 20))

    # Since hough functions are separated into 4 datasets (hough1, hough2, hough3, hough4) because of their size,
    # but we want them to be downloaded into the same directory, for each dataset that starts with 'h' the directory
    # name is set to 'hough'.
    if i[0] == 'h':
        i = 'hough'

    # Make directory with the name of the dataset
    outdir = i
    dir = Path(outdir)
    dir.mkdir(parents=True, exist_ok=True)

    # Go through the files in the dataset and download them
    for f in files:
        link = f['links']['self']
        size = f['size'] / 2 ** 20

        fname = f['key']
        checksum = f['checksum']

        remote_hash, local_hash = check_hash(i+'/'+fname, checksum)

        # In case donwloading stops at some point and if its restarted, this ensures for already downloaded files
        # to be skipped to save time.
        if remote_hash == local_hash:
            print(f'\t\t {fname} is already downloaded.')
            continue

        temp = requests.get(link)
        open(i+'/'+fname, 'wb').write(temp.content)
        print(f'\t\t{i}/{fname}   size: {size:.2f} MB')
    print('\n')
print('All files have been downloaded.')
