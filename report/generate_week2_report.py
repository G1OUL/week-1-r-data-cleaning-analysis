"""
generate_week2_report.py
Constructs a comprehensive, publication-quality DOCX report for:
"Week 2: Data Visualization and Insight Communication Using R"
UCI Adult / Census Income Dataset
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLOTS_DIR    = os.path.join(PROJECT_ROOT, "plots")
REPORT_PATH  = os.path.join(PROJECT_ROOT, "report", "Week2_Data_Visualization_Report.docx")
R_DIR        = os.path.join(PROJECT_ROOT, "R")
OUTPUTS_DIR  = os.path.join(PROJECT_ROOT, "outputs")

# ── Colour palette (Academic Navy / Slate) ──────────────────────────────────
COLOR_PRIMARY   = RGBColor(27,  54,  93)   # #1B365D Deep Navy
COLOR_SECONDARY = RGBColor(70,  92,  122)  # #465C7A Slate
COLOR_TEXT      = RGBColor(33,  37,  41)   # #212529 Charcoal
COLOR_MUTED     = RGBColor(108, 117, 125)  # #6C757D Muted Gray
COLOR_CODE      = RGBColor(40,  44,  52)   # #282C34 Code Text
COLOR_RED       = RGBColor(192, 57,  43)   # Warning red
COLOR_CAUTION   = RGBColor(241, 196, 15)   # Caution amber


# ── Document helpers ─────────────────────────────────────────────────────────

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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
        f'<w:top    w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left    w:val="none"/>'
        f'<w:right   w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_page_number(doc):
    """Insert a page number field into the last paragraph."""
    p = doc.paragraphs[-1]._p
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    p.append(fld)
    instr = OxmlElement("w:instrText")
    instr.text = "PAGE"
    p.append(instr)
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    p.append(fld2)

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    h.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    h.paragraph_format.space_after  = Pt(4)
    run = h.runs[0]
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(18); run.font.color.rgb = COLOR_PRIMARY;   run.bold = True
    elif level == 2:
        run.font.size = Pt(14); run.font.color.rgb = COLOR_SECONDARY; run.bold = True
    elif level == 3:
        run.font.size = Pt(12); run.font.color.rgb = COLOR_SECONDARY; run.bold = True
    return h

def add_para(doc, text="", bold_prefix=None, space_after=6, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.font.name = "Calibri"; r.font.size = Pt(11); r.bold = True
        r.font.color.rgb = COLOR_PRIMARY
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"; r.font.size = Pt(11)
        r.font.color.rgb = color if color else COLOR_TEXT
    return p

def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(11); r.font.color.rgb = COLOR_TEXT

def add_callout(doc, text, bg="F0F4F8"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit   = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.italic = True
    r.font.color.rgb = COLOR_SECONDARY
    doc.add_paragraph()

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit   = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "1E1E2E")
    set_cell_margins(cell, top=150, bottom=150, left=200, right=200)
    p = cell.paragraphs[0]
    r = p.add_run(code_text.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(205, 214, 244)  # Light lavender code color
    doc.add_paragraph()

def add_figure(doc, png_filename, caption_text):
    img_path = os.path.join(PLOTS_DIR, png_filename)
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(img_path, width=Inches(6.0))
    else:
        add_para(doc, f"[Image not found: {png_filename}]", color=COLOR_RED)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(12)
    cr = cap.add_run(caption_text)
    cr.font.name = "Calibri"; cr.font.size = Pt(9.5); cr.italic = True
    cr.font.color.rgb = COLOR_MUTED

def add_insight_box(doc, label, text, bg="F8F9FA"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit   = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    p = cell.paragraphs[0]
    rb = p.add_run(label + " ")
    rb.font.name = "Calibri"; rb.font.size = Pt(11); rb.bold = True; rb.font.color.rgb = COLOR_PRIMARY
    rt = p.add_run(text)
    rt.font.name = "Calibri"; rt.font.size = Pt(11); rt.font.color.rgb = COLOR_TEXT
    doc.add_paragraph()

def read_r_script(script_name):
    path = os.path.join(R_DIR, script_name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"# {script_name} not found"


# ── Visualization metadata ───────────────────────────────────────────────────

VIZUALISATIONS = [
    {
        "num": 1, "title": "Income Distribution",
        "figure": "Figure 1. Distribution of Annual Income Thresholds",
        "png": "week2_01_income_distribution.png",
        "purpose": (
            "To quantify and visually communicate the frequency of each income "
            "category (<=50K, >50K) present in the 1994 U.S. Census Bureau dataset, "
            "establishing the baseline class distribution before any comparative analysis."
        ),
        "why_chart": (
            "A simple vertical bar chart (column chart) was selected because income "
            "is a nominal categorical variable with only two levels. Bar charts are "
            "universally readable, allow exact count labels, and provide clear visual "
            "magnitude comparison. No other chart type is more appropriate for "
            "summarising a dichotomous categorical distribution."
        ),
        "code_snippet": """# Professional bar chart of income distribution
df_inc <- adult %>%
  count(income) %>%
  mutate(pct = n / sum(n) * 100,
         label = sprintf("%s\\n(%.1f%%)", format(n, big.mark = ","), pct))

ggplot(df_inc, aes(x = income, y = n, fill = income)) +
  geom_col(width = 0.52, show.legend = FALSE) +
  geom_text(aes(label = label), vjust = -0.3, fontface = "bold") +
  scale_fill_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F")) +
  scale_y_continuous(labels = comma, limits = c(0, 28000)) +
  labs(title = "Figure 1. Distribution of Annual Income Thresholds",
       x = "Annual Income Category", y = "Number of Individuals")""",
        "interpretation": (
            "The chart reveals a pronounced class imbalance: 24,698 individuals "
            "(75.91%) earn <=50K annually, compared to only 7,839 individuals (24.09%) "
            "who earn >50K. This imbalance has a ratio of approximately 3.15:1. "
            "The visual immediately communicates to a non-technical viewer that "
            "\"most people in this dataset earn no more than $50,000 a year.\""
        ),
        "insight": (
            "The UCI Adult dataset exhibits a severe class imbalance: 3 out of 4 "
            "surveyed workers earn at or below $50,000 per year. This structural skew "
            "must be acknowledged when interpreting any subsequent proportional comparisons."
        ),
    },
    {
        "num": 2, "title": "Age Distribution",
        "figure": "Figure 2. Distribution of Worker Age",
        "png": "week2_02_age_distribution.png",
        "purpose": (
            "To examine the age structure of the surveyed workforce and identify any "
            "concentration, spread, and skewness in the age variable."
        ),
        "why_chart": (
            "A histogram is the definitive chart type for displaying the empirical "
            "frequency distribution of a continuous variable. It groups observations "
            "into adjacent intervals (bins), reveals unimodality or multimodality, "
            "and displays skewness that summary statistics alone may not communicate."
        ),
        "code_snippet": """age_median <- median(adult$age)  # 37
age_mean   <- mean(adult$age)    # 38.59

ggplot(adult, aes(x = age)) +
  geom_histogram(binwidth = 2, fill = "#3498DB", color = "white", alpha = 0.85) +
  geom_vline(xintercept = age_median, color = "#C0392B", linetype = "dashed") +
  annotate("text", x = age_median + 2, y = 2400,
           label = sprintf("Median: %d yrs\\nMean: %.1f yrs", age_median, age_mean)) +
  labs(title = "Figure 2. Distribution of Worker Age",
       x = "Age (Years)", y = "Count of Observations")""",
        "interpretation": (
            "The distribution is right-skewed (skewness = +0.56): the modal mass of "
            "workers falls between ages 25 and 45. The median age is 37 years (mean 38.6), "
            "with 50% of workers falling in the interquartile range of 28 to 48 years. "
            "A long right tail extends to age 90, representing retirees or individuals "
            "with supplementary work. The slight rightward skew means the mean is pulled "
            "above the median by older workers."
        ),
        "insight": (
            "The workforce is predominantly composed of prime-working-age adults (25–45), "
            "with a right-skewed age distribution. The median worker is 37 years old, "
            "and the IQR is 20 years (Q1=28, Q3=48), indicating a moderately broad "
            "age profile across the surveyed population."
        ),
    },
    {
        "num": 3, "title": "Education Distribution",
        "figure": "Figure 3. Distribution of Highest Educational Attainment",
        "png": "week2_03_education_distribution.png",
        "purpose": (
            "To display the frequency of workers at each educational level, ordered "
            "from lowest (Preschool) to highest (Doctorate), enabling a quick scan "
            "of workforce qualification composition."
        ),
        "why_chart": (
            "A horizontal bar chart was selected because the education variable is "
            "ordinal (naturally ranked from lowest to highest). Sorting by intrinsic "
            "education hierarchy (not by frequency) preserves educational order. "
            "Horizontal orientation avoids overlapping long labels and improves "
            "readability across 16 categories."
        ),
        "code_snippet": """df_edu <- adult %>%
  count(education, education_num) %>%
  arrange(education_num) %>%  # order by intrinsic hierarchy
  mutate(pct = n / sum(n) * 100,
         education = factor(education, levels = education))

ggplot(df_edu, aes(x = education, y = n, fill = education_num)) +
  geom_col(width = 0.72) +
  geom_text(aes(label = sprintf("%s (%.1f%%)", format(n, big.mark=","), pct)),
            hjust = -0.1, size = 3.5) +
  scale_fill_gradient(low = "#85C1E9", high = "#1B4F72") +
  coord_flip() +
  labs(title = "Figure 3. Distribution of Highest Educational Attainment")""",
        "interpretation": (
            "High-school graduation (HS-grad) is by far the most common educational "
            "credential (10,494 individuals, 32.3% of the workforce), followed by "
            "Some-college (7,282, 22.4%). Together, these two categories account for "
            "54.6% of the sample. Advanced credentials are relatively rare: Bachelors "
            "(16.5%), Masters (5.3%), Doctorate (1.3%), and Prof-school (1.8%). "
            "Very early educational levels (Preschool, 1st-4th) are negligible."
        ),
        "insight": (
            "The 1994 U.S. workforce surveyed in this dataset was predominantly "
            "high-school-level qualified (54.6% HS-grad or Some-college). Only 24.7% "
            "held a Bachelor's degree or higher, reflecting the educational attainment "
            "landscape of the early 1990s U.S. population."
        ),
    },
    {
        "num": 4, "title": "Education vs Income",
        "figure": "Figure 4. Proportional Income Distribution by Educational Attainment",
        "png": "week2_04_education_vs_income.png",
        "purpose": (
            "To examine whether observed proportions of high-income earners differ "
            "systematically across educational levels, using percentage-within-group "
            "comparison to avoid being misled by unequal group sizes."
        ),
        "why_chart": (
            "A 100% proportional stacked bar chart (filled bar) is the optimal choice "
            "when comparing compositions across groups of very different sizes. It "
            "eliminates the distortion caused by raw counts (e.g., HS-grad appears "
            "dominant due to sheer frequency, not necessarily income rate)."
        ),
        "code_snippet": """df_edu_inc <- adult %>%
  group_by(education, education_num, income) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(education) %>%
  mutate(total = sum(n), pct = n / total * 100) %>%
  ungroup() %>%
  arrange(education_num) %>%
  mutate(education = factor(education, levels = unique(education)))

ggplot(df_edu_inc, aes(x = education, y = pct, fill = income)) +
  geom_col(position = "fill", width = 0.72) +
  scale_y_continuous(labels = percent_format()) +
  scale_fill_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F")) +
  coord_flip()""",
        "interpretation": (
            "There is a clear monotonic pattern: as educational attainment increases, "
            "the observed proportion of high-income earners rises substantially. "
            "Preschool: 0.0%; HS-grad: 15.9%; Bachelors: 41.5%; Masters: 55.7%; "
            "Prof-school: 73.4%; Doctorate: 74.1%. "
            "It is important to note that this is an observational association, not "
            "a controlled experiment. Many other variables (age, occupation, work hours) "
            "are simultaneously associated with both education and income, so this chart "
            "CANNOT establish that higher education directly causes higher income."
        ),
        "insight": (
            "A monotonically increasing income proportion is observed as education "
            "rises, from 0% at Preschool to 74.1% at Doctorate level. The association "
            "is strong and consistent, but does not demonstrate causation. Confounding "
            "factors including age, occupation, and hours worked must also be considered."
        ),
    },
    {
        "num": 5, "title": "Workclass vs Income",
        "figure": "Figure 5. Proportional Income Distribution Across Workclass Sectors",
        "png": "week2_05_workclass_vs_income.png",
        "purpose": (
            "To compare the observed proportion of high-income earners across different "
            "employment sectors (private, government, self-employed) to identify "
            "systematic sector-level income differences."
        ),
        "why_chart": (
            "As with Education vs Income (Figure 4), a 100% proportional stacked bar "
            "chart is appropriate because groups have widely different sizes (Private: "
            "24,509 vs Never-worked: 7). Proportions allow valid within-category "
            "comparison that raw counts cannot support."
        ),
        "code_snippet": """df_wc_inc <- adult %>%
  group_by(workclass) %>%
  summarise(
    total    = n(),
    n_high   = sum(income == ">50K"),
    pct_high = sum(income == ">50K") / n() * 100
  )
# Sort by >50K percentage, then plot proportional stacked bar""",
        "interpretation": (
            "Self-employed incorporated workers display the highest observed proportion "
            "of high earners (55.7%), followed by Federal Government workers (38.7%). "
            "Private sector employees — the largest group at 75.3% of the workforce — "
            "have a relatively lower observed proportion of 21.0%. Never-worked and "
            "Without-pay categories have 0% high earners. These differences reflect "
            "sector characteristics and occupational composition within each category."
        ),
        "insight": (
            "Self-employed incorporated individuals and government workers display "
            "substantially higher observed high-income proportions compared to private "
            "sector employees. This likely reflects occupational composition and business "
            "ownership effects rather than direct sector causation."
        ),
    },
    {
        "num": 6, "title": "Age vs Income",
        "figure": "Figure 6. Age Distribution Contrasted by Income Group",
        "png": "week2_06_age_vs_income.png",
        "purpose": (
            "To directly compare the full age distribution between the <=50K and >50K "
            "income groups, including central tendency, spread, and shape."
        ),
        "why_chart": (
            "A hybrid violin + boxplot combines the best of both worlds: the violin "
            "body shows full distributional shape (density), while the embedded "
            "boxplot provides exact quantile positions (median, Q1, Q3) and identifies "
            "outliers. This is superior to a boxplot alone (which loses shape) or "
            "a density plot alone (which loses precise quantile information)."
        ),
        "code_snippet": """ggplot(adult, aes(x = income, y = age, fill = income)) +
  geom_violin(alpha = 0.5, trim = FALSE) +
  geom_boxplot(width = 0.18, fill = "white") +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3.5, fill = "#F39C12") +
  scale_fill_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F"))""",
        "interpretation": (
            "Higher earners (>50K) have a substantially older age profile. The median "
            "age for the <=50K group is 34 years (IQR: 25–46) versus 44 years (IQR: "
            "36–51) for the >50K group — a 10-year difference in median age. The violin "
            "shape for <=50K is wider at younger ages, indicating greater density of "
            "younger workers. The >50K group peaks in the 40–55 range. Both groups "
            "show some older outliers up to age 90."
        ),
        "insight": (
            "Workers in the >$50K income category are systematically older (median: "
            "44 vs 34 years; difference = 10 years). This is consistent with career "
            "progression effects, but cannot be separated from other correlated "
            "factors such as education, experience, and occupation type."
        ),
    },
    {
        "num": 7, "title": "Hours per Week Distribution",
        "figure": "Figure 7. Distribution of Weekly Working Hours",
        "png": "week2_07_hours_distribution.png",
        "purpose": (
            "To visualise the full distribution of weekly working hours, identifying "
            "its shape, modal values, and the extent of very long or part-time work."
        ),
        "why_chart": (
            "A histogram is the appropriate choice for a continuous variable (hours "
            "per week, range 1–99). It reveals the pronounced spike at 40 hours that "
            "would be invisible in a boxplot, and shows the right tail of overworking "
            "that summary statistics alone would not communicate."
        ),
        "code_snippet": """ggplot(adult, aes(x = hours_per_week)) +
  geom_histogram(binwidth = 2, fill = "#16A085", color = "white", alpha = 0.85) +
  geom_vline(xintercept = 40, color = "#C0392B", linetype = "dashed") +
  annotate("rect", xmin = 38, xmax = 42, ymin = 0, ymax = 16000, alpha = 0.15, fill = "#E74C3C") +
  labs(title = "Figure 7. Distribution of Weekly Working Hours",
       x = "Hours Worked per Week", y = "Number of Observations")""",
        "interpretation": (
            "The most striking feature is a dramatic spike at exactly 40 hours per week: "
            "15,204 individuals (46.7% of the total workforce) work precisely 40 hours. "
            "This represents the statutory full-time workweek and reflects strong "
            "institutional norms in the U.S. labour market. 23.8% work fewer than 40 "
            "hours (part-time) and 29.4% work more than 40 hours. A smaller right tail "
            "extends to 99 hours per week, representing intensive work arrangements."
        ),
        "insight": (
            "Nearly half the surveyed workforce (46.7%) works exactly 40 hours per week, "
            "demonstrating strong institutional anchoring to the statutory full-time "
            "workweek. The distribution is bimodal — a sharp 40-hour spike followed by "
            "a small secondary cluster around 50–60 hours among overtime workers."
        ),
    },
    {
        "num": 8, "title": "Hours per Week vs Income",
        "figure": "Figure 8. Weekly Hours Worked Compared Between Income Categories",
        "png": "week2_08_hours_vs_income.png",
        "purpose": (
            "To compare the distribution of weekly working hours between the two income "
            "categories to quantify whether high earners systematically work more hours."
        ),
        "why_chart": (
            "The same hybrid violin + boxplot approach used for age (Figure 6) is "
            "appropriate here. Hours per week is continuous with a non-normal distribution "
            "(spike at 40), so preserving distributional shape via violin is essential. "
            "The embedded boxplot provides precise median and IQR comparisons."
        ),
        "code_snippet": """ggplot(adult, aes(x = income, y = hours_per_week, fill = income)) +
  geom_violin(alpha = 0.5, trim = FALSE) +
  geom_boxplot(width = 0.18, fill = "white") +
  stat_summary(fun = mean, geom = "point", shape = 23, size = 3.5, fill = "#F39C12") +
  scale_fill_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F"))""",
        "interpretation": (
            "High earners work substantially more hours on average. The <=50K group "
            "has a median of 40 hours (IQR: 35–40; mean: 38.8) while the >50K group "
            "has a median of 40 hours (IQR: 40–50; mean: 45.5). Despite identical "
            "medians, the distributional shapes differ substantially: the >50K group "
            "has a much wider right tail (Q3=50 vs Q3=40 for <=50K), indicating that "
            "high earners are significantly more likely to work overtime hours."
        ),
        "insight": (
            "While both groups share a median of 40 hrs/week, the >$50K group works "
            "substantially more overtime: their Q3 is 50 hours compared to 40 hours "
            "for the <=50K group, and their mean is 45.5 vs 38.8 hours. This "
            "association does not establish a causal relationship."
        ),
    },
    {
        "num": 9, "title": "Age vs Hours per Week (Scatter Plot)",
        "figure": "Figure 9. Bivariate Relationship: Worker Age vs Weekly Working Hours",
        "png": "week2_09_age_vs_hours_scatter.png",
        "purpose": (
            "To explore the joint distribution of age and weekly hours, and to visually "
            "assess whether these two continuous variables show any systematic pattern, "
            "coloured by income group to add a third dimension."
        ),
        "why_chart": (
            "A scatter plot is the standard visualisation for exploring the relationship "
            "between two continuous variables. Transparency (alpha = 0.35) mitigates "
            "overplotting in a large dataset. Loess smoothing curves reveal the overall "
            "trend for each income group without imposing a linear assumption."
        ),
        "code_snippet": """set.seed(42)
adult_sample <- adult %>% sample_n(4000)  # Subsample for visual clarity

ggplot(adult_sample, aes(x = age, y = hours_per_week, color = income)) +
  geom_point(alpha = 0.35, size = 1.3) +
  geom_smooth(method = "loess", se = TRUE, linewidth = 1.1) +
  scale_color_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F"))""",
        "interpretation": (
            "The scatter plot reveals no strong linear relationship between age and "
            "weekly hours overall. The most prominent visual feature is a dense "
            "horizontal band at exactly 40 hours per week, confirming the full-time "
            "norm. The loess trend lines show that >50K earners maintain consistently "
            "higher average weekly hours across the prime career age range (35–55). "
            "Extreme observations (>80 hrs/week) are scattered across all ages. No "
            "clear curvilinear pattern links age to hours in either group."
        ),
        "insight": (
            "No strong linear relationship exists between age and hours worked. The "
            "scatter reveals that working patterns are determined more by institutional "
            "norms (40-hour spike) than by age. The Pearson correlation between age "
            "and hours per week is r = 0.069 (near-zero), confirming negligible linear "
            "association."
        ),
    },
    {
        "num": 10, "title": "Capital Gain Distribution",
        "figure": "Figure 10. Distribution of Positive Capital Gains (Log10 Scale)",
        "png": "week2_10_capital_gain_distribution.png",
        "purpose": (
            "To visualise the distribution of positive capital gains, addressing the "
            "challenge of a highly zero-dominated, heavily right-skewed financial variable."
        ),
        "why_chart": (
            "Capital gain spans four orders of magnitude ($114 to $99,999) among those "
            "reporting positive values. A standard linear-scale histogram would compress "
            "all values into a narrow strip near zero, making the distribution "
            "completely unreadable. A log10 x-axis is the analytically correct approach "
            "for such extreme right-skewed distributions. Zero values are excluded before "
            "log transformation because log(0) is undefined — this is clearly disclosed "
            "in the subtitle."
        ),
        "code_snippet": """# IMPORTANT: Zero values (91.7%) excluded before log transform
cg_nonzero <- adult %>% filter(capital_gain > 0)

ggplot(cg_nonzero, aes(x = capital_gain)) +
  geom_histogram(bins = 35, fill = "#E67E22", color = "white", alpha = 0.85) +
  geom_vline(xintercept = median(cg_nonzero$capital_gain),
             color = "#900C3F", linetype = "dashed") +
  scale_x_log10(labels = dollar_format()) +
  labs(subtitle = "Zero values (91.7% of population) isolated;\\n
  positive gains span 3 orders of magnitude")""",
        "interpretation": (
            "Of 32,537 individuals, 29,825 (91.7%) report zero capital gains — typical "
            "for wage workers without investment portfolios. Of the 2,712 (8.3%) "
            "reporting positive gains, the distribution on the log scale shows "
            "a spread from $114 to $99,999. The non-zero median is $7,298 (mean: "
            "$12,939). A notable cluster appears at the top-coded ceiling of $99,999 "
            "(159 individuals), which is a data censoring artifact from the original "
            "U.S. Census Bureau survey."
        ),
        "insight": (
            "Capital gain is dominated by zero values (91.7%), indicating that "
            "investment income is concentrated among a small minority. Among the 8.3% "
            "with positive gains, the distribution spans several orders of magnitude "
            "with a long right tail. The top-code at $99,999 introduces right-censoring "
            "that prevents observation of the true upper extremes."
        ),
    },
    {
        "num": 11, "title": "Correlation Heatmap",
        "figure": "Figure 11. Pearson Correlation Matrix of Continuous Census Features",
        "png": "week2_11_correlation_heatmap.png",
        "purpose": (
            "To simultaneously visualise all pairwise linear correlations between the "
            "six continuous numerical variables in the dataset, supporting multicollinearity "
            "assessment and identifying which variable pairs move together."
        ),
        "why_chart": (
            "A correlation heatmap with colour-scaled tiles and embedded coefficient "
            "values is the standard approach for summarising an n×n correlation matrix. "
            "Colour divergence from white (r=0) to red (r=+1) or blue (r=-1) allows "
            "instant detection of strong and weak relationships. It is superior to "
            "printing the raw matrix because it exploits human pattern recognition "
            "through colour encoding."
        ),
        "code_snippet": """library(reshape2)
num_cols <- c("age", "fnlwgt", "education_num", "capital_gain",
              "capital_loss", "hours_per_week")
cor_mat    <- cor(adult[, num_cols])
cor_melted <- melt(cor_mat)

ggplot(cor_melted, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "white") +
  geom_text(aes(label = sprintf("%.3f", value)), size = 3.8, fontface = "bold") +
  scale_fill_gradient2(low = "#2980B9", mid = "white", high = "#C0392B",
                       midpoint = 0, limit = c(-1, 1))""",
        "interpretation": (
            "The heatmap reveals uniformly weak-to-moderate linear correlations across "
            "all variable pairs. The strongest positive associations are: "
            "education_num ↔ hours_per_week (r = 0.148) and "
            "education_num ↔ capital_gain (r = 0.123). "
            "The only notable negative correlation is age ↔ fnlwgt (r = -0.076). "
            "The fnlwgt (census sampling weight) variable shows near-zero correlations "
            "with everything, confirming it reflects survey design rather than "
            "personal characteristics. No strong multicollinearity exists among "
            "predictors (all |r| < 0.15)."
        ),
        "insight": (
            "All pairwise linear correlations between continuous features are weak "
            "(all |r| < 0.15). The strongest finding is the positive association "
            "between education years and hours worked (r = 0.148). CAUTION: "
            "Correlation measures linear statistical association only. It does NOT "
            "imply causation, and cannot capture non-linear relationships."
        ),
    },
    {
        "num": 12, "title": "Creative: Occupation vs Income",
        "figure": "Figure 12. Proportional Income Disparity Across Occupations",
        "png": "week2_12_occupation_vs_income.png",
        "purpose": (
            "To reveal the full spectrum of occupational income inequality across "
            "14 occupation categories — from the highest-income professional roles "
            "to the lowest-income service positions — using proportional comparison "
            "that is not distorted by group size differences."
        ),
        "why_chart": (
            "An ordered proportional stacked bar chart sorted by >50K percentage "
            "was chosen as the creative visualisation because it communicates "
            "economic inequality with maximum clarity. Ordering by observed proportion "
            "creates a gradient from most to least economically advantaged occupations, "
            "which would be invisible in a conventional alphabetical or frequency-sorted chart."
        ),
        "code_snippet": """df_occ_inc <- adult %>%
  group_by(occupation) %>%
  summarise(
    total    = n(),
    n_high   = sum(income == ">50K"),
    pct_high = sum(income == ">50K") / n() * 100
  ) %>%
  arrange(pct_high)  # Sort ascending so highest appears at top after coord_flip

ggplot(df_occ_inc_long, aes(x = occupation, y = pct, fill = income)) +
  geom_col(position = "fill", width = 0.72) +
  coord_flip() +
  scale_fill_manual(values = c("<=50K" = "#2B5C8F", ">50K" = "#D9534F"))""",
        "interpretation": (
            "The visualisation reveals stark occupational economic stratification. "
            "Executive-managerial workers have a 48.4% observed high-income rate, "
            "closely followed by Prof-specialty (34.3%) and Protective-service (32.5%). "
            "In sharp contrast, Other-service (4.2%), Private-household-service (0.7%), "
            "and Farming-fishing (11.6%) show very low proportions of high earners. "
            "This disparity is consistent with known wage hierarchies but reflects "
            "the dataset's 1994 snapshot and does not account for occupation-level "
            "confounders."
        ),
        "insight": (
            "Occupational category is strongly associated with income group, with "
            "a 48-percentage-point gap between the highest (Exec-managerial: 48.4%) "
            "and lowest (Priv-house-serv: 0.7%) occupations. This visual directly "
            "communicates the economic stratification embedded in occupational choice "
            "and represents the single strongest categorical predictor of income "
            "observed in the dataset."
        ),
    },
]


# ── R code snippets for appendix ────────────────────────────────────────────

def get_r_script_section(script_name, start_marker=None, end_marker=None):
    """Read a segment of an R script for the appendix."""
    code = read_r_script(script_name)
    if start_marker and start_marker in code:
        idx = code.index(start_marker)
        code = code[idx:]
    if end_marker and end_marker in code:
        idx = code.index(end_marker) + len(end_marker)
        code = code[:idx]
    return code


# ── Build document ───────────────────────────────────────────────────────────

def build_report():
    doc = Document()

    # Page margins
    from docx.oxml import OxmlElement
    for sec in doc.sections:
        sec.page_width   = Inches(8.5)
        sec.page_height  = Inches(11)
        sec.left_margin  = Inches(1.1)
        sec.right_margin = Inches(1.1)
        sec.top_margin   = Inches(1.0)
        sec.bottom_margin = Inches(1.0)

    # ─── TITLE PAGE ────────────────────────────────────────────────────────
    doc.add_paragraph()
    doc.add_paragraph()
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_r = title_p.add_run("Week 2: Data Visualization and\nInsight Communication Using R")
    title_r.font.name = "Calibri"; title_r.font.size = Pt(26)
    title_r.font.color.rgb = COLOR_PRIMARY; title_r.bold = True

    doc.add_paragraph()
    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_r = sub_p.add_run("UCI Adult / Census Income Dataset\n1994 U.S. Census Bureau Current Population Survey")
    sub_r.font.name = "Calibri"; sub_r.font.size = Pt(14); sub_r.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph()
    doc.add_paragraph()
    detail_p = doc.add_paragraph()
    detail_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    details = [
        "Prepared for Academic Submission",
        "Course: Data Analytics",
        "Dataset: UCI Adult Dataset (Kohavi & Becker, 1996)",
        "Dataset DOI: https://doi.org/10.24432/C5XW20",
        "Analysis Environment: R 4.6.1 with ggplot2",
        "Reproducible Code: R/08_week2_visualizations.R + R/09_week2_analysis.R",
        "Total Observations: 32,537 | Variables: 15",
    ]
    for d in details:
        dr = detail_p.add_run(d + "\n")
        dr.font.name = "Calibri"; dr.font.size = Pt(11.5); dr.font.color.rgb = COLOR_TEXT

    doc.add_page_break()

    # ─── TABLE OF CONTENTS ─────────────────────────────────────────────────
    add_heading(doc, "Table of Contents", level=1)
    toc_items = [
        ("1.", "Introduction and Dataset Overview", 3),
        ("2.", "Connection to Week 1 and Data Preparation", 3),
        ("3.", "Visualization Design Strategy", 3),
        ("4.", "Visualization 1 — Income Distribution", 3),
        ("5.", "Visualization 2 — Age Distribution", 3),
        ("6.", "Visualization 3 — Education Distribution", 3),
        ("7.", "Visualization 4 — Education vs Income", 3),
        ("8.", "Visualization 5 — Workclass vs Income", 3),
        ("9.", "Visualization 6 — Age vs Income", 3),
        ("10.", "Visualization 7 — Hours per Week Distribution", 3),
        ("11.", "Visualization 8 — Hours per Week vs Income", 3),
        ("12.", "Visualization 9 — Age vs Hours per Week (Scatter)", 3),
        ("13.", "Visualization 10 — Capital Gain", 3),
        ("14.", "Visualization 11 — Correlation Heatmap", 3),
        ("15.", "Visualization 12 — Creative: Occupation vs Income", 3),
        ("16.", "Line Chart Design Decision", 3),
        ("17.", "Evidence-Based Insights (11 Findings)", 3),
        ("18.", "Non-Technical Communication Summary", 3),
        ("19.", "Limitations", 3),
        ("20.", "Conclusion", 3),
        ("21.", "References", 3),
        ("Appendix", "Complete Week 2 R Code", 3),
    ]
    for num, title, _ in toc_items:
        tp = doc.add_paragraph()
        tp.paragraph_format.space_after = Pt(2)
        tr = tp.add_run(f"  {num}   {title}")
        tr.font.name = "Calibri"; tr.font.size = Pt(11); tr.font.color.rgb = COLOR_TEXT
    doc.add_page_break()

    # ─── 1. INTRODUCTION ───────────────────────────────────────────────────
    add_heading(doc, "1. Introduction and Dataset Overview", level=1)
    add_para(doc, text=(
        "This report constitutes the Week 2 submission for the Data Analytics "
        "course assignment titled 'Data Visualization and Insight Communication Using R'. "
        "Week 2 directly extends the Week 1 pipeline — which performed data cleaning, "
        "missing value imputation, outlier analysis, normalization, and exploratory data "
        "analysis — by producing a comprehensive suite of publication-quality visualizations "
        "and deriving evidence-based insights from the cleaned dataset."
    ))
    add_para(doc, text=(
        "The analysis uses the UCI Adult / Census Income Dataset (Kohavi & Becker, 1996), "
        "drawn from the 1994 U.S. Census Bureau Current Population Survey (CPS). The "
        "target variable distinguishes whether an individual's annual income exceeds or "
        "does not exceed $50,000. After Week 1 cleaning (mode imputation of missing values, "
        "deduplication, and factor encoding), the analysis-ready dataset contains "
        "32,537 observations across 15 variables: 6 continuous and 9 categorical."
    ))
    add_callout(doc, (
        "Dataset Citation: Kohavi, R., & Becker, B. (1996). Adult Dataset. "
        "UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20"
    ))

    add_heading(doc, "Dataset Variable Reference", level=2)
    headers = ["Variable", "Type", "Description"]
    rows = [
        ("age", "Continuous", "Age of individual (17–90 years)"),
        ("workclass", "Categorical (8 levels)", "Employment sector (Private, Government, etc.)"),
        ("fnlwgt", "Continuous", "Census sampling weight (survey design variable)"),
        ("education", "Ordinal (16 levels)", "Highest educational credential"),
        ("education_num", "Continuous", "Years of education (1–16)"),
        ("marital_status", "Categorical (7 levels)", "Marital status"),
        ("occupation", "Categorical (14 levels)", "Occupational category"),
        ("relationship", "Categorical (6 levels)", "Household relationship role"),
        ("race", "Categorical (5 levels)", "Racial classification"),
        ("sex", "Binary", "Sex (Male / Female)"),
        ("capital_gain", "Continuous", "Investment capital gain in USD"),
        ("capital_loss", "Continuous", "Investment capital loss in USD"),
        ("hours_per_week", "Continuous", "Weekly hours worked (1–99)"),
        ("native_country", "Categorical (41 levels)", "Country of birth"),
        ("income", "Binary Target", "Annual income: <=50K or >50K"),
    ]
    table = doc.add_table(rows=len(rows)+1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)
    for i, hdr in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_background(cell, "1B365D")
        p = cell.paragraphs[0]
        r = p.add_run(hdr)
        r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.color.rgb = RGBColor(255,255,255); r.bold = True
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = table.cell(ri+1, ci)
            if ri % 2 == 0: set_cell_background(cell, "F8F9FA")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = COLOR_TEXT
    doc.add_paragraph()
    doc.add_page_break()

    # ─── 2. CONNECTION TO WEEK 1 ───────────────────────────────────────────
    add_heading(doc, "2. Connection to Week 1 and Data Preparation", level=1)
    add_para(doc, text=(
        "Week 2 builds directly on the cleaned and preprocessed dataset produced "
        "during Week 1. No modifications were made to the original raw data files "
        "(data/original/adult.data). The complete Week 1 analytical pipeline remains "
        "intact and independently reproducible via run_all.R."
    ))
    add_para(doc, bold_prefix="Starting Dataset: ", text=(
        "Week 2 loads adult_cleaned.rds from the outputs/ directory — the same "
        "RDS file produced by Script 03 (03_cleaning.R) and used through Scripts "
        "04–07 in Week 1."
    ))
    add_heading(doc, "Data Preparation Notes for Visualization", level=2)
    prep_items = [
        "Income factor levels confirmed: \"<=50K\" and \">50K\" (no recoding needed).",
        "Education was already sorted as an Ordered Factor across 16 levels.",
        "All character whitespace was stripped during Week 1 import (strip.white = TRUE).",
        "Capital gain zero-values were explicitly handled: zero observations were "
        "excluded before log10 transformation to prevent undefined log(0) values.",
        "A random subsample (n = 4,000) was used for the scatter plot to mitigate "
        "overplotting while preserving representativeness (set.seed(42) for reproducibility).",
        "No imputation, normalization, or dummy encoding was required for visualization "
        "(these were already applied during Week 1 when needed).",
    ]
    for item in prep_items:
        add_bullet(doc, item)
    doc.add_paragraph()
    doc.add_page_break()

    # ─── 3. VISUALIZATION DESIGN STRATEGY ─────────────────────────────────
    add_heading(doc, "3. Visualization Design Strategy", level=1)
    add_para(doc, text=(
        "All Week 2 visualizations were created using ggplot2 (Wickham, 2016) with "
        "a custom academic theme (theme_academic) designed for publication-quality "
        "output at 300 DPI. Chart types were selected based on the data type, "
        "analytical question, and audience readability principles."
    ))

    add_heading(doc, "Chart Type Selection Rationale", level=2)
    strategy_table_data = [
        ("Bar Chart", "Nominal/Ordinal categorical frequency", "Income dist., Workclass/Income, Occupation/Income"),
        ("Histogram", "Continuous variable distribution", "Age, Hours per week, Capital gain"),
        ("Violin + Boxplot", "Continuous variable comparison across groups", "Age vs Income, Hours vs Income"),
        ("Scatter Plot", "Bivariate relationship: two continuous variables", "Age vs Hours per Week"),
        ("Proportional Stacked Bar", "Category composition comparison across groups", "Education×Income, Workclass×Income, Occupation×Income"),
        ("Heatmap (Correlation)", "Symmetric matrix of pairwise statistics", "Correlation matrix"),
        ("Ordered Cohort Line", "Trend across ordered categorical axis", "Age cohort income rate (Figure 13)"),
    ]
    headers_s = ["Chart Type", "Best Suited For", "Used In"]
    t_s = doc.add_table(rows=len(strategy_table_data)+1, cols=3)
    t_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_s)
    for i, hdr in enumerate(headers_s):
        cell = t_s.cell(0, i)
        set_cell_background(cell, "1B365D")
        p = cell.paragraphs[0]
        r = p.add_run(hdr)
        r.font.name = "Calibri"; r.font.size = Pt(10.5); r.font.color.rgb = RGBColor(255,255,255); r.bold = True
    for ri, rd in enumerate(strategy_table_data):
        for ci, val in enumerate(rd):
            cell = t_s.cell(ri+1, ci)
            if ri % 2 == 0: set_cell_background(cell, "F8F9FA")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Calibri"; r.font.size = Pt(10); r.font.color.rgb = COLOR_TEXT
    doc.add_paragraph()

    add_heading(doc, "Universal Design Principles Applied", level=2)
    design_items = [
        "300 DPI output saved via ggsave() for all Week 2 charts.",
        "Consistent two-color palette: Navy (#2B5C8F) for <=50K, Coral Red (#D9534F) for >50K.",
        "Clear titles, descriptive axis labels, and source captions on every chart.",
        "No 3D charts — all visualizations are 2D to prevent perceptual distortion.",
        "No truncated or misleading y-axes — all bar charts start at zero.",
        "Log-scale x-axis used only for capital gain, with explicit disclosure in subtitle.",
        "Transparency (alpha) applied to scatter points to handle overplotting.",
        "Summary statistics (mean diamonds, median lines) overlaid on distributional charts.",
    ]
    for item in design_items:
        add_bullet(doc, item)
    doc.add_page_break()

    # ─── VISUALIZATIONS 1–12 ───────────────────────────────────────────────
    for viz in VIZUALISATIONS:
        add_heading(doc, f"Visualization {viz['num']} — {viz['title']}", level=1)

        add_heading(doc, "Purpose", level=3)
        add_para(doc, viz["purpose"])

        add_heading(doc, "Why This Chart?", level=3)
        add_para(doc, viz["why_chart"])

        add_heading(doc, "R Code", level=3)
        add_code_block(doc, viz["code_snippet"])

        add_heading(doc, "Output", level=3)
        add_figure(doc, viz["png"], viz["figure"])

        add_heading(doc, "Interpretation", level=3)
        add_para(doc, viz["interpretation"])

        add_heading(doc, "Key Insight", level=3)
        add_callout(doc, viz["insight"])

        doc.add_page_break()

    # ─── LINE CHART DECISION ──────────────────────────────────────────────
    add_heading(doc, "Line Chart Design Decision", level=1)
    add_para(doc, text=(
        "The Week 2 assignment specification mentions line charts as one of the "
        "required visualization types. The following decision-making process was "
        "applied rigorously to this dataset:"
    ))
    add_callout(doc, (
        "DESIGN DECISION: A conventional time-series line chart was NOT produced "
        "in this report because the UCI Adult Dataset (1994 U.S. Census CPS) "
        "is a single-wave cross-sectional survey. It contains NO temporal variable "
        "— no year, month, date, or time-series identifier is present in any of "
        "the 15 variables. Drawing a line chart along an arbitrary or fabricated "
        "time axis would produce a misleading visualization that implies temporal "
        "change when no time dimension exists in the data."
    ), bg="FFF3CD")
    add_para(doc, text=(
        "However, an analytically justified ordered-category trend visualization "
        "was produced as Figure 13 (Supplementary: Age Cohort Income Trend). "
        "This uses synthetic cross-sectional age brackets (17–25, 26–35, 36–45, "
        "46–55, 56–65, 66+) as an ordered categorical X-axis, connected by a line "
        "to show the trend across life-cycle stages. This is clearly labelled as "
        "a COHORT COMPARISON across age brackets, not a longitudinal time series."
    ))
    add_figure(doc, "week2_13_age_cohort_income_trend.png",
               "Figure 13. Life-Cycle Cohort Trend: High-Income Rate Across Age Brackets (Cross-Sectional, Not Longitudinal)")
    add_para(doc, text=(
        "Figure 13 reveals an inverted U-curve: the proportion of high-income "
        "earners rises from 10.4% in the youngest cohort (17–25) to peak at "
        "40.0% in the 46–55 bracket, then declines to 21.9% in the 66+ cohort "
        "as retirees return to part-time or reduced-income arrangements. This "
        "pattern is consistent with career lifecycle theory, though the cross-sectional "
        "design cannot separate age effects from cohort or period effects."
    ))
    doc.add_page_break()

    # ─── INSIGHTS ─────────────────────────────────────────────────────────
    add_heading(doc, "Evidence-Based Insights", level=1)
    add_callout(doc, (
        "All quantitative values stated below are derived from actual computation on "
        "the cleaned dataset (N = 32,537). No statistics have been estimated or fabricated. "
        "Causal language is deliberately avoided throughout."
    ))

    insights = [
        {
            "num": 1,
            "finding": "The dataset exhibits severe class imbalance: 24,698 individuals (75.91%) earn <=50K, while 7,839 (24.09%) earn >50K — a ratio of 3.15:1.",
            "evidence": "Figure 1 (Income Distribution Bar Chart); exact count computation.",
            "interpretation": "The majority of 1994 U.S. CPS survey respondents earned at or below $50,000 annually, consistent with the broad wage structure of the early 1990s U.S. economy.",
            "caution": "This distribution reflects the 1994 U.S. population and should not be applied to present-day income distributions.",
        },
        {
            "num": 2,
            "finding": "Workers in the >$50K category are systematically older: median age 44 years versus 34 years for <=50K earners — a 10-year median gap.",
            "evidence": "Figure 6 (Violin + Boxplot: Age vs Income); tapply(adult$age, adult$income, median).",
            "interpretation": "Older workers are more likely to appear in the high-income category, consistent with career accumulation of experience and seniority.",
            "caution": "Age and income are associated but this does not prove that aging causes higher income. Occupation, education, and hours worked are simultaneously associated.",
        },
        {
            "num": 3,
            "finding": "Education shows a monotonically increasing association with high income: from 0% at Preschool to 41.5% at Bachelors, 55.7% at Masters, and 74.1% at Doctorate.",
            "evidence": "Figure 4 (Proportional Stacked Bar: Education vs Income); group_by(education) summarise.",
            "interpretation": "Advanced educational credentials are associated with substantially higher observed rates of high income in this dataset.",
            "caution": "This is an observational association. Confounders including age, occupational selection, and pre-existing socioeconomic conditions are not controlled for.",
        },
        {
            "num": 4,
            "finding": "Nearly half the workforce (46.73%, N=15,204) works exactly 40 hours per week, demonstrating strong institutional anchoring to the statutory full-time workweek.",
            "evidence": "Figure 7 (Hours per Week Histogram); sum(adult$hours_per_week == 40).",
            "interpretation": "The 40-hour full-time norm dominates U.S. workforce structure. Employers and employees coordinate on this institutional standard.",
            "caution": "The spike at 40 hours may partly reflect rounding or reporting bias — respondents may round to 40 even when actual hours differ slightly.",
        },
        {
            "num": 5,
            "finding": "Higher earners work substantially more hours on average: mean 45.5 hrs/week for >50K versus 38.8 hrs/week for <=50K; Q3 extends to 50 hours for >50K vs 40 hours for <=50K.",
            "evidence": "Figure 8 (Hours per Week vs Income Violin+Boxplot); tapply(adult$hours_per_week, adult$income, mean).",
            "interpretation": "High-income workers are more likely to work extended hours, consistent with salaried professional roles and incentive structures rewarding effort with higher pay.",
            "caution": "Causality is unclear: high income may encourage more work, or more work may lead to higher income, or both may reflect occupational type as a third variable.",
        },
        {
            "num": 6,
            "finding": "Capital gain is dominated by zero values (91.7% of the population). Among the 8.3% with positive gains, the distribution spans orders of magnitude ($114 to $99,999) with a top-code at $99,999 affecting 159 individuals.",
            "evidence": "Figure 10 (Capital Gain Log-Scale Histogram); sum(adult$capital_gain == 0).",
            "interpretation": "Investment income is concentrated among a small minority of the workforce. The vast majority of workers rely exclusively on wage and salary income.",
            "caution": "The top-code ceiling at $99,999 is a data censoring artifact. The true right tail of capital gains is unknown.",
        },
        {
            "num": 7,
            "finding": "Self-Employed Incorporated workers have the highest observed high-income proportion (55.7%), compared to Private sector employees (21.0%).",
            "evidence": "Figure 5 (Workclass vs Income Proportional Bar); group_by(workclass) summarise.",
            "interpretation": "Self-employment with incorporated status is associated with substantially higher income rates, likely reflecting business ownership and revenue distribution arrangements.",
            "caution": "Workclass categories differ enormously in size (Private: N=24,509; Self-emp-inc: N=1,116). Proportions are comparable but sample sizes affect precision.",
        },
        {
            "num": 8,
            "finding": "Occupational stratification is dramatic: Exec-managerial (48.4% high income) and Prof-specialty (34.3%) contrast sharply with Other-service (4.2%) and Priv-house-serv (0.7%).",
            "evidence": "Figure 12 (Creative: Occupation vs Income Proportional Bar); group_by(occupation) summarise.",
            "interpretation": "Occupation type is the single strongest observable categorical predictor of income category in this dataset, reflecting the labour market's occupational wage hierarchy.",
            "caution": "Occupation and education are correlated — the effect of occupation cannot be fully separated from the effect of educational attainment without multivariate analysis.",
        },
        {
            "num": 9,
            "finding": "All pairwise Pearson correlations between the six continuous variables are weak (all |r| < 0.15). The strongest positive correlation is education_num vs hours_per_week (r = 0.148).",
            "evidence": "Figure 11 (Correlation Heatmap); cor(adult[, num_cols]).",
            "interpretation": "The continuous features are largely independent of each other in linear terms, which is favorable for multivariate modeling. The education–hours association is consistent with salaried professional employment norms.",
            "caution": "Pearson correlation measures only LINEAR association. Non-linear dependencies would not be captured. Correlation does NOT imply causation.",
        },
        {
            "num": 10,
            "finding": "High-income earners are older across the whole age range: the >50K group IQR (36–51) is entirely above the lower half of the <=50K IQR (25–46).",
            "evidence": "Figure 6 (Age vs Income Violin+Boxplot); tapply(adult$age, adult$income, quantile).",
            "interpretation": "The distributional separation between income groups in age space is substantial. The entire middle 50% of >50K workers (age 36–51) overlaps only with the upper half of the <=50K group.",
            "caution": "This cross-sectional pattern may conflate age with birth cohort, career timing, and generational economic conditions.",
        },
        {
            "num": 11,
            "finding": "The HS-grad and Some-college categories jointly account for 54.6% of the workforce but only 15.9% and 19.0% of their respective members earn >50K — substantially below the 24.1% overall rate for advanced-degree holders.",
            "evidence": "Figure 3 (Education Distribution) and Figure 4 (Education vs Income); group computation.",
            "interpretation": "The modal qualification level of the 1994 workforce (high school diploma or some college) is associated with substantially below-average rates of high income, highlighting the economic premium on post-secondary degrees.",
            "caution": "These are observed proportions from a 1994 cross-sectional survey. Degree premia and workforce composition have changed substantially since then.",
        },
    ]

    for ins in insights:
        add_heading(doc, f"Insight {ins['num']}", level=2)
        add_insight_box(doc, "Finding:", ins["finding"])
        add_insight_box(doc, "Evidence:", ins["evidence"], bg="EFF8FF")
        add_insight_box(doc, "Interpretation:", ins["interpretation"])
        add_insight_box(doc, "Caution:", ins["caution"], bg="FFF8E7")

    doc.add_page_break()

    # ─── NON-TECHNICAL SUMMARY ─────────────────────────────────────────────
    add_heading(doc, "Non-Technical Communication Summary", level=1)
    add_para(doc, text=(
        "For readers without a statistical background, the following plain-language "
        "summary communicates the key findings from all 12 visualizations:"
    ))

    plain_items = [
        "Most people in this dataset (about 3 in 4) earn $50,000 or less per year.",
        "Most workers are in their 30s and 40s. Younger people (under 30) are less likely to earn high incomes.",
        "Workers with higher university degrees are more likely to be in the higher income group.",
        "Almost half the workers in this dataset work exactly 40 hours a week — this is the normal full-time working week.",
        "People in higher-paying occupations (like managers and professionals) are much more likely to be high earners than people in service jobs.",
        "Only about 1 in 12 workers reports any investment income at all. Those who do vary enormously — from a few hundred dollars to nearly $100,000.",
        "People who work for themselves (self-employed, incorporated) tend to have higher income rates than private sector workers.",
        "None of the mathematical measures of relationship (correlation) between the numerical variables is particularly strong.",
        "IMPORTANT REMINDER: These are patterns observed in a 30-year-old survey. The data shows what was true in 1994 and cannot tell us what is true today or why.",
    ]
    for item in plain_items:
        add_bullet(doc, item)

    doc.add_page_break()

    # ─── LIMITATIONS ──────────────────────────────────────────────────────
    add_heading(doc, "Limitations", level=1)
    limitations = [
        "Temporal Currency: The dataset reflects the 1994 U.S. Census population. Economic conditions, wage levels, occupational composition, and income distributions have changed substantially over three decades. Results should not be generalized to contemporary conditions.",
        "Cross-Sectional Design: The dataset captures a single point in time. Longitudinal causal claims (e.g., that education causes income growth over time) cannot be made from this data.",
        "Income Top-Coding: The >50K category is a binary indicator, not a precise income measurement. The income variable does not distinguish between $51,000 and $1,000,000. Similarly, capital gain is top-coded at $99,999.",
        "Missing Data Resolution: Week 1 resolved 4,262 missing values (~13%) using mode imputation. Mode imputation introduces artificial modal concentration and reduces variability. Any analysis of workclass, occupation, or native_country should acknowledge this.",
        "Sampling Weights Not Applied: The fnlwgt variable represents census sampling weights, which are needed to produce nationally representative estimates. This analysis does not apply these weights, so results are unweighted and may not represent the full U.S. population.",
        "Observational Associations: All observed relationships between variables are associational, not causal. Confounding variables are present throughout the dataset. Multivariate regression or causal inference methods would be needed to isolate any single variable's effect.",
        "Binary Income Variable: The binary income threshold ($50K) was meaningful in 1994 but its real purchasing power in 2024 is approximately $102,000 due to inflation. Comparisons to present-day income statistics require this adjustment.",
    ]
    for i, lim in enumerate(limitations, 1):
        colon_idx = lim.index(":")
        add_para(doc, bold_prefix=f"{i}. {lim[:colon_idx]}: ", text=lim[colon_idx+2:])

    doc.add_page_break()

    # ─── CONCLUSION ────────────────────────────────────────────────────────
    add_heading(doc, "Conclusion", level=1)
    add_para(doc, text=(
        "This Week 2 report has presented a comprehensive data visualization and "
        "insight communication analysis of the UCI Adult / Census Income Dataset. "
        "Twelve primary visualizations (Figures 1–12) and one supplementary cohort "
        "trend chart (Figure 13) were produced using ggplot2 in R, each selected on "
        "the basis of the data type and analytical question it was designed to address."
    ))
    add_para(doc, text=(
        "The analysis revealed several consistent patterns: income class imbalance "
        "(75.9% <=50K), a monotonic education–income association (0% to 74% high "
        "income from Preschool to Doctorate), dramatic occupational stratification "
        "(0.7% to 48.4% across occupations), an older age profile for high earners "
        "(median 44 vs 34 years), and strong institutional anchoring at the 40-hour "
        "workweek (46.7% of the workforce). Capital gain is concentrated among a "
        "small minority (8.3%) with extreme skewness requiring log-scale treatment."
    ))
    add_para(doc, text=(
        "All insights are grounded in actual computed statistics from the dataset. "
        "Causal language was avoided throughout, and limitations of the cross-sectional, "
        "30-year-old, weighted survey design were explicitly acknowledged. "
        "The Week 1 pipeline remains fully intact and reproducible alongside this "
        "Week 2 extension within the same GitHub repository."
    ))
    doc.add_page_break()

    # ─── REFERENCES ────────────────────────────────────────────────────────
    add_heading(doc, "References", level=1)
    refs = [
        "Kohavi, R., & Becker, B. (1996). Adult Dataset. UCI Machine Learning Repository. https://doi.org/10.24432/C5XW20",
        "Wickham, H. (2016). ggplot2: Elegant Graphics for Data Analysis (2nd ed.). Springer. https://ggplot2.tidyverse.org",
        "Wickham, H., François, R., Henry, L., & Müller, K. (2023). dplyr: A Grammar of Data Manipulation. R package version 1.1.x. https://dplyr.tidyverse.org",
        "Wickham, H., & Girlich, M. (2023). tidyr: Tidy Messy Data. R package version 1.3.x. https://tidyr.tidyverse.org",
        "Wei, T., & Simko, V. (2021). corrplot: Visualization of a Correlation Matrix. R package version 0.92. https://CRAN.R-project.org/package=corrplot",
        "Wickham, H. (2023). scales: Scale Functions for Visualization. R package version 1.3.x. https://scales.r-lib.org",
        "Grolemund, G., & Wickham, H. (2017). R for Data Science. O'Reilly Media. https://r4ds.had.co.nz",
        "Tufte, E. R. (2001). The Visual Display of Quantitative Information (2nd ed.). Graphics Press.",
        "Cairo, A. (2016). The Truthful Art: Data, Charts, and Maps for Communication. New Riders.",
        "U.S. Census Bureau. (1994). Current Population Survey (CPS) — Annual Social and Economic Supplement. U.S. Department of Commerce.",
    ]
    for i, ref in enumerate(refs, 1):
        rp = doc.add_paragraph()
        rp.paragraph_format.space_after = Pt(4)
        rp.paragraph_format.first_line_indent = Inches(-0.3)
        rp.paragraph_format.left_indent = Inches(0.3)
        rr = rp.add_run(f"{i}. {ref}")
        rr.font.name = "Calibri"; rr.font.size = Pt(10.5); rr.font.color.rgb = COLOR_TEXT
    doc.add_page_break()

    # ─── APPENDIX: R CODE ─────────────────────────────────────────────────
    add_heading(doc, "Appendix: Complete Week 2 R Code", level=1)
    add_para(doc, text=(
        "The following sections present the complete, unabridged R source code used "
        "to generate all visualizations and analyses in this report. The code is "
        "organized into two scripts to maintain separation of concerns:"
    ))
    add_bullet(doc, "R/08_week2_visualizations.R — All 13 ggplot2 visualization figures")
    add_bullet(doc, "R/09_week2_analysis.R — All analytical computations and insights")
    doc.add_paragraph()

    add_heading(doc, "R/08_week2_visualizations.R", level=2)
    code_08 = read_r_script("08_week2_visualizations.R")
    # Add code in chunks to avoid extremely long code blocks
    MAX_BLOCK = 3000
    start = 0
    while start < len(code_08):
        chunk = code_08[start:start+MAX_BLOCK]
        add_code_block(doc, chunk)
        start += MAX_BLOCK

    add_heading(doc, "R/09_week2_analysis.R", level=2)
    code_09 = read_r_script("09_week2_analysis.R")
    start = 0
    while start < len(code_09):
        chunk = code_09[start:start+MAX_BLOCK]
        add_code_block(doc, chunk)
        start += MAX_BLOCK

    doc.save(REPORT_PATH)
    print(f"\nWeek 2 Report saved successfully:\n  {REPORT_PATH}")


if __name__ == "__main__":
    build_report()
