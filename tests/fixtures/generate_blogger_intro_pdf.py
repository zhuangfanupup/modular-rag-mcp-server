"""
Generate a PDF for blogger introduction and notes overview.
Contains personal introduction, notes description, and sample images.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
import io
from pathlib import Path
import os


def register_chinese_font():
    """Register a Chinese font for PDF generation."""
    # Try to find a Chinese font on the system
    font_paths = [
        # Windows fonts
        "C:/Windows/Fonts/msyh.ttc",  # 寰蒋闆呴粦
        "C:/Windows/Fonts/simsun.ttc",  # 瀹嬩綋
        "C:/Windows/Fonts/simhei.ttf",  # 榛戜綋
        # Mac fonts
        "/System/Library/Fonts/PingFang.ttc",
        # Linux fonts
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                return 'ChineseFont'
            except:
                continue
    
    # Fallback to Helvetica if no Chinese font found
    return 'Helvetica'


def get_image_paths():
    """Get paths for the external images."""
    script_dir = Path(__file__).parent
    sample_docs_dir = script_dir / "sample_documents"
    
    return {
        'design_thinking': sample_docs_dir / "design_thinking.png",
        'project_intro': sample_docs_dir / "project_intro.png"
    }


def generate_blogger_intro_pdf(output_path):
    """Generate a PDF document with blogger introduction."""
    
    # Register Chinese font
    chinese_font = register_chinese_font()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=30,
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles with Chinese font
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontName=chinese_font,
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=12,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=chinese_font,
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=18
    )
    
    list_style = ParagraphStyle(
        'ListStyle',
        parent=styles['BodyText'],
        fontName=chinese_font,
        fontSize=11,
        leftIndent=20,
        spaceAfter=8,
        leading=16
    )
    
    # ==================== 灏侀潰椤?====================
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("涓嶈浆鍒板ぇ妯″瀷涓嶆敼鍚?, title_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("鍗氫富浠嬬粛 & 绗旇璇存槑", heading_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # 灏侀潰淇℃伅琛ㄦ牸
    cover_data = [
        ['浣滆€?', '涓嶈浆鍒板ぇ妯″瀷涓嶆敼鍚?],
        ['骞冲彴:', '灏忕孩涔?+ B绔?],
        ['鏂瑰悜:', '澶фā鍨嬪紑鍙?],
        ['鏂囨。鐗堟湰:', '2026骞?鏈?],
    ]
    cover_table = Table(cover_data, colWidths=[1.5*inch, 3.5*inch])
    cover_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
    ]))
    elements.append(cover_table)
    elements.append(PageBreak())
    
    # ==================== 绗竴閮ㄥ垎锛氫釜浜轰粙缁?====================
    elements.append(Paragraph("1. 涓汉浠嬬粛", heading_style))
    
    intro_text = """
    灏忕孩涔?+ B绔欏崥涓伙紝鍙?85瀛﹀巻锛屾牎鎷涙瘯涓氬悗杩涘叆鍥藉唴涓€绾垮ぇ鍘傦紝鐩墠灏辫亴浜庡浼佷竴绾垮ぇ鍘傘€備富瑕佸紑鍙戣瑷€鏄疌++銆?
    """
    elements.append(Paragraph(intro_text.strip(), body_style))
    
    achievement_text = """
    閫氳繃鑷锛屼粠0AI鍩虹鍑哄彂锛岃嚜瀛︽帉鎻′簡Agent銆丷AG绛夋妧鏈紝鎴愬姛鎷垮埌浜?涓ぇ妯″瀷鐨刼ffer锛屽叾涓寘鎷細
    """
    elements.append(Paragraph(achievement_text.strip(), body_style))
    
    # Offer鍒楄〃
    milestones = [
        "浜笢锛堢畻娉曞矖锛?,
        "鍗冮棶C绔?,
        "缃戦緳",
        "SAP锛堜笘鐣?00寮哄浼侊級",
        "骞冲畨璇佸埜",
        "鍗庢灄璇佸埜"
    ]
    for item in milestones:
        elements.append(Paragraph(f"鈥?{item}", list_style))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # ==================== 绗簩閮ㄥ垎锛氱瑪璁颁粙缁?====================
    elements.append(Paragraph("2. 绗旇浠嬬粛", heading_style))
    
    notes_intro = """
    涓嶈浆鍒板ぇ妯″瀷涓嶆敼鍚嶅湪鑷鐨勮繃绋嬩腑锛屾妸鎵€鏈夎嚜瀛﹁繃绋嬩腑閬囧埌鐨勯棶棰橈紝鎬荤粨鍦ㄤ簡鏂囨。涓€傜洰鍓嶆枃妗ｅ凡缁忔湁12涓囧瓧銆?
    """
    elements.append(Paragraph(notes_intro.strip(), body_style))
    
    design_concept = """
    鏂囨。璁捐鐨勭悊蹇垫槸锛氶拡瀵逛簬0鍩虹瀛﹀憳锛屼互搴旂敤鏂瑰悜涓轰富锛岀畻娉曟柟鍚戜负杈呭姪锛屽府鍔?鍩虹鐨勫悓瀛﹀揩閫熻浆琛屽埌澶фā鍨嬨€?
    绗旇璁捐鐨勬渶澶х殑鐞嗗康鏄細<b>绐佸嚭閲嶇偣锛岃娓呮姣忎釜鐭ヨ瘑鐐逛负浠€涔堣鑰冿紝鎬庝箞澶嶄範锛岃澶嶄範澶氭繁鍏ャ€?/b>
    """
    elements.append(Paragraph(design_concept.strip(), body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ==================== 绗旇鍐呭璇﹁В ====================
    elements.append(Paragraph("绗旇鍐呭鍖呮嫭锛?, subheading_style))
    
    # 2.1 闈㈣瘯鐪熼
    elements.append(Paragraph("<b>2.1 闈㈣瘯鐪熼锛?0+鍏徃锛?/b>", body_style))
    case_content = """
    鍖呭惈瀹屾暣鐨勫矖浣岼D锛堝府鍔╁ぇ瀹舵湁閽堝鎬у涔狅級銆侀棶棰樿В鏋愩€佸弬鑰冭祫鏂欍€佷釜浜哄弽鎬濄€佽棰戣瑙ｃ€?
    """
    elements.append(Paragraph(case_content.strip(), list_style))
    
    # 2.2 鍏偂鍐呭
    elements.append(Paragraph("<b>2.2 鍏偂鍐呭</b>", body_style))
    bagu_content = """
    娑电洊Agent銆丷AG銆佹ā鍨嬪熀纭€銆佸井璋冦€佹帹鐞嗛儴缃茬瓑鍐呭銆傛渶閲嶈鐨勬€濇兂鏄畬鍏ㄦ牴鎹潰璇曞唴瀹癸紝
    閽堝鎬ф€荤粨鍏偂鈥斺€旈潰璇曞父鑰冪殑灏辨€荤粨鐨勬繁鍏ワ紝涓嶅父鑰冪殑灏辨€荤粨鐨勫皯锛岀獊鍑洪噸鐐瑰拰鎬濊矾锛?
    涓嶆兂璁╄浆琛岀殑浜洪櫡鍏?鎰熻浠€涔堥兘瑕佸锛屼笉鐭ラ亾瀛﹀娣?鐨勫洶澧冦€?
    """
    elements.append(Paragraph(bagu_content.strip(), list_style))
    
    # 2.3 椤圭洰
    elements.append(Paragraph("<b>2.3 鑷爺RAG椤圭洰</b>", body_style))
    project_content = """
    鑷爺浜嗕竴涓猂AG椤圭洰锛屽寘鍚畬鏁寸殑椤圭洰鎶€鏈紑鍙戞枃妗ｅ拰浠ｇ爜銆傞」鐩笉鍏夋€荤粨璇ラ」鐩父瑙佺殑闈㈣瘯闂鍜岃В鏋愩€?
    绠€鍘嗗浣曞啓銆侀」鐩璁＄殑浠ｇ爜鍜屾妧鏈瑙ｃ€傛洿閲嶈鐨勬槸鎬荤粨璁茶В鑷繁鍐欓」鐩殑鎬濊矾锛屼笉鍏夋彁渚涢」鐩紝
    鏇撮噸瑕佹彁渚涘啓椤圭洰鐨勬€濊矾锛屽浼氫互鍚庝篃鑳借交鏉炬墿灞曘€傚悓鏍疯鍐呭鍖呭惈瑙嗛璁茶В銆?
    """
    elements.append(Paragraph(project_content.strip(), list_style))
    
    # 2.4 鍙傝€冭祫鏂?
    elements.append(Paragraph("<b>2.4 鍙傝€冭祫鏂?/b>", body_style))
    reference_content = """
    灏嗚嚜瀛﹁繃绋嬩腑閬囧埌鐨勫ソ鐨勫弬鑰冭祫鏂欍€佽棰戯紝鎬荤粨鍦ㄦ枃妗ｄ腑銆傝澶у鍋氬埌鍙鐓х潃绗旇瀛﹀氨鍙互銆?
    """
    elements.append(Paragraph(reference_content.strip(), list_style))
    
    # 2.5 鎸佺画鏇存柊
    elements.append(Paragraph("<b>2.5 鎸佺画鏇存柊</b>", body_style))
    update_content = """
    浠庢枃妗ｄ笂绾跨洰鍓嶅凡缁忔洿鏂颁簡2涓鏈堜簡銆傚崥涓绘瘡澶╀笅鐝氨鍦ㄦ暣鐞嗙瑪璁帮紝鍋氬埌鍜屽ぇ瀹朵竴璧峰涔犮€?
    杩囧畬骞翠篃浼氭洿鏂版洿澶氶潰缁忋€佺畻娉曠浉鍏冲唴瀹癸紝鎸佺画鏇存柊锛屽叡鍚岃繘姝ワ紝浣嗕粠鏈定浠枫€?
    """
    elements.append(Paragraph(update_content.strip(), list_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # 浠锋牸淇℃伅
    price_info = """
    <b>绗旇鐩墠鍦ㄥ皬绾功閾炬帴鍞崠锛屼环鏍?99鍏冦€?/b>
    """
    elements.append(Paragraph(price_info, body_style))
    
    elements.append(PageBreak())
    
    # ==================== 鍥剧墖1锛氳璁℃€濊矾 ====================
    elements.append(Paragraph("鍥剧墖1锛氳璁℃€濊矾", heading_style))
    
    # Get image paths
    image_paths = get_image_paths()
    
    # Add design thinking image (use external image)
    design_img_path = image_paths['design_thinking']
    if design_img_path.exists():
        # Calculate appropriate size while maintaining aspect ratio
        with PILImage.open(design_img_path) as pil_img:
            orig_width, orig_height = pil_img.size
            # Max width is 6 inches, calculate height to maintain ratio
            max_width = 6 * inch
            aspect_ratio = orig_height / orig_width
            img_width = min(max_width, orig_width * 0.8)  # Scale down if needed
            img_height = img_width * aspect_ratio
            # Cap max height
            if img_height > 7 * inch:
                img_height = 7 * inch
                img_width = img_height / aspect_ratio
        
        img_flowable1 = Image(str(design_img_path), width=img_width, height=img_height)
        elements.append(img_flowable1)
    else:
        elements.append(Paragraph(f"[鍥剧墖鏈壘鍒? {design_img_path}]", body_style))
    
    elements.append(PageBreak())
    
    # ==================== 鍥剧墖2锛氶」鐩粙缁?====================
    elements.append(Paragraph("鍥剧墖2锛氶」鐩粙缁?, heading_style))
    
    # Add project intro image (use external image)
    project_img_path = image_paths['project_intro']
    if project_img_path.exists():
        # Calculate appropriate size while maintaining aspect ratio
        with PILImage.open(project_img_path) as pil_img:
            orig_width, orig_height = pil_img.size
            # Max width is 6 inches, calculate height to maintain ratio
            max_width = 6 * inch
            aspect_ratio = orig_height / orig_width
            img_width = min(max_width, orig_width * 0.8)  # Scale down if needed
            img_height = img_width * aspect_ratio
            # Cap max height
            if img_height > 7 * inch:
                img_height = 7 * inch
                img_width = img_height / aspect_ratio
        
        img_flowable2 = Image(str(project_img_path), width=img_width, height=img_height)
        elements.append(img_flowable2)
    else:
        elements.append(Paragraph(f"[鍥剧墖鏈壘鍒? {project_img_path}]", body_style))

    # Build the PDF
    doc.build(elements)
    print(f"PDF generated successfully: {output_path}")


def main():
    """Main function to generate the blogger intro PDF."""
    # Get the output path
    output_dir = Path(__file__).parent / "sample_documents"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / "blogger_intro.pdf"
    
    # Generate the PDF
    generate_blogger_intro_pdf(output_path)


if __name__ == "__main__":
    main()

