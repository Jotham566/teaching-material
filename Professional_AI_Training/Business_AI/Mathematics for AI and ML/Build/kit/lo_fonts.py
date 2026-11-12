"""Make headless LibreOffice use the brand font (Lato) when it converts slides and documents to PDF.

LibreOffice run with -env:UserInstallation=<profile> reads fonts from <profile>/user/fonts; it does not reliably see the Mac's own
font folders when run headless. Without this, PDFs fall back to other fonts and some symbols (+, -, <) print wrongly in bold text."""
import shutil
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent / 'brand' / 'fonts'


def seed(user_installation_arg):
    """user_installation_arg: the '-env:UserInstallation=file:///...' argument passed to soffice."""
    url = user_installation_arg.split('=', 1)[1]
    d = Path(url.replace('file://', '', 1)) / 'user' / 'fonts'
    d.mkdir(parents=True, exist_ok=True)
    for f in FONTS.glob('Lato-*.ttf'):
        t = d / f.name
        if not t.exists():
            shutil.copy2(f, t)
