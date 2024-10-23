from utils import get_ip_address
#temporary data directory
BASE_FOLDER = 'temp'
SUBFOLDERS = ['temp_image', 'temp_pdf']
# CONVERTED_PDF_PATH= 'converted_file.pdf'
IMAGES_TYPE=['jpg', 'jpeg', 'png', 'gif','bmp','tiff','svg']
# urdu api address
URDU_API_BASE_URL = get_ip_address()
CROPS="crops"
API_KEY = "apikey1"
DOC_SUPPORTED_FORMATS = [
    'commonmark', 'creole', 'csv', 'docbook', 'docx', 'dokuwiki', 'epub', 'fb2', 'gfm',
    'haddock', 'html', 'ipynb', 'jats', 'jira', 'json', 'latex', 'man', 'markdown',
    'markdown_github', 'markdown_mmd', 'markdown_phpextra', 'markdown_strict',
    'mediawiki', 'muse', 'native', 'odt', 'opml', 'org', 'rst', 't2t', 'textile',
    'tikiwiki', 'twiki', 'vimwiki'
]
EXCEL_SUPPORTED_FORMATS = ['xls', 'xlsx', 'xlsm', 'xlsb', 'csv', 'tsv', 'ods', 'xml', 'xlam', 'xltx', 'xltm']
POWERPOINT_SUPPORTED_EXTENSIONS = ['ppt', 'pptx', 'pps', 'ppsx', 'pot', 'potx']
NOT_SUPPORTED_FORMAT = ["mp3", "wav", "aac", "flac", "ogg", "wma", "aiff", "m4a"] + ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm", "mpeg", "3gp"]


