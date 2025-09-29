import os, json, hmac, hashlib, uuid, datetime, re
from app.utility.base_object import BaseObject

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import Color

# Logos
LOGO_TOP_CENTER    = 'plugins/training/static/templates/mitreCaldera.png'
LOGO_BOTTOM_LEFT = 'plugins/training/static/templates/caldera_logo.png'

# Colors to match the screenshot
WHITE = Color(1, 1, 1)
GREY  = Color(0.85, 0.85, 0.85)
RED   = Color(0.86, 0.0, 0.0)     # Caldera-ish red



SECRET_FILE = 'plugins/training/.secret'
OUT_DIR     = 'plugins/training/generated_certificates'
INDEX_FILE  = os.path.join(OUT_DIR, 'issued.json')
TEMPLATE_BG_PNG = 'plugins/training/static/templates/caldera_cert.png'


def _ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(TEMPLATE_BG_PNG), exist_ok=True)

def _load_or_create_secret():
    _ensure_dirs()
    if os.path.exists(SECRET_FILE):
        return open(SECRET_FILE, 'rb').read()
    s = uuid.uuid4().bytes
    with open(SECRET_FILE, 'wb') as f:
        f.write(s)
    return s

def _load_index():
    _ensure_dirs()
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def _save_index(idx):
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(idx, f, indent=2)

class CertificateService(BaseObject):
    def __init__(self):
        super().__init__()
        self.secret = _load_or_create_secret()

    def _key(self, instance_id, user_id, cert_id):
        return f'{instance_id}:{user_id}:{cert_id}'

    def already_issued(self, instance_id, user_id, cert_id):
        idx = _load_index()
        return self._key(instance_id, user_id, cert_id) in idx

    def mark_issued(self, instance_id, user_id, cert_id, path, name):
        idx = _load_index()
        idx[self._key(instance_id, user_id, cert_id)] = {
            'path': path, 
            'name': name, 
            'issued_at': datetime.datetime.utcnow().isoformat()+'Z'
        }
        _save_index(idx)

    def clear_issued_for_user_cert(self, instance_id, user_id, cert_id):
        idx = _load_index()
        idx.pop(self._key(instance_id, user_id, cert_id), None)
        _save_index(idx)

    def signed_token(self, payload: str) -> str:
        sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        return f'{payload}.{sig}'

    def verify_token(self, token: str) -> str:
        try:
            payload, sig = token.rsplit('.', 1)
        except ValueError:
            return None
        exp_sig = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
        return payload if hmac.compare_digest(sig, exp_sig) else None
    
    def _safe_part(self, s: str) -> str:
        """Filesystem-safe chunk for filenames."""
        s = s.strip()
        s = re.sub(r'\s+', '_', s)                 # spaces -> underscores
        s = re.sub(r'[^A-Za-z0-9._-]', '', s)      # drop weird chars
        return s or 'User'

    def _register_fonts_if_available(self, pdfmetrics, ttfonts):
        try:
            if os.path.exists(FONT_REGULAR):
                pdfmetrics.registerFont(ttfonts.TTFont('CertRegular', FONT_REGULAR))
            if os.path.exists(FONT_BOLD):
                pdfmetrics.registerFont(ttfonts.TTFont('CertBold', FONT_BOLD))
        except Exception:
            # ignore font registration errors; we’ll fall back to Helvetica
            pass
    
    def _draw_image_keep_aspect(self, c, path, x, y, target_w=None, target_h=None):
        """Draw image at (x,y) with either target_w or target_h, preserving aspect.
        (x,y) is the lower-left corner (ReportLab coordinates)."""
        if not os.path.exists(path):
            return
        img = ImageReader(path)
        iw, ih = img.getSize()
        if target_w and not target_h:
            scale = target_w / float(iw)
            w, h = target_w, ih * scale
        elif target_h and not target_w:
            scale = target_h / float(ih)
            w, h = iw * scale, target_h
        elif target_w and target_h:
            # fit inside the box
            scale = min(target_w/iw, target_h/ih)
            w, h = iw*scale, ih*scale
        else:
            w, h = iw, ih
        c.drawImage(img, x, y, width=w, height=h, mask='auto')

    def _draw_centered(self, canvas, text, y, font_name, font_size, fill_rgb):
        from reportlab.lib.colors import Color
        c = canvas
        c.setFont(font_name, font_size)
        c.setFillColor(Color(*fill_rgb))
        page_w, _ = c._pagesize
        c.drawCentredString(page_w/2.0, y, text)
    
    def _build_pdf(self, out_pdf: str, learner_name: str, cert_title: str, date_str: str):
        # Fonts (keep your existing register fallback)
        self._register_fonts_if_available(pdfmetrics, TTFont)
        FONT_H1   = 'CertBold'    if 'CertBold'    in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'
        FONT_H2   = 'CertRegular' if 'CertRegular' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
        FONT_NAME = 'CertBold'    if 'CertBold'    in pdfmetrics.getRegisteredFontNames() else 'Helvetica-Bold'

        # Landscape letter
        page_w, page_h = landscape(letter)
        c = canvas.Canvas(out_pdf, pagesize=(page_w, page_h))

        # Background (scaled to page)
        if os.path.exists(TEMPLATE_BG_PNG):
            bg = ImageReader(TEMPLATE_BG_PNG)
            c.drawImage(bg, 0, 0, width=page_w, height=page_h)

        # Top-center MITRE|CALDERA logo
        if LOGO_TOP_CENTER and os.path.exists(LOGO_TOP_CENTER):
            logo = ImageReader(LOGO_TOP_CENTER)
            iw, ih   = logo.getSize()
            target_h = 40
            aspect   = iw / ih
            target_w = target_h * aspect
            logo_x   = (page_w - target_w) / 2
            logo_y   = page_h - target_h - 60
            c.drawImage(logo, logo_x, logo_y, width=target_w, height=target_h, mask='auto')
            # add comfortable space under the logo
            top_y = logo_y - 10
        else:
            top_y = page_h - 140

        # Bottom-left Caldera logo (larger)
        self._draw_image_keep_aspect(c, LOGO_BOTTOM_LEFT, x=24, y=28, target_h=120)

        # Title — sits just under the centered logo
        c.setFillColor(WHITE)
        c.setFont(FONT_H1, 46)
        c.drawCentredString(page_w/2.0, top_y - 33, "CERTIFICATE OF COMPLETION")

        # “This certificate is presented to:”
        c.setFillColor(GREY)
        c.setFont(FONT_H2, 16)
        c.drawCentredString(page_w/2.0, top_y - 70, "THIS CERTIFICATE IS PRESENTED TO:")

        # NAME (red, bold)
        c.setFillColor(RED)
        c.setFont(FONT_NAME, 36)
        c.drawCentredString(page_w/2.0, top_y - 120, learner_name)

        # Divider line under the name
        c.setStrokeColor(WHITE)
        c.setLineWidth(1.5)
        c.line(page_w*0.18, top_y - 136, page_w*0.82, top_y - 136)

        # “For the successful completion…” line
        c.setFillColor(GREY)
        c.setFont(FONT_H2, 16)
        line = f"FOR THE SUCCESSFUL COMPLETION OF THE {cert_title.upper()} TRAINING PLUGIN"
        c.drawCentredString(page_w/2.0, top_y - 180, line)

        # Bottom-right “CERTIFICATION DATE:” and date (aligned with bottom-left logo)
        logo_bottom   = 28                 # same y as Caldera logo bottom
        right_margin  = page_w - 28        # page right padding

        # Text settings (unchanged fonts/sizes)
        label      = "CERTIFICATION DATE:"
        label_font = FONT_H1
        label_size = 12
        date_font  = FONT_H2
        date_size  = 14
        line_gap   = 1                     # gap between the two lines

        # Measure text to size the box
        label_w = c.stringWidth(label, label_font, label_size)
        date_w  = c.stringWidth(date_str, date_font, date_size)
        max_w   = max(label_w, date_w)

        # Box geometry
        box_pad_x = 8
        box_pad_y = 8
        box_w     = max_w + (box_pad_x * 2)
        box_h     = label_size + line_gap + date_size + (box_pad_y * 2)

        # Anchor the box to the page’s right padding and the bottom-left logo’s bottom
        box_x = right_margin - box_w
        box_y = logo_bottom

        # Draw black background box (no stroke)
        c.setFillColorRGB(0, 0, 0)
        c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=0)

        # Baselines for the two lines inside the box
        label_y = box_y + box_h - box_pad_y - 8
        date_y  = label_y - (label_size + 6) 

        # Draw label (right-aligned to the inner right edge of the box)
        c.setFillColor(WHITE)
        c.setFont(label_font, label_size)
        c.drawRightString(box_x + box_w - box_pad_x, label_y, label)

        # Draw date centered under the label, inside the box
        c.setFont(date_font, date_size)
        center_x = box_x + (box_w / 2.0)
        c.drawCentredString(center_x, date_y, date_str)

        c.showPage()
        c.save()

    def issue(self, instance_id, user_id, cert_name, display_name):
        """
        Build and return a PDF path. Filename format:
        Caldera_User_Certificate_<Name>_<YYYYMMDD>.pdf
        """
        _ensure_dirs()
        safe_name = self._safe_part(display_name)
        date_tag  = datetime.datetime.now().strftime('%Y%m%d')
        base = f'Caldera_User_Certificate_{safe_name}_{date_tag}.pdf'
        out_pdf = os.path.join(OUT_DIR, base)

        # Visible strings
        display_cert_title = "MITRE Caldera™ User"

        # Render PDF
        pretty_date = datetime.datetime.now().strftime('%B %d, %Y')
        self._build_pdf(out_pdf, safe_name, display_cert_title, pretty_date)

        return out_pdf

    def get_record(self, instance_id, user_id, cert_id):
        # Return issuance record or None.
        idx = _load_index()
        return idx.get(self._key(instance_id, user_id, cert_id))