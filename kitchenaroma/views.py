from django.http import HttpResponse
from pathlib import Path
import os

def assetlinks(request):
    file_path = Path(__file__).resolve().parent.parent
    asset_folder = os.path.join(file_path, '.well-known')
    asset_dir = os.path.join(asset_folder, 'assetlinks.json')
    f = open(asset_dir, 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")