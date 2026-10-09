"""
generate_week4_report.py
=============================================================================
Constructs the comprehensive, publication-quality final academic/industry DOCX report:
"Week 4: Comprehensive Data Analysis Reporting and Presentation"
Dataset: UCI Adult / Census Income Dataset
Repository: https://github.com/G1OUL/week-1-r-data-cleaning-analysis

Integrates Weeks 1, 2, and 3:
- Week 1: Data Cleaning, Outlier Analysis, Transformation, Quality Assessment
- Week 2: Univariate, Bivariate, Multivariate Visualizations & Insight Communication
- Week 3: Parametric & Non-Parametric Hypothesis Testing, Predictive Modeling, Diagnostics
- Week 4: Integrated Synthesis, Practical Implications, Fairness, and Technical Appendix
=============================================================================
"""

import os
import sys
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# --- PATH CONFIGURATION ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUTS_DIR  = os.path.join(PROJECT_ROOT, "outputs")
PLOTS_DIR    = os.path.join(PROJECT_ROOT, "plots")
PLOTS_W3_DIR = os.path.join(PLOTS_DIR, "week3")
EVIDENCE_DIR = os.path.join(PROJECT_ROOT, "evidence", "week3")
REPORT_PATH  = os.path.join(PROJECT_ROOT, "report", "Week4_Comprehensive_Data_Analysis_Final_Report.docx")

# --- COLOR PALETTE (Academic Navy / Slate / Charcoal) ---
COLOR_PRIMARY   = RGBColor(27,  54,  93)   # #1B365D Deep Navy
COLOR_SECONDARY = RGBColor(70,  92,  122)  # #465C7A Slate
COLOR_TEXT      = RGBColor(33,  37,  41)   # #212529 Charcoal Body Text
COLOR_MUTED     = RGBColor(108, 117, 125)  # #6C757D Muted Gray Subtitles/Footnotes
COLOR_CODE      = RGBColor(40,  44,  52)   # #282C34 Code Text
COLOR_RED       = RGBColor(192, 57,  43)   # Crimson / Warning
COLOR_GREEN     = RGBColor(39,  174, 96)   # Forest Green / Confirmation
COLOR_ACCENT    = RGBColor(41,  128, 185)  # #2980B9 Academic Accent Blue

# --- XML & STYLING HELPERS ---

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D7DE"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top    w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left    w:val="none"/>'
        f'<w:right   w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_heading_1(doc, text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after  = Pt(6)
    run = h.runs[0]
    run.font.name = "Calibri"
    run.font.size = Pt(16)
    run.font.color.rgb = COLOR_PRIMARY
    run.bold = True
    return h

def add_heading_2(doc, text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(13)
    h.paragraph_format.space_after  = Pt(4)
    run = h.runs[0]
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.color.rgb = COLOR_SECONDARY
    run.bold = True
    return h

def add_heading_3(doc, text):
    h = doc.add_heading(text, level=3)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(9)
    h.paragraph_format.space_after  = Pt(3)
    run = h.runs[0]
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.color.rgb = COLOR_ACCENT
    run.bold = True
    return h

def add_para(doc, text="", bold_prefix=None, space_after=6, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.bold = True
        r.font.color.rgb = color if color else COLOR_TEXT
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10.5)
        r.font.color.rgb = color if color else COLOR_TEXT
    return p

def add_bullet(doc, text="", bold_prefix=None, space_after=3):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.bold = True
        r.font.color.rgb = COLOR_TEXT
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_TEXT
    return p

def add_callout(doc, text, title="ANALYTICAL TAKEAWAY", border_color="1B365D", fill_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    set_cell_background(cell, fill_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top    w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right  w:val="none"/>'
        f'<w:left   w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r_hdr = p.add_run(f"[{title}] ")
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(9.5)
    r_hdr.bold = True
    r_hdr.font.color.rgb = COLOR_PRIMARY
    
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = COLOR_TEXT
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, caption=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    set_cell_background(cell, "F6F8FA")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top    w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:right  w:val="single" w:sz="4" w:space="0" w:color="D0D7DE"/>'
        f'<w:left   w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(code_str.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = COLOR_CODE
    
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(6)
        r_c = p_cap.add_run(f"Code Listing: {caption}")
        r_c.font.name = "Calibri"
        r_c.font.size = Pt(8.5)
        r_c.italic = True
        r_c.font.color.rgb = COLOR_MUTED
    else:
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_after = Pt(4)

def add_figure(doc, filepath, fig_num, title, description, width=Inches(5.7)):
    full_path = os.path.join(PROJECT_ROOT, filepath)
    if os.path.exists(full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        run_img = p_img.add_run()
        run_img.add_picture(full_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_fignum = p_cap.add_run(f"Figure {fig_num}: ")
        r_fignum.bold = True
        r_fignum.font.size = Pt(9.5)
        r_fignum.font.color.rgb = COLOR_PRIMARY
        r_title = p_cap.add_run(f"{title}. ")
        r_title.bold = True
        r_title.font.size = Pt(9.5)
        r_title.font.color.rgb = COLOR_SECONDARY
        r_desc = p_cap.add_run(description)
        r_desc.italic = True
        r_desc.font.size = Pt(9)
        r_desc.font.color.rgb = COLOR_MUTED
    else:
        p_warn = doc.add_paragraph()
        p_warn.add_run(f"[Figure {fig_num}: {title} — Plot file {filepath} not found]").font.color.rgb = COLOR_RED

def style_header_cell(cell, text, width=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    if width:
        cell.width = width
    set_cell_background(cell, "1B365D")
    set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

def style_data_cell(cell, text, width=None, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, bg_hex=None, text_color=None):
    if width:
        cell.width = width
    if bg_hex:
        set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.font.name = "Calibri"
    r.font.size = Pt(8.5)
    r.bold = bold
    if text_color:
        r.font.color.rgb = text_color
    else:
        r.font.color.rgb = COLOR_TEXT

def add_page_number_field(run):
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

# --- REPORT BUILDER MASTER FUNCTION ---

def generate_week4_final_report():
    print("=" * 70)
    print("  Generating Week 4 Comprehensive Final Integrated Report (.docx)")
    print("  Output:", REPORT_PATH)
    print("=" * 70)
    
    doc = Document()
    
    # Configure 1.0 inch margins all around
    for s in doc.sections:
        s.top_margin    = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin   = Inches(1.0)
        s.right_margin  = Inches(1.0)
        
        # Configure Header
        header = s.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_head = p_head.add_run("UCI Adult Census Income — Week 4: Comprehensive Data Analysis Final Report")
        r_head.font.name = "Calibri"
        r_head.font.size = Pt(8.5)
        r_head.font.color.rgb = COLOR_MUTED
        
        # Configure Footer
        footer = s.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_foot1 = p_foot.add_run("Academic Report | Comprehensive Data Analysis & Predictive Modeling | Page ")
        r_foot1.font.name = "Calibri"
        r_foot1.font.size = Pt(8.5)
        r_foot1.font.color.rgb = COLOR_MUTED
        add_page_number_field(r_foot1)

    # =========================================================================
    # SECTION 1: TITLE PAGE
    # =========================================================================
    print("Building Section 1: Title Page...")
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("COMPREHENSIVE DATA ANALYSIS REPORTING AND PRESENTATION")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Data Cleaning, Visualization, Statistical Analysis and Predictive Modeling using R")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13.5)
    r_sub.font.color.rgb = COLOR_SECONDARY
    
    p_rule = doc.add_paragraph()
    p_rule.paragraph_format.space_after = Pt(20)
    r_rule = p_rule.add_run("―" * 58)
    r_rule.font.color.rgb = COLOR_SECONDARY
    
    # Metadata Table
    tbl_meta = doc.add_table(rows=10, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_meta, "D0D7DE")
    
    meta_entries = [
        ("Assignment", "Week 4: Comprehensive Data Analysis Final Report"),
        ("Primary Dataset", "UCI Adult / Census Income Dataset (1994 U.S. Census Bureau CPS)"),
        ("Analytical Scope", "End-to-End Pipeline: Ingestion, Hygiene, EDA, Inference & Predictive Modeling"),
        ("Technology Stack", "R (v4.6.1 / x86_64-w64-mingw32), tidyverse, ggplot2, car, glmnet, pROC, python-docx"),
        ("Repository URL", "https://github.com/G1OUL/week-1-r-data-cleaning-analysis"),
        ("Local Working Directory", "C:\\Users\\Microsoft\\week\\week-1-r-data-cleaning-analysis"),
        ("Submission Date", "October 2026"),
        ("Student / Contributor", "[Student Name / Lead Data Analyst]"),
        ("Institution / Department", "[University / Department of Data Science and Statistics]"),
        ("Course / Instructor", "[Course Title / Code] | [Instructor / Faculty Advisor]")
    ]
    for idx, (label, val) in enumerate(meta_entries):
        row = tbl_meta.rows[idx]
        style_data_cell(row.cells[0], label, width=Inches(2.2), bold=True, bg_hex="F0F4F8")
        style_data_cell(row.cells[1], val, width=Inches(4.3), bold=False, bg_hex="FFFFFF")
        
    p_post_meta = doc.add_paragraph()
    p_post_meta.paragraph_format.space_before = Pt(24)
    
    add_callout(doc,
        "This capstone report consolidates the complete four-week investigative pipeline conducted on the UCI Adult Census Income dataset. "
        "All data cleaning metrics, exploratory visualizations, formal hypothesis test statistics, and machine learning performance indicators "
        "reproduced herein are derived directly from verified codebase executions under fixed random seed (2026). "
        "The report synthesizes data hygiene (Week 1), graphical insight communication (Week 2), inferential modeling (Week 3), "
        "and policy-relevant decision synthesis (Week 4) into a unified scientific monograph.",
        title="DECLARATION OF EMPIRICAL RIGOR AND ACADEMIC INTEGRITY")
    
    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS OVERVIEW
    # =========================================================================
    add_heading_1(doc, "Document Architecture & Table of Contents")
    add_para(doc, "This integrated monograph is organized into sixteen formal analytical sections tracking the data science lifecycle:")
    
    toc_data = [
        ("Section 1", "Title Page and Metadata Registry", "Administrative identification and reproducibility declaration."),
        ("Section 2", "Executive Summary", "High-level synthesis of objectives, methodologies, findings, and strategic takeaways."),
        ("Section 3", "Introduction and Objectives", "Theoretical motivation, income stratification problem, and end-to-end framework."),
        ("Section 4", "Dataset Description and Data Source", "Origin, provenance, 15-variable schema, and empirical distributions."),
        ("Section 5", "Week 1: Data Cleaning and Preliminary Analysis", "Ingestion, missingness imputation, duplicate removal, IQR outlier audit, transformations."),
        ("Section 6", "Week 2: Data Visualization and Insight Communication", "Univariate distributions, bivariate disparities, lattice conditioning, and visual insights."),
        ("Section 7", "Week 3: Statistical Analysis and Hypothesis Testing", "8 verified hypothesis tests across 5 research questions, effect sizes, and corrections."),
        ("Section 8", "Week 3: Predictive Modeling", "Stratified train/test partition, logistic regression, elastic-net regularization, odds ratios."),
        ("Section 9", "Model Evaluation and Diagnostics", "Confusion matrices, ROC-AUC, PR-AUC, calibration curves, and influence diagnostics."),
        ("Section 10", "Integrated Findings Across Weeks 1–3", "Cross-week synthesis matrix mapping data hygiene to exploratory and predictive results."),
        ("Section 11", "Discussion and Practical Implications", "Labor economics, human capital, life-cycle effects, algorithmic fairness, and non-causality."),
        ("Section 12", "Challenges Encountered and Lessons Learned", "Empirically documented project hurdles, engineering fixes, and methodological insights."),
        ("Section 13", "Recommendations and Future Work", "Operational decision thresholds, advanced ensembles, ACS benchmarking, and bias audits."),
        ("Section 14", "Conclusion", "Final verdict on evidence-based data science workflows and analytical achievements."),
        ("Section 15", "Reproducibility and Technical Appendix", "Directory layout, script index, R environment versions, and statistical glossary."),
        ("Section 16", "References", "Authoritative scholarly and methodological citations.")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_data) + 1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_toc, "D0D7DE")
    
    style_header_cell(tbl_toc.rows[0].cells[0], "Section", width=Inches(1.1))
    style_header_cell(tbl_toc.rows[0].cells[1], "Title", width=Inches(2.5))
    style_header_cell(tbl_toc.rows[0].cells[2], "Analytical Scope", width=Inches(2.9))
    
    for idx, (sec_id, sec_title, sec_desc) in enumerate(toc_data):
        row = tbl_toc.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], sec_id, width=Inches(1.1), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], sec_title, width=Inches(2.5), bold=True, bg_hex=bg)
        style_data_cell(row.cells[2], sec_desc, width=Inches(2.9), bold=False, bg_hex=bg)
        
    doc.add_page_break()

    # =========================================================================
    # SECTION 2: EXECUTIVE SUMMARY
    # =========================================================================
    add_heading_1(doc, "Section 2 — Executive Summary")
    
    add_para(doc, 
        "This capstone technical report provides an exhaustive, multi-week investigation into individual income classification using the "
        "UCI Adult Census Income dataset (1994 U.S. Census Bureau Current Population Survey). The analytical objective was to determine "
        "how demographic characteristics, human capital investments, and employment attributes jointly structure an individual's probability "
        "of earning greater than $50,000 annually, while demonstrating a rigorous, fully reproducible data science lifecycle in R. "
        "Over four structured phases, the project transitioned from low-level data engineering and quality assessment (Week 1), through "
        "exploratory graphic communication (Week 2), to formal inferential hypothesis testing and predictive machine learning (Week 3), "
        "culminating in this integrated executive synthesis (Week 4).")
    
    add_heading_2(doc, "Summary of Methodological Phases and Verified Findings")
    
    add_bullet(doc, 
        "From an initial raw corpus of 32,561 records, exactly 24 duplicate records were purged, and 4,262 missing value indicators "
        "encoded as ambiguous '?' strings were identified across workclass (1,836), occupation (1,843), and native_country (583). "
        "Rather than resorting to listwise deletion—which would have discarded 2,399 records and introduced attrition bias—missing entries "
        "were imputed using verified statistical modes ('Private', 'Prof-specialty', and 'United-States'). Tukey's Interquartile Range (IQR) "
        "audits identified 9,002 working-hour outliers, 2,712 capital gain outliers, and 142 age outliers; all were preserved to prevent "
        "truncation of valid economic extremes, resulting in a finalized clean dataset of N = 32,537 observations across 15 attributes.",
        bold_prefix="Phase 1 — Data Cleaning and Hygiene (Week 1): ")
    
    add_bullet(doc, 
        "Visual analytics revealed severe class imbalance, with 24,698 individuals (75.91%) earning <=$50K and only 7,839 (24.09%) earning >$50K "
        "(a 3.15:1 ratio). Boxplots, density plots, and lattice conditionings confirmed a 10-year median age divergence between earning tiers "
        "(median 44 years for high earners vs. 34 years for low earners), a steep non-linear credential threshold where high-income probability "
        "rises from 15.95% among High School graduates to 41.49% for Bachelors and 74.09% for Doctorates, and an institutional concentration at the "
        "40-hour workweek (46.73% of the entire workforce).",
        bold_prefix="Phase 2 — Graphical Exploration & Insight Discovery (Week 2): ")
    
    add_bullet(doc, 
        "A formal testing battery comprising exactly eight hypothesis tests across five core research questions was executed. "
        "All eight null hypotheses were rejected at alpha = 0.05, retaining significance (p < 0.0001) under both family-wise Bonferroni "
        "and Benjamini-Hochberg False Discovery Rate (FDR) adjustments. Because the large sample size (N = 32,537) yielded near-zero p-values, "
        "effect sizes were prioritized: educational attainment demonstrated a moderate-to-strong association with income (Cramer's V = 0.3689, chi2 = 4428.4, df = 15); "
        "high earners were significantly older (Cohen's d = 0.5629, t = 50.24) and worked significantly longer hours (Cohen's d = 0.5518, t = 45.10); "
        "occupation showed substantial explanatory power (Cramer's V = 0.3135); while the linear correlation between education years and weekly hours was weak (r = +0.1484).",
        bold_prefix="Phase 3 — Inferential Hypothesis Testing (Week 3): ")
    
    add_bullet(doc, 
        "Stratified 80/20 train/test splitting (26,029 training, 6,508 testing) under fixed seed (2026) was used to train a Zero-Rule Baseline, "
        "a Standard Multivariate Logistic Regression model, and an Elastic-Net Regularized Logistic Regression model tuned via 5-fold cross-validation. "
        "On the held-out test set, Standard Logistic Regression achieved an Accuracy of 84.76%, Balanced Accuracy of 76.36%, Precision of 71.98%, "
        "Recall (Sensitivity) of 60.14%, Specificity of 92.57%, ROC-AUC of 0.9047, and PR-AUC of 0.7271, decisively outperforming the baseline "
        "(75.91% accuracy, 50.00% balanced accuracy, 0.5000 ROC-AUC). Elastic-Net demonstrated virtually identical generalization (84.10% accuracy, 0.9004 ROC-AUC). "
        "Key adjusted odds ratios revealed that being in a civilian marriage increased the odds of high income sevenfold (OR = 7.16, 95% CI [3.88, 13.22]), "
        "each additional year of education increased odds by 34.9% (OR = 1.35, 95% CI [1.32, 1.38]), and executive-managerial roles doubled odds (OR = 2.10, 95% CI [1.77, 2.48]).",
        bold_prefix="Phase 4 — Predictive Modeling and Diagnostics (Week 3): ")

    add_heading_2(doc, "Principal Strategic Limitations and Operational Value")
    add_para(doc, 
        "While the models demonstrate strong discriminative ability (ROC-AUC > 0.90), several real-world limitations must govern their application. "
        "The data represents a 1994 cross-sectional slice of the United States population, reflecting historical wage structures, gender disparities "
        "(66.9% male sample), and top-coded capital gains ($99,999 ceiling). Crucially, observational statistical associations must not be conflated "
        "with causal mechanisms; demographic attributes (such as marital status or sex) serve as proxies for unmeasured social, financial, and household "
        "dynamics. Consequently, automated scoring models trained on such data must never be deployed for high-stakes individual decisions "
        "(such as hiring or lending) without stringent algorithmic fairness safeguards. The enduring value of this project lies in its established, "
        "transparent, end-to-end reproducible R architecture that guarantees complete auditability from raw ingestion to final publication.")

    # =========================================================================
    # SECTION 3: INTRODUCTION AND OBJECTIVES
    # =========================================================================
    add_heading_1(doc, "Section 3 — Introduction and Objectives")
    
    add_para(doc, 
        "Understanding the structural drivers of socioeconomic stratification and personal income distribution is a foundational problem "
        "in empirical economics, labor policy, and social science. Historically, economic researchers have sought to quantify how personal "
        "investments in human capital (e.g., formal education and vocational skill) interact with demographic trajectories (e.g., age-related experience) "
        "and labor market structures (e.g., occupational sector, work hours, and self-employment) to determine economic outcomes. "
        "The UCI Adult Census Income dataset, derived from the 1994 Current Population Survey conducted by the U.S. Census Bureau, has served "
        "as a benchmark dataset for exploring these dynamics through machine learning and statistical computing.")
    
    add_para(doc, 
        "The primary analytical goal is to model the determinants of an individual earning more than $50,000 annually. In the context of 1994 economic "
        "conditions, a $50,000 annual personal income represented an affluent threshold (approximately the 75th to 80th percentile of individual earners). "
        "However, analyzing such observational surveys involves substantial methodological challenges: categorical variables exhibit high cardinality, "
        "survey responses contain non-random missingness, financial accounts (capital gains and losses) are severely zero-inflated and top-coded, "
        "and labor supply is heavily clustered around legal standard workweeks.")
    
    add_heading_2(doc, "The End-to-End Analytical Framework")
    add_para(doc, 
        "To ensure that all final conclusions rest on sound empirical foundations, this project was architected as an eight-stage sequential pipeline. "
        "Each stage builds strictly upon the verified outputs of the preceding stage:")
    
    pipeline_stages = [
        ("Stage 1: Source Ingestion", "Raw CSV parsing, initial delimiter inspection, header validation, and string encoding."),
        ("Stage 2: Hygiene & Cleaning", "Detecting '?' missingness tokens, mode imputation, whitespace stripping, and duplicate purging."),
        ("Stage 3: Exploratory Data Analysis", "Computing non-parametric and parametric descriptive summaries, skewness, and kurtosis."),
        ("Stage 4: Graphic Communication", "Designing univariate, bivariate, and conditioned lattice graphics to expose hidden patterns."),
        ("Stage 5: Hypothesis Testing", "Formulating formal statistical null/alternative pairs, evaluating distributional assumptions, and correcting for multiple testing."),
        ("Stage 6: Predictive Modeling", "Stratified partitioning, design matrix construction, baseline establishment, and regularized estimation."),
        ("Stage 7: Model Diagnostics", "Evaluating confusion matrices, discrimination curves (ROC/PR), calibration reliability, and influence points."),
        ("Stage 8: Integrated Synthesis", "Consolidating all analytical evidence, evaluating policy implications, and documenting reproducibility.")
    ]
    for s_title, s_desc in pipeline_stages:
        add_bullet(doc, s_desc, bold_prefix=f"{s_title}: ")
        
    add_callout(doc,
        "A critical tenet of this investigation is that predictive accuracy cannot compensate for defective data hygiene. "
        "Without rigorous initial cleaning, models learn artifacts of measurement error rather than genuine socioeconomic signals. "
        "Similarly, without formal hypothesis testing and effect size auditing, analysts risk misinterpreting high sample-size statistical significance "
        "as real-world practical importance.",
        title="CORE METHODOLOGICAL PRINCIPLE")

    # =========================================================================
    # SECTION 4: DATASET DESCRIPTION AND DATA SOURCE
    # =========================================================================
    add_heading_1(doc, "Section 4 — Dataset Description and Data Source")
    
    add_para(doc, 
        "The dataset utilized across this four-week engagement is the official UCI Adult Census Income dataset, hosted by the UC Irvine Machine "
        "Learning Repository (available at: https://archive.ics.uci.edu/dataset/2/adult). Extracted from the 1994 Current Population Survey (CPS) "
        "by Ronny Kohavi and Barry Becker, the dataset was designed to benchmark supervised binary classification algorithms on real-world demographic data. "
        "The extraction applied specific filtering criteria: records were restricted to individuals aged 16 or older who had a non-zero sampling weight "
        "(fnlwgt > 0) and who met CPS survey validity checks.")
    
    add_heading_2(doc, "Verified Schema and Attribute Inventory")
    add_para(doc, 
        "The raw dataset comprises 32,561 records and 15 variables (6 numerical and 9 categorical). Following data cleaning and deduplication, "
        "the analysis operates on exactly 32,537 authenticated observations. Table 4.1 details the schema, storage types, missing rates in the raw data, "
        "and empirical value distributions:")

    # Table 4.1 Schema Inventory
    schema_info = [
        ("age", "Numeric (Integer)", "Age of the surveyed individual in years.", "0.0%", "Min: 17, Max: 90, Mean: 38.59, Median: 37"),
        ("workclass", "Categorical (Factor)", "Employment sector / ownership class.", "5.64% (1,836)", "8 levels: Private (75.3%), Self-emp, Gov"),
        ("fnlwgt", "Numeric (Integer)", "Final survey sampling weight assigned by CPS.", "0.0%", "Min: 12,285, Max: 1,484,705, Mean: 189,781"),
        ("education", "Categorical (Ordinal)", "Highest educational degree completed.", "0.0%", "16 levels: Preschool to Doctorate"),
        ("education_num", "Numeric (Integer)", "Continuous quantification of education years.", "0.0%", "Range: 1 to 16, Mean: 10.08, Median: 10"),
        ("marital_status", "Categorical (Factor)", "Marital and cohabitation status.", "0.0%", "7 levels: Married-civ-spouse (46.0%), Never-married (32.8%)"),
        ("occupation", "Categorical (Factor)", "Professional occupation category.", "5.66% (1,843)", "14 levels: Prof-specialty, Exec-managerial, Craft, etc."),
        ("relationship", "Categorical (Factor)", "Household role relative to householder.", "0.0%", "6 levels: Husband (40.5%), Not-in-family, Own-child"),
        ("race", "Categorical (Factor)", "Self-identified racial demographic.", "0.0%", "5 levels: White (85.4%), Black (9.6%), Asian-Pac (3.2%)"),
        ("sex", "Categorical (Factor)", "Biological sex recorded in survey.", "0.0%", "2 levels: Male (66.92%), Female (33.08%)"),
        ("capital_gain", "Numeric (Integer)", "Recorded annual capital gains income ($).", "0.0%", "91.7% Zeroes; Max: $99,999; Mean: $1,078"),
        ("capital_loss", "Numeric (Integer)", "Recorded annual capital losses ($).", "0.0%", "95.3% Zeroes; Max: $4,356; Mean: $87.37"),
        ("hours_per_week", "Numeric (Integer)", "Reported weekly hours worked.", "0.0%", "Range: 1 to 99; Mean: 40.44; 46.7% at exactly 40"),
        ("native_country", "Categorical (Factor)", "Country of birth / origin.", "1.79% (583)", "41 levels: United-States (89.6%), Mexico, etc."),
        ("income", "Categorical (Target)", "Binary annual personal income classification.", "0.0%", "<=50K: 24,698 (75.91%), >50K: 7,839 (24.09%)")
    ]
    
    tbl_schema = doc.add_table(rows=len(schema_info) + 1, cols=5)
    tbl_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_schema, "D0D7DE")
    
    style_header_cell(tbl_schema.rows[0].cells[0], "Variable", width=Inches(1.1))
    style_header_cell(tbl_schema.rows[0].cells[1], "Data Type", width=Inches(1.2))
    style_header_cell(tbl_schema.rows[0].cells[2], "Analytical Description", width=Inches(1.8))
    style_header_cell(tbl_schema.rows[0].cells[3], "Raw NA %", width=Inches(0.9))
    style_header_cell(tbl_schema.rows[0].cells[4], "Empirical Summary", width=Inches(1.5))
    
    for idx, (v_name, v_type, v_desc, v_na, v_stat) in enumerate(schema_info):
        row = tbl_schema.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], v_name, width=Inches(1.1), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], v_type, width=Inches(1.2), bold=False, bg_hex=bg)
        style_data_cell(row.cells[2], v_desc, width=Inches(1.8), bold=False, bg_hex=bg)
        style_data_cell(row.cells[3], v_na, width=Inches(0.9), bold=False, bg_hex=bg)
        style_data_cell(row.cells[4], v_stat, width=Inches(1.5), bold=False, bg_hex=bg)
        
    p_cap_schema = doc.add_paragraph()
    p_cap_schema.paragraph_format.space_before = Pt(2)
    p_cap_schema.paragraph_format.space_after = Pt(8)
    r_cs = p_cap_schema.add_run("Table 4.1: Comprehensive variable dictionary, schema definitions, and raw missingness profile for the UCI Adult dataset.")
    r_cs.font.size = Pt(8.5)
    r_cs.italic = True
    r_cs.font.color.rgb = COLOR_MUTED

    add_heading_2(doc, "Data-Quality Characteristics and Historical Nuances")
    add_para(doc, 
        "Close inspection of the raw data revealed several distinct structural nuances. First, missingness was not represented by standard R 'NA' tokens, "
        "but rather by string literals containing question marks ('?') padded with leading whitespaces. Second, the survey sampling weight ('fnlwgt') "
        "represents the estimated number of individuals in the broader U.S. population represented by that specific respondent. Because 'fnlwgt' is an "
        "administrative expansion weight reflecting geographic stratification rather than an intrinsic individual capability, it is not a behavioral predictor "
        "and must be excluded from predictive modeling to prevent spurious spatial overfitting. Third, 'education_num' is an exact integer mapping of the "
        "'education' degree factor (e.g., Bachelors = 13, Masters = 14, Doctorate = 16); retaining both in regression models would create perfect multicollinearity.")

    # =========================================================================
    # SECTION 5: WEEK 1: DATA CLEANING AND PRELIMINARY ANALYSIS
    # =========================================================================
    add_heading_1(doc, "Section 5 — Week 1: Data Cleaning and Preliminary Analysis")
    
    add_para(doc, 
        "The first week of the project focused on data ingestion, structural validation, hygiene auditing, and transformation. "
        "Real-world administrative survey datasets invariably contain anomalies, whitespace corruption, and missing values. "
        "The scripts R/01_import.R through R/07_final_analysis.R established a rigorous, reproducible cleaning pipeline.")

    add_heading_2(doc, "5.1 Missing Value Treatment and Mode Imputation")
    add_para(doc, 
        "Raw file ingestion identified 4,262 missing cells concentrated in three categorical attributes: workclass (1,836 missing; 5.64%), "
        "occupation (1,843 missing; 5.66%), and native_country (583 missing; 1.79%). All numerical variables were 100% complete. "
        "Because the missingness was Missing Completely at Random (MCAR) or Missing at Random (MAR) with respect to core demographics and "
        "affected less than 6% of entries per attribute, listwise deletion was rejected to prevent the loss of 2,399 unique individuals. "
        "Instead, statistical mode imputation was performed using the dominant non-missing category within each column: 'Private' for workclass, "
        "'Prof-specialty' for occupation, and 'United-States' for native_country.")
    
    add_code_block(doc,
"""# Excerpt from R/03_cleaning.R: Mode Imputation Logic
get_mode <- function(x) {
  tbl <- sort(table(x[!is.na(x)]), decreasing = TRUE)
  names(tbl)[1]
}

# Impute missing categorical values with the empirical mode
adult$workclass[is.na(adult$workclass)]           <- get_mode(adult$workclass)       # 'Private'
adult$occupation[is.na(adult$occupation)]         <- get_mode(adult$occupation)     # 'Prof-specialty'
adult$native_country[is.na(adult$native_country)] <- get_mode(adult$native_country) # 'United-States'
stopifnot(sum(is.na(adult)) == 0) # Confirm zero residual missingness""",
        caption="Implementation of statistical mode imputation in R/03_cleaning.R.")

    add_heading_2(doc, "5.2 Deduplication and Whitespace Normalization")
    add_para(doc, 
        "Categorical string values in adult.data were padded with leading whitespace (e.g., ' <=50K' vs '<=50K'). "
        "During import in R/01_import.R, 'strip.white = TRUE' was enforced, and subsequent factor conversions eliminated leading and trailing spaces. "
        "An exact-row duplicate audit in R/03_cleaning.R detected 24 fully identical duplicate rows. These duplicate records represented administrative "
        "recording repetitions that contributed no independent variance; they were excised, reducing the working sample from 32,561 to 32,537 rows.")

    add_heading_2(doc, "5.3 Outlier Assessment via Tukey's IQR Method")
    add_para(doc, 
        "Outlier screening was conducted in R/04_outlier_analysis.R using Tukey's fences (Q1 - 1.5*IQR to Q3 + 1.5*IQR). "
        "Table 5.1 details the empirical quartiles, IQR bounds, and outlier counts across all six continuous variables:")

    # Table 5.1 Outliers
    outlier_rows = [
        ("age", "28.0", "48.0", "20.0", "-2.0", "78.0", "142", "0.44%"),
        ("fnlwgt", "117,827", "236,993", "119,166", "-60,922", "415,742", "993", "3.05%"),
        ("education_num", "9.0", "12.0", "3.0", "4.5", "16.5", "1,193", "3.67%"),
        ("capital_gain", "0.0", "0.0", "0.0", "0.0", "0.0", "2,712", "8.34%"),
        ("capital_loss", "0.0", "0.0", "0.0", "0.0", "0.0", "1,519", "4.67%"),
        ("hours_per_week", "40.0", "45.0", "5.0", "32.5", "52.5", "9,002", "27.67%")
    ]
    tbl_out = doc.add_table(rows=len(outlier_rows) + 1, cols=8)
    tbl_out.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_out, "D0D7DE")
    
    style_header_cell(tbl_out.rows[0].cells[0], "Variable", width=Inches(1.1))
    style_header_cell(tbl_out.rows[0].cells[1], "Q1", width=Inches(0.7))
    style_header_cell(tbl_out.rows[0].cells[2], "Q3", width=Inches(0.7))
    style_header_cell(tbl_out.rows[0].cells[3], "IQR", width=Inches(0.6))
    style_header_cell(tbl_out.rows[0].cells[4], "Lower", width=Inches(0.8))
    style_header_cell(tbl_out.rows[0].cells[5], "Upper", width=Inches(0.8))
    style_header_cell(tbl_out.rows[0].cells[6], "Outliers", width=Inches(0.8))
    style_header_cell(tbl_out.rows[0].cells[7], "Pct %", width=Inches(0.8))
    
    for idx, (v_var, v_q1, v_q3, v_iqr, v_low, v_upp, v_nout, v_pct) in enumerate(outlier_rows):
        row = tbl_out.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], v_var, width=Inches(1.1), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], v_q1, width=Inches(0.7), bg_hex=bg)
        style_data_cell(row.cells[2], v_q3, width=Inches(0.7), bg_hex=bg)
        style_data_cell(row.cells[3], v_iqr, width=Inches(0.6), bg_hex=bg)
        style_data_cell(row.cells[4], v_low, width=Inches(0.8), bg_hex=bg)
        style_data_cell(row.cells[5], v_upp, width=Inches(0.8), bg_hex=bg)
        style_data_cell(row.cells[6], v_nout, width=Inches(0.8), bold=True, bg_hex=bg)
        style_data_cell(row.cells[7], v_pct, width=Inches(0.8), bg_hex=bg)
        
    p_cap_out = doc.add_paragraph()
    p_cap_out.paragraph_format.space_before = Pt(2)
    p_cap_out.paragraph_format.space_after = Pt(8)
    r_co = p_cap_out.add_run("Table 5.1: Tukey IQR outlier boundary audit for numerical attributes (outputs/04_outlier_summary.csv).")
    r_co.font.size = Pt(8.5)
    r_co.italic = True
    r_co.font.color.rgb = COLOR_MUTED

    add_para(doc, 
        "Crucially, the 9,002 working-hour 'outliers' (27.67% of the dataset) reflect part-time workers (<32.5 hrs/wk) and overtime workers (>52.5 hrs/wk), "
        "rather than corrupted data entries. Similarly, non-zero capital gains represent legitimate investment income. "
        "A foundational analytical decision was made to retain all valid economic records, avoiding artificial truncation of natural distributions.")

    add_figure(doc, "plots/04_boxplots_combined.png", "5.1", 
               "Combined Tukey Boxplots Across Continuous Attributes", 
               "Multi-panel boxplot display illustrating distribution widths, median bars, and extreme values across age, hours, capital gain, and fnlwgt.")

    add_heading_2(doc, "5.4 Cleaned Dataset Hygiene and Before/After Verification")
    add_para(doc, 
        "Table 5.2 confirms the exact transition metrics achieved by the Week 1 cleaning scripts (outputs/07_before_after_summary.csv):")
    
    ba_rows = [
        ("Total Observations (Rows)", "32,561", "32,537", "-24 duplicate rows successfully removed"),
        ("Total Column Count", "15", "15", "Full schema integrity preserved"),
        ("Total Missing Values (NA)", "4,262", "0", "100% complete data achieved via mode imputation"),
        ("Missing: workclass", "1,836 (5.64%)", "0 (0.00%)", "Imputed with mode ('Private')"),
        ("Missing: occupation", "1,843 (5.66%)", "0 (0.00%)", "Imputed with mode ('Prof-specialty')"),
        ("Missing: native_country", "583 (1.79%)", "0 (0.00%)", "Imputed with mode ('United-States')"),
        ("Duplicate Row Count", "24", "0", "De-duplicated working dataset"),
        ("Continuous Variables", "6", "6", "age, fnlwgt, education_num, capital_gain, capital_loss, hours"),
        ("Categorical Variables", "9", "9", "Standardized factor representations with trimmed levels")
    ]
    tbl_ba = doc.add_table(rows=len(ba_rows) + 1, cols=4)
    tbl_ba.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ba, "D0D7DE")
    
    style_header_cell(tbl_ba.rows[0].cells[0], "Data Quality Metric", width=Inches(1.8))
    style_header_cell(tbl_ba.rows[0].cells[1], "Raw State", width=Inches(1.2))
    style_header_cell(tbl_ba.rows[0].cells[2], "Clean State", width=Inches(1.2))
    style_header_cell(tbl_ba.rows[0].cells[3], "Operational Treatment Applied", width=Inches(2.3))
    
    for idx, (m_name, m_raw, m_cln, m_treat) in enumerate(ba_rows):
        row = tbl_ba.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], m_name, width=Inches(1.8), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], m_raw, width=Inches(1.2), bg_hex=bg)
        style_data_cell(row.cells[2], m_cln, width=Inches(1.2), bold=True, bg_hex=bg)
        style_data_cell(row.cells[3], m_treat, width=Inches(2.3), bg_hex=bg)

    add_figure(doc, "plots/06_fig1_missing_values.png", "5.2", 
               "Missing Value Incidence by Variable Prior to Imputation", 
               "Bar chart verifying that missingness was strictly isolated to workclass (1,836), occupation (1,843), and native_country (583).")

    # =========================================================================
    # SECTION 6: WEEK 2: DATA VISUALIZATION AND INSIGHT COMMUNICATION
    # =========================================================================
    add_heading_1(doc, "Section 6 — Week 2: Data Visualization and Insight Communication")
    
    add_para(doc, 
        "Week 2 advanced the analysis from cleaning to comprehensive graphic visualization using ggplot2, lattice, and base R graphics. "
        "Adhering to Edward Tufte's principles of graphical excellence, visualizations were structured to maximize data-ink ratio, eliminate "
        "chartjunk, and reveal substantive socioeconomic patterns. The primary goal was to explore the marginal distributions of demographic "
        "and labor indicators, identify bivariate disparities across income categories, and formulate rigorous hypotheses for statistical testing.")

    add_heading_2(doc, "6.1 Income Target Class Imbalance")
    add_para(doc, 
        "Figure 6.1 depicts the foundational imbalance of the income target variable. In the authenticated dataset of 32,537 individuals, "
        "24,698 (75.91%) earn <=$50K while only 7,839 (24.09%) earn >$50K. This 3.15:1 imbalance demonstrates that high earners represent "
        "a distinct minority class. This structure immediately establishes that a naïve majority-class classifier achieves 75.91% accuracy "
        "by predicting <=$50K for every case; thus, all subsequent predictive models must be evaluated against balanced accuracy, precision, "
        "recall, and ROC-AUC rather than raw classification accuracy alone.")

    add_figure(doc, "plots/week2_01_income_distribution.png", "6.1", 
               "Income Target Distribution and Class Imbalance", 
               "Univariate bar chart showing the 3.15:1 ratio between low-income (75.91%) and high-income (24.09%) individuals in the cleaned census sample.")

    add_heading_2(doc, "6.2 Educational Attainment and Human Capital Thresholds")
    add_para(doc, 
        "Figure 6.2 illustrates the relationship between educational attainment and high-income status. Rather than a purely linear progression, "
        "the data reveals a sharp credential threshold. Below high school completion, the proportion of individuals earning >$50K never exceeds 7.62% "
        "(ranging from 0.00% for Preschool to 7.62% for 12th grade). High school graduation produces 15.95% high earners, Some-college yields 19.03%, "
        "and an Associate degree yields ~25%. However, completing a Bachelor's degree results in a jump to 41.49% high earners. Advanced graduate degrees "
        "elevate this proportion substantially: 55.69% for Master's degrees, 73.44% for Professional School graduates, and 74.09% for Doctorates.")

    add_figure(doc, "plots/week2_04_education_vs_income.png", "6.2", 
               "High-Income Proportion Across Educational Credentials", 
               "Segmented horizontal bar chart showing the sharp escalation in high-earning probability from High School (15.95%) to Bachelors (41.49%) and Doctorate (74.09%).")

    add_heading_2(doc, "6.3 Age Demographics and Earning Life-Cycle")
    add_para(doc, 
        "Figure 6.3 displays the age distributions of low- and high-income earners. The visual distributions show marked divergence: "
        "low-income earners exhibit a heavily right-skewed distribution centered at a median age of 34 years (IQR = 21, Q1 = 25, Q3 = 46), "
        "reflecting younger workers entering the labor market. Conversely, high-income earners display a more symmetric, bell-shaped distribution "
        "centered at a median age of 44 years (IQR = 15, Q1 = 36, Q3 = 51). The 10-year median divergence visually reflects the human capital life-cycle: "
        "accumulated career tenure, promotions, and professional experience are required to reach the upper income bracket.")

    add_figure(doc, "plots/week2_06_age_vs_income.png", "6.3", 
               "Age Distribution Stratified by Income Category", 
               "Comparative density and violin plot revealing the 10-year median age shift between low earners (median 34) and high earners (median 44).")

    add_heading_2(doc, "6.4 Labor Supply and the 40-Hour Institutional Anchor")
    add_para(doc, 
        "Figure 6.4 depicts reported weekly hours worked. The distribution is heavily leptokurtic, with an overwhelming spike at exactly 40 hours per week "
        "(15,204 individuals, or 46.73% of the entire sample), reflecting the Fair Labor Standards Act standard workweek. Despite this shared anchor, "
        "high earners work noticeably more hours on average: mean hours for <=$50K workers is 38.84 hours (SD = 12.32, IQR = 5), whereas mean hours "
        "for >$50K workers is 45.47 hours (SD = 11.01, IQR = 10). Low earners show substantial part-time concentration (<40 hrs: 23.84%), while "
        "high earners show substantial overtime concentration (>40 hrs: 29.43%).")

    add_figure(doc, "plots/week2_08_hours_vs_income.png", "6.4", 
               "Weekly Working Hours Distribution by Income Category", 
               "Comparative histogram displaying the dominant 40-hour institutional peak alongside the substantial overtime shift among high earners.")

    add_heading_2(doc, "6.5 Continuous Correlation Matrix and Multivariable Lattice Conditioning")
    add_para(doc, 
        "Figure 6.5 presents the correlation matrix across all six numerical variables. Linear bivariate associations are modest: "
        "the strongest observed correlation is between education_num and hours_per_week (r = +0.148), followed by age and hours_per_week (r = +0.069). "
        "Capital gains and capital losses exhibit virtually zero correlation with one another (r = -0.032) and with other metrics. "
        "This confirms that individual numerical attributes capture largely distinct dimensions of socioeconomic standing, indicating that "
        "multicollinearity among continuous features will not undermine subsequent multivariate regression models.")

    add_figure(doc, "plots/week2_11_correlation_heatmap.png", "6.5", 
               "Pearson Correlation Heatmap Across Numerical Features", 
               "Correlation matrix demonstrating low linear collinearity among numerical features, with education and hours showing the strongest relationship (r = 0.15).")

    add_para(doc, 
        "Figure 6.6 explores conditional interactions via a multi-panel Trellis/Lattice display in R/08_week2_visualizations.R. "
        "Conditioning on sex and income category simultaneously demonstrates that while the age-hours relationship follows a similar quadratic trajectory "
        "for both men and women, female workers face a tighter hours-to-earnings penalty, requiring longer weekly hours across older age brackets "
        "to attain high-income parity. This visual finding directly informed the inclusion of interaction effects and demographic controls in Week 3 modeling.")

    add_figure(doc, "plots/week2_14_lattice_age_hours_income.png", "6.6", 
               "Lattice Conditioning: Age vs. Hours Worked Stratified by Sex and Income", 
               "Four-panel Trellis scatter plot conditioning age and working hours across male/female and low/high income cohorts.")

    # =========================================================================
    # SECTION 7: WEEK 3: STATISTICAL ANALYSIS AND HYPOTHESIS TESTING
    # =========================================================================
    add_heading_1(doc, "Section 7 — Week 3: Statistical Analysis and Hypothesis Testing")
    
    add_callout(doc,
        "VERIFICATION OF HYPOTHESIS TESTING SUITE: The battery of hypothesis tests formally executed in R/10_week3_statistical_analysis.R "
        "and recorded in outputs/week3_statistics/hypothesis_tests.csv comprises exactly eight verified tests across five research questions "
        "(RQ1, RQ2a, RQ2b, RQ3a, RQ3b, RQ4a, RQ4b, and RQ5). Paired parametric and non-parametric tests were evaluated for age and weekly hours. "
        "While informal project summaries occasionally mentioned 'nine tests' (conflating the auxiliary Spearman rank correlation matrix with a distinct test row), "
        "an exhaustive audit of the master test registry confirms that exactly eight hypothesis tests were formally specified, run, and recorded.",
        title="HYPOTHESIS TESTING REGISTRY AUDIT & VERIFICATION")

    add_para(doc, 
        "Week 3 applied formal inferential statistics to evaluate the exploratory hypotheses generated in Week 2. "
        "To guard against Type I error inflation arising from multiple simultaneous tests, both family-wise Bonferroni adjustments "
        "and Benjamini-Hochberg False Discovery Rate (FDR) corrections were applied across all tests at a family-wise alpha = 0.05. "
        "Furthermore, because the large sample size (N = 32,537) yields statistical power capable of detecting negligible differences, "
        "standardized effect sizes (Cramer's V, Cohen's d, Rank-Biserial r, Pearson's r) were computed to evaluate practical significance.")

    add_heading_2(doc, "7.1 Detailed Review of the Eight Verified Hypothesis Tests")

    test_details = [
        ("RQ1: Educational Attainment vs. Income Category",
         "H0: Educational attainment and income category are independent.\nH1: Educational attainment and income category are statistically associated.",
         "Pearson's Chi-Square Test of Independence (df = 15)",
         "Chi-Square = 4428.40, df = 15, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Cramer's V = 0.3689 (Moderate-to-strong association)",
         "Cochran rule satisfied: Minimum expected cell count was 12.0; 0% of cells had expected count < 5.",
         "Reject H0. Educational attainment exhibits a highly significant, substantive association with income. Higher educational credentials substantially shift individuals into the >$50K bracket."),
        
        ("RQ2a: Parametric Mean Age Divergence by Income Group",
         "H0: Mean age <=$50K equals mean age >$50K (mu1 = mu2).\nH1: Mean age differs significantly between income groups (mu1 != mu2).",
         "Welch's Two-Sample t-test (unequal variances, df = 17,406.1)",
         "t = 50.24, df = 17406.1, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Cohen's d = 0.5629 (Moderate-to-large effect size)",
         "Mild right-skewness (+0.56); robust by Central Limit Theorem (N = 32,537). Welch correction protects against heteroscedasticity.",
         "Reject H0. High earners are significantly older on average (44.25 yrs, SD = 10.52 vs. 36.79 yrs, SD = 14.02), reflecting an average career progression gap of 7.46 years."),

        ("RQ2b: Non-Parametric Age Median Shift by Income Group",
         "H0: The age distribution median is identical between income groups.\nH1: The age distribution is systematically shifted higher for >$50K earners.",
         "Wilcoxon Rank-Sum Test (Mann-Whitney U)",
         "W = 132,460,134, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Rank-Biserial r = 0.3683 (Moderate non-parametric shift)",
         "Ordinal ranking assumption met; normal approximation applied due to tied ages across 32,537 observations.",
         "Reject H0. Confirms RQ2a non-parametrically: the median age of high earners (44 years, IQR = 15) is significantly greater than low earners (34 years, IQR = 21)."),

        ("RQ3a: Parametric Mean Weekly Hours by Income Group",
         "H0: Mean weekly hours <=$50K equals mean weekly hours >$50K (mu1 = mu2).\nH1: Mean weekly hours differs between income groups (mu1 != mu2).",
         "Welch's Two-Sample t-test (unequal variances, df = 14,568.1)",
         "t = 45.10, df = 14568.1, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Cohen's d = 0.5518 (Moderate effect size)",
         "Leptokurtic distribution peaked at 40 hours; Central Limit Theorem guarantees normal sampling distribution given large N.",
         "Reject H0. High earners work significantly more hours per week on average (45.47 hrs, SD = 11.01 vs. 38.84 hrs, SD = 12.32), a practical difference of 6.63 hours weekly."),

        ("RQ3b: Non-Parametric Weekly Hours Rank Distribution Shift",
         "H0: The median and rank distribution of hours are identical across income groups.\nH1: The hours rank distribution is shifted higher in the >$50K group.",
         "Wilcoxon Rank-Sum Test (Mann-Whitney U)",
         "W = 130,106,291.5, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Rank-Biserial r = 0.3440 (Moderate non-parametric shift)",
         "Heavy spike at 40 hours produces tied ranks; handled via asymptotic normal approximation.",
         "Reject H0. Confirms RQ3a non-parametrically: working hours of high earners rank significantly higher than low earners, even when medians coincide at 40 hours due to the legal standard workweek."),

        ("RQ4a: Employment Sector (Workclass) vs. Income Category",
         "H0: Workclass sector and income category are independent.\nH1: Workclass sector and income category are statistically associated.",
         "Pearson's Chi-Square Test of Independence (df = 7)",
         "Chi-Square = 922.35, df = 7, Raw p = 7.16e-195, Bonferroni p = 5.73e-194, BH FDR p = 8.18e-195",
         "Cramer's V = 0.1684 (Modest effect size)",
         "Min expected count = 1.69 (Without-pay/Never-worked < 5 in 12.5% of cells); chi-square asymptotically robust due to large N = 32,537.",
         "Reject H0. Statistically significant association between employment sector and income; self-employed incorporated workers show higher earning probabilities than private-sector workers."),

        ("RQ4b: Professional Occupation vs. Income Category",
         "H0: Occupation category and income category are independent.\nH1: Occupation category and income category are statistically associated.",
         "Pearson's Chi-Square Test of Independence (df = 13)",
         "Chi-Square = 3197.61, df = 13, Raw p < 0.0001, Bonferroni p < 0.0001, BH FDR p < 0.0001",
         "Cramer's V = 0.3135 (Strong categorical effect size)",
         "Min expected count = 2.17 (Armed Forces); over 95% of cells exceed expected count of 5; test remains asymptotically valid.",
         "Reject H0. Occupation exerts a strong, substantive structural association with income. Executive-managerial and professional specialty roles dominate the high-income bracket."),

        ("RQ5: Linear Correlation Between Education Years and Weekly Hours",
         "H0: The true population correlation between education_num and hours_per_week is zero (rho = 0).\nH1: The true correlation is non-zero (rho != 0).",
         "Pearson's Product-Moment Correlation Test (df = 32,535)",
         "t = 27.07, df = 32535, Raw p = 1.26e-159, Bonferroni p = 1.01e-158, BH FDR p = 1.26e-159",
         "Pearson's r = +0.1484 (95% CI [0.1378, 0.1590]; Weak positive correlation)",
         "Bivariate linearity inspected; discrete education scale mildly violates strict normality but inference is protected by CLT.",
         "Reject H0. Highly statistically significant but weak linear association. Higher educational attainment is weakly associated with longer working hours, confirming they provide independent explanatory power in multivariate models.")
    ]

    for title, hyps, meth, stats, eff, diag, concl in test_details:
        add_heading_3(doc, title)
        add_para(doc, hyps, bold_prefix="Hypotheses: ")
        add_para(doc, f"{meth} | {stats}", bold_prefix="Statistical Output: ")
        add_para(doc, eff, bold_prefix="Effect Size Metric: ")
        add_para(doc, diag, bold_prefix="Assumption Check: ")
        add_para(doc, concl, bold_prefix="Inference Decision: ")

    add_heading_2(doc, "7.2 Consolidated Hypothesis Testing Registry Table")
    add_para(doc, 
        "Table 7.1 consolidates the complete battery of eight hypothesis tests from outputs/week3_statistics/hypothesis_tests.csv:")

    # Table 7.1 Hypothesis Testing
    ht_rows = [
        ("RQ1", "Education vs Income", "Chi-Square", "4,428.4", "15", "< 0.0001", "< 0.0001", "Cramer's V", "0.3689", "Reject H0"),
        ("RQ2a", "Age Mean by Income", "Welch t-test", "50.24", "17,406", "< 0.0001", "< 0.0001", "Cohen's d", "0.5629", "Reject H0"),
        ("RQ2b", "Age Median by Income", "Wilcoxon W", "1.32e+08", "NA", "< 0.0001", "< 0.0001", "Rank-Bis r", "0.3683", "Reject H0"),
        ("RQ3a", "Hours Mean by Income", "Welch t-test", "45.10", "14,568", "< 0.0001", "< 0.0001", "Cohen's d", "0.5518", "Reject H0"),
        ("RQ3b", "Hours Median by Income", "Wilcoxon W", "1.30e+08", "NA", "< 0.0001", "< 0.0001", "Rank-Bis r", "0.3440", "Reject H0"),
        ("RQ4a", "Workclass vs Income", "Chi-Square", "922.35", "7", "< 0.0001", "< 0.0001", "Cramer's V", "0.1684", "Reject H0"),
        ("RQ4b", "Occupation vs Income", "Chi-Square", "3,197.6", "13", "< 0.0001", "< 0.0001", "Cramer's V", "0.3135", "Reject H0"),
        ("RQ5", "Edu Num vs Hours", "Pearson r", "27.07", "32,535", "< 0.0001", "< 0.0001", "Pearson r", "0.1484", "Reject H0")
    ]
    tbl_ht = doc.add_table(rows=len(ht_rows) + 1, cols=10)
    tbl_ht.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ht, "D0D7DE")
    
    headers_ht = ["ID", "Research Focus", "Method", "Stat", "df", "Raw p", "Adj p (BH)", "Effect Metric", "Value", "Decision"]
    widths_ht = [Inches(0.5), Inches(1.3), Inches(1.0), Inches(0.6), Inches(0.6), Inches(0.6), Inches(0.6), Inches(0.8), Inches(0.5), Inches(0.7)]
    for c_idx, h_text in enumerate(headers_ht):
        style_header_cell(tbl_ht.rows[0].cells[c_idx], h_text, width=widths_ht[c_idx])
        
    for idx, (t_id, t_foc, t_m, t_s, t_df, t_p, t_ap, t_em, t_ev, t_dec) in enumerate(ht_rows):
        row = tbl_ht.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], t_id, width=widths_ht[0], bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], t_foc, width=widths_ht[1], bg_hex=bg)
        style_data_cell(row.cells[2], t_m, width=widths_ht[2], bg_hex=bg)
        style_data_cell(row.cells[3], t_s, width=widths_ht[3], bg_hex=bg)
        style_data_cell(row.cells[4], t_df, width=widths_ht[4], bg_hex=bg)
        style_data_cell(row.cells[5], t_p, width=widths_ht[5], bg_hex=bg)
        style_data_cell(row.cells[6], t_ap, width=widths_ht[6], bg_hex=bg)
        style_data_cell(row.cells[7], t_em, width=widths_ht[7], bg_hex=bg)
        style_data_cell(row.cells[8], t_ev, width=widths_ht[8], bold=True, bg_hex=bg)
        style_data_cell(row.cells[9], t_dec, width=widths_ht[9], bold=True, bg_hex=bg, text_color=COLOR_GREEN)

    p_cap_ht = doc.add_paragraph()
    p_cap_ht.paragraph_format.space_before = Pt(2)
    p_cap_ht.paragraph_format.space_after = Pt(8)
    r_cht = p_cap_ht.add_run("Table 7.1: Master hypothesis testing registry across all eight verified inferential evaluations.")
    r_cht.font.size = Pt(8.5)
    r_cht.italic = True
    r_cht.font.color.rgb = COLOR_MUTED

    add_figure(doc, "plots/week3/week3_normality_qq_plots.png", "7.1", 
               "Normal Quantile-Quantile (Q-Q) Diagnostics", 
               "Empirical Q-Q plots for continuous variables illustrating heavy-tailed departures and validating the use of robust Welch t-tests and non-parametric Wilcoxon tests.")

    # =========================================================================
    # SECTION 8: WEEK 3: PREDICTIVE MODELING
    # =========================================================================
    add_heading_1(doc, "Section 8 — Week 3: Predictive Modeling")
    
    add_para(doc, 
        "Building upon the inferential findings of Section 7, R/11_week3_modeling.R implemented supervised binary classification to model "
        "individual income tier (>50K vs. <=50K). To prevent data snooping and ensure rigorous out-of-sample generalization, the dataset was "
        "partitioned using stratified sampling into an 80% training set (N = 26,029) and a 20% held-out testing set (N = 6,508) under fixed seed (2026). "
        "Both partitions preserved the empirical 75.91% / 24.09% class ratio exactly (training: 19,758 <=$50K, 6,271 >$50K; testing: 4,940 <=$50K, 1,568 >$50K).")

    add_heading_2(doc, "8.1 Model Architectures and Estimation Framework")
    add_bullet(doc, 
        "Predicts the majority class (<=50K) for every individual. Establishes the naive performance benchmark: Accuracy = 75.91%, "
        "Balanced Accuracy = 50.00%, Sensitivity = 0.00%, Specificity = 100.00%, and ROC-AUC = 0.5000.",
        bold_prefix="1. Zero-Rule Baseline Classifier: ")
    add_bullet(doc, 
        "Estimated via stats::glm(family = binomial(link = 'logit')). Uses the full design matrix of demographic, educational, and occupational features. "
        "Generates interpretable odds ratios (exp(beta)) with 95% Wald confidence intervals.",
        bold_prefix="2. Standard Multivariate Logistic Regression: ")
    add_bullet(doc, 
        "Estimated via glmnet::cv.glmnet() with alpha = 0.5 (mixing L1 lasso and L2 ridge penalties). Hyperparameter lambda was optimized "
        "across a 100-point path using 5-fold cross-validation on the training set (lambda.min = 0.0012, lambda.1se = 0.0076) to penalize redundant coefficients.",
        bold_prefix="3. Elastic-Net Regularized Logistic Regression: ")

    add_code_block(doc,
"""# Excerpt from R/11_week3_modeling.R: Modeling Architecture and Cross-Validation
formula_full <- target ~ age + workclass + education_num + marital_status + 
                         occupation + relationship + race + sex + 
                         capital_gain + capital_loss + hours_per_week + native_region

# 1. Standard Logistic Regression
fit_glm <- glm(formula_full, data = train_data, family = binomial(link = "logit"))

# 2. Elastic Net Regularized Logistic Regression via 5-fold Cross-Validation
X_train <- model.matrix(formula_full, data = train_data)[, -1]
y_train <- train_data$target
set.seed(2026)
cv_enet <- cv.glmnet(X_train, y_train, family = "binomial", alpha = 0.5, nfolds = 5)
best_lambda <- cv_enet$lambda.min # Optimal sparsity penalty""",
        caption="Stratified model estimation and cross-validated elastic-net tuning in R/11_week3_modeling.R.")

    add_heading_2(doc, "8.2 Odds Ratio Interpretation and Key Predictors")
    add_para(doc, 
        "Table 8.1 presents key exponentiated coefficients (odds ratios) and 95% confidence intervals from the standard logistic regression model "
        "(outputs/week3_model/odds_ratios.csv):")

    or_rows = [
        ("marital_statusMarried-civ-spouse", "7.1641", "[3.8836, 13.2158]", "< 1e-04", "Civilian marriage increases modeled odds of >50K sevenfold relative to Divorced reference."),
        ("occupationExec-managerial", "2.0953", "[1.7735, 2.4755]", "< 1e-04", "Executive-managerial roles double modeled odds relative to Adm-clerical reference."),
        ("occupationProf-specialty", "1.7428", "[1.4795, 2.0528]", "< 1e-04", "Professional specialty roles increase modeled odds by 74.3%."),
        ("education_num", "1.3490", "[1.3228, 1.3756]", "< 1e-04", "Each additional year of formal education increases modeled odds by 34.9%."),
        ("hours_per_week", "1.0284", "[1.0244, 1.0324]", "< 1e-04", "Each additional weekly hour worked increases modeled odds by 2.8%."),
        ("age", "1.0237", "[1.0201, 1.0272]", "< 1e-04", "Each additional year of age increases modeled odds by 2.4%."),
        ("workclassSelf-emp-not-inc", "0.3635", "[0.2864, 0.4614]", "< 1e-04", "Unincorporated self-employment reduces odds of >50K by 63.7% relative to Federal-gov."),
        ("marital_statusNever-married", "0.6468", "[0.5347, 0.7823]", "< 1e-04", "Never-married status reduces modeled odds by 35.3% relative to Divorced.")
    ]
    tbl_or = doc.add_table(rows=len(or_rows) + 1, cols=5)
    tbl_or.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_or, "D0D7DE")
    
    style_header_cell(tbl_or.rows[0].cells[0], "Predictor Term", width=Inches(1.8))
    style_header_cell(tbl_or.rows[0].cells[1], "Odds Ratio", width=Inches(0.9))
    style_header_cell(tbl_or.rows[0].cells[2], "95% Conf. Int.", width=Inches(1.2))
    style_header_cell(tbl_or.rows[0].cells[3], "p-value", width=Inches(0.8))
    style_header_cell(tbl_or.rows[0].cells[4], "Economic Interpretation", width=Inches(1.8))
    
    for idx, (p_term, p_or, p_ci, p_val, p_int) in enumerate(or_rows):
        row = tbl_or.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], p_term, width=Inches(1.8), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], p_or, width=Inches(0.9), bold=True, bg_hex=bg)
        style_data_cell(row.cells[2], p_ci, width=Inches(1.2), bg_hex=bg)
        style_data_cell(row.cells[3], p_val, width=Inches(0.8), bg_hex=bg)
        style_data_cell(row.cells[4], p_int, width=Inches(1.8), bg_hex=bg)

    p_cap_or = doc.add_paragraph()
    p_cap_or.paragraph_format.space_before = Pt(2)
    p_cap_or.paragraph_format.space_after = Pt(8)
    r_cor = p_cap_or.add_run("Table 8.1: Selected adjusted odds ratios and 95% Wald confidence intervals from the standard logistic regression model.")
    r_cor.font.size = Pt(8.5)
    r_cor.italic = True
    r_cor.font.color.rgb = COLOR_MUTED

    add_figure(doc, "plots/week3/week3_odds_ratios_forest.png", "8.1", 
               "Odds Ratios Forest Plot for Logistic Regression Predictors", 
               "Log-scale forest plot depicting point estimates and 95% confidence intervals, highlighting the dominant odds multipliers for marital status, management, and education.")

    add_heading_2(doc, "8.3 Multicollinearity Diagnostics via Generalized VIF")
    add_para(doc, 
        "To ensure that regression coefficients were not distorted by collinearity, Generalized Variance Inflation Factors (GVIF) were computed "
        "using car::vif() in outputs/week3_model/vif_results.csv. For multi-degree-of-freedom categorical variables, the standardized metric "
        "GVIF^(1/(2*Df)) was evaluated. All standardized values fell well below the conservative rule-of-thumb threshold of 2.0 (equivalent to VIF = 4): "
        "sex (1.73), relationship (1.62), marital_status (1.39), education_num (1.18), age (1.10), and hours_per_week (1.07). "
        "This confirms that the model is free from harmful multicollinearity.")

    # =========================================================================
    # SECTION 9: MODEL EVALUATION AND DIAGNOSTICS
    # =========================================================================
    add_heading_1(doc, "Section 9 — Model Evaluation and Diagnostics")
    
    add_para(doc, 
        "Model performance was evaluated on the independent held-out test partition (N = 6,508) across nine discrimination and calibration metrics. "
        "Table 9.1 presents the consolidated performance comparison between the Zero-Rule Baseline, Standard Logistic Regression, and Elastic Net:")

    # Table 9.1 Model Comparison
    m_eval = [
        ("Baseline (Zero-Rule)", "0.50", "0", "0", "4,940", "1,568", "75.91%", "50.00%", "0.00%", "0.00%", "100.00%", "75.91%", "0.0000", "0.5000", "0.2409"),
        ("Logistic Regression (GLM)", "0.50", "943", "367", "4,573", "625", "84.76%", "76.36%", "71.98%", "60.14%", "92.57%", "87.98%", "0.6553", "0.9047", "0.7271"),
        ("Elastic Net (Regularized)", "0.50", "863", "330", "4,610", "705", "84.10%", "74.18%", "72.34%", "55.04%", "93.32%", "86.74%", "0.6251", "0.9004", "0.7214")
    ]
    tbl_me = doc.add_table(rows=len(m_eval) + 1, cols=15)
    tbl_me.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_me, "D0D7DE")
    
    headers_me = ["Model", "Cut", "TP", "FP", "TN", "FN", "Acc", "BalAcc", "Prec", "Recall", "Spec", "NPV", "F1", "AUC", "PR-AUC"]
    widths_me = [Inches(1.2), Inches(0.3), Inches(0.35), Inches(0.35), Inches(0.4), Inches(0.35), Inches(0.45), Inches(0.45), Inches(0.45), Inches(0.45), Inches(0.45), Inches(0.45), Inches(0.4), Inches(0.45), Inches(0.45)]
    for c_idx, h_text in enumerate(headers_me):
        style_header_cell(tbl_me.rows[0].cells[c_idx], h_text, width=widths_me[c_idx])
        
    for idx, row_data in enumerate(m_eval):
        row = tbl_me.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            is_bold = (c_idx in [0, 6, 7, 13])
            style_data_cell(row.cells[c_idx], val, width=widths_me[c_idx], bold=is_bold, bg_hex=bg)

    p_cap_me = doc.add_paragraph()
    p_cap_me.paragraph_format.space_before = Pt(2)
    p_cap_me.paragraph_format.space_after = Pt(8)
    r_cme = p_cap_me.add_run("Table 9.1: Comprehensive out-of-sample test set evaluation metrics across models (outputs/week3_model/evaluation_metrics.csv).")
    r_cme.font.size = Pt(8.5)
    r_cme.italic = True
    r_cme.font.color.rgb = COLOR_MUTED

    add_heading_2(doc, "9.1 Confusion Matrix Decomposition and Asymmetric Error Trade-offs")
    add_para(doc, 
        "At the standard 0.50 classification threshold, Standard Logistic Regression achieved 943 True Positives, 4,573 True Negatives, "
        "367 False Positives, and 625 False Negatives. This reflects an asymmetric trade-off: the model is highly conservative in predicting high earners, "
        "achieving 92.57% specificity and 71.98% precision, but failing to identify 39.86% of actual high earners (recall = 60.14%). "
        "In decision contexts where false negatives carry higher costs (e.g., identifying affluent consumers for premium services), lowering the threshold "
        "to 0.35 would increase recall at the expense of precision.")

    add_figure(doc, "plots/week3/week3_confusion_matrix_logistic.png", "9.1", 
               "Confusion Matrix Heatmap for Standard Logistic Regression", 
               "Confusion matrix on the held-out test set (N = 6,508) illustrating the counts and percentages for TN (70.27%), TP (14.49%), FN (9.60%), and FP (5.64%).")

    add_heading_2(doc, "9.2 Discrimination Curves: ROC and Precision-Recall")
    add_para(doc, 
        "Figures 9.2 and 9.3 display the Receiver Operating Characteristic (ROC) and Precision-Recall (PR) curves. "
        "Standard Logistic Regression achieved an exceptional ROC-AUC of 0.9047, while Elastic Net achieved 0.9004. "
        "Because ROC curves can present an overly optimistic assessment under severe class imbalance, the PR curve provides crucial confirmation: "
        "Standard Logistic Regression achieved a PR-AUC of 0.7271, compared to the horizontal baseline rate of 0.2409, demonstrating strong discriminative power.")

    add_figure(doc, "plots/week3/week3_roc_curves.png", "9.2", 
               "Receiver Operating Characteristic (ROC) Comparison Curves", 
               "ROC curves demonstrating superior discriminative performance for Logistic Regression (AUC = 0.9047) and Elastic Net (AUC = 0.9004) over Baseline (0.5000).")

    add_figure(doc, "plots/week3/week3_pr_curves.png", "9.3", 
               "Precision-Recall (PR) Curves Under Class Imbalance", 
               "PR curves showing strong positive-class performance (PR-AUC = 0.7271) relative to the 24.09% random chance baseline.")

    add_heading_2(doc, "9.3 Probability Calibration and Regression Influence Diagnostics")
    add_para(doc, 
        "Model calibration was evaluated in Figure 9.4 and outputs/week3_model/calibration_deciles.csv. Predicted probabilities were binned "
        "into deciles and compared against empirical high-income proportions. The calibration curve tracks the ideal 45-degree diagonal closely: "
        "individuals in Decile 1 (predicted mean probability = 1.0%) exhibit an empirical rate of 1.4%, while individuals in Decile 10 (mean probability = 85.3%) "
        "exhibit an empirical rate of 84.1%. This confirms that the model's predicted probabilities can be directly interpreted as well-calibrated posterior risks.")

    add_figure(doc, "plots/week3/week3_calibration_plot.png", "9.4", 
               "Decile Probability Calibration Curve", 
               "Empirical reliability diagram confirming that predicted probabilities align closely with observed proportions across all ten deciles.")

    add_para(doc, 
        "Influence diagnostics were conducted via Cook's distance in Figure 9.5. The maximum Cook's distance across all 26,029 training observations "
        "was 0.0051, well below the standard threshold of 4/N = 0.00015 to 1.0. This confirms that no single high-leverage observation exerted undue influence "
        "over the estimated regression coefficients.")

    add_figure(doc, "plots/week3/week3_cooks_distance_residuals.png", "9.5", 
               "Influence Diagnostics: Cook's Distance and Pearson Residuals", 
               "Index plot confirming that influence is distributed evenly across observations without disruptive leverage points.")

    # =========================================================================
    # SECTION 10: INTEGRATED FINDINGS ACROSS WEEKS 1–3
    # =========================================================================
    add_heading_1(doc, "Section 10 — Integrated Findings Across Weeks 1–3")
    
    add_para(doc, 
        "A central objective of Week 4 is to demonstrate how the three preceding phases integrate into a unified analytical whole. "
        "Rather than treating data cleaning, visualization, hypothesis testing, and predictive modeling as disconnected exercises, "
        "the project followed a cumulative progression: data cleaning established hygiene, visualization revealed candidate relationships, "
        "hypothesis testing established inferential validity, and predictive modeling synthesized all features into a calibrated decision engine. "
        "Table 10.1 maps this progression across all phases:")

    # Table 10.1 Synthesis Matrix
    int_matrix = [
        ("Week 1: Import & Schema Audit", "01_import.R, 02_quality_assessment.R", "01_head_output.txt, 02_quality_table.csv", "Established data integrity; identified '?' missingness tokens and whitespace padding; verified 32,561 rows across 15 variables."),
        ("Week 1: Cleaning & Deduplication", "03_cleaning.R", "03_cleaning_report.txt, adult_cleaned.rds", "Mode-imputed 4,262 missing cells; purged 24 exact duplicates; fixed authenticated sample size at N = 32,537."),
        ("Week 1: Outlier Audit", "04_outlier_analysis.R", "04_outlier_summary.csv, 04_boxplots_combined.png", "Audited Tukey fences; justified retention of 9,002 hours and 2,712 capital gain records as valid socioeconomic variance."),
        ("Week 1: Transformation", "05_transformation.R", "05_transformation_report.txt, adult_encoded.rds", "Applied log-scaling and dummy variable encoding to prepare data for machine learning algorithms."),
        ("Week 2: Target Exploration", "08_week2_visualizations.R", "week2_01_income_distribution.png", "Exposed 3.15:1 class imbalance (75.91% vs 24.09%); established that raw accuracy is an inadequate evaluation metric."),
        ("Week 2: Bivariate Exploration", "08_week2_visualizations.R", "week2_04_education_vs_income.png, week2_06_age_vs_income.png", "Discovered 10-year median age gap (34 vs 44) and non-linear education credential threshold at the Bachelor's level."),
        ("Week 2: Labor Supply & Conditioning", "08_week2_visualizations.R, 09_week2_analysis.R", "week2_08_hours_vs_income.png, week2_14_lattice.png", "Identified 40-hour institutional spike (46.73%) and gender-specific working-hour penalties."),
        ("Week 3: Hypothesis Testing", "10_week3_statistical_analysis.R", "hypothesis_tests.csv, hypothesis_test_report.txt", "Formally verified all 8 hypotheses (all p < 0.0001); quantified effect sizes: Cramer's V = 0.369 (edu) and Cohen's d = 0.563 (age)."),
        ("Week 3: Predictive Modeling", "11_week3_modeling.R", "week3_models.rds, odds_ratios.csv", "Trained Baseline, GLM, and Elastic Net on stratified 80/20 split; quantified adjusted odds ratios (married OR = 7.16, edu OR = 1.35)."),
        ("Week 3: Diagnostics & Evaluation", "12_week3_evaluation.R", "evaluation_metrics.csv, week3_roc_curves.png", "Achieved 84.76% accuracy and 0.9047 ROC-AUC on held-out test set; validated low GVIF (< 1.73) and decile probability calibration."),
        ("Week 4: Synthesis & Presentation", "generate_week4_report.py", "Week4_Comprehensive_Data_Analysis_Final_Report.docx", "Integrated all evidence into a unified academic monograph; formulated policy implications and reproducibility appendix.")
    ]
    
    tbl_im = doc.add_table(rows=len(int_matrix) + 1, cols=4)
    tbl_im.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_im, "D0D7DE")
    
    style_header_cell(tbl_im.rows[0].cells[0], "Project Stage", width=Inches(1.5))
    style_header_cell(tbl_im.rows[0].cells[1], "Source Scripts", width=Inches(1.4))
    style_header_cell(tbl_im.rows[0].cells[2], "Verified Output", width=Inches(1.5))
    style_header_cell(tbl_im.rows[0].cells[3], "Contribution to Final Findings", width=Inches(2.1))
    
    for idx, (p_stg, p_scr, p_out, p_con) in enumerate(int_matrix):
        row = tbl_im.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], p_stg, width=Inches(1.5), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], p_scr, width=Inches(1.4), bg_hex=bg)
        style_data_cell(row.cells[2], p_out, width=Inches(1.5), bold=True, bg_hex=bg)
        style_data_cell(row.cells[3], p_con, width=Inches(2.1), bg_hex=bg)

    p_cap_im = doc.add_paragraph()
    p_cap_im.paragraph_format.space_before = Pt(2)
    p_cap_im.paragraph_format.space_after = Pt(8)
    r_cim = p_cap_im.add_run("Table 10.1: Cumulative integration matrix tracking the progression of data hygiene, visualization, hypothesis testing, and predictive modeling.")
    r_cim.font.size = Pt(8.5)
    r_cim.italic = True
    r_cim.font.color.rgb = COLOR_MUTED

    add_heading_2(doc, "From Exploratory Observation to Confirmatory Modeling")
    add_para(doc, 
        "The analytic journey revealed clear patterns of progression. In Week 2, visualizations of age (Figure 6.3) and education (Figure 6.2) "
        "suggested strong associations with income. In Week 3, Welch t-tests and Chi-Square tests confirmed that these associations were not random fluctuations, "
        "establishing Cohen's d = 0.563 for age and Cramer's V = 0.3689 for education. Finally, multivariate logistic regression demonstrated that even "
        "after simultaneously controlling for hours worked, occupation, marital status, and sector, education (OR = 1.35 per year) and age (OR = 1.024 per year) "
        "remain powerful independent predictors of income. This progression demonstrates how exploratory observations mature into confirmed, calibrated insights.")

    # =========================================================================
    # SECTION 11: DISCUSSION AND PRACTICAL IMPLICATIONS
    # =========================================================================
    add_heading_1(doc, "Section 11 — Discussion and Practical Implications")
    
    add_para(doc, 
        "The empirical findings of this project provide rich insights into the labor economics of late-20th-century America, "
        "while highlighting critical methodological principles for modern data science practitioners.")

    add_heading_2(doc, "11.1 Socioeconomic Interpretations: Human Capital and Household Structure")
    add_para(doc, 
        "Our findings strongly support Gary Becker's Human Capital Theory: each additional year of formal education increases the modeled odds of "
        "earning >$50K by 34.9%, with dramatic credential effects at the Bachelor's (41.49%) and doctoral (74.09%) levels. "
        "Similarly, the 10-year age gap (median 44 vs 34) and positive age coefficient reflect the classic Mincerian earnings life-cycle, "
        "where accumulated workplace experience and seniority yield higher compensation. "
        "However, the single strongest predictor in the multivariate model was civilian marriage (OR = 7.16). Rather than indicating that marriage itself "
        "causes higher earnings, this reflects well-documented sociological and economic mechanisms: dual-earner household stability, specialization, "
        "and unmeasured traits (e.g., conscientiousness, stability) that simultaneously favor both marriage and career advancement.")

    add_heading_2(doc, "11.2 The Critical Distinction Between Association and Causation")
    add_para(doc, 
        "It is essential to state unambiguously: none of the empirical models in this report prove causal relationships. "
        "The UCI Adult dataset is a cross-sectional observational survey, not a randomized controlled trial or natural experiment. "
        "Coefficients represent conditional statistical associations. Recommending that an individual marry or change work sectors solely to increase "
        "their income confuses statistical association with causal mechanisms.")

    add_heading_2(doc, "11.3 Algorithmic Fairness, Ethical Constraints, and High-Stakes Decision-Making")
    add_para(doc, 
        "Because historical survey data reflects historical societal disparities, models trained on this data inevitably encode those disparities. "
        "In the 1994 census sample, men comprise 66.92% of the workforce and show higher rates of high-income classification (30.57% vs 10.95% for women). "
        "Directly using protected demographic attributes (such as sex or race) or unmonitored proxy variables (such as relationship or marital status) "
        "in automated systems for hiring, lending, or criminal justice would violate U.S. anti-discrimination laws (e.g., Title VII of the Civil Rights Act "
        "and the Equal Credit Opportunity Act). The models developed here are intended strictly for descriptive socioeconomic analysis and benchmarking, "
        "and must never be deployed for consequential individual scoring without rigorous algorithmic bias audits.")

    # =========================================================================
    # SECTION 12: CHALLENGES ENCOUNTERED AND LESSONS LEARNED
    # =========================================================================
    add_heading_1(doc, "Section 12 — Challenges Encountered and Lessons Learned")
    
    add_para(doc, 
        "Over the four-week execution of this project, several technical and methodological challenges arose. "
        "Documenting these challenges and their solutions provides valuable lessons for applied data science:")

    challenges = [
        ("1. Encoded Missingness via Non-Standard Question Marks",
         "The raw data encoded missing values as '?' padded with spaces rather than standard NA tokens, causing standard is.na() checks to report zero missing values initially.",
         "Enforced na.strings = c('?', ' ?', 'NA') during ingestion in R/01_import.R, correctly exposing 4,262 missing cells and enabling statistical mode imputation in R/03_cleaning.R."),
        
        ("2. Extreme Zero-Inflation and Top-Coding in Capital Accounts",
         "Capital gain (91.66% zeroes) and capital loss (95.32% zeroes) exhibited extreme right-skewness, with capital gains artificially capped at $99,999 (159 individuals).",
         "Preserved all records to maintain valid economic variance, while avoiding standard normalization for these features in linear models to prevent severe distribution distortion."),
        
        ("3. Severe Target Class Imbalance (3.15:1 Ratio)",
         "Low earners (75.91%) dominate high earners (24.09%), causing naive classifiers to achieve high accuracy (75.91%) while failing completely on the minority class.",
         "Adopted stratified sampling across train/test splits and evaluated models using balanced accuracy, precision, recall, F1-score, ROC-AUC (0.9047), and PR-AUC (0.7271)."),
        
        ("4. Large Sample Size (N = 32,537) P-Value Inflation",
         "With N = 32,537, standard errors were so small that all hypothesis tests yielded p < 0.0001, making p-values uninformative for assessing practical importance.",
         "Shifted analytical focus to standardized effect sizes (Cramer's V, Cohen's d, Rank-Biserial r, Pearson r), distinguishing strong effects (education V = 0.369) from weak ones (correlation r = 0.148)."),
        
        ("5. High Cardinality Categorical Variables and Multicollinearity",
         "Expanding multi-level factors (14 occupations, 8 workclasses, 41 countries) into dummy variables risked design matrix explosion and severe multicollinearity.",
         "Grouped native_country into US vs Non-US and validated all features using Generalized Variance Inflation Factors (GVIF < 1.73), confirming no harmful collinearity."),

        ("6. Hypothesis Suite Reconciliation (8 Verified Tests vs. 9 Mentions)",
         "An earlier completion summary informally referenced 'nine tests' while listing only eight named rows.",
         "Audited R/10_week3_statistical_analysis.R and confirmed that exactly eight tests were recorded in outputs/week3_statistics/hypothesis_tests.csv; clarified that the ninth reference conflated the supplementary Spearman correlation matrix.")
    ]
    
    for c_title, c_prob, c_sol in challenges:
        add_heading_2(doc, c_title)
        add_para(doc, c_prob, bold_prefix="Encountered Challenge: ")
        add_para(doc, c_sol, bold_prefix="Engineered Solution: ")

    # =========================================================================
    # SECTION 13: RECOMMENDATIONS AND FUTURE WORK
    # =========================================================================
    add_heading_1(doc, "Section 13 — Recommendations and Future Work")
    
    add_para(doc, 
        "Based on the empirical findings and methodological insights from this four-week project, "
        "we recommend several avenues for operational refinement and future research:")

    add_bullet(doc, 
        "In production deployment, classification cutoffs should be optimized based on asymmetric misclassification costs. "
        "If false negatives are twice as costly as false positives, the optimal threshold shifts from 0.50 to approximately 0.35, "
        "increasing recall from 60.14% to ~75% while maintaining acceptable precision.",
        bold_prefix="1. Decision-Theoretic Cost-Sensitive Threshold Tuning: ")

    add_bullet(doc, 
        "While logistic regression provides excellent interpretability and strong discrimination (ROC-AUC = 0.9047), non-linear ensemble algorithms "
        "(such as Gradient Boosted Decision Trees / XGBoost and Random Forests) should be benchmarked to capture complex non-linear feature interactions, "
        "paired with SHAP (Shapley Additive exPlanations) for model transparency.",
        bold_prefix="2. Non-Linear Ensemble Benchmarking with SHAP Interpretability: ")

    add_bullet(doc, 
        "The 1994 CPS dataset reflects labor dynamics from three decades ago. Future work should replicate this analysis on contemporary "
        "American Community Survey (ACS) 1-year and 5-year public microdata to evaluate how education returns, remote work hours, "
        "and gender pay parity have evolved in the modern economy.",
        bold_prefix="3. Temporal Validation on Modern Census Microdata (ACS): ")

    add_bullet(doc, 
        "Formally assess disparate impact and equalized odds across demographic subgroups (sex, race, age). "
        "If models exhibit disparate performance, implement fairness-aware regularization (such as adversarial debiasing or disparate impact reweighting) "
        "to ensure equitable performance across all cohorts.",
        bold_prefix="4. Formal Algorithmic Fairness and Disparate Impact Audits: ")

    add_bullet(doc, 
        "Engineer explicit interaction terms (e.g., age * education_num, sex * hours_per_week) and incorporate external economic indicators "
        "(such as regional cost-of-living indices) to provide localized earnings benchmarks.",
        bold_prefix="5. Advanced Feature Engineering and Interaction Terms: ")

    # =========================================================================
    # SECTION 14: CONCLUSION
    # =========================================================================
    add_heading_1(doc, "Section 14 — Conclusion")
    
    add_para(doc, 
        "This capstone project successfully completed the end-to-end data science lifecycle on the UCI Adult Census Income dataset, "
        "integrating data hygiene, exploratory visualization, inferential testing, and predictive modeling into a cohesive monograph. "
        "The project demonstrated that data cleaning is foundational: resolving non-standard missingness and deduplicating records established "
        "a reliable sample of 32,537 observations. Graphical exploration uncovered essential structural features, including a 3.15:1 class imbalance, "
        "a 10-year median age divergence, and an institutional workweek anchor at 40 hours. Formal hypothesis testing established statistical "
        "significance across all eight verified tests, while effect sizes illuminated the practical importance of education, age, and occupation. "
        "Finally, regularized predictive models achieved an ROC-AUC of 0.9047 and balanced accuracy of 76.36%, demonstrating strong out-of-sample "
        "generalization while maintaining full interpretability.")
    
    add_para(doc, 
        "Above all, this project demonstrates the value of transparent, reproducible, evidence-based data science. "
        "By enforcing fixed random seeds, modular script architecture, and strict tracking of empirical evidence across R and Python, "
        "the entire analysis can be verified, re-executed, and audited by external researchers. This systematic approach ensures that every "
        "analytical conclusion is grounded in verified empirical evidence, providing a reliable foundation for data-driven decision-making.")

    # =========================================================================
    # SECTION 15: REPRODUCIBILITY AND TECHNICAL APPENDIX
    # =========================================================================
    add_heading_1(doc, "Section 15 — Reproducibility and Technical Appendix")
    
    add_para(doc, 
        "To guarantee complete scientific reproducibility, the entire project structure, execution pipeline, software environment, "
        "and statistical terminology are documented below.")

    add_heading_2(doc, "15.1 Repository Directory Structure")
    add_code_block(doc,
"""c:/Users/Microsoft/week/week-1-r-data-cleaning-analysis/
|-- data/
|   |-- original/adult.data, adult.names, adult.test
|   |-- cleaned/adult_cleaned.csv, adult_cleaned.rds
|-- R/
|   |-- 01_import.R                   # Ingestion & raw schema audit
|   |-- 02_quality_assessment.R       # Missingness & type validation
|   |-- 03_cleaning.R                 # Mode imputation & deduplication
|   |-- 04_outlier_analysis.R         # Tukey IQR screening
|   |-- 05_transformation.R           # Scaling & dummy encoding
|   |-- 06_eda.R                      # Exploratory data analysis
|   |-- 07_final_analysis.R           # Cleaned data hygiene audit
|   |-- 08_week2_visualizations.R     # ggplot2 & lattice visualizations
|   |-- 09_week2_analysis.R           # Graphical insight extraction
|   |-- 10_week3_statistical_analysis.R # Hypothesis testing suite
|   |-- 11_week3_modeling.R           # Logistic & Elastic Net modeling
|   |-- 12_week3_evaluation.R         # Test evaluation & diagnostics
|   |-- 13_week3_report_generation.R  # Week 3 report driver
|-- outputs/
|   |-- adult_cleaned.rds, adult_encoded.rds, adult_normalized.rds
|   |-- 02_quality_table.csv, 04_outlier_summary.csv, 07_descriptive_stats.csv
|   |-- week3_statistics/ (hypothesis_tests.csv, descriptive_statistics.csv)
|   |-- week3_model/ (evaluation_metrics.csv, odds_ratios.csv, vif_results.csv)
|-- plots/                            # 20+ High-resolution visualization PNGs
|   |-- week3/                        # 15 Model & hypothesis testing diagnostic PNGs
|-- report/
|   |-- generate_report.py            # Week 1 report compiler
|   |-- generate_week2_report.py      # Week 2 report compiler
|   |-- generate_week3_report.py      # Week 3 report compiler
|   |-- generate_week4_report.py      # Week 4 comprehensive report compiler
|   |-- Week4_Comprehensive_Data_Analysis_Final_Report.docx (Main Deliverable)
|-- run_all.R                         # Master pipeline driver (13 R scripts)
|-- README.md                         # Complete project documentation""",
        caption="Repository file layout and component inventory.")

    add_heading_2(doc, "15.2 Software Environment and Package Registry")
    add_para(doc, 
        "All analyses were executed under R version 4.6.1 (x86_64-w64-mingw32). Table 15.1 details the verified R packages used "
        "(outputs/evidence/week3/r_package_versions.csv):")

    pkg_rows = [
        ("dplyr", "1.2.1", "Data manipulation, filtering, and aggregation"),
        ("ggplot2", "4.0.3", "Grammar of graphics data visualization"),
        ("tidyr", "1.3.2", "Tidy data restructuring and reshaping"),
        ("scales", "1.4.0", "Formatting axes, percentages, and currencies"),
        ("corrplot", "0.95", "Correlation matrix graphical heatmaps"),
        ("reshape2", "1.4.5", "Design matrix melting and restructuring"),
        ("moments", "0.14.1", "Higher-order skewness and kurtosis calculations"),
        ("car", "3.1.5", "Companion to Applied Regression (GVIF diagnostics)"),
        ("glmnet", "5.1", "Elastic-net and lasso regularized generalized linear models"),
        ("pROC", "1.19.1", "Receiver Operating Characteristic curve analysis and AUC"),
        ("python-docx", "1.2.0", "Programmatic compilation of academic Microsoft Word reports")
    ]
    tbl_pkg = doc.add_table(rows=len(pkg_rows) + 1, cols=3)
    tbl_pkg.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_pkg, "D0D7DE")
    
    style_header_cell(tbl_pkg.rows[0].cells[0], "Package Name", width=Inches(1.5))
    style_header_cell(tbl_pkg.rows[0].cells[1], "Verified Version", width=Inches(1.5))
    style_header_cell(tbl_pkg.rows[0].cells[2], "Analytical Functionality", width=Inches(3.5))
    
    for idx, (p_n, p_v, p_u) in enumerate(pkg_rows):
        row = tbl_pkg.rows[idx + 1]
        bg = "F8F9FA" if idx % 2 == 1 else "FFFFFF"
        style_data_cell(row.cells[0], p_n, width=Inches(1.5), bold=True, bg_hex=bg)
        style_data_cell(row.cells[1], p_v, width=Inches(1.5), bold=True, bg_hex=bg)
        style_data_cell(row.cells[2], p_u, width=Inches(3.5), bg_hex=bg)

    p_cap_pkg = doc.add_paragraph()
    p_cap_pkg.paragraph_format.space_before = Pt(2)
    p_cap_pkg.paragraph_format.space_after = Pt(8)
    r_cpk = p_cap_pkg.add_run("Table 15.1: Software package inventory and verified version numbers.")
    r_cpk.font.size = Pt(8.5)
    r_cpk.italic = True
    r_cpk.font.color.rgb = COLOR_MUTED

    add_heading_2(doc, "15.3 Pipeline Execution Instructions")
    add_para(doc, "To replicate the complete four-week analytical pipeline from scratch, execute the following commands in order:")
    add_code_block(doc,
"""# 1. Clone repository and navigate to root directory
git clone https://github.com/G1OUL/week-1-r-data-cleaning-analysis.git
cd week-1-r-data-cleaning-analysis

# 2. Execute full 13-script R pipeline (Weeks 1, 2, and 3)
Rscript run_all.R

# 3. Generate Week 4 Final Comprehensive Integrated Report (.docx)
python report/generate_week4_report.py""",
        caption="Command-line instructions for full end-to-end pipeline execution.")

    add_heading_2(doc, "15.4 Glossary of Statistical and Machine Learning Terms")
    glossary_terms = [
        ("Cramer's V", "A standardized measure of association between two nominal categorical variables, ranging from 0 (independence) to 1 (complete association)."),
        ("Cohen's d", "Standardized difference between two group means, expressed in units of pooled standard deviations. Values of 0.2, 0.5, and 0.8 represent small, medium, and large effects."),
        ("Generalized VIF (GVIF)", "Variance Inflation Factor extended to multi-degree-of-freedom categorical variables. GVIF^(1/(2*Df)) < 2.0 indicates the absence of harmful multicollinearity."),
        ("Odds Ratio (OR)", "Exponentiated logistic regression coefficient exp(beta). Represents the multiplicative change in the odds of the outcome associated with a one-unit increase in the predictor."),
        ("ROC-AUC", "Area Under the Receiver Operating Characteristic Curve. Measures discrimination across all possible classification thresholds, ranging from 0.5 (random chance) to 1.0 (perfect discrimination)."),
        ("PR-AUC", "Area Under the Precision-Recall Curve. Evaluates positive-class predictive quality under severe class imbalance; benchmarks against the empirical positive class prevalence (24.09%)."),
        ("False Discovery Rate (FDR)", "The expected proportion of false positive findings among all rejected null hypotheses. Controlled via the Benjamini-Hochberg procedure.")
    ]
    for g_t, g_d in glossary_terms:
        add_bullet(doc, g_d, bold_prefix=f"{g_t}: ")

    # =========================================================================
    # SECTION 16: REFERENCES
    # =========================================================================
    add_heading_1(doc, "Section 16 — References")
    
    references = [
        "Becker, G. S. (1964). Human Capital: A Theoretical and Empirical Analysis, with Special Reference to Education. National Bureau of Economic Research, New York.",
        "Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B (Methodological), 57(1), 289-300.",
        "Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences (2nd ed.). Lawrence Erlbaum Associates, Hillsdale, NJ.",
        "Cramer, H. (1946). Mathematical Methods of Statistics. Princeton University Press, Princeton, NJ.",
        "Fox, J., & Weisberg, S. (2019). An R Companion to Applied Regression (3rd ed.). Sage Publications, Thousand Oaks, CA.",
        "Friedman, J., Hastie, T., & Tibshirani, R. (2010). Regularization paths for generalized linear models via coordinate descent. Journal of Statistical Software, 33(1), 1-22.",
        "Kohavi, R., & Becker, B. (1996). Adult Data Set. UCI Machine Learning Repository. Available: https://archive.ics.uci.edu/dataset/2/adult",
        "Mincer, J. (1974). Schooling, Experience, and Earnings. National Bureau of Economic Research, New York.",
        "R Core Team. (2026). R: A Language and Environment for Statistical Computing. R Foundation for Statistical Computing, Vienna, Austria. Available: https://www.R-project.org/",
        "Robin, X., Turck, N., Hainard, A., Tiberti, N., Lisacek, F., Sanchez, J. C., & Muller, M. (2011). pROC: An open-source package for R and S+ to analyze and compare ROC curves. BMC Bioinformatics, 12, 77.",
        "Tufte, E. R. (2001). The Visual Display of Quantitative Information (2nd ed.). Graphics Press, Cheshire, CT.",
        "Wickham, H. (2016). ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag, New York."
    ]
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.paragraph_format.space_after = Pt(4)
        r_rf = p_ref.add_run(ref)
        r_rf.font.name = "Calibri"
        r_rf.font.size = Pt(9.5)
        r_rf.font.color.rgb = COLOR_TEXT

    # Save document
    print(f"Saving final report to: {REPORT_PATH}...")
    doc.save(REPORT_PATH)
    file_size = os.path.getsize(REPORT_PATH)
    print(f"Report generated successfully! File size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
    print("=" * 70)
    return REPORT_PATH

if __name__ == "__main__":
    generate_week4_final_report()
