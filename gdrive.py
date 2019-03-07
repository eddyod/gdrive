import requests
from pathlib import Path


def download_from_gdrive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination, readwrite):
        CHUNK_SIZE = 32768

        with open(destination, readwrite) as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    params = {}
    params['id'] = id
    session = requests.Session()
    response = session.get(URL, params=params, stream=True)
    token = get_confirm_token(response)

    if token:
        params['confirm'] = token
    else:
        print('No token, cannot continue')
        return

    filePath = Path(destination)

    if filePath.is_file():
        resume_byte_pos = filePath.stat().st_size
        print("File", destination, " already exists, size:", resume_byte_pos)
        resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
        response = session.get(URL, params=params, stream=True, headers=resume_header)
        readwrite = "ab"
    else:
        print('File', destination, 'does not exist')
        response = session.get(URL, params=params, stream=True)
        readwrite = "wb"

    print(params)
    save_response_content(response, destination, readwrite)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 gdrive.py FILEID destination")
    else:
        # TAKE ID FROM SHAREABLE LINK
        file_id = sys.argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination = sys.argv[2]
        download_from_gdrive(file_id, destination)
