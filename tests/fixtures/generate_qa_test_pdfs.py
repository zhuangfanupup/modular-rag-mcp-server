"""Generate Chinese QA test PDF documents for QA_TEST_PLAN.

Creates three PDFs used by Section O (鏂囨。鏇挎崲涓庡鍦烘櫙楠岃瘉):
1. chinese_technical_doc.pdf  鈥?绾腑鏂囨妧鏈枃妗?(~8 椤?
2. chinese_table_chart_doc.pdf 鈥?鍚腑鏂囪〃鏍煎拰娴佺▼鍥剧殑鏂囨。 (~6 椤? 鍚浘鐗?
3. chinese_long_doc.pdf        鈥?30+ 椤典腑鏂囬暱鏂囨。

Usage:
    python tests/fixtures/generate_qa_test_pdfs.py
"""

from __future__ import annotations

import io
import os
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

_CHINESE_FONT: str | None = None


def _register_chinese_font() -> str:
    """Register a Chinese TrueType font and return its name."""
    global _CHINESE_FONT
    if _CHINESE_FONT is not None:
        return _CHINESE_FONT

    candidates = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("ChineseFont", path))
                _CHINESE_FONT = "ChineseFont"
                return _CHINESE_FONT
            except Exception:
                continue

    _CHINESE_FONT = "Helvetica"
    return _CHINESE_FONT


# ---------------------------------------------------------------------------
# Shared style factory
# ---------------------------------------------------------------------------


def _make_styles():
    font = _register_chinese_font()
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "ZH_Title", parent=base["Heading1"], fontName=font, fontSize=24,
        textColor=colors.HexColor("#1a1a1a"), spaceAfter=30, alignment=TA_CENTER,
    )
    h1 = ParagraphStyle(
        "ZH_H1", parent=base["Heading2"], fontName=font, fontSize=18,
        textColor=colors.HexColor("#2c3e50"), spaceAfter=14, spaceBefore=20,
    )
    h2 = ParagraphStyle(
        "ZH_H2", parent=base["Heading3"], fontName=font, fontSize=14,
        textColor=colors.HexColor("#34495e"), spaceAfter=10, spaceBefore=14,
    )
    body = ParagraphStyle(
        "ZH_Body", parent=base["BodyText"], fontName=font, fontSize=11,
        alignment=TA_JUSTIFY, spaceAfter=12, leading=18,
    )
    code = ParagraphStyle(
        "ZH_Code", parent=base["Code"], fontName="Courier", fontSize=9,
        spaceAfter=10, leading=13, leftIndent=20, backColor=colors.HexColor("#f5f5f5"),
    )
    caption = ParagraphStyle(
        "ZH_Caption", parent=base["Normal"], fontName=font, fontSize=9,
        alignment=TA_CENTER, textColor=colors.grey, spaceAfter=12,
    )
    return {"title": title, "h1": h1, "h2": h2, "body": body, "code": code,
            "caption": caption, "normal": base["Normal"]}


def _table_style(header_color: str = "#2c3e50"):
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, -1), _register_chinese_font()),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")]),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
    ])


def _create_chart_image(width: int, height: int, title: str, chart_type: str = "bar") -> io.BytesIO:
    """Create a simple chart-like image for embedding in PDFs."""
    img = PILImage.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # border
    draw.rectangle([2, 2, width - 3, height - 3], outline="#2c3e50", width=2)

    if chart_type == "bar":
        # simple bar chart
        bar_colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
        bar_w = width // 8
        base_y = height - 40
        for i, c in enumerate(bar_colors):
            h = 30 + (i * 25 + 40) % (height - 100)
            x0 = 40 + i * (bar_w + 15)
            draw.rectangle([x0, base_y - h, x0 + bar_w, base_y], fill=c)
    elif chart_type == "flow":
        # simple flow-chart boxes
        boxes = [
            (50, 30, 180, 70, "#3498db", "鏂囨。杈撳叆"),
            (50, 100, 180, 140, "#2ecc71", "鏂囨湰鍒嗗潡"),
            (50, 170, 180, 210, "#e74c3c", "鍚戦噺缂栫爜"),
            (220, 100, 350, 140, "#f39c12", "BM25绱㈠紩"),
            (220, 170, 350, 210, "#9b59b6", "娣峰悎妫€绱?),
        ]
        for x0, y0, x1, y1, c, _label in boxes:
            draw.rectangle([x0, y0, x1, y1], fill=c, outline="#2c3e50")
        # arrows (simple lines)
        draw.line([(130, 70), (130, 100)], fill="#2c3e50", width=2)
        draw.line([(130, 140), (130, 170)], fill="#2c3e50", width=2)
        draw.line([(180, 120), (220, 120)], fill="#2c3e50", width=2)
        draw.line([(285, 140), (285, 170)], fill="#2c3e50", width=2)
    elif chart_type == "pie":
        cx, cy, r = width // 2, height // 2, min(width, height) // 3
        slices = [(0, 120, "#3498db"), (120, 200, "#e74c3c"), (200, 280, "#2ecc71"), (280, 360, "#f39c12")]
        for start, end, c in slices:
            draw.pieslice([cx - r, cy - r, cx + r, cy + r], start, end, fill=c, outline="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ===================================================================
# 1. 绾腑鏂囨妧鏈枃妗?(~8 椤?
# ===================================================================

def generate_chinese_technical_doc(output: Path) -> None:
    doc = SimpleDocTemplate(str(output), pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=30)
    s = _make_styles()
    elems: list = []

    # 灏侀潰
    elems.append(Spacer(1, 2 * inch))
    elems.append(Paragraph("澶ц瑷€妯″瀷搴旂敤寮€鍙戞妧鏈寚鍗?, s["title"]))
    elems.append(Spacer(1, 0.3 * inch))
    elems.append(Paragraph("鈥斺€斾粠 RAG 鍒?Agent 鐨勫疄鎴樻墜鍐?, s["h2"]))
    elems.append(Spacer(1, 0.5 * inch))
    cover = [
        ["浣滆€?, "Modular RAG 椤圭洰缁?],
        ["鐗堟湰", "v1.0 鈥?2026 骞?2 鏈?],
        ["鍒嗙被", "鍐呴儴鎶€鏈枃妗?/ QA 娴嬭瘯鐢?],
    ]
    t = Table(cover, colWidths=[1.5 * inch, 4 * inch])
    t.setStyle(_table_style())
    elems.append(t)
    elems.append(PageBreak())

    # 鐩綍
    elems.append(Paragraph("鐩綍", s["h1"]))
    toc = [
        "绗竴绔? 澶ц瑷€妯″瀷鍩虹姒傚康",
        "绗簩绔? 妫€绱㈠寮虹敓鎴愶紙RAG锛夋灦鏋勮璁?,
        "绗笁绔? 鏂囨。鍒嗗潡绛栫暐璇﹁В",
        "绗洓绔? 鍚戦噺妫€绱笌娣峰悎鎼滅储",
        "绗簲绔? 閲嶆帓搴忔満鍒朵笌璇勪及鏂规硶",
        "绗叚绔? Agent 涓庡伐鍏疯皟鐢?,
        "绗竷绔? 鐢熶骇閮ㄧ讲涓庢€ц兘浼樺寲",
    ]
    for item in toc:
        elems.append(Paragraph(item, s["body"]))
    elems.append(PageBreak())

    # ---- 绗竴绔?----
    elems.append(Paragraph("绗竴绔? 澶ц瑷€妯″瀷鍩虹姒傚康", s["h1"]))
    elems.append(Paragraph(
        "澶ц瑷€妯″瀷锛圠arge Language Model, LLM锛夋槸鍩轰簬 Transformer 鏋舵瀯锛?
        "閫氳繃娴烽噺鏂囨湰鏁版嵁杩涜棰勮缁冭€屽緱鍒扮殑娣卞害绁炵粡缃戠粶銆備唬琛ㄦ€фā鍨嬪寘鎷?GPT-4銆丆laude銆?
        "DeepSeek 绛夈€侺LM 鐨勬牳蹇冩€濇兂鏄皢鑷劧璇█寤烘ā涓?Token 搴忓垪鐨勬鐜囧垎甯冿紝閫氳繃"
        "鑷洖褰掓柟寮忛€愪釜 Token 鐢熸垚鏂囨湰銆?, s["body"]))
    elems.append(Paragraph(
        "涓庝紶缁?NLP 鏂规硶鐩告瘮锛孡LM 鍏锋湁浠ヤ笅鍏抽敭浼樺娍锛?, s["body"]))
    advantages = [
        "寮哄ぇ鐨勪笂涓嬫枃鐞嗚В鑳藉姏锛岃兘澶熷鐞嗛暱鏂囨。鍜屽鏉傛寚浠?,
        "Few-shot 鍜?Zero-shot 瀛︿範鑳藉姏锛屾棤闇€澶ч噺鏍囨敞鏁版嵁",
        "璺ㄤ换鍔℃硾鍖栬兘鍔涳紝鍚屼竴妯″瀷鍙畬鎴愮炕璇戙€佹憳瑕併€丵A 绛夊绉嶄换鍔?,
        "鏀寔澶氳疆瀵硅瘽鍜屾€濈淮閾撅紙Chain-of-Thought锛夋帹鐞?,
    ]
    for a in advantages:
        elems.append(Paragraph(f"鈥?{a}", s["body"]))

    elems.append(Paragraph("1.1 Transformer 鏋舵瀯瑕佺偣", s["h2"]))
    elems.append(Paragraph(
        "Transformer 鏋舵瀯鏈€鍒濈敱 Vaswani 绛変汉鍦?2017 骞存彁鍑猴紙Attention Is All You Need锛夛紝"
        "鍏舵牳蹇冪粍浠跺寘鎷澶磋嚜娉ㄦ剰鍔涙満鍒讹紙Multi-Head Self-Attention锛夈€佸墠棣堢缁忕綉缁滐紙FFN锛夈€?
        "灞傚綊涓€鍖栵紙Layer Normalization锛夊拰娈嬪樊杩炴帴锛圧esidual Connection锛夈€傚湪 LLM 涓紝"
        "閫氬父鍙娇鐢?Decoder 閮ㄥ垎锛岄€氳繃鍥犳灉娉ㄦ剰鍔涙帺鐮佸疄鐜拌嚜鍥炲綊鐢熸垚銆?, s["body"]))
    elems.append(Paragraph(
        "娉ㄦ剰鍔涜绠楃殑鏍稿績鍏紡涓?Attention(Q,K,V) = softmax(QK^T / 鈭歞_k) V锛屽叾涓?Q銆並銆乂 "
        "鍒嗗埆浠ｈ〃鏌ヨ銆侀敭鍜屽€肩煩闃碉紝d_k 涓洪敭鍚戦噺缁村害銆傚澶存敞鎰忓姏灏嗚緭鍏ユ姇褰卞埌 h 涓笉鍚岀殑瀛愮┖闂达紝"
        "骞惰璁＄畻娉ㄦ剰鍔涘悗鎷兼帴杈撳嚭銆?, s["body"]))

    elems.append(Paragraph("1.2 Tokenization 涓庤瘝琛?, s["h2"]))
    elems.append(Paragraph(
        "鍒嗚瘝锛圱okenization锛夋槸灏嗗師濮嬫枃鏈浆鍖栦负妯″瀷鍙鐞嗙殑鏁存暟搴忓垪鐨勫叧閿楠ゃ€?
        "甯歌鐨勫瓙璇嶅垎璇嶇畻娉曞寘鎷?BPE锛圔yte Pair Encoding锛夈€乄ordPiece 鍜?SentencePiece銆?
        "涓枃鍦烘櫙涓嬶紝BPE 閫氬父灏嗘瘡涓眽瀛椾綔涓轰竴涓垨澶氫釜 Token锛屽洜姝や腑鏂囨枃鏈殑 Token 鏁伴噺"
        "寰€寰€澶氫簬绛夐暱鐨勮嫳鏂囨枃鏈€傝繖瀵?RAG 绯荤粺鐨?Chunk 澶у皬璁捐鏈夌洿鎺ュ奖鍝嶃€?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗簩绔?----
    elems.append(Paragraph("绗簩绔? 妫€绱㈠寮虹敓鎴愶紙RAG锛夋灦鏋勮璁?, s["h1"]))
    elems.append(Paragraph(
        "RAG锛圧etrieval-Augmented Generation锛夊皢淇℃伅妫€绱笌鏂囨湰鐢熸垚鐩哥粨鍚堬紝閫氳繃"
        "鍦ㄧ敓鎴愭椂寮曞叆澶栭儴鐭ヨ瘑搴撶殑鐩稿叧鏂囨。鐗囨锛屾樉钁楀噺灏?LLM 鐨勫够瑙夐棶棰橈紝鍚屾椂浣挎ā鍨?
        "鑳藉鍥炵瓟瓒呭嚭璁粌鏁版嵁鑼冨洿鐨勫疄鏃舵€ч棶棰樸€?, s["body"]))

    elems.append(Paragraph("2.1 Naive RAG vs Advanced RAG", s["h2"]))
    elems.append(Paragraph(
        "Naive RAG 閲囩敤鏈€绠€鍗曠殑銆屾绱?鎷兼帴-鐢熸垚銆嶆祦绋嬶細灏嗙敤鎴锋煡璇㈢紪鐮佷负鍚戦噺锛?
        "鍦ㄥ悜閲忔暟鎹簱涓绱?Top-K 鐩镐技鏂囨。锛屾嫾鎺ュ埌 Prompt 涓氦鐢?LLM 鐢熸垚鍥炵瓟銆?
        "鍏剁己鐐瑰寘鎷細妫€绱㈣川閲忓彈闄愪簬鍗曚竴鍚戦噺鐩镐技搴︺€佺己涔忛噸鎺掑簭鏈哄埗銆?
        "鏃犳硶澶勭悊澶氳烦鎺ㄧ悊绛夈€?, s["body"]))
    elems.append(Paragraph(
        "Advanced RAG 鍦?Naive RAG 鍩虹涓婂紩鍏ュ椤逛紭鍖栵細鏌ヨ鏀瑰啓锛圦uery Rewriting锛夈€?
        "娣峰悎妫€绱紙Hybrid Search combining Dense + Sparse锛夈€侀噸鎺掑簭锛圧eranking via "
        "Cross-Encoder 鎴?LLM锛夈€佷互鍙婃枃妗ｅ垎鍧椾紭鍖栵紙Smart Chunking + Metadata Enrichment锛夈€?
        "鏈」鐩疄鐜颁簡瀹屾暣鐨?Advanced RAG 閾捐矾銆?, s["body"]))

    elems.append(Paragraph("2.2 Modular RAG 璁捐鐞嗗康", s["h2"]))
    elems.append(Paragraph(
        "Modular RAG 灏?RAG 娴佺▼鍒嗚В涓哄彲鐙珛鏇挎崲鐨勬ā鍧楋細Loader 鈫?Splitter 鈫?Transformer 鈫?"
        "Embedder 鈫?Vector Store 鈫?Retriever 鈫?Reranker 鈫?Generator銆傛瘡涓ā鍧楀畾涔夋娊璞℃帴鍙ｏ紝"
        "閫氳繃宸ュ巶妯″紡鍜岄厤缃枃浠堕┍鍔ㄥ疄渚嬪寲锛屽疄鐜般€屼箰楂樼Н鏈ㄥ紡銆嶇殑鐏垫椿缁勫悎銆?, s["body"]))
    elems.append(Paragraph(
        "杩欑璁捐鐨勬牳蹇冧紭鍔垮湪浜庯細鍙互鍦ㄤ笉淇敼浠ｇ爜鐨勬儏鍐典笅锛岄€氳繃 settings.yaml 涓€閿垏鎹?
        " LLM Provider锛圓zure / DeepSeek / Ollama锛夈€丒mbedding 妯″瀷銆丷eranker 绛栫暐绛夛紝"
        "鏋佸ぇ鍦版柟渚夸簡 A/B 娴嬭瘯鍜屾妧鏈€夊瀷銆?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗笁绔?----
    elems.append(Paragraph("绗笁绔? 鏂囨。鍒嗗潡绛栫暐璇﹁В", s["h1"]))
    elems.append(Paragraph(
        "鏂囨。鍒嗗潡锛圕hunking锛夋槸 RAG 绯荤粺涓喅瀹氭绱㈣川閲忕殑鍏抽敭鐜妭銆傚垎鍧楄繃澶т細瀵艰嚧妫€绱?
        "鍣０澧炲姞銆丩LM 涓婁笅鏂囧埄鐢ㄧ巼涓嬮檷锛涘垎鍧楄繃灏忓垯浼氫涪澶辫涔変笂涓嬫枃锛屽奖鍝嶅洖绛旇繛璐€с€?, s["body"]))

    elems.append(Paragraph("3.1 甯歌鍒嗗潡鏂规硶", s["h2"]))
    methods = [
        ["鏂规硶", "鍘熺悊", "閫傜敤鍦烘櫙"],
        ["鍥哄畾闀垮害鍒囧垎", "鎸夊瓧绗︽暟鎴?Token 鏁扮瓑鍒?, "缁撴瀯绠€鍗曠殑绾枃鏈?],
        ["閫掑綊瀛楃鍒囧垎", "鎸夊垎闅旂浼樺厛绾ч€掑綊鍒囧垎", "閫氱敤鏂囨。锛堟帹鑽愶級"],
        ["璇箟鍒嗗潡", "鍩轰簬 Embedding 鐩镐技搴﹀垽鏂竟鐣?, "闀挎枃妗ｃ€佷富棰樺鍙?],
        ["Markdown 鍒囧垎", "鎸夋爣棰樺眰绾у垏鍒?, "Markdown / 鎶€鏈枃妗?],
    ]
    mt = Table(methods, colWidths=[1.8 * inch, 2.5 * inch, 2 * inch])
    mt.setStyle(_table_style("#27ae60"))
    elems.append(mt)
    elems.append(Spacer(1, 0.2 * inch))

    elems.append(Paragraph("3.2 Chunk 澧炲己锛歊efiner 涓?Metadata Enrichment", s["h2"]))
    elems.append(Paragraph(
        "鍘熷鍒囧垎鍚庣殑 Chunk 鍙兘瀛樺湪鎴柇涓嶈嚜鐒躲€佺己涔忎笂涓嬫枃绛夐棶棰樸€侰hunk Refiner 鍒╃敤 LLM "
        "瀵?Chunk 鏂囨湰杩涜鏀瑰啓娑﹁壊锛屼娇鍏舵洿鍔犺嚜鍖呭惈銆佽涔夊畬鏁淬€侻etadata Enricher 鍒欎负姣忎釜 "
        "Chunk 鐢熸垚 title銆乻ummary 鍜?tags 鍏冧俊鎭紝鍦ㄦ绱㈤樁娈靛彲鐢ㄤ簬杈呭姪杩囨护鍜屾帓搴忋€?, s["body"]))
    elems.append(Paragraph(
        "鍥剧墖澶勭悊鏂归潰锛岀郴缁熶細鎻愬彇 PDF 涓殑宓屽叆鍥剧墖锛岃皟鐢?Vision LLM锛堝 GPT-4o锛夌敓鎴愪腑鏂?
        "鍥剧墖鎻忚堪锛圛mage Caption锛夛紝骞跺皢鎻忚堪鏂囨湰娉ㄥ叆瀵瑰簲 Chunk 鐨?metadata 涓紝浠庤€屽疄鐜?
        "璺ㄦā鎬佹绱⑩€斺€旂敤鎴峰彲浠ラ€氳繃鏂囧瓧鏌ヨ鏉ユ壘鍒扮浉鍏崇殑鍥捐〃鍜屽浘鐗囧唴瀹广€?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗洓绔?----
    elems.append(Paragraph("绗洓绔? 鍚戦噺妫€绱笌娣峰悎鎼滅储", s["h1"]))
    elems.append(Paragraph(
        "鍚戦噺妫€绱紙Dense Retrieval锛夐€氳繃灏嗘枃鏈紪鐮佷负楂樼淮绋犲瘑鍚戦噺锛屽埄鐢ㄤ綑寮︾浉浼煎害鎴栧唴绉?
        "璁＄畻璇箟鐩镐技鎬э紝鏄幇浠ｄ俊鎭绱㈢殑鏍稿績鎶€鏈€傚父鐢ㄧ殑 Embedding 妯″瀷鍖呮嫭 OpenAI "
        "text-embedding-ada-002锛?536 缁达級銆丅GE 绯诲垪锛?68/1024 缁达級绛夈€?, s["body"]))

    elems.append(Paragraph("4.1 BM25 绋€鐤忔绱?, s["h2"]))
    elems.append(Paragraph(
        "BM25锛圔est Matching 25锛夋槸缁忓吀鐨勬鐜囨绱㈡ā鍨嬶紝鍩轰簬璇嶉锛圱F锛夊拰閫嗘枃妗ｉ鐜囷紙IDF锛?
        "璁＄畻鏂囨。涓庢煡璇㈢殑鐩稿叧鎬с€傚叾浼樺娍鍦ㄤ簬瀵圭簿纭叧閿瘝鍖归厤鐨勫鐞嗛潪甯告湁鏁堬紝鐗瑰埆鏄笓鏈夊悕璇嶃€?
        "閿欏埆瀛楃瓑鍦烘櫙涓嬭〃鐜颁紭浜庣函璇箟妫€绱€傛湰椤圭洰浣跨敤 jieba 鍒嗚瘝 + rank_bm25 搴撳疄鐜颁腑鏂?"
        "BM25 妫€绱€?, s["body"]))

    elems.append(Paragraph("4.2 RRF 铻嶅悎绠楁硶", s["h2"]))
    elems.append(Paragraph(
        "Reciprocal Rank Fusion (RRF) 鏄竴绉嶇畝鍗曢珮鏁堢殑鎺掑悕铻嶅悎绠楁硶锛屽叕寮忎负锛?
        "score(d) = 危 1/(k + rank_i(d))锛屽叾涓?k 涓哄钩婊戝父鏁帮紙榛樿 60锛夛紝rank_i(d) 涓?
        "鏂囨。 d 鍦ㄧ i 涓帓鍚嶅垪琛ㄤ腑鐨勪綅缃€俁RF 鐨勪紭鍔垮湪浜庝笉渚濊禆鍘熷鍒嗘暟鐨勯噺绾诧紝"
        "鍙互鐩存帴铻嶅悎涓嶅悓妫€绱㈡柟娉曠殑鎺掑悕缁撴灉銆?, s["body"]))

    elems.append(Paragraph("4.3 ChromaDB 鍚戦噺瀛樺偍", s["h2"]))
    elems.append(Paragraph(
        "ChromaDB 鏄竴涓交閲忕骇鐨勫紑婧愬悜閲忔暟鎹簱锛屾敮鎸?Embedding 瀛樺偍銆佸厓鏁版嵁杩囨护鍜岃繎浼兼渶杩戦偦"
        "锛圓NN锛夋悳绱€傛湰椤圭洰浣跨敤 ChromaDB 鎸佷箙鍖栧瓨鍌ㄦā寮忥紝鏁版嵁淇濆瓨鍦ㄦ湰鍦?SQLite 鏂囦欢涓紝"
        "閫傚悎涓汉椤圭洰鍜屼腑灏忚妯″簲鐢ㄥ満鏅€?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗簲绔?----
    elems.append(Paragraph("绗簲绔? 閲嶆帓搴忔満鍒朵笌璇勪及鏂规硶", s["h1"]))
    elems.append(Paragraph(
        "閲嶆帓搴忥紙Reranking锛夋槸 RAG 鐨勭簿鎺掗樁娈碉紝鍦ㄧ矖鎺掑彫鍥炵殑鍊欓€夐泦鍩虹涓婅繘琛屾洿绮剧粏鐨勭浉鍏虫€?
        "璇勪及銆傚父瑙佹柟妗堝寘鎷?Cross-Encoder Reranker 鍜?LLM Reranker 涓ょ銆?, s["body"]))

    elems.append(Paragraph("5.1 Cross-Encoder vs Bi-Encoder", s["h2"]))
    elems.append(Paragraph(
        "Bi-Encoder锛堝弻濉旀ā鍨嬶級灏嗘煡璇㈠拰鏂囨。鍒嗗埆缂栫爜涓虹嫭绔嬪悜閲忥紝閫氳繃浣欏鸡鐩镐技搴﹁绠楀尮閰嶅害锛?
        "閫熷害蹇絾绮惧害鏈夐檺銆侰ross-Encoder 灏嗘煡璇㈠拰鏂囨。鎷兼帴鍚庡悓鏃惰緭鍏ユā鍨嬶紝閫氳繃娉ㄦ剰鍔涙満鍒?
        "鎹曟崏缁嗙矑搴︿氦浜掞紝绮惧害鏇撮珮浣嗛€熷害杈冩參銆俁AG 涓€氬父浣跨敤 Bi-Encoder 鍋氱矖鎺掞紝"
        "Cross-Encoder 鍋氱簿鎺掋€?, s["body"]))

    elems.append(Paragraph("5.2 璇勪及鎸囨爣", s["h2"]))
    metrics_data = [
        ["鎸囨爣鍚嶇О", "绫诲瀷", "璇存槑"],
        ["Hit Rate", "妫€绱㈡寚鏍?, "Top-K 缁撴灉涓槸鍚﹀寘鍚纭枃妗?],
        ["MRR", "妫€绱㈡寚鏍?, "姝ｇ‘鏂囨。棣栨鍑虹幇浣嶇疆鐨勫€掓暟"],
        ["Faithfulness", "鐢熸垚鎸囨爣 (Ragas)", "鐢熸垚绛旀鏄惁蹇犲疄浜庢绱笂涓嬫枃"],
        ["Answer Relevancy", "鐢熸垚鎸囨爣 (Ragas)", "鐢熸垚绛旀涓庣敤鎴烽棶棰樼殑鐩稿叧搴?],
        ["Context Precision", "鐢熸垚鎸囨爣 (Ragas)", "妫€绱笂涓嬫枃涓浉鍏充俊鎭殑鍗犳瘮"],
    ]
    et = Table(metrics_data, colWidths=[1.8 * inch, 1.5 * inch, 3 * inch])
    et.setStyle(_table_style("#8e44ad"))
    elems.append(et)
    elems.append(PageBreak())

    # ---- 绗叚绔?----
    elems.append(Paragraph("绗叚绔? Agent 涓庡伐鍏疯皟鐢?, s["h1"]))
    elems.append(Paragraph(
        "Agent 鏄寚鑳藉鑷富瑙勫垝浠诲姟銆佽皟鐢ㄥ閮ㄥ伐鍏锋潵瀹屾垚澶嶆潅鐩爣鐨?AI 绯荤粺銆?
        "涓庣畝鍗曠殑 RAG 鏌ヨ涓嶅悓锛孉gent 鍙互鏍规嵁鐢ㄦ埛鎸囦护鑷姩鍒嗚В浠诲姟銆侀€夋嫨鍚堥€傜殑宸ュ叿"
        "锛堝鎼滅储寮曟搸銆佽绠楀櫒銆佷唬鐮佹墽琛屽櫒锛夛紝杩唬鎵ц鐩村埌鑾峰緱婊℃剰缁撴灉銆?, s["body"]))

    elems.append(Paragraph("6.1 MCP 鍗忚", s["h2"]))
    elems.append(Paragraph(
        "Model Context Protocol锛圡CP锛夋槸 Anthropic 鎻愬嚭鐨勬爣鍑嗗寲 AI 妯″瀷涓庡閮ㄥ伐鍏蜂氦浜掔殑鍗忚銆?
        "瀹冨畾涔変簡宸ュ叿鍙戠幇锛坱ools/list锛夈€佸伐鍏疯皟鐢紙tools/call锛夌瓑 JSON-RPC 2.0 鎺ュ彛鏍囧噯銆?
        "鏈」鐩疄鐜颁簡涓€涓?MCP Server锛屾毚闇蹭簡 query_knowledge_hub銆乴ist_collections 鍜?"
        "get_document_summary 涓変釜宸ュ叿锛屽彲琚?VS Code Copilot 鎴?Claude Desktop 鐩存帴璋冪敤銆?, s["body"]))

    elems.append(Paragraph("6.2 ReAct 鎺ㄧ悊妯″紡", s["h2"]))
    elems.append(Paragraph(
        "ReAct锛圧easoning + Acting锛夋槸涓€绉嶅皢鎺ㄧ悊涓庤鍔ㄤ氦鏇胯繘琛岀殑 Agent 妯″紡銆?
        "LLM 鍏堣繘琛屾帹鐞嗘€濊€冿紙Thought锛夛紝鐒跺悗閫夋嫨涓€涓鍔紙Action锛夛紝瑙傚療琛屽姩缁撴灉"
        "锛圤bservation锛夛紝鍐嶇户缁帹鐞嗭紝寰幆寰€澶嶇洿鍒板緱鍑烘渶缁堢瓟妗堛€傝繖绉嶆ā寮忎娇 Agent 鐨?
        "鍐崇瓥杩囩▼鏇村姞閫忔槑銆佸彲璋冭瘯銆?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗竷绔?----
    elems.append(Paragraph("绗竷绔? 鐢熶骇閮ㄧ讲涓庢€ц兘浼樺寲", s["h1"]))
    elems.append(Paragraph(
        "灏?RAG 绯荤粺浠庡紑鍙戠幆澧冮儴缃插埌鐢熶骇鐜闇€瑕佽€冭檻澶氫釜缁村害锛氭湇鍔″彲鐢ㄦ€с€佸搷搴斿欢杩熴€?
        "鏁版嵁瀹夊叏鍜屾垚鏈帶鍒躲€備互涓嬫槸鍏抽敭浼樺寲绛栫暐銆?, s["body"]))

    elems.append(Paragraph("7.1 缂撳瓨绛栫暐", s["h2"]))
    elems.append(Paragraph(
        "瀵逛簬閲嶅鎴栫浉浼肩殑鏌ヨ锛屽彲浠ュ紩鍏ヨ涔夌紦瀛橈紙Semantic Cache锛夛細灏嗘煡璇㈠悜閲忎笌缂撳瓨搴撲腑鐨?
        "鍘嗗彶鏌ヨ杩涜鐩镐技搴﹀尮閰嶏紝鑻ヨ秴杩囬槇鍊煎垯鐩存帴杩斿洖缂撳瓨缁撴灉锛岄伩鍏嶉噸澶嶇殑 Embedding 璁＄畻"
        "鍜?LLM 璋冪敤锛屾樉钁楅檷浣庡欢杩熷拰鎴愭湰銆?, s["body"]))

    elems.append(Paragraph("7.2 鎵瑰鐞嗕笌寮傛", s["h2"]))
    elems.append(Paragraph(
        "Embedding 璁＄畻鍜?LLM 璋冪敤鏄?RAG 閾捐矾涓渶鑰楁椂鐨勭幆鑺傘€傞€氳繃鎵归噺 Embedding "
        "锛堝皢澶氫釜 Chunk 鍚堝苟涓轰竴娆?API 璋冪敤锛夊拰寮傛骞跺彂锛坅syncio / ThreadPool锛夛紝"
        "鍙互澶у箙鎻愬崌鏁版嵁鎽勫彇鍜屾煡璇㈢殑鍚炲悙閲忋€傛湰椤圭洰鐨?BatchProcessor 缁勪欢瀹炵幇浜?
        "鍙厤缃殑鎵归噺澶у皬鍜屽苟鍙戝害銆?, s["body"]))

    elems.append(Paragraph("7.3 鍙娴嬫€?, s["h2"]))
    elems.append(Paragraph(
        "鐢熶骇绯荤粺蹇呴』鍏峰瀹屽杽鐨勫彲瑙傛祴鎬ц兘鍔涖€傛湰椤圭洰閫氳繃缁撴瀯鍖栨棩蹇楋紙JSON Lines 鏍煎紡锛夈€?
        "鍏ㄩ摼璺?Trace锛堣褰曟瘡涓樁娈电殑杈撳叆/杈撳嚭/鑰楁椂锛夊拰 Streamlit Dashboard 涓変綅涓€浣?
        "瀹炵幇鍙鍖栫洃鎺с€傛瘡娆℃憚鍙栧拰鏌ヨ鎿嶄綔閮戒細鑷姩鐢熸垚 Trace 璁板綍锛屼究浜庨棶棰樻帓鏌ュ拰鎬ц兘鍒嗘瀽銆?, s["body"]))

    # Build
    doc.build(elems)
    print(f"鉁?Generated: {output}")


# ===================================================================
# 2. 鍚腑鏂囪〃鏍煎拰娴佺▼鍥剧殑鏂囨。 (~6 椤? 鍚浘鐗?
# ===================================================================

def generate_chinese_table_chart_doc(output: Path) -> None:
    doc = SimpleDocTemplate(str(output), pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=30)
    s = _make_styles()
    elems: list = []

    # 灏侀潰
    elems.append(Spacer(1, 2 * inch))
    elems.append(Paragraph("RAG 绯荤粺鎬ц兘璇勬祴鎶ュ憡", s["title"]))
    elems.append(Spacer(1, 0.3 * inch))
    elems.append(Paragraph("鍚〃鏍间笌娴佺▼鍥?路 QA 娴嬭瘯鐢?, s["h2"]))
    elems.append(Spacer(1, 0.5 * inch))
    cover = [
        ["鏂囨。绫诲瀷", "鎬ц兘璇勬祴鎶ュ憡"],
        ["鐗堟湰", "v1.0 鈥?2026 骞?2 鏈?],
        ["鐢ㄩ€?, "QA 娴嬭瘯 / Section O"],
    ]
    ct = Table(cover, colWidths=[1.5 * inch, 4 * inch])
    ct.setStyle(_table_style())
    elems.append(ct)
    elems.append(PageBreak())

    # ---- 绗竴绔狅細绯荤粺鏋舵瀯娴佺▼鍥?----
    elems.append(Paragraph("绗竴绔? RAG 绯荤粺鏁翠綋鏋舵瀯", s["h1"]))
    elems.append(Paragraph(
        "涓嬪浘灞曠ず浜?Modular RAG 绯荤粺鐨勬牳蹇冨鐞嗘祦绋嬨€傛枃妗ｄ粠杈撳叆鍒版渶缁堟绱㈢粨鏋滐紝"
        "渚濇缁忚繃鍔犺浇銆佸垎鍧椼€佸寮恒€佺紪鐮併€佸瓨鍌ㄤ簲涓樁娈点€?, s["body"]))

    # 娴佺▼鍥?
    flow_buf = _create_chart_image(400, 250, "RAG Pipeline", "flow")
    elems.append(Image(flow_buf, width=5 * inch, height=3 * inch))
    elems.append(Paragraph("鍥?1锛歊AG 鏁版嵁鎽勫彇娴佺▼鍥?, s["caption"]))
    elems.append(Spacer(1, 0.2 * inch))

    elems.append(Paragraph(
        "濡傚浘 1 鎵€绀猴紝鏂囨。棣栧厛閫氳繃 Loader 妯″潡杩涜瑙ｆ瀽锛堟敮鎸?PDF銆丮arkdown銆乄ord 绛夋牸寮忥級锛?
        "鎻愬彇绾枃鏈拰宓屽叆鍥剧墖銆傞殢鍚庤繘鍏?Splitter 妯″潡杩涜鏅鸿兘鍒嗗潡锛屽啀閫氳繃 Transformer 妯″潡"
        "杩涜 LLM 澧炲己锛圕hunk 绮剧偧 + 鍏冩暟鎹敓鎴?+ 鍥剧墖鎻忚堪锛夈€傛渶鍚庣粡 Embedder 缂栫爜涓哄悜閲忥紝"
        "瀛樺叆 ChromaDB 鍜?BM25 绱㈠紩銆?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗簩绔狅細Embedding 妯″瀷瀵规瘮 ----
    elems.append(Paragraph("绗簩绔? Embedding 妯″瀷鎬ц兘瀵规瘮", s["h1"]))
    elems.append(Paragraph(
        "涓嶅悓 Embedding 妯″瀷鍦ㄧ淮搴︺€侀€熷害銆佹垚鏈拰璐ㄩ噺涓婂悇鏈夊樊寮傘€備笅琛ㄥ姣斾簡甯哥敤妯″瀷鐨勫叧閿弬鏁般€?, s["body"]))

    embed_data = [
        ["妯″瀷鍚嶇О", "缁村害", "寤惰繜(ms)", "鎴愭湰", "涓枃璐ㄩ噺"],
        ["text-embedding-ada-002", "1536", "25", "$0.0001/1K tokens", "鑹ソ"],
        ["text-embedding-3-small", "1536", "20", "$0.00002/1K tokens", "鑹ソ"],
        ["text-embedding-3-large", "3072", "35", "$0.00013/1K tokens", "浼樼"],
        ["BGE-large-zh", "1024", "15", "鍏嶈垂锛堟湰鍦帮級", "浼樼"],
        ["GTE-large-zh", "1024", "18", "鍏嶈垂锛堟湰鍦帮級", "浼樼"],
        ["M3E-base", "768", "12", "鍏嶈垂锛堟湰鍦帮級", "鑹ソ"],
    ]
    et = Table(embed_data, colWidths=[2 * inch, 0.8 * inch, 0.9 * inch, 1.8 * inch, 0.9 * inch])
    et.setStyle(_table_style("#2980b9"))
    elems.append(et)
    elems.append(Paragraph("琛?1锛氫富娴?Embedding 妯″瀷鍙傛暟瀵规瘮", s["caption"]))
    elems.append(Spacer(1, 0.2 * inch))

    # 鏌辩姸鍥?
    bar_buf = _create_chart_image(450, 250, "Embedding 寤惰繜瀵规瘮", "bar")
    elems.append(Image(bar_buf, width=5 * inch, height=2.8 * inch))
    elems.append(Paragraph("鍥?2锛氬悇 Embedding 妯″瀷寤惰繜瀵规瘮锛坢s锛?, s["caption"]))
    elems.append(PageBreak())

    # ---- 绗笁绔狅細妫€绱㈢瓥鐣ュ姣?----
    elems.append(Paragraph("绗笁绔? 妫€绱㈢瓥鐣ユ€ц兘瀵规瘮", s["h1"]))
    elems.append(Paragraph(
        "娣峰悎妫€绱紙Hybrid Search锛夌粨鍚堜簡绋犲瘑鍚戦噺鍜岀█鐤忓叧閿瘝涓ょ妫€绱㈡柟寮忕殑浼樺娍銆?
        "涓嬭〃灞曠ず浜嗕笉鍚屾绱㈢瓥鐣ュ湪鏍囧噯娴嬭瘯闆嗕笂鐨勮〃鐜般€?, s["body"]))

    retrieval_data = [
        ["妫€绱㈢瓥鐣?, "Precision@5", "Recall@10", "NDCG@10", "骞冲潎寤惰繜(ms)"],
        ["绾瀵嗘绱?, "0.72", "0.65", "0.78", "45"],
        ["绾█鐤忔绱?(BM25)", "0.68", "0.71", "0.73", "28"],
        ["娣峰悎妫€绱?(RRF)", "0.80", "0.78", "0.84", "65"],
        ["娣峰悎妫€绱?+ Cross-Encoder", "0.85", "0.82", "0.88", "89"],
        ["娣峰悎妫€绱?+ LLM Rerank", "0.83", "0.80", "0.87", "320"],
    ]
    rt = Table(retrieval_data, colWidths=[2.2 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch, 1.2 * inch])
    rt.setStyle(_table_style("#27ae60"))
    elems.append(rt)
    elems.append(Paragraph("琛?2锛氭绱㈢瓥鐣ユ€ц兘瀵规瘮", s["caption"]))
    elems.append(Spacer(1, 0.3 * inch))

    elems.append(Paragraph(
        "浠庤〃 2 鍙互鐪嬪嚭锛屾贩鍚堟绱?+ Cross-Encoder 閲嶆帓鐨勬柟妗堝湪绮惧害鎸囨爣涓婅〃鐜版渶浣筹紝"
        "浣嗗欢杩熶篃鐩稿杈冮珮銆傜函 BM25 妫€绱㈠欢杩熸渶浣庯紝浣嗙簿搴︿笉澶熺悊鎯炽€傚疄闄呴儴缃蹭腑闇€瑕佹牴鎹?
        "涓氬姟鍦烘櫙鍦ㄧ簿搴﹀拰寤惰繜涔嬮棿鍋氭潈琛°€?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗洓绔狅細鍒嗗潡鍙傛暟瀹為獙 ----
    elems.append(Paragraph("绗洓绔? 鍒嗗潡鍙傛暟璋冧紭瀹為獙", s["h1"]))
    elems.append(Paragraph(
        "Chunk Size 鍜?Chunk Overlap 鏄垎鍧楃瓥鐣ヤ腑鏈€閲嶈鐨勪袱涓秴鍙傛暟銆備笅琛ㄥ睍绀轰簡"
        "涓嶅悓鍙傛暟缁勫悎瀵规绱㈣川閲忕殑褰卞搷銆?, s["body"]))

    chunk_exp = [
        ["Chunk Size", "Overlap", "Chunk 鏁伴噺", "Hit Rate", "MRR", "澶囨敞"],
        ["256", "50", "48", "0.65", "0.58", "鍒嗗潡杩囧皬锛屼笂涓嬫枃涓㈠け"],
        ["512", "100", "26", "0.78", "0.72", "杈冨ソ骞宠　"],
        ["1000", "200", "14", "0.82", "0.76", "鎺ㄨ崘閰嶇疆"],
        ["1500", "300", "10", "0.75", "0.70", "鍒嗗潡鍋忓ぇ锛屽櫔澹板鍔?],
        ["2000", "400", "8", "0.68", "0.62", "鍒嗗潡杩囧ぇ锛屾绱笉绮剧‘"],
    ]
    cet = Table(chunk_exp, colWidths=[0.9*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.8*inch, 2*inch])
    cet.setStyle(_table_style("#e67e22"))
    elems.append(cet)
    elems.append(Paragraph("琛?3锛氬垎鍧楀弬鏁板妫€绱㈣川閲忕殑褰卞搷", s["caption"]))
    elems.append(Spacer(1, 0.2 * inch))

    # 楗煎浘
    pie_buf = _create_chart_image(350, 250, "鑰楁椂鍒嗗竷", "pie")
    elems.append(Image(pie_buf, width=4 * inch, height=2.8 * inch))
    elems.append(Paragraph("鍥?3锛氭憚鍙栧悇闃舵鑰楁椂鍗犳瘮鍒嗗竷", s["caption"]))
    elems.append(Spacer(1, 0.2 * inch))

    elems.append(Paragraph(
        "鏍规嵁瀹為獙缁撴灉锛屾帹鑽愪娇鐢?chunk_size=1000, chunk_overlap=200 鐨勯厤缃紝鍦ㄤ繚鐣欒冻澶?
        "涓婁笅鏂囩殑鍚屾椂鑾峰緱杈冮珮鐨勬绱㈢簿搴︺€傚悓鏃跺缓璁紑鍚?LLM Chunk Refiner锛岃繘涓€姝ユ彁鍗?
        "Chunk 鐨勮涔夊畬鏁存€с€?, s["body"]))
    elems.append(PageBreak())

    # ---- 绗簲绔狅細閰嶇疆绀轰緥 ----
    elems.append(Paragraph("绗簲绔? 閰嶇疆鍙傝€?, s["h1"]))
    elems.append(Paragraph(
        "浠ヤ笅鏄帹鑽愮殑 settings.yaml 鍏抽敭閰嶇疆椤规眹鎬昏〃锛?, s["body"]))

    config_data = [
        ["閰嶇疆璺緞", "鎺ㄨ崘鍊?, "璇存槑"],
        ["llm.provider", "azure", "LLM 鏈嶅姟鍟?],
        ["llm.model", "gpt-4o", "LLM 妯″瀷鍚?],
        ["embedding.provider", "azure", "Embedding 鏈嶅姟鍟?],
        ["embedding.model", "text-embedding-ada-002", "Embedding 妯″瀷"],
        ["ingestion.chunk_size", "1000", "鍒嗗潡澶у皬锛堝瓧绗︼級"],
        ["ingestion.chunk_overlap", "200", "鍒嗗潡閲嶅彔锛堝瓧绗︼級"],
        ["retrieval.dense_top_k", "10", "绋犲瘑妫€绱?Top-K"],
        ["retrieval.sparse_top_k", "10", "绋€鐤忔绱?Top-K"],
        ["retrieval.rrf_k", "60", "RRF 骞虫粦甯告暟"],
        ["rerank.provider", "none", "閲嶆帓搴忔柟寮?],
        ["rerank.top_k", "3", "鏈€缁堣繑鍥炴潯鏁?],
    ]
    cft = Table(config_data, colWidths=[2.2 * inch, 2 * inch, 2.5 * inch])
    cft.setStyle(_table_style("#16a085"))
    elems.append(cft)
    elems.append(Paragraph("琛?4锛氭帹鑽愰厤缃」姹囨€?, s["caption"]))

    # Build
    doc.build(elems)
    print(f"鉁?Generated: {output}")


# ===================================================================
# 3. 30+ 椤典腑鏂囬暱鏂囨。
# ===================================================================

def generate_chinese_long_doc(output: Path) -> None:
    doc = SimpleDocTemplate(str(output), pagesize=A4,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=30)
    s = _make_styles()
    elems: list = []

    # 灏侀潰
    elems.append(Spacer(1, 2 * inch))
    elems.append(Paragraph("澶фā鍨嬮潰璇曞叓鑲＄煡璇嗘墜鍐?, s["title"]))
    elems.append(Spacer(1, 0.3 * inch))
    elems.append(Paragraph("RAG 路 Agent 路 寰皟 路 鎺ㄧ悊閮ㄧ讲 路 璇勪及", s["h2"]))
    elems.append(Spacer(1, 0.5 * inch))
    cover = [
        ["浣滆€?, "Modular RAG 椤圭洰缁?],
        ["鐗堟湰", "v1.0 鈥?2026 骞?2 鏈?],
        ["椤垫暟", "30+ 椤?],
        ["鐢ㄩ€?, "QA 娴嬭瘯闀挎枃妗?/ Section O"],
    ]
    ct = Table(cover, colWidths=[1.5 * inch, 4 * inch])
    ct.setStyle(_table_style())
    elems.append(ct)
    elems.append(PageBreak())

    # 鐩綍
    elems.append(Paragraph("鐩綍", s["h1"]))
    chapters = [
        "绗竴绔? Transformer 涓庢敞鎰忓姏鏈哄埗",
        "绗簩绔? 棰勮缁冧笌寰皟鎶€鏈?,
        "绗笁绔? Prompt Engineering",
        "绗洓绔? 妫€绱㈠寮虹敓鎴愶紙RAG锛?,
        "绗簲绔? 鍚戦噺鏁版嵁搴撲笌 Embedding",
        "绗叚绔? 娣峰悎妫€绱笌閲嶆帓搴?,
        "绗竷绔? 鏂囨。澶勭悊涓庡垎鍧楃瓥鐣?,
        "绗叓绔? Agent 涓庡伐鍏疯皟鐢?,
        "绗節绔? 妯″瀷璇勪及涓庡熀鍑嗘祴璇?,
        "绗崄绔? 鎺ㄧ悊浼樺寲涓庨儴缃?,
        "绗崄涓€绔? 澶氭ā鎬佸ぇ妯″瀷",
        "绗崄浜岀珷  瀹夊叏涓庡榻?,
        "绗崄涓夌珷  琛屼笟搴旂敤妗堜緥",
        "绗崄鍥涚珷  闈㈣瘯楂橀闂绮鹃€?,
        "绗崄浜旂珷  椤圭洰瀹炴垬缁忛獙鎬荤粨",
    ]
    for ch in chapters:
        elems.append(Paragraph(ch, s["body"]))
    elems.append(PageBreak())

    # ---------- 鍐呭鐢熸垚锛堟瘡绔?~2 椤碉級 ----------

    chapter_contents = [
        # 绗竴绔?
        ("绗竴绔? Transformer 涓庢敞鎰忓姏鏈哄埗", [
            ("1.1 鑷敞鎰忓姏鏈哄埗鍘熺悊",
             "鑷敞鎰忓姏鏈哄埗锛圫elf-Attention锛夋槸 Transformer 鐨勬牳蹇冪粍浠躲€傚畠鍏佽妯″瀷鍦ㄥ鐞嗘瘡涓?Token 鏃讹紝"
             "鑳藉鍏虫敞杈撳叆搴忓垪涓殑鎵€鏈夊叾浠?Token锛屼粠鑰屾崟鑾烽暱璺濈渚濊禆鍏崇郴銆傝绠楄繃绋嬪彲浠ユ弿杩颁负锛?
             "棣栧厛灏嗚緭鍏ュ悜閲忛€氳繃涓変釜绾挎€у彉鎹㈠垎鍒槧灏勪负 Query锛圦锛夈€並ey锛圞锛夊拰 Value锛圴锛夛紝"
             "鐒跺悗璁＄畻 Q 涓?K 鐨勭偣绉苟杩涜缂╂斁鍜?Softmax 褰掍竴鍖栵紝鏈€鍚庝笌 V 鍔犳潈姹傚拰寰楀埌杈撳嚭銆?),
            ("1.2 澶氬ご娉ㄦ剰鍔?,
             "澶氬ご娉ㄦ剰鍔涳紙Multi-Head Attention锛夊皢杈撳叆绌洪棿鍒掑垎涓?h 涓瓙绌洪棿锛屽湪姣忎釜瀛愮┖闂寸嫭绔嬭绠?
             "娉ㄦ剰鍔涳紝鏈€鍚庢嫾鎺ユ墍鏈夊瓙绌洪棿鐨勮緭鍑恒€傝繖浣挎ā鍨嬭兘澶熷悓鏃跺叧娉ㄤ笉鍚屼綅缃殑涓嶅悓绫诲瀷鐨勪俊鎭€?
             "渚嬪锛屼竴涓?Head 鍙兘鍏虫敞璇硶鍏崇郴锛屽彟涓€涓?Head 鍏虫敞璇箟鐩镐技鎬с€侴PT-4 绛夌幇浠ｆā鍨嬮€氬父"
             "浣跨敤 32-128 涓?Head銆?),
            ("1.3 浣嶇疆缂栫爜",
             "鐢变簬 Self-Attention 鏈韩涓嶅寘鍚綅缃俊鎭紝闇€瑕侀澶栨坊鍔犱綅缃紪鐮侊紙Positional Encoding锛夈€?
             "鍘熷 Transformer 浣跨敤姝ｅ鸡浣欏鸡鍑芥暟鐢熸垚鍥哄畾浣嶇疆缂栫爜锛涘悗缁爺绌舵彁鍑轰簡鏃嬭浆浣嶇疆缂栫爜"
             "锛圧oPE锛夊拰 ALiBi 绛夋柟妗堬紝鍦ㄦ敮鎸佹洿闀夸笂涓嬫枃鐨勫悓鏃朵繚鎸佽壇濂界殑娉涘寲鑳藉姏銆俁oPE 閫氳繃"
             "鏃嬭浆鍚戦噺鐨勬柟寮忓皢鐩稿浣嶇疆淇℃伅缂栫爜鍒版敞鎰忓姏璁＄畻涓紝琚?LLaMA銆丟PT-NeoX 绛夋ā鍨嬪箍娉涢噰鐢ㄣ€?),
            ("1.4 KV Cache 涓庢帹鐞嗕紭鍖?,
             "鍦ㄨ嚜鍥炲綊鐢熸垚杩囩▼涓紝姣忎竴姝ラ兘闇€瑕佽绠楀綋鍓?Token 瀵规墍鏈変箣鍓?Token 鐨勬敞鎰忓姏銆?
             "KV Cache 鎶€鏈皢宸茶绠楃殑 Key 鍜?Value 鍚戦噺缂撳瓨璧锋潵锛岄伩鍏嶉噸澶嶈绠楋紝灏嗘帹鐞嗙殑鏃堕棿澶嶆潅搴?
             "浠?O(n虏) 闄嶄綆鍒?O(n)銆備絾 KV Cache 鐨勬樉瀛樺崰鐢ㄩ殢搴忓垪闀垮害绾挎€у闀匡紝鎴愪负澶勭悊闀夸笂涓嬫枃鐨?
             "涓昏鐡堕涔嬩竴銆傚父瑙佷紭鍖栨柟妗堝寘鎷?GQA锛圙rouped Query Attention锛夈€丮QA锛圡ulti-Query "
             "Attention锛夌瓑銆?),
        ]),
        # 绗簩绔?
        ("绗簩绔? 棰勮缁冧笌寰皟鎶€鏈?, [
            ("2.1 棰勮缁冭寖寮?,
             "澶ц瑷€妯″瀷鐨勯璁粌閫氬父閲囩敤鑷洖褰掕瑷€寤烘ā鐩爣锛圕ausal Language Modeling锛夛紝鍗抽娴嬩笅涓€涓?"
             "Token銆傝缁冩暟鎹潵鑷簰鑱旂綉澶ц妯℃枃鏈鏂欙紙濡?Common Crawl銆乄ikipedia銆丟itHub 浠ｇ爜绛夛級锛?
             "Token 鏁伴噺閫氬父鍦ㄤ竾浜跨骇鍒€傞璁粌闃舵闇€瑕佹暟鍗冨紶 GPU 杩愯鏁板懆鐢氳嚦鏁版湀銆?),
            ("2.2 SFT 鐩戠潱寰皟",
             "棰勮缁冨畬鎴愬悗锛屾ā鍨嬪叿澶囦簡鍩虹鐨勮瑷€鐞嗚В鍜岀敓鎴愯兘鍔涳紝浣嗘棤娉曞緢濂藉湴閬靛惊浜虹被鎸囦护銆?
             "鐩戠潱寰皟锛圫upervised Fine-Tuning, SFT锛変娇鐢ㄩ珮璐ㄩ噺鐨勬寚浠?鍥炵瓟瀵规暟鎹泦瀵规ā鍨嬭繘琛?
             "浜屾璁粌锛屼娇鍏跺浼氭寜鐓ф寚浠ゆ牸寮忓洖绛旈棶棰樸€係FT 鏁版嵁璐ㄩ噺杩滄瘮鏁伴噺閲嶈銆?),
            ("2.3 RLHF 涓?DPO",
             "浜虹被鍙嶉寮哄寲瀛︿範锛圧LHF锛夐€氳繃璁粌濂栧姳妯″瀷锛圧eward Model锛夋潵璇勪及妯″瀷杈撳嚭鐨勮川閲忥紝"
             "鐒跺悗浣跨敤 PPO 绠楁硶浼樺寲妯″瀷绛栫暐浣垮叾鑾峰緱鏇撮珮鐨勫鍔便€侱PO锛圖irect Preference Optimization锛?
             "鍒欑渷鍘讳簡濂栧姳妯″瀷鐨勮缁冿紝鐩存帴浠庝汉绫诲亸濂芥暟鎹腑瀛︿範绛栫暐锛岀畝鍖栦簡璁粌娴佺▼銆?),
            ("2.4 LoRA 涓?QLoRA",
             "鍏ㄥ弬鏁板井璋冮渶瑕佸法澶х殑璁＄畻璧勬簮锛孡oRA锛圠ow-Rank Adaptation锛夐€氳繃鍦ㄥ師濮嬫潈閲嶇煩闃垫梺"
             "娣诲姞浣庣З鍒嗚В鐭╅樀锛圓路B锛宺ank << d锛夛紝浠呰缁冭繖浜涙柊澧炲弬鏁帮紝澶у箙闄嶄綆鏄惧瓨鍜岃绠楅渶姹傘€?
             "QLoRA 杩涗竴姝ュ皢妯″瀷鏉冮噸閲忓寲涓?4-bit锛岄厤鍚?LoRA 鍦ㄦ秷璐圭骇 GPU 涓婁篃鑳藉井璋冨ぇ妯″瀷銆?),
        ]),
        # 绗笁绔?
        ("绗笁绔? Prompt Engineering", [
            ("3.1 Prompt 璁捐鍘熷垯",
             "鏈夋晥鐨?Prompt 搴斿綋娓呮櫚銆佸叿浣擄紝鍖呭惈瓒冲鐨勪笂涓嬫枃淇℃伅銆傚父瑙佺殑璁捐鍘熷垯鍖呮嫭锛氭彁渚涙槑纭殑"
             "浠诲姟璇存槑锛堜綘鏄竴涓?XX 涓撳锛夈€佺粰鍑鸿緭鍑烘牸寮忚姹傦紙璇风敤 JSON 鏍煎紡杈撳嚭锛夈€佹彁渚涚ず渚?
             "锛團ew-shot锛夈€佷互鍙婃楠ゅ寲寮曞锛堝厛鍒嗘瀽鈥﹀啀鎬荤粨鈥︽渶鍚庣粰鍑哄缓璁級銆?),
            ("3.2 鎬濈淮閾?(Chain-of-Thought)",
             "鎬濈淮閾撅紙CoT锛夋彁绀洪€氳繃瑕佹眰妯″瀷銆岄€愭鎬濊€冦€嶆潵鎻愬崌鎺ㄧ悊璐ㄩ噺銆傜爺绌惰〃鏄庯紝鍦?Prompt 涓?
             "鍔犲叆銆孡et's think step by step銆嶇瓑寮曞璇紝鍙互鏄捐憲鎻愬崌鏁板鎺ㄧ悊銆侀€昏緫鎺ㄧ悊绛変换鍔＄殑鍑嗙‘鐜囥€?
             "鍙樼鍖呮嫭 Self-Consistency锛堝娆￠噰鏍峰彇澶氭暟鎶曠エ锛夊拰 Tree-of-Thought锛堟爲鐘跺垎鏀帰绱級銆?),
            ("3.3 RAG 鍦烘櫙鐨?Prompt",
             "鍦?RAG 绯荤粺涓紝Prompt 闇€瑕佸皢妫€绱㈠埌鐨勪笂涓嬫枃淇℃伅涓庣敤鎴锋煡璇㈢粨鍚堛€傚吀鍨嬫ā鏉夸负锛歕n"
             "'浣犳槸涓€涓煡璇嗗姪鎵嬨€傛牴鎹互涓嬪弬鑰冭祫鏂欏洖绛旂敤鎴风殑闂銆傚鏋滆祫鏂欎腑娌℃湁鐩稿叧淇℃伅锛?
             "璇峰瀹炲憡鐭ユ棤娉曞洖绛斻€俓n\n鍙傝€冭祫鏂欙細{context}\n\n鐢ㄦ埛闂锛歿query}'\n\n"
             "闇€瑕佹敞鎰忎笂涓嬫枃鐨勬帓鍒楅『搴忋€侀暱搴︽帶鍒跺拰鏍煎紡鏍囨敞锛屼互鎻愬崌 LLM 鐨勭瓟妗堣川閲忋€?),
            ("3.4 Prompt 娉ㄥ叆涓庡畨鍏?,
             "Prompt 娉ㄥ叆鏄寚鎭舵剰鐢ㄦ埛閫氳繃绮惧績鏋勯€犵殑杈撳叆鏉ョ粫杩囩郴缁?Prompt 鐨勭害鏉燂紝浣?LLM 鎵ц"
             "闈為鏈熺殑琛屼负銆傞槻寰℃帾鏂藉寘鎷細杈撳叆杩囨护涓?sanitization銆佺郴缁?Prompt 涓庣敤鎴疯緭鍏ョ殑"
             "鏄庣‘鍒嗛殧銆佽緭鍑烘牸寮忕害鏉熸楠屻€佷互鍙婁娇鐢?Constitutional AI 绛夋柟娉曡缁冩ā鍨嬬殑鎷掔粷鑳藉姏銆?),
        ]),
        # 绗洓绔?
        ("绗洓绔? 妫€绱㈠寮虹敓鎴愶紙RAG锛?, [
            ("4.1 RAG 姒傝堪",
             "RAG 閫氳繃鍦?LLM 鐢熸垚鍓嶅紩鍏ヤ俊鎭绱㈤樁娈碉紝灏嗙浉鍏冲閮ㄧ煡璇嗘敞鍏ュ埌鐢熸垚涓婁笅鏂囦腑锛?
             "浠庤€屽噺灏戝够瑙夈€佹彁渚涘疄鏃剁煡璇嗘洿鏂般€佸苟浣垮洖绛斿彲婧簮銆俁AG 宸叉垚涓轰紒涓氱骇 AI 搴旂敤鐨?
             "鏍囧噯鏋舵瀯妯″紡锛屽箍娉涘簲鐢ㄤ簬鐭ヨ瘑搴撻棶绛斻€佹枃妗ｅ垎鏋愩€佸鏈嶅璇濈瓑鍦烘櫙銆?),
            ("4.2 RAG 閾捐矾鍒嗚В",
             "瀹屾暣鐨?RAG 閾捐矾鍖呭惈浠ヤ笅鏍稿績闃舵锛歕n"
             "1. 鏁版嵁鎽勫彇锛圛ngestion锛夛細瑙ｆ瀽鏂囨。 鈫?鍒嗗潡 鈫?澧炲己 鈫?鍚戦噺鍖?鈫?瀛樺偍\n"
             "2. 鏌ヨ澶勭悊锛圦uery Processing锛夛細鏌ヨ鏀瑰啓 鈫?鍏抽敭璇嶆彁鍙朶n"
             "3. 妫€绱紙Retrieval锛夛細绋犲瘑妫€绱?+ 绋€鐤忔绱?鈫?铻嶅悎\n"
             "4. 閲嶆帓搴忥紙Reranking锛夛細Cross-Encoder 鎴?LLM 绮炬帓\n"
             "5. 鐢熸垚锛圙eneration锛夛細Prompt 鏋勫缓 鈫?LLM 鐢熸垚 鈫?寮曠敤鏍囨敞"),
            ("4.3 RAG 甯歌闂",
             "甯歌鐨?RAG 澶辫触妯″紡鍖呮嫭锛氭绱笉鍒扮浉鍏虫枃妗ｏ紙鍙洖鐜囦綆锛夈€佹绱㈠埌鐨勬枃妗ｄ笉绮剧‘"
             "锛堢簿纭巼浣庯級銆丩LM 鏈兘姝ｇ‘鍒╃敤涓婁笅鏂囷紙蹇犲疄搴︿綆锛夈€佷互鍙婂垎鍧椾笉鍚堢悊瀵艰嚧鍏抽敭淇℃伅"
             "琚埅鏂€傞拡瀵硅繖浜涢棶棰橈紝鍙互浠庡垎鍧楃瓥鐣ャ€佹绱㈡柟娉曘€侀噸鎺掑簭鍜?Prompt 璁捐绛夊涓淮搴?
             "杩涜浼樺寲銆?),
            ("4.4 闈㈣瘯楂橀闂",
             "- Q: RAG 鍜屽井璋冪殑鍖哄埆锛熷悇鑷€傜敤鍦烘櫙锛焅n"
             "- Q: 濡備綍璇勪及 RAG 绯荤粺鐨勮川閲忥紵鏈夊摢浜涜瘎浼版寚鏍囷紵\n"
             "- Q: RAG 绯荤粺涓浣曞鐞嗗璺虫帹鐞嗛棶棰橈紵\n"
             "- Q: 濡備綍瑙ｅ喅 RAG 涓殑骞昏闂锛焅n"
             "- Q: 娣峰悎妫€绱㈢浉姣旂函鍚戦噺妫€绱㈡湁浠€涔堜紭鍔匡紵"),
        ]),
        # 绗簲绔?
        ("绗簲绔? 鍚戦噺鏁版嵁搴撲笌 Embedding", [
            ("5.1 Embedding 妯″瀷閫夊瀷",
             "閫夋嫨 Embedding 妯″瀷鏃堕渶瑕佺患鍚堣€冭檻浠ヤ笅鍥犵礌锛氬悜閲忕淮搴︼紙褰卞搷瀛樺偍鍜岃绠楁垚鏈級銆?
             "鎺ㄧ悊閫熷害锛堝奖鍝嶆憚鍙栧拰鏌ヨ寤惰繜锛夈€佽涔夎川閲忥紙灏ゅ叾鏄腑鏂囧拰澶氳瑷€鑳藉姏锛夈€佷互鍙婇儴缃叉柟寮?
             "锛堜簯绔?API vs 鏈湴鎺ㄧ悊锛夈€傚浜庝腑鏂囧満鏅紝BGE-large-zh 鍜?GTE-large-zh 鍦?MTEB "
             "涓枃姒滃崟涓婅〃鐜版渶浣炽€?),
            ("5.2 鍚戦噺鏁版嵁搴撳姣?,
             "涓绘祦鍚戦噺鏁版嵁搴撳寘鎷?ChromaDB锛堣交閲忕骇銆侀€傚悎蹇€熷師鍨嬶級銆丗AISS锛團acebook 寮€婧愩€?
             "楂樻€ц兘 ANN 鎼滅储锛夈€丮ilvus锛堝垎甯冨紡銆侀€傚悎澶ц妯＄敓浜х幆澧冿級銆丳inecone锛堝叏鎵樼浜戞湇鍔★級銆?
             "鍜?Weaviate锛堟敮鎸佹贩鍚堟悳绱㈠拰 GraphQL锛夈€傛湰椤圭洰閫夋嫨 ChromaDB锛屽洜鍏剁畝鍗曟槗鐢ㄣ€?
             "鏀寔鎸佷箙鍖栥€佷笖涓?Python 鐢熸€侀泦鎴愯壇濂姐€?),
            ("5.3 ANN 绱㈠紩绠楁硶",
             "杩戜技鏈€杩戦偦锛圓NN锛夌畻娉曟槸鍚戦噺妫€绱㈢殑鏍稿績銆傚父瑙佹柟妗堝寘鎷細\n"
             "- HNSW锛圚ierarchical Navigable Small World锛夛細澶氬眰鍥剧粨鏋勶紝鏌ヨ蹇絾鏋勫缓鎱n"
             "- IVF锛圛nverted File Index锛夛細鍊掓帓绱㈠紩 + 鑱氱被锛岄€傚悎澶ц妯℃暟鎹甛n"
             "- PQ锛圥roduct Quantization锛夛細鍚戦噺鍘嬬缉锛屽ぇ骞呴檷浣庡瓨鍌╘n"
             "ChromaDB 榛樿浣跨敤 HNSW 绠楁硶锛屽浜庢湰椤圭洰鐨勬暟鎹妯℃槸鏈€浼橀€夋嫨銆?),
            ("5.4 Embedding 浼樺寲鎶€宸?,
             "鎻愬崌 Embedding 璐ㄩ噺鐨勬妧宸э細\n"
             "1. 鍦?Chunk 鍓嶆坊鍔?Instruction Prefix锛堝銆屼负妫€绱紭鍖栵細銆嶏級\n"
             "2. 浣跨敤 Matryoshka Embedding 鎸夐渶鎴柇缁村害\n"
             "3. 瀵规煡璇㈠仛 HyDE锛圚ypothetical Document Embedding锛夋墿灞昞n"
             "4. 浣跨敤棰嗗煙寰皟鐨?Embedding 妯″瀷鎻愬崌涓撲笟棰嗗煙鏁堟灉"),
        ]),
        # 绗叚绔?
        ("绗叚绔? 娣峰悎妫€绱笌閲嶆帓搴?, [
            ("6.1 绋犲瘑妫€绱?vs 绋€鐤忔绱?,
             "绋犲瘑妫€绱㈠熀浜庤涔夊悜閲忕浉浼煎害锛屾搮闀垮鐞嗗悓涔夎瘝銆佽繎涔夎瘝鍜岃涔夌悊瑙ｏ紱绋€鐤忔绱㈠熀浜庡叧閿瘝"
             "鍖归厤锛堝 BM25锛夛紝鎿呴暱澶勭悊涓撴湁鍚嶈瘝銆佺簿纭暟瀛楀拰浣庨璇嶆眹銆備袱鑰呭叿鏈夊ぉ鐒剁殑浜掕ˉ鎬э細"
             "绋犲瘑妫€绱㈣В鍐炽€岃涔夋紓绉汇€嶉棶棰橈紝绋€鐤忔绱㈣В鍐炽€岀簿纭尮閰嶃€嶉棶棰樸€?),
            ("6.2 RRF 铻嶅悎绛栫暐",
             "RRF锛圧eciprocal Rank Fusion锛夋槸鏈€绠€鍗曟湁鏁堢殑鎺掑悕铻嶅悎鏂规硶銆傚叕寮忥細"
             "score(d) = 危 1/(k + rank_i(d))锛屽叾涓?k 閫氬父鍙?60銆俁RF 鐨勪紭鍔挎槸涓庡垎鏁伴噺绾叉棤鍏筹紝"
             "鍙互鐩存帴铻嶅悎涓嶅悓绯荤粺鐨勬帓鍚嶇粨鏋溿€傜浉姣斾簬 CombSUM銆丆ombMNZ 绛夋潈閲嶆柟妗堬紝"
             "RRF 涓嶉渶瑕佽皟鍙傦紝椴佹鎬ф洿濂姐€?),
            ("6.3 Cross-Encoder Reranker",
             "Cross-Encoder 灏嗘煡璇㈠拰鏂囨。鎷兼帴涓轰竴涓簭鍒楄緭鍏?BERT 绫绘ā鍨嬶紝閫氳繃鍏ㄤ氦浜掓敞鎰忓姏"
             "璁＄畻绮剧粏鐨勭浉鍏虫€у垎鏁般€傚父鐢ㄦā鍨嬪寘鎷?ms-marco-MiniLM-L-12-v2 鍜?BGE-reranker銆?
             "Cross-Encoder 绮惧害楂樹絾閫熷害鎱紙O(n) 娆″墠鍚戜紶鎾級锛岄€氬父鐢ㄤ簬瀵圭矖鎺?Top-50 缁撴灉"
             "杩涜绮炬帓锛屾渶缁堝彇 Top-3~5 浣滀负鏈€缁堢粨鏋溿€?),
            ("6.4 LLM Reranker",
             "浣跨敤 LLM锛堝 GPT-4o锛変綔涓?Reranker锛岄€氳繃 Prompt 璁╂ā鍨嬪姣忎釜 Chunk 涓?Query 鐨?
             "鐩稿叧鎬ф墦鍒嗭紙1-10 鍒嗭級锛岀劧鍚庢寜鍒嗘暟閲嶆帓銆備紭鍔挎槸绮惧害楂樸€佸彲瑙ｉ噴鎬у己锛涚己鐐规槸寤惰繜楂樸€?
             "鎴愭湰澶с€傞€傚悎瀵瑰噯纭巼瑕佹眰鏋侀珮銆佸寤惰繜涓嶆晱鎰熺殑鍦烘櫙銆?),
        ]),
        # 绗竷绔?
        ("绗竷绔? 鏂囨。澶勭悊涓庡垎鍧楃瓥鐣?, [
            ("7.1 鏂囨。瑙ｆ瀽",
             "鏂囨。瑙ｆ瀽鏄?RAG 鏁版嵁鎽勫彇鐨勭涓€姝ャ€侾DF 瑙ｆ瀽闈复鐨勬寫鎴樺寘鎷細琛ㄦ牸璇嗗埆銆佸鏍忔帓鐗堛€?
             "鎵弿浠?OCR銆佸浘鐗囨彁鍙栥€佷互鍙婇〉鐪夐〉鑴氳繃婊ゃ€傛湰椤圭洰浣跨敤 MarkItDown 搴撳皢 PDF 杞崲涓?"
             "Markdown 鏍煎紡锛屼繚鐣欐爣棰樺眰绾у拰鏍煎紡淇℃伅锛屼负鍚庣画鍒嗗潡鎻愪緵缁撴瀯鍖栫嚎绱€?),
            ("7.2 鍒嗗潡绛栫暐閫夋嫨",
             "涓嶅悓绫诲瀷鐨勬枃妗ｉ€傚悎涓嶅悓鐨勫垎鍧楃瓥鐣ワ細缁撴瀯鍖栨妧鏈枃妗ｉ€傚悎鎸夋爣棰樺眰绾у垏鍒嗭紱闀跨瘒鍙欒堪鎬ф枃鏈?
             "閫傚悎璇箟鍒嗗潡锛堝熀浜?Embedding 鐩镐技搴︽娴嬩富棰樿浆鎹㈢偣锛夛紱浠ｇ爜鏂囨。閫傚悎鎸夊嚱鏁?绫讳负鍗曚綅"
             "鍒囧垎銆傛湰椤圭洰榛樿浣跨敤閫掑綊瀛楃鍒囧垎锛坈hunk_size=1000, overlap=200锛夛紝骞跺彲閫氳繃閰嶇疆鍒囨崲銆?),
            ("7.3 鍏冩暟鎹寮?,
             "涓?Chunk 闄勫姞涓板瘜鐨勫厓鏁版嵁鍙互鏄捐憲鎻愬崌妫€绱㈡晥鏋溿€傛湰椤圭洰閫氳繃 LLM 涓烘瘡涓?Chunk 鐢熸垚锛?
             "- title锛氭鎷?Chunk 涓婚鐨勭煭鏍囬\n"
             "- summary锛?0-100 瀛楃殑鍐呭鎽樿\n"
             "- tags锛?-5 涓叧閿瘝鏍囩\n"
             "杩欎簺鍏冩暟鎹彲鐢ㄤ簬妫€绱㈡椂鐨勮緟鍔╄繃婊ゃ€佸湪鎼滅储缁撴灉涓彁渚涘揩閫熼瑙堛€?),
            ("7.4 鍥剧墖澶勭悊娴佺▼",
             "瀵逛簬鍖呭惈鍥剧墖鐨?PDF锛岀郴缁熶細锛歕n"
             "1. 鍦ㄨВ鏋愰樁娈垫彁鍙栧祵鍏ュ浘鐗囷紝浠?SHA256 鍝堝笇鍛藉悕瀛樺偍\n"
             "2. 璋冪敤 Vision LLM锛堝 GPT-4o锛夌敓鎴愪腑鏂囧浘鐗囨弿杩癨n"
             "3. 灏嗗浘鐗囨弿杩版敞鍏ュ搴?Chunk 鐨?metadata\n"
             "4. 鍦ㄦ煡璇㈡椂鍙€氳繃鏂囧瓧鎻忚堪鍖归厤鍒扮浉鍏冲浘鐗嘰n"
             "5. MCP 宸ュ叿杩斿洖缁撴灉鏃跺寘鍚?Base64 缂栫爜鐨勫浘鐗囬瑙?),
        ]),
        # 绗叓绔?
        ("绗叓绔? Agent 涓庡伐鍏疯皟鐢?, [
            ("8.1 Agent 鍩虹姒傚康",
             "Agent 鏄兘澶熻嚜涓绘劅鐭ョ幆澧冦€佽鍒掍换鍔°€佹墽琛屽姩浣滃苟鏍规嵁鍙嶉璋冩暣绛栫暐鐨?AI 绯荤粺銆?
             "涓庣畝鍗曠殑 Prompt 鈫?Response 妯″紡涓嶅悓锛孉gent 寮曞叆浜嗗伐鍏疯皟鐢ㄣ€佽蹇嗙鐞嗗拰鍙嶆€濇満鍒讹紝"
             "浣?LLM 鑳藉澶勭悊闇€瑕佸姝ユ帹鐞嗗拰澶栭儴浜や簰鐨勫鏉備换鍔°€?),
            ("8.2 宸ュ叿璋冪敤鏈哄埗",
             "宸ュ叿璋冪敤锛團unction Calling / Tool Use锛夋槸 Agent 鐨勬牳蹇冭兘鍔涖€傜幇浠?LLM 鏀寔鍦?
             "瀵硅瘽涓敓鎴愮粨鏋勫寲鐨勫伐鍏疯皟鐢ㄨ姹傦紙JSON 鏍煎紡锛夛紝鐢辫繍琛屾椂鎵ц瀵瑰簲鍔熻兘鍚庡皢缁撴灉杩斿洖缁?
             "妯″瀷銆傚父瑙佸伐鍏风被鍨嬪寘鎷細鎼滅储寮曟搸銆佹暟鎹簱鏌ヨ銆佽绠楀櫒銆佷唬鐮佹墽琛屽櫒銆佹枃浠舵搷浣滅瓑銆?),
            ("8.3 MCP 鍗忚璇﹁В",
             "Model Context Protocol (MCP) 鏍囧噯鍖栦簡 LLM 涓庡伐鍏蜂箣闂寸殑閫氫俊鍗忚銆傛牳蹇冩帴鍙ｅ寘鎷細\n"
             "- tools/list锛氳繑鍥炲彲鐢ㄥ伐鍏峰垪琛ㄥ強鍏跺弬鏁?Schema\n"
             "- tools/call锛氭墽琛屾寚瀹氬伐鍏峰苟杩斿洖缁撴灉\n"
             "- resources/list锛氬垪鍑哄彲璁块棶鐨勮祫婧愶紙濡傛枃浠躲€佹暟鎹簱锛塡n"
             "鏈」鐩殑 MCP Server 閫氳繃 Stdio 浼犺緭灞備笌 VS Code Copilot 闆嗘垚銆?),
            ("8.4 Agent 璁捐妯″紡",
             "甯歌鐨?Agent 璁捐妯″紡鍖呮嫭锛歕n"
             "- ReAct锛歊easoning + Acting 浜ゆ浛杩涜\n"
             "- Plan-and-Execute锛氬厛鍒跺畾瀹屾暣璁″垝鍐嶉€愭鎵ц\n"
             "- Reflection锛氭墽琛屽悗鑷垜鍙嶆€濆苟淇\n"
             "- Multi-Agent锛氬涓?Agent 鍗忎綔瀹屾垚浠诲姟锛屽悇鑷礋璐ｄ笉鍚岃亴鑳?),
        ]),
        # 绗節绔?
        ("绗節绔? 妯″瀷璇勪及涓庡熀鍑嗘祴璇?, [
            ("9.1 RAG 璇勪及妗嗘灦",
             "RAG 绯荤粺鐨勮瘎浼伴渶瑕佸悓鏃惰€冭檻妫€绱㈣川閲忓拰鐢熸垚璐ㄩ噺涓や釜缁村害銆傛绱㈢淮搴﹀叧娉ㄧ殑鏄兘鍚?
             "鎵惧埌姝ｇ‘鐨勬枃妗ｏ紙Hit Rate銆丮RR銆丯DCG锛夛紱鐢熸垚缁村害鍏虫敞鐨勬槸 LLM 杈撳嚭鐨勮川閲?
             "锛團aithfulness銆丄nswer Relevancy銆丆ontext Precision锛夈€?),
            ("9.2 Ragas 璇勪及宸ュ叿",
             "Ragas 鏄竴涓笓闂ㄧ敤浜?RAG 绯荤粺璇勪及鐨勫紑婧愭鏋躲€傚畠鎻愪緵浜嗕竴绯诲垪鍩轰簬 LLM-as-Judge "
             "鐨勮瘎浼版寚鏍囷細Faithfulness 琛￠噺鍥炵瓟鏄惁蹇犲疄浜庢绱笂涓嬫枃锛孉nswer Relevancy 琛￠噺"
             "鍥炵瓟涓庨棶棰樼殑鐩稿叧搴︼紝Context Precision 琛￠噺妫€绱笂涓嬫枃涓浉鍏充俊鎭殑鍗犳瘮銆?
             "Ragas 閫氳繃璋冪敤 LLM 瀵瑰洖绛旇繘琛岃嚜鍔ㄨ瘎鍒嗭紝鏃犻渶浜哄伐鏍囨敞銆?),
            ("9.3 Golden Test Set",
             "Golden Test Set 鏄竴缁勯瀹氫箟鐨勬煡璇?鏈熸湜绛旀瀵癸紝鐢ㄤ簬鎵归噺璇勪及绯荤粺鐨勭鍒扮璐ㄩ噺銆?
             "鏋勫缓 Golden Test Set 鏃跺簲瑕嗙洊涓嶅悓绫诲瀷鐨勬煡璇細浜嬪疄鎬ч棶棰樸€佹帹鐞嗘€ч棶棰樸€佸璺抽棶棰樸€?
             "鍚﹀畾鏌ヨ绛夈€傛湰椤圭洰鍦?tests/fixtures/golden_test_set.json 涓淮鎶や簡娴嬭瘯闆嗐€?),
            ("9.4 A/B 娴嬭瘯鏂规硶",
             "瀵?RAG 绯荤粺鐨勬敼鍔紙濡傚垏鎹?Embedding 妯″瀷銆佽皟鏁村垎鍧楀弬鏁帮級闇€瑕侀€氳繃 A/B 娴嬭瘯楠岃瘉"
             "鏁堟灉銆傛柟娉曟槸鍦ㄧ浉鍚岀殑 Golden Test Set 涓婂垎鍒繍琛屾敼鍔ㄥ墠鍚庣殑绯荤粺锛屽姣斿悇椤规寚鏍囥€?
             "Evaluation Panel 椤甸潰鐨?History 鍔熻兘鏀寔淇濆瓨鍜屽姣斿巻鍙茶瘎浼拌褰曘€?),
        ]),
        # 绗崄绔?
        ("绗崄绔? 鎺ㄧ悊浼樺寲涓庨儴缃?, [
            ("10.1 妯″瀷閲忓寲",
             "妯″瀷閲忓寲灏嗘诞鐐规潈閲嶈浆鎹负浣庣簿搴﹁〃绀猴紙濡?INT8銆両NT4銆丗P16锛夛紝澶у箙闄嶄綆妯″瀷鐨?
             "瀛樺偍绌洪棿鍜屾帹鐞嗚绠楅噺銆傚父鐢ㄦ柟妗堝寘鎷細GPTQ锛圥ost-Training Quantization锛夈€?
             "AWQ锛圓ctivation-aware Weight Quantization锛夊拰 bitsandbytes锛圢F4 閲忓寲锛夈€?
             "4-bit 閲忓寲閫氬父鍙皢妯″瀷澶у皬鍑忓皯 75%锛屾€ц兘鎹熷け鍦?1-3% 浠ュ唴銆?),
            ("10.2 鎺ㄧ悊妗嗘灦",
             "涓绘祦鐨?LLM 鎺ㄧ悊妗嗘灦鍖呮嫭锛歕n"
             "- vLLM锛氭敮鎸?PagedAttention锛屽唴瀛樻晥鐜囬珮\n"
             "- TGI锛圱ext Generation Inference锛夛細HuggingFace 鍑哄搧\n"
             "- Ollama锛氭湰鍦伴儴缃蹭竴閿繍琛孿n"
             "- LM Studio锛氬浘褰㈠寲鏈湴閮ㄧ讲宸ュ叿\n"
             "- TensorRT-LLM锛歂VIDIA 瀹樻柟浼樺寲妗嗘灦\n"
             "閫夋嫨妗嗘灦鏃堕渶缁煎悎鑰冭檻鍚炲悙閲忛渶姹傘€佺‖浠舵潯浠跺拰鏄撶敤鎬с€?),
            ("10.3 Serving 绛栫暐",
             "鐢熶骇鐜涓殑 LLM Serving 闇€瑕佽€冭檻锛氬苟鍙戣姹傜鐞嗭紙璇锋眰闃熷垪 + 鎵瑰鐞嗭級銆?
             "娴佸紡杈撳嚭锛圫erver-Sent Events / WebSocket锛夈€佽礋杞藉潎琛★紙澶氬疄渚?+ Gateway锛夈€?
             "浠ュ強鏁呴殰鎭㈠锛堝仴搴锋鏌?+ 鑷姩閲嶅惎锛夈€傚浜?RAG 搴旂敤锛岃繕闇€瑕佽€冭檻 Embedding "
             "鏈嶅姟鍜屽悜閲忔暟鎹簱鐨勭嫭绔嬫墿灞曘€?),
            ("10.4 鎴愭湰浼樺寲",
             "浣跨敤浜戠 API 鐨勬垚鏈紭鍖栫瓥鐣ワ細\n"
             "1. 璇箟缂撳瓨鍑忓皯閲嶅璋冪敤\n"
             "2. 鍚堢悊璁剧疆 max_tokens 閬垮厤娴垂\n"
             "3. 浣跨敤杈冨皬妯″瀷鍋氬垵绛涳紝澶фā鍨嬪仛绮炬帓\n"
             "4. 瀵归潪鍏抽敭鍔熻兘浣跨敤鏇翠究瀹滅殑妯″瀷锛堝 Chunk Refiner 鐢ㄨ緝灏忔ā鍨嬶級\n"
             "5. 鎵归噺 Embedding 鍑忓皯 API 璋冪敤娆℃暟"),
        ]),
        # 绗崄涓€绔?
        ("绗崄涓€绔? 澶氭ā鎬佸ぇ妯″瀷", [
            ("11.1 瑙嗚璇█妯″瀷 (VLM)",
             "瑙嗚璇█妯″瀷锛堝 GPT-4o銆丆laude Vision銆丟emini锛夎兘澶熷悓鏃剁悊瑙ｆ枃鏈拰鍥惧儚锛?
             "鏄疄鐜板妯℃€?RAG 鐨勫熀纭€銆傚湪鏈」鐩腑锛孷LM 鐢ㄤ簬涓?PDF 涓彁鍙栫殑鍥剧墖鐢熸垚涓枃鎻忚堪"
             "锛圛mage Captioning锛夛紝浣垮浘鐗囧唴瀹逛篃鍙互閫氳繃鏂囧瓧妫€绱㈣鍙戠幇銆?),
            ("11.2 澶氭ā鎬?RAG",
             "澶氭ā鎬?RAG 灏嗘绱㈣寖鍥翠粠绾枃鏈墿灞曞埌鍥炬枃娣峰悎鍐呭銆傚疄鐜版€濊矾鏈変袱绉嶏細\n"
             "1. 灏嗗浘鐗囪浆鍖栦负鏂囨湰鎻忚堪鍚庣粺涓€鍋氭枃鏈绱紙鏈」鐩噰鐢ㄦ柟妗堬級\n"
             "2. 浣跨敤 CLIP 绛夊妯℃€?Embedding 妯″瀷鍚屾椂缂栫爜鏂囨湰鍜屽浘鐗嘰n"
             "鏂规 1 瀹炵幇绠€鍗曘€佸吋瀹规€уソ锛涙柟妗?2 淇濈暀浜嗘洿涓板瘜鐨勮瑙変俊鎭絾澶嶆潅搴︽洿楂樸€?),
            ("11.3 鍥剧墖鎻忚堪鐢熸垚鏈€浣冲疄璺?,
             "鐢熸垚楂樿川閲?Image Caption 鐨勫叧閿細\n"
             "1. 浣跨敤鍏蜂綋鐨?Prompt 鎸囧鎻忚堪閲嶇偣锛堝銆岃璇︾粏鎻忚堪鍥句腑鐨勬祦绋嬪拰鏁版嵁銆嶏級\n"
             "2. 涓轰笉鍚岀被鍨嬬殑鍥剧墖浣跨敤涓嶅悓鐨?Prompt锛堟埅鍥?vs 鐓х墖 vs 鍥捐〃锛塡n"
             "3. 杈撳嚭涓枃鎻忚堪浠ュ尮閰嶄腑鏂囨绱㈤渶姹俓n"
             "4. 闄愬埗鎻忚堪闀垮害锛岄伩鍏嶈繃闀跨殑 caption 骞叉壈妫€绱?),
            ("11.4 OCR 涓庢枃妗ｇ悊瑙?,
             "瀵逛簬鎵弿浠?PDF锛岄渶瑕佷娇鐢?OCR锛堝厜瀛﹀瓧绗﹁瘑鍒級鎻愬彇鏂囧瓧銆傜幇浠?OCR 鏂规鍖呮嫭 "
             "Tesseract锛堝紑婧愶級銆丄zure Document Intelligence锛堜簯鏈嶅姟锛夊拰 PaddleOCR锛堢櫨搴﹀紑婧愶級銆?
             "缁撳悎 Layout 鍒嗘瀽妯″瀷鍙互杩涗竴姝ョ悊瑙ｆ枃妗ｇ増闈㈢粨鏋勶紝姝ｇ‘璇嗗埆琛ㄦ牸銆佹爣棰樺拰娈佃惤銆?),
        ]),
        # 绗崄浜岀珷
        ("绗崄浜岀珷  瀹夊叏涓庡榻?, [
            ("12.1 瀵归綈鎶€鏈?,
             "妯″瀷瀵归綈锛圓lignment锛夋棬鍦ㄤ娇 LLM 鐨勮涓虹鍚堜汉绫讳环鍊艰鍜屾剰鍥俱€備富瑕佹墜娈靛寘鎷?RLHF銆?
             "DPO銆丆onstitutional AI 绛夈€傚榻愮殑鐩爣閫氬父姒傛嫭涓?HHH 鍘熷垯锛欻elpful锛堟湁甯姪锛夈€?
             "Harmless锛堟棤瀹筹級銆丠onest锛堣瘹瀹烇級銆?),
            ("12.2 RAG 瀹夊叏娉ㄦ剰浜嬮」",
             "RAG 绯荤粺闈复鐨勫畨鍏ㄩ闄╁寘鎷細\n"
             "1. 鐭ヨ瘑搴撴姇姣掞細鎭舵剰鏂囨。琚憚鍏ョ煡璇嗗簱锛屾薄鏌撴绱㈢粨鏋淺n"
             "2. Prompt 娉ㄥ叆锛氱敤鎴烽€氳繃鏌ヨ娉ㄥ叆鎭舵剰鎸囦护\n"
             "3. 鏁版嵁娉勯湶锛氭晱鎰熸枃妗ｅ唴瀹归€氳繃妫€绱㈢粨鏋滄毚闇瞈n"
             "4. 寮曠敤浼€狅細LLM 缂栭€犱笉瀛樺湪鐨勫紩鐢ㄦ潵婧?),
            ("12.3 闃插尽鎺柦",
             "閽堝涓婅堪椋庨櫓鐨勯槻寰℃柟妗堬細\n"
             "1. 鏂囨。鎽勫叆鏃惰繘琛屽唴瀹瑰鏌ュ拰鍒嗙被\n"
             "2. 鏌ヨ杈撳叆杩囨护鍜?sanitization\n"
             "3. 鍩轰簬瑙掕壊鐨勮闂帶鍒讹紙RBAC锛夛紝涓嶅悓鐢ㄦ埛鍙兘妫€绱㈡巿鏉冩枃妗n"
             "4. 杈撳嚭妫€楠岋細楠岃瘉寮曠敤鐨?chunk_id 鍜?source 纭疄瀛樺湪\n"
             "5. 瀹¤鏃ュ織锛氳褰曟墍鏈夋煡璇㈠拰杩斿洖鍐呭锛屼究浜庤拷婧?),
            ("12.4 绾㈤槦娴嬭瘯",
             "绾㈤槦娴嬭瘯锛圧ed Teaming锛夐€氳繃妯℃嫙鏀诲嚮鏉ュ彂鐜扮郴缁熷畨鍏ㄦ紡娲炪€傚 RAG 绯荤粺锛?
             "绾㈤槦娴嬭瘯搴旇鐩栵細鎭舵剰鏌ヨ锛堝皾璇曟彁鍙栫郴缁?Prompt锛夈€佽秺鐙辨敾鍑伙紙缁曡繃瀹夊叏闄愬埗锛夈€?
             "鏁版嵁鎻愬彇鏀诲嚮锛堝皾璇曡幏鍙栧畬鏁存枃妗ｅ唴瀹癸級绛夊満鏅€傚缓璁畾鏈熻繘琛岀孩闃熻瘎浼般€?),
        ]),
        # 绗崄涓夌珷
        ("绗崄涓夌珷  琛屼笟搴旂敤妗堜緥", [
            ("13.1 浼佷笟鐭ヨ瘑搴?,
             "浼佷笟鍐呴儴鐭ヨ瘑搴撴槸 RAG 鏈€鍏稿瀷鐨勫簲鐢ㄥ満鏅€傛牳蹇冮渶姹傚寘鎷細澶氭牸寮忔枃妗ｆ敮鎸併€?
             "鏉冮檺鎺у埗銆佸疄鏃舵洿鏂板拰楂樺彲鐢ㄦ€с€傚吀鍨嬫灦鏋勪负锛氭枃妗ｇ鐞嗙郴缁?鈫?鑷姩鎽勫彇 Pipeline 鈫?"
             "鍚戦噺鏁版嵁搴?鈫?RAG API 鈫?浼佷笟鑱婂ぉ鏈哄櫒浜?宸ュ崟绯荤粺闆嗘垚銆?),
            ("13.2 鏅鸿兘瀹㈡湇",
             "鍩轰簬 RAG 鐨勬櫤鑳藉鏈嶇郴缁熷皢浜у搧鏂囨。銆丗AQ銆佸巻鍙插伐鍗曠瓑浣滀负鐭ヨ瘑婧愶紝鐢ㄦ埛鎻愰棶鏃?
             "妫€绱㈢浉鍏冲唴瀹瑰苟鐢熸垚鍥炵瓟銆傜浉姣旂函 LLM 瀹㈡湇锛孯AG 瀹㈡湇鐨勪紭鍔挎槸鍥炵瓟鏇村噯纭€佸彲婧簮銆?
             "涓斿彲浠ラ€氳繃鏇存柊鐭ヨ瘑搴撳揩閫熷搷搴旀柊浜у搧/鏂版斂绛栧彉鏇淬€?),
            ("13.3 浠ｇ爜鍔╂墜",
             "浠ｇ爜鍔╂墜锛堝 GitHub Copilot锛夊彲浠ラ€氳繃 RAG 鎶€鏈帴鍏ラ」鐩唬鐮佸簱鍜屾枃妗ｏ紝"
             "浣?LLM 鍦ㄧ敓鎴愪唬鐮佹椂鑳藉鍙傝€冮」鐩殑鐜版湁瀹炵幇鍜岀害瀹氥€侻CP 鍗忚涓烘鎻愪緵浜嗘爣鍑嗗寲"
             "鎺ュ彛锛屼娇 AI 浠ｇ爜鍔╂墜鑳藉鍔ㄦ€佸彂鐜板拰鏌ヨ椤圭洰鐨勭煡璇嗗簱銆?),
            ("13.4 娉曞緥/鍖荤枟鏂囨。鍒嗘瀽",
             "鍦ㄦ硶寰嬪拰鍖荤枟绛変笓涓氶鍩燂紝RAG 绯荤粺鍙互甯姪涓撲笟浜哄憳蹇€熸绱㈠拰鍒嗘瀽澶ч噺鏂囨。銆?
             "杩欎簺鍦烘櫙瀵瑰噯纭€ц姹傛瀬楂橈紝閫氬父闇€瑕侊細棰嗗煙寰皟鐨?Embedding 妯″瀷銆佷弗鏍肩殑寮曠敤杩芥函"
             "鏈哄埗銆佷互鍙婁汉宸ュ鏍哥幆鑺傘€俁AG 鍦ㄦ绫诲満鏅腑浣滀负銆岃緟鍔╁伐鍏枫€嶈€岄潪銆屾浛浠ｅ喅绛栬€呫€嶃€?),
        ]),
        # 绗崄鍥涚珷
        ("绗崄鍥涚珷  闈㈣瘯楂橀闂绮鹃€?, [
            ("14.1 RAG 鐩稿叧闂",
             "Q1: 瑙ｉ噴 RAG 鐨勫伐浣滃師鐞嗭紝浠ュ強瀹冨浣曡В鍐?LLM 鐨勫够瑙夐棶棰橈紵\n"
             "Q2: 娣峰悎妫€绱紙Hybrid Search锛夌殑鍘熺悊鍜屼紭鍔挎槸浠€涔堬紵\n"
             "Q3: Cross-Encoder 鍜?Bi-Encoder 鐨勫尯鍒紵鍦?RAG 涓悇鑷殑瑙掕壊锛焅n"
             "Q4: 浣犳槸濡備綍璁捐鏂囨。鍒嗗潡绛栫暐鐨勶紵鑰冭檻浜嗗摢浜涘洜绱狅紵\n"
             "Q5: RAG vs 寰皟锛團ine-tuning锛夛紝鍒嗗埆鍦ㄤ粈涔堝満鏅笅浣跨敤锛?),
            ("14.2 Embedding 鐩稿叧闂",
             "Q1: 浣欏鸡鐩镐技搴﹀拰鍐呯Н锛圖ot Product锛夋湁浠€涔堝尯鍒紵浠€涔堟椂鍊欑敤鍝釜锛焅n"
             "Q2: 浠€涔堟槸 ANN锛堣繎浼兼渶杩戦偦锛夛紵甯歌鐨?ANN 绠楁硶鏈夊摢浜涳紵\n"
             "Q3: 濡備綍璇勪及 Embedding 妯″瀷鐨勮川閲忥紵鏈夊摢浜?Benchmark锛焅n"
             "Q4: Embedding 缁村害瓒婇珮瓒婂ソ鍚楋紵缁村害瀵规绱㈡晥鏋滃拰鎬ц兘鏈変粈涔堝奖鍝嶏紵\n"
             "Q5: 濡備綍澶勭悊銆岄鍩熺壒瀹氳瘝姹囥€嶇殑 Embedding 鏁堟灉涓嶅ソ鐨勯棶棰橈紵"),
            ("14.3 绯荤粺璁捐闂",
             "Q1: 璁捐涓€涓敮鎸佺櫨涓囩骇鏂囨。鐨?RAG 绯荤粺锛屼綘浼氭€庝箞鍋氾紵\n"
             "Q2: 濡備綍瀹炵幇 RAG 绯荤粺鐨勫閲忔洿鏂帮紙鏂板/鍒犻櫎/淇敼鏂囨。锛夛紵\n"
             "Q3: 濡備綍鐩戞帶 RAG 绯荤粺鐨勭嚎涓婅川閲忥紵鏈夊摢浜涘叧閿寚鏍囷紵\n"
             "Q4: 濡備綍澶勭悊 RAG 涓殑澶氳瑷€闂锛焅n"
             "Q5: 浣犵殑 RAG 椤圭洰涓亣鍒颁簡浠€涔堟妧鏈寫鎴橈紵濡備綍瑙ｅ喅鐨勶紵"),
            ("14.4 Agent 鐩稿叧闂",
             "Q1: 浠€涔堟槸 Agent锛熷拰鏅€氱殑 LLM 瀵硅瘽鏈変粈涔堝尯鍒紵\n"
             "Q2: 瑙ｉ噴 ReAct 妯″紡鐨勫伐浣滄祦绋嬨€俓n"
             "Q3: 宸ュ叿璋冪敤锛團unction Calling锛夋槸濡備綍瀹炵幇鐨勶紵\n"
             "Q4: 澶?Agent 鍗忎綔鏈夊摢浜涘父瑙佹ā寮忥紵\n"
             "Q5: 濡備綍璇勪及 Agent 鐨勮兘鍔涘拰鍙潬鎬э紵"),
        ]),
        # 绗崄浜旂珷
        ("绗崄浜旂珷  椤圭洰瀹炴垬缁忛獙鎬荤粨", [
            ("15.1 椤圭洰鏋舵瀯鍥為【",
             "鏈」鐩噰鐢?Modular RAG 鏋舵瀯锛屾牳蹇冩ā鍧楀寘鎷細鏂囨。瑙ｆ瀽锛圡arkItDown锛夈€?
             "鏅鸿兘鍒嗗潡锛圧ecursiveCharacterTextSplitter + LLM Refiner锛夈€佸弻璺紪鐮?
             "锛圓zure Embedding + BM25/jieba锛夈€佹贩鍚堟绱紙RRF 铻嶅悎锛夈€佸彲閫夐噸鎺掑簭"
             "锛圕ross-Encoder / LLM Reranker锛夈€佷互鍙?MCP Server 瀵瑰鎺ュ彛銆傚叏閾捐矾閲囩敤"
             "閰嶇疆椹卞姩鐨勫伐鍘傛ā寮忥紝鏀寔涓€閿垏鎹?Provider銆?),
            ("15.2 鎶€鏈寒鐐逛笌闈㈣瘯璇濇湳",
             "绠€鍘嗗拰闈㈣瘯涓彲浠ラ噸鐐圭獊鍑猴細\n"
             "1. 鍏ㄩ摼璺彲瑙傛祴鎬э細Streamlit Dashboard + 缁撴瀯鍖?Trace + 璇勪及闈㈡澘\n"
             "2. 娣峰悎妫€绱㈢瓥鐣ワ細Dense + Sparse + RRF 铻嶅悎 + 鍙€?Reranking\n"
             "3. 澶氭ā鎬佹敮鎸侊細PDF 鍥剧墖鎻愬彇 + Vision LLM Captioning\n"
             "4. 鍙彃鎷旀灦鏋勶細宸ュ巶妯″紡 + 閰嶇疆椹卞姩锛岄浂浠ｇ爜鍒囨崲 Provider\n"
             "5. 鏁版嵁瀹屾暣鎬э細SHA256 骞傜瓑鎽勫彇 + 璺ㄥ瓨鍌ㄧ骇鑱斿垹闄?),
            ("15.3 韪╁潙璁板綍",
             "寮€鍙戣繃绋嬩腑閬囧埌鐨勫吀鍨嬮棶棰樺拰瑙ｅ喅鏂规锛歕n"
             "1. 涓枃 BM25 鍒嗚瘝锛氶渶浣跨敤 jieba 鏇夸唬榛樿鑻辨枃鍒嗚瘝鍣╘n"
             "2. PDF 琛ㄦ牸瑙ｆ瀽锛歁arkItDown 瀵瑰鏉傝〃鏍兼敮鎸佹湁闄愶紝鍙兘涓㈠け鏍煎紡\n"
             "3. 鍚戦噺缁村害涓嶅尮閰嶏細鍒囨崲 Embedding 妯″瀷鍚庨渶瑕侀噸鏂版憚鍙栨墍鏈夋枃妗n"
             "4. Trace 鏂囦欢杩囧ぇ锛氶渶瑕佸畾鏈熸竻鐞嗘垨寮曞叆鏃ュ織杞浆\n"
             "5. Windows 缂栫爜闂锛氭帶鍒跺彴杈撳嚭闇€瑕佹樉寮忚缃?UTF-8 缂栫爜"),
            ("15.4 涓嬩竴姝ヨ鍒?,
             "鍙互缁х画杩唬鐨勬柟鍚戯細\n"
             "- 寮曞叆 GraphRAG锛岀粨鍚堢煡璇嗗浘璋彁鍗囧璺虫帹鐞嗚兘鍔沑n"
             "- 娣诲姞 Streaming Response 娴佸紡鐢熸垚\n"
             "- 鎺ュ叆鏇村鍚戦噺鏁版嵁搴擄紙FAISS銆丮ilvus锛塡n"
             "- 瀹炵幇鑷姩鍖?CI/CD 娴嬭瘯绠＄嚎\n"
             "- 鏀寔鏇村鏂囨。鏍煎紡锛圚TML銆佷唬鐮佹枃浠躲€侀煶瑙嗛杞啓锛?),
        ]),
    ]

    for ch_title, sections in chapter_contents:
        elems.append(Paragraph(ch_title, s["h1"]))
        for sec_title, sec_body in sections:
            elems.append(Paragraph(sec_title, s["h2"]))
            # Split by \n for multi-line paragraphs
            for para in sec_body.split("\n"):
                stripped = para.strip()
                if stripped:
                    elems.append(Paragraph(stripped, s["body"]))
        # Add padding content to ensure ~2 pages per chapter
        elems.append(Spacer(1, 0.15 * inch))
        elems.append(Paragraph("鏈珷灏忕粨", s["h2"]))
        elems.append(Paragraph(
            f"浠ヤ笂浠嬬粛浜唟ch_title[4:]}鐨勬牳蹇冩蹇靛拰鍏抽敭鎶€鏈鐐广€?
            "鐞嗚В杩欎簺鐭ヨ瘑瀵逛簬鏋勫缓楂樿川閲忕殑 RAG 绯荤粺鑷冲叧閲嶈銆傚湪瀹為檯闈㈣瘯涓紝"
            "闈㈣瘯瀹樺線寰€浼氫粠鍩虹姒傚康鍑哄彂锛岄€愭娣卞叆鍒板疄鐜扮粏鑺傚拰宸ョ▼缁忛獙銆?
            "寤鸿璇昏€呭湪闃呰鏈珷鍐呭鐨勫熀纭€涓婏紝缁撳悎椤圭洰浠ｇ爜杩涜瀹炶返楠岃瘉锛?
            "鍔犳繁瀵瑰悇椤规妧鏈殑鐞嗚В銆傚悓鏃讹紝娉ㄦ剰鍏虫敞璇ラ鍩熺殑鏈€鏂拌繘灞曪紝"
            "鍥犱负澶фā鍨嬫妧鏈彂灞曡繀閫燂紝鏂扮殑鏂规硶鍜屽伐鍏蜂笉鏂秾鐜般€?, s["body"]))
        elems.append(Paragraph(
            "鍦ㄥ噯澶囬潰璇曟椂锛屽缓璁皢鏈珷鐨勭煡璇嗙偣涓庡疄闄呴」鐩粡楠岀浉缁撳悎銆?
            "涓嶄粎瑕佽兘澶熸竻鏅板湴瑙ｉ噴鎶€鏈師鐞嗭紝杩樿鑳藉璇存槑鍦ㄥ疄闄呴」鐩腑"
            "濡備綍閫夊瀷銆佸浣曡皟浼樸€侀亣鍒颁簡鍝簺闂浠ュ強濡備綍瑙ｅ喅銆?
            "杩欑鐞嗚涓庡疄璺电粨鍚堢殑鍥炵瓟鏂瑰紡锛岃兘澶熺粰闈㈣瘯瀹樼暀涓嬫繁鍒诲嵃璞°€?
            "姝ゅ锛屽缓璁噯澶囦竴浜涘叿浣撶殑鏁版嵁鍜屾寚鏍囨潵鏀拺浣犵殑鎶€鏈喅绛栵紝"
            "渚嬪閫夋嫨鏌愪釜 Embedding 妯″瀷鍚庢绱㈢簿搴︽彁鍗囦簡澶氬皯銆?
            "寮曞叆 Reranker 鍚?Top-3 鍛戒腑鐜囦粠 X 鎻愬崌鍒?Y 绛夈€?, s["body"]))
        elems.append(Paragraph("寤朵几鎬濊€?, s["h2"]))
        elems.append(Paragraph(
            "瀛︿範鎶€鏈煡璇嗕笉鑳戒粎鍋滅暀鍦ㄨ〃闈紝闇€瑕佹繁鍏ユ€濊€冩瘡椤规妧鏈儗鍚庣殑璁捐鍔ㄦ満鍜屽彇鑸嶃€?
            "渚嬪锛屼负浠€涔?RAG 绯荤粺瑕侀噰鐢ㄤ袱闃舵妫€绱紙绮楁帓 + 绮炬帓锛夛紵杩欐槸鍥犱负绮炬帓妯″瀷"
            "锛堝 Cross-Encoder锛夎櫧鐒剁簿搴﹂珮锛屼絾璁＄畻鎴愭湰澶э紝鏃犳硶瀵瑰叏搴撹繘琛屾墦鍒嗐€?
            "閫氳繃绮楁帓蹇€熺瓫閫夊€欓€夐泦锛屽啀鐢ㄧ簿鎺掑仛绮剧粏璇勪及锛屾棦淇濊瘉浜嗙簿搴﹀張鎺у埗浜嗗欢杩熴€?
            "杩欑'婕忔枟寮?鏋舵瀯鎬濇兂鍦ㄦ悳绱㈠紩鎿庛€佹帹鑽愮郴缁熺瓑棰嗗煙閮芥湁骞挎硾搴旂敤銆?
            "闈㈣瘯涓鏋滆兘灞曠ず鍑鸿繖绉嶈法棰嗗煙鐨勬妧鏈閲庡拰宸ョ▼鐩磋锛屼細闈炲父鍔犲垎銆?
            "鍚屾椂锛屼篃瑕佸叧娉ㄥ悇绉嶆妧鏈殑灞€闄愭€у拰閫傜敤杈圭晫銆傛病鏈夐摱寮癸紝姣忕鏂规閮芥湁鍏?
            "鏈€浣冲簲鐢ㄥ満鏅€傝兘澶熸牴鎹叿浣撻渶姹傞€夋嫨鍚堥€傜殑鎶€鏈柟妗堬紝鏄珮绾у伐绋嬪笀鐨勬牳蹇冭兘鍔涖€?, s["body"]))
        elems.append(PageBreak())

    # Build
    doc.build(elems)
    print(f"鉁?Generated: {output}")


# ===================================================================
# Main
# ===================================================================

def main() -> None:
    output_dir = Path(__file__).parent / "sample_documents"
    output_dir.mkdir(parents=True, exist_ok=True)

    generate_chinese_technical_doc(output_dir / "chinese_technical_doc.pdf")
    generate_chinese_table_chart_doc(output_dir / "chinese_table_chart_doc.pdf")
    generate_chinese_long_doc(output_dir / "chinese_long_doc.pdf")

    print("\n馃帀 All QA test PDFs generated successfully!")


if __name__ == "__main__":
    main()

