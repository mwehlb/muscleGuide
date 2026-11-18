import html
import math
import ssl
import certifi
import urllib.request
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Muscle Guide", page_icon="💪", layout="wide", initial_sidebar_state="collapsed")

IMAGE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"

# ---------- 0. Style (CSS makes the site look like a real website) ----------
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1250px; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
[data-testid="stSidebar"], [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] { display: none; }
footer { visibility: hidden; }

.brand { font-size: 24px; font-weight: 800; padding-top: 6px; background: linear-gradient(90deg, #34d399, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.page-title { font-size: 40px; font-weight: 800; line-height: 1.15; margin: 18px 0 6px 0; }
.page-sub { font-size: 17px; opacity: 0.75; margin-bottom: 18px; }

.panel { background: rgba(128, 128, 128, 0.09); border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 18px; padding: 22px 26px; }
.panel h2 { margin: 6px 0 12px 0; padding: 0; font-size: 30px; font-weight: 800; }
.panel p { margin: 0 0 10px 0; font-size: 16px; line-height: 1.55; }
.tag { display: inline-block; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #34d399; font-weight: 700; }
.mini-row { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
.mini { flex: 1; min-width: 110px; background: rgba(128, 128, 128, 0.12); border-radius: 14px; padding: 12px 14px; }
.mini b { display: block; font-size: 24px; font-weight: 800; }
.mini span { font-size: 12px; opacity: 0.75; }

.chip { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; margin: 0 6px 6px 0; background: rgba(128, 128, 128, 0.2); }
.ex-name { font-size: 20px; font-weight: 700; margin: 4px 0 8px 0; line-height: 1.25; }
.rank { display: inline-block; min-width: 28px; text-align: center; padding: 2px 8px; border-radius: 8px; background: linear-gradient(90deg, #34d399, #10b981); color: #06281d; font-weight: 800; font-size: 13px; margin-right: 8px; }
.meter-label { font-size: 12px; opacity: 0.75; margin: 6px 0 4px 0; }
.meter { height: 8px; background: rgba(128, 128, 128, 0.25); border-radius: 99px; overflow: hidden; margin-bottom: 12px; }
.meter div { height: 100%; background: linear-gradient(90deg, #34d399, #10b981); border-radius: 99px; }
.score-box { text-align: center; padding: 6px 0 10px 0; }
.score-box span { font-size: 12px; opacity: 0.75; }

.big-score { font-size: 56px; font-weight: 800; line-height: 1; background: linear-gradient(90deg, #34d399, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.step { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 10px; padding: 12px 16px; background: rgba(128, 128, 128, 0.09); border-radius: 12px; }
.step-num { flex: 0 0 30px; height: 30px; border-radius: 50%; background: linear-gradient(135deg, #34d399, #10b981); color: #06281d; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 14px; }
.step-text { line-height: 1.5; font-size: 15px; }
.section-title { font-size: 20px; font-weight: 800; margin: 26px 0 12px 0; }
.footer { text-align: center; opacity: 0.55; font-size: 13px; margin-top: 40px; }

.stat-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.stat-table th, .stat-table td { padding: 9px 12px; text-align: left; border-bottom: 1px solid rgba(128, 128, 128, 0.25); }
.stat-table th { color: #34d399; font-size: 13px; }
.columns-chart { width: 100%; table-layout: fixed; border-collapse: collapse; }
.columns-chart td { vertical-align: bottom; text-align: center; padding: 0 4px; }
.col-bar { width: 100%; border-radius: 8px 8px 0 0; background: linear-gradient(180deg, #34d399, #059669); min-height: 3px; }
.col-value { font-size: 12px; font-weight: 600; margin-bottom: 4px; }
.col-label { font-size: 12px; opacity: 0.75; margin-top: 6px; }
.range-row { display: flex; align-items: center; margin-bottom: 16px; }
.range-name { width: 34%; font-size: 14px; padding-right: 10px; }
.range-track { position: relative; flex: 1; height: 14px; background: rgba(128, 128, 128, 0.2); border-radius: 8px; }
.range-fill { position: absolute; top: 0; height: 100%; background: linear-gradient(90deg, #34d399, #10b981); border-radius: 8px; opacity: 0.6; }
.range-dot { position: absolute; top: -3px; width: 20px; height: 20px; margin-left: -10px; border-radius: 50%; background: #ffffff; border: 4px solid #10b981; box-sizing: border-box; }
.range-text { width: 22%; font-size: 12px; opacity: 0.8; padding-left: 12px; }
.heat { border-collapse: collapse; width: 100%; }
.heat td { text-align: center; height: 30px; font-size: 11px; font-weight: 600; border: 2px solid rgba(128, 128, 128, 0.08); }
.heat th.rowhead { text-align: right; padding-right: 10px; font-weight: 600; white-space: nowrap; font-size: 12px; }
.heat th.vert { height: 120px; vertical-align: bottom; padding-bottom: 6px; }
.heat th.vert span { writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; font-size: 12px; font-weight: 600; }
.verdict { border-left: 5px solid #22c55e; background: rgba(34, 197, 94, 0.12); padding: 14px 18px; border-radius: 12px; margin-top: 14px; font-size: 15px; line-height: 1.5; }
.clean-row { display: flex; gap: 16px; align-items: center; padding: 12px 18px; background: rgba(128, 128, 128, 0.09); border-radius: 12px; margin-bottom: 8px; }
.clean-num { min-width: 60px; text-align: center; font-weight: 800; font-size: 26px; background: linear-gradient(90deg, #34d399, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.clean-text { font-size: 14px; line-height: 1.5; }

[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 18px; }
[data-testid="stImage"] img { border-radius: 12px; }
.stButton button { border-radius: 12px; font-weight: 600; width: 100%; }
.stButton button[kind="primary"], .stButton button[data-testid="stBaseButton-primary"] { background: linear-gradient(90deg, #34d399, #10b981); color: #06281d; border: none; font-weight: 700; }
.stButton button[kind="secondary"], .stButton button[data-testid="stBaseButton-secondary"] { background: rgba(128, 128, 128, 0.12); border: 1px solid rgba(128, 128, 128, 0.3); }
.stButton button:hover { filter: brightness(1.12); }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ---------- 1. Words in two languages ----------
text = {
    "mn": {
        "title": "Фитнесийн булчингийн хөтөч",
        "intro": "Булчингаа сонгоод, түүнд зориулсан дасгалуудыг зурагтай нь хараарай. Бүх дасгал жинхэнэ өгөгдөл дээр суурилсан.",
        "hero_exercises": "дасгал",
        "hero_muscles": "булчингийн бүлэг",
        "hero_photos": "зураг",
        "filters": "Шүүлтүүр",
        "level": "Түвшин",
        "equipment": "Хэрэгсэл",
        "how_many": "Хэдэн дасгал харуулах вэ",
        "tab1": "Булчин сонгох",
        "tab2": "Өгөгдлийн шинжилгээ",
        "click": "Булчингаа сонго",
        "where": "Хаана байдаг вэ?",
        "use": "Юунд ажилладаг вэ?",
        "front": "Урд тал",
        "back": "Ар тал",
        "found": "Олдсон дасгал",
        "average": "Дундаж булчин",
        "best": "Хамгийн их",
        "muscles_word": " булчин",
        "chart_level": "Түвшнээр нь",
        "chart_equipment": "Хэрэгслээр нь",
        "top": "Шилдэг дасгалууд: ",
        "caption": "Хамгийн олон булчинг ажиллуулдаг дасгал эхэндээ байна. Дасгалын нэр, заавар англи хэлээр байгаа.",
        "level_word": "Түвшин:",
        "equipment_word": "Хэрэгсэл:",
        "worked": "Ажиллах булчингийн тоо:",
        "none": "Эдгээр шүүлтүүрээр дасгал олдсонгүй. Өөр түвшин эсвэл хэрэгсэл сонгоно уу.",
        "no_photo": "Зураг ачаалагдсангүй",
        "details": "Дэлгэрэнгүй харах",
        "start_pose": "Эхлэх байрлал",
        "end_pose": "Дуусах байрлал",
        "primary_word": "Гол ажиллах булчин",
        "secondary_word": "Туслах булчин",
        "legend": "Улаан = гол булчин, улбар шар = туслах булчин",
        "steps_word": "Хийх алхмууд (англиар)",
        "score_title": "Үр дүнтэй байдлын оноо",
        "score_a": "Энэ дасгал нийт дасгалын ",
        "score_b": "%-иас илүү олон булчинг ажиллуулдаг.",
        "unknown": "тодорхойгүй",
        "compare_title": "Бусад дасгалтай харьцуулалт",
        "this_exercise": "Энэ дасгал",
        "avg_same": "Дундаж: ",
        "avg_all": "Бүх дасгалын дундаж",
        "data1": "Булчин бүрт хэдэн дасгал байдаг вэ?",
        "data2": "Олон булчинтай дасгал ба нэг булчинтай дасгал",
        "data3": "Аль хэрэгсэлтэй дасгал хамгийн олон булчинг ажиллуулдаг вэ?",
        "finding": "Гол дүгнэлт",
        "ratio_a": "Олон булчинтай дасгал ",
        "ratio_b": " дахин олон булчинг ажиллуулдаг.",
        "avg_unit": "дундаж булчин",
        "note": "Энд \"үр дүнтэй\" гэдэг нь илүү олон булчинг ажиллуулах гэсэн үг. Өгөгдөлд булчин томрох үр дүн байхгүй тул аль дасгал булчинг илүү томруулахыг батлах боломжгүй.",
        "footer": "Өгөгдөл: free-exercise-db (нээлттэй эх сурвалж) · Дата сайенсийн төсөл",
        "nav_explorer": "Булчин судлах",
        "nav_analysis": "Өгөгдлийн шинжилгээ",
        "nav_about": "Төслийн тухай",
        "brand": "Булчингийн хөтөч",
        "back": "← Буцах",
        "also": "Мөн ажиллана:",
        "muscles_label": "булчин ажиллана",
        "page_title": "Булчингаа сонгоод, дасгалаа ол",
        "page_sub": "Баруун талаас булчингаа сонго. Зураг дээр тэр булчин улаанаар гарна, доор нь тохирох дасгалууд харагдана.",
        "about_goal_title": "Төслийн зорилго",
        "about_goal": "Олон хүн фитнесээр хичээллэхдээ булчингийн нэрийг ойлгодоггүй, аль дасгал хамгийн үр дүнтэй болохыг мэддэггүй. Энэ апп булчин бүрийг зураг болон монгол тайлбартай нь үзүүлж, дасгалуудыг жинхэнэ өгөгдлөөр харьцуулна.",
        "about_question_title": "Судалгааны асуулт",
        "about_question": "Аль дасгал хамгийн олон булчинг ажиллуулдаг вэ? Олон булчинтай (compound) дасгал нэг булчинтай (isolation) дасгалаас үнэхээр илүү олон булчинг ажиллуулдаг уу?",
        "about_data_title": "Өгөгдөл",
        "about_data": "free-exercise-db: 876 дасгалтай нээлттэй (public domain) өгөгдөл, GitHub дээр байдаг. Дасгал бүр нэр, түвшин, хэрэгсэл, булчин, заавар, зурагтай.",
        "about_columns_title": "Баганын тайлбар",
        "about_col_head": ["Багана", "Утга"],
        "about_columns": [
            ["name", "Дасгалын нэр"],
            ["force", "Хөдөлгөөний чиглэл (түлхэх, татах, барих)"],
            ["level", "Түвшин (эхлэгч, дунд, ахисан)"],
            ["mechanic", "Төрөл (олон булчинтай / нэг булчинтай)"],
            ["equipment", "Хэрэгсэл"],
            ["primaryMuscles", "Гол ажиллах булчингууд"],
            ["secondaryMuscles", "Туслах булчингууд"],
            ["instructions", "Хийх алхмууд"],
            ["category", "Ангилал (хүч, суналт, кардио ...)"],
            ["images", "Зургийн замууд"],
            ["id", "Дасгалын код"],
            ["muscles_count", "Ажиллах булчингийн тоо (миний нэмсэн шинэ багана)"],
        ],
        "about_method_title": "Арга зүй",
        "about_method": [
            "Өгөгдлийг уншиж, хоосон болон давхардсан утгыг олж цэвэрлэсэн.",
            "Шинэ багана muscles_count (дасгал бүрийн ажиллуулдаг булчингийн тоо) үүсгэсэн.",
            "Тайлбарлах шинжилгээ хийсэн: тархалт, дундаж, медиан.",
            "t-тестээр compound ба isolation дасгалыг харьцуулсан.",
            "Булчингийн хослолыг матрицаар тооцсон.",
            "Python, pandas, Streamlit ашиглан интерактив апп болгосон.",
        ],
        "about_results_title": "Үндсэн үр дүн",
        "about_res_a": "Олон булчинтай дасгал дунджаар ",
        "about_res_b": " булчин, нэг булчинтай дасгал ",
        "about_res_c": " булчинг ажиллуулдаг. Статистикийн шинжилгээг «Өгөгдлийн шинжилгээ» хэсгээс харна уу.",
        "about_limits_title": "Хязгаарлалт",
        "about_limits": "Өгөгдөлд булчин томрох, хүч нэмэгдэх үр дүн байхгүй. Иймээс «үр дүнтэй» гэдэг нь «илүү олон булчинг ажиллуулдаг» гэсэн утгатай. Дасгалын нэр, заавар англи хэлээр байгаа.",
        "about_tech_title": "Ашигласан технологи",
        "sub1": "Өгөгдлийн тойм",
        "sub2": "Харьцуулалт ба туршилт",
        "sub3": "Булчингийн хослол",
        "sub4": "Шилдэг дасгалууд",
        "ov_rows": "мөр (дасгал)",
        "ov_cols": "багана",
        "ov_avg": "дундаж ажиллах булчин",
        "clean_title": "Өгөгдөл цэвэрлэсэн алхмууд",
        "clean_note": "Жинхэнэ өгөгдөл хэзээ ч төгс байдаггүй. Эхлээд алдааг олж, дараа нь засдаг.",
        "clean1": ["Хэрэгсэл хоосон байсан", "«Бусад» гэж бөглөсөн"],
        "clean2": ["Дасгалын төрөл (compound / isolation) хоосон байсан", "Харьцуулалтад оруулаагүй"],
        "clean3": ["Хөдөлгөөний чиглэл хоосон байсан", "«Тодорхойгүй» гэж тэмдэглэсэн"],
        "clean4": ["Нэг булчин хоёр удаа бүртгэгдсэн байсан", "Нэг удаа тоолсон"],
        "clean5": ["Зураггүй дасгал", "Зургийн оронд мессеж харуулсан"],
        "hist_title": "Нэг дасгал хэдэн булчинг ажиллуулдаг вэ?",
        "hist_note": "Тэнхлэг дээр: ажиллах булчингийн тоо. Баганын өндөр: тийм дасгалын тоо.",
        "mean_word": "Дундаж",
        "median_word": "Медиан",
        "mode_word": "Хамгийн түгээмэл",
        "max_word": "Хамгийн их",
        "min_word": "Хамгийн бага",
        "std_word": "Стандарт хазайлт",
        "count_word": "Тоо (n)",
        "hist_a": "Дасгалын ",
        "hist_b": "% нь 3 буюу түүнээс цөөн булчинг ажиллуулдаг. Олон булчинг ажиллуулдаг дасгал цөөхөн байна.",
        "hyp_title": "Таамаглал",
        "hyp_text": "Олон булчинтай (compound) дасгал нэг булчинтай (isolation) дасгалаас илүү олон булчинг ажиллуулдаг.",
        "stats_title": "Хоёр бүлгийн статистик",
        "range_title": "Хамгийн бага ба хамгийн их утгын хүрээ (цагаан цэг = дундаж)",
        "test_title": "Ялгаа санамсаргүй юу? (t-тест)",
        "t_word": "t утга",
        "p_word": "p утга",
        "d_word": "Ялгааны хэмжээ (Cohen's d)",
        "effect_large": "Ялгаа маш их",
        "effect_mid": "Ялгаа дунд зэрэг",
        "effect_small": "Ялгаа бага",
        "p_explain": "p утга 0.05-аас бага бол ялгаа азаар гарсан биш гэж үздэг.",
        "verdict_yes": "Таамаглал батлагдлаа: ялгаа санамсаргүй биш. Олон булчинтай дасгал үнэхээр илүү олон булчинг ажиллуулдаг.",
        "verdict_no": "Таамаглал батлагдсангүй: ялгаа санамсаргүй байж магадгүй.",
        "by_level": "Түвшин бүрийн дундаж булчингийн тоо",
        "by_muscle": "Аль булчингийн дасгал хамгийн олон булчинг ажиллуулдаг вэ?",
        "heat_title": "Аль булчингууд хамт ажилладаг вэ?",
        "heat_note": "Мөр = гол булчин, багана = туслах булчин. Тоо нь тухайн гол булчинтай дасгалуудын хэдэн хувьд тэр туслах булчин оролцдогийг харуулна.",
        "pairs_title": "Хамгийн түгээмэл хослолууд",
        "top_title": "Хамгийн олон булчинг ажиллуулдаг 10 дасгал",
        "top_note": "Зүүн талын шүүлтүүр (түвшин, хэрэгсэл) энд бас ажиллана.",
        "levels": {"all": "Бүгд", "beginner": "Эхлэгч", "intermediate": "Дунд", "expert": "Ахисан"},
        "equipments": {
            "all": "Бүгд",
            "body only": "Биеийн жингээр",
            "dumbbell": "Гантель",
            "barbell": "Штанг",
            "machine": "Тренажер",
            "cable": "Кабель тренажер",
            "kettlebells": "Гир (kettlebell)",
            "bands": "Резинэн оосор",
            "medicine ball": "Хүнд бөмбөг",
            "exercise ball": "Фитбол",
            "e-z curl bar": "EZ штанг",
            "foam roll": "Хөөсөн бул",
            "other": "Бусад",
        },
        "mechanics": {
            "compound": "Олон булчинтай (compound)",
            "isolation": "Нэг булчинтай (isolation)",
        },
        "forces": {"push": "Түлхэх", "pull": "Татах", "static": "Барьж зогсох"},
        "categories": {
            "strength": "Хүчний дасгал",
            "stretching": "Суналт",
            "cardio": "Кардио",
            "plyometrics": "Үсрэлтийн дасгал",
            "powerlifting": "Пауэрлифтинг",
            "olympic weightlifting": "Олимпийн өргөлт",
            "strongman": "Стронгмен",
        },
    },
    "en": {
        "title": "Gym Muscle Explorer",
        "intro": "Pick a muscle and see the exercises for it, with pictures. Everything is built on real data.",
        "hero_exercises": "exercises",
        "hero_muscles": "muscle groups",
        "hero_photos": "photos",
        "filters": "Filters",
        "level": "Level",
        "equipment": "Equipment",
        "how_many": "How many exercises to show",
        "tab1": "Muscle explorer",
        "tab2": "Data analysis",
        "click": "Click a muscle",
        "where": "Where is it?",
        "use": "What does it do?",
        "front": "Front",
        "back": "Back",
        "found": "Exercises found",
        "average": "Average muscles",
        "best": "Best",
        "muscles_word": " muscles",
        "chart_level": "By level",
        "chart_equipment": "By equipment",
        "top": "Top exercises for ",
        "caption": "Exercises that work the most muscles are first.",
        "level_word": "Level:",
        "equipment_word": "Equipment:",
        "worked": "Muscles worked:",
        "none": "No exercises with these filters. Try another level or equipment.",
        "no_photo": "Photo did not load",
        "details": "See details",
        "start_pose": "Start position",
        "end_pose": "End position",
        "primary_word": "Main muscles",
        "secondary_word": "Helper muscles",
        "legend": "Red = main muscle, orange = helper muscle",
        "steps_word": "Steps",
        "score_title": "Efficiency score",
        "score_a": "This exercise works more muscles than ",
        "score_b": "% of all exercises.",
        "unknown": "unknown",
        "compare_title": "Compared with other exercises",
        "this_exercise": "This exercise",
        "avg_same": "Average: ",
        "avg_all": "Average of all exercises",
        "data1": "How many exercises does each muscle have?",
        "data2": "Compound vs isolation exercises",
        "data3": "Which equipment works the most muscles?",
        "finding": "Key finding",
        "ratio_a": "Compound exercises work ",
        "ratio_b": " times more muscles than isolation exercises.",
        "avg_unit": "muscles on average",
        "note": "Here, efficient means working more muscles. The data has no muscle growth results, so it cannot prove which exercise builds more muscle.",
        "footer": "Data: free-exercise-db (open source) · Data science project",
        "nav_explorer": "Muscle explorer",
        "nav_analysis": "Data analysis",
        "nav_about": "About",
        "brand": "Muscle Guide",
        "back": "← Back",
        "also": "Also works:",
        "muscles_label": "muscles worked",
        "page_title": "Pick a muscle, find your exercise",
        "page_sub": "Choose a muscle on the right. It turns red on the body picture, and the matching exercises appear below.",
        "about_goal_title": "Project goal",
        "about_goal": "Many people in the gym do not understand muscle names, and they do not know which exercises are the most efficient. This app shows every muscle with a picture and a simple explanation, and it compares exercises with real data.",
        "about_question_title": "Research question",
        "about_question": "Which exercises work the most muscles? Do compound exercises really work more muscles than isolation exercises?",
        "about_data_title": "Data",
        "about_data": "free-exercise-db: an open (public domain) dataset of 876 exercises on GitHub. Every exercise has a name, level, equipment, muscles, instructions, and photos.",
        "about_columns_title": "Column descriptions",
        "about_col_head": ["Column", "Meaning"],
        "about_columns": [
            ["name", "Exercise name"],
            ["force", "Movement direction (push, pull, hold)"],
            ["level", "Level (beginner, intermediate, expert)"],
            ["mechanic", "Type (compound / isolation)"],
            ["equipment", "Equipment"],
            ["primaryMuscles", "Main muscles worked"],
            ["secondaryMuscles", "Helper muscles"],
            ["instructions", "Steps to do the exercise"],
            ["category", "Category (strength, stretching, cardio ...)"],
            ["images", "Photo paths"],
            ["id", "Exercise code"],
            ["muscles_count", "Number of muscles worked (a new column I made)"],
        ],
        "about_method_title": "Method",
        "about_method": [
            "Loaded the data and found and cleaned empty and duplicated values.",
            "Made a new column, muscles_count, with the number of muscles each exercise works.",
            "Explored the data: distribution, mean, median.",
            "Compared compound and isolation exercises with a t-test.",
            "Calculated which muscles work together with a matrix.",
            "Built an interactive app with Python, pandas, and Streamlit.",
        ],
        "about_results_title": "Main result",
        "about_res_a": "Compound exercises work ",
        "about_res_b": " muscles on average and isolation exercises work ",
        "about_res_c": ". See the Data analysis page for the statistical test.",
        "about_limits_title": "Limits",
        "about_limits": "The data has no muscle growth or strength results. So \"efficient\" here means \"works more muscles\". Exercise names and steps are in English.",
        "about_tech_title": "Technology",
        "sub1": "Data overview",
        "sub2": "Comparison & test",
        "sub3": "Muscle partners",
        "sub4": "Top exercises",
        "ov_rows": "rows (exercises)",
        "ov_cols": "columns",
        "ov_avg": "average muscles worked",
        "clean_title": "Data cleaning steps",
        "clean_note": "Real data is never perfect. First we find the problems, then we fix them.",
        "clean1": ["Equipment was empty", "Filled with \"other\""],
        "clean2": ["Exercise type (compound / isolation) was empty", "Left out of the comparison"],
        "clean3": ["Movement direction was empty", "Marked as unknown"],
        "clean4": ["Same muscle was listed twice", "Counted once"],
        "clean5": ["Exercises without photos", "Show a message instead"],
        "hist_title": "How many muscles does one exercise work?",
        "hist_note": "Bottom: number of muscles worked. Bar height: how many exercises.",
        "mean_word": "Mean",
        "median_word": "Median",
        "mode_word": "Most common",
        "max_word": "Maximum",
        "min_word": "Minimum",
        "std_word": "Std. deviation",
        "count_word": "Count (n)",
        "hist_a": "",
        "hist_b": "% of exercises work 3 muscles or fewer. Exercises that work many muscles are rare.",
        "hyp_title": "Hypothesis",
        "hyp_text": "Compound exercises work more muscles than isolation exercises.",
        "stats_title": "Statistics of the two groups",
        "range_title": "Range from minimum to maximum (white dot = mean)",
        "test_title": "Is the difference by chance? (t-test)",
        "t_word": "t value",
        "p_word": "p value",
        "d_word": "Effect size (Cohen's d)",
        "effect_large": "Very large difference",
        "effect_mid": "Medium difference",
        "effect_small": "Small difference",
        "p_explain": "If the p value is below 0.05, we say the difference is not luck.",
        "verdict_yes": "Hypothesis supported: the difference is not by chance. Compound exercises really work more muscles.",
        "verdict_no": "Hypothesis not supported: the difference may be by chance.",
        "by_level": "Average muscles worked by level",
        "by_muscle": "Which muscle group has the most efficient exercises?",
        "heat_title": "Which muscles work together?",
        "heat_note": "Row = main muscle, column = helper muscle. The number is the % of exercises of that main muscle that also use the helper muscle.",
        "pairs_title": "Most common pairs",
        "top_title": "Top 10 exercises that work the most muscles",
        "top_note": "The filters on the left (level, equipment) also work here.",
        "levels": {"all": "All", "beginner": "Beginner", "intermediate": "Intermediate", "expert": "Expert"},
        "equipments": {"all": "All"},
        "mechanics": {"compound": "Compound (many muscles)", "isolation": "Isolation (one muscle)"},
        "forces": {"push": "Push", "pull": "Pull", "static": "Hold"},
        "categories": {
            "strength": "Strength",
            "stretching": "Stretching",
            "cardio": "Cardio",
            "plyometrics": "Plyometrics",
            "powerlifting": "Powerlifting",
            "olympic weightlifting": "Olympic weightlifting",
            "strongman": "Strongman",
        },
    },
}

# For each muscle: [name, where it is, what it does]
muscle_info = {
    "mn": {
        "abdominals": ["Хэвлийн булчин", "Хэвлийн урд хэсэгт байдаг.", "Биеийг урагш нугалах, нурууг тогтвортой барихад тусална."],
        "abductors": ["Гуяны гадна талын булчин", "Гуяны гадна тал, ташааны хажууд байдаг.", "Хөлөө хажуу тийш өргөхөд ажиллана."],
        "adductors": ["Гуяны дотор талын булчин", "Гуяны дотор талд байдаг.", "Хоёр хөлөө биеийн голд нь шахан цуглуулахад ажиллана."],
        "biceps": ["Гарын урд булчин (бицепс)", "Мөр ба тохойн хооронд, гарын урд талд байдаг.", "Тохойгоо нугалж, юм өргөхөд ажиллана."],
        "calves": ["Шилбэний булчин (тугал)", "Өвдгөөс доош, шилбэний ар талд байдаг.", "Хөлийн хуруун дээр зогсох, гүйх, үсрэхэд ажиллана."],
        "chest": ["Цээжний булчин", "Цээжний урд талд байдаг.", "Юм түлхэх хөдөлгөөнд ажиллана (жишээ нь гар тулах)."],
        "forearms": ["Шууны булчин", "Тохой ба бугуйн хооронд байдаг.", "Юм атгах, барихад ажиллана."],
        "glutes": ["Өгзгийн булчин", "Өгзөгт, ташааны ар талд байдаг.", "Алхах, гүйх, сууж байгаад босоход ажиллана."],
        "hamstrings": ["Гуяны ар булчин", "Гуяны ар талд байдаг.", "Өвдгөө нугалахад ажиллана."],
        "lats": ["Нурууны өргөн булчин", "Нурууны хоёр хажуу, суганаас доош байдаг.", "Юм өөртөө татахад ажиллана (жишээ нь татлага)."],
        "lower back": ["Нурууны доод хэсгийн булчин", "Бүсэлхийн хэсэгт, ар талд байдаг.", "Нурууг тэнийлгэж, зөв байрлалд барина."],
        "middle back": ["Нурууны дунд хэсгийн булчин", "Хоёр мөрний ирний хооронд байдаг.", "Мөрөө ар тийш татаж, нуруугаа тэгшлэхэд ажиллана."],
        "neck": ["Хүзүүний булчин", "Хүзүүнд байдаг.", "Толгойг дэмжиж, хөдөлгөнө."],
        "quadriceps": ["Гуяны урд булчин", "Гуяны урд талд байдаг.", "Өвдгөө тэнийлгэх, суугаад босох, гүйхэд ажиллана."],
        "shoulders": ["Мөрний булчин", "Мөрний орчим, гарын дээд хэсэгт байдаг.", "Гараа дээш, хажуу тийш өргөхөд ажиллана."],
        "traps": ["Хүзүү, мөрний булчин (трапец)", "Хүзүүнээс мөр хүртэл, нурууны дээд хэсэгт байдаг.", "Мөрөө дээш хавчихад ажиллана."],
        "triceps": ["Гарын ар булчин (трицепс)", "Мөр ба тохойн хооронд, гарын ар талд байдаг.", "Тохойгоо тэнийлгэхэд ажиллана."],
    },
    "en": {
        "abdominals": ["Abs (abdominals)", "Front of your belly.", "Bends your body forward and keeps your back stable."],
        "abductors": ["Outer thigh (abductors)", "On the outside of your hips and thighs.", "Lifts your leg out to the side."],
        "adductors": ["Inner thigh (adductors)", "Inside of your thighs.", "Pulls your legs together."],
        "biceps": ["Biceps", "Front of your upper arm.", "Bends your elbow when you lift something."],
        "calves": ["Calves", "Back of your lower leg, below the knee.", "Helps you stand on your toes, run and jump."],
        "chest": ["Chest (pectorals)", "Front of your upper body.", "Pushes things away, like in a push-up."],
        "forearms": ["Forearms", "Between your elbow and wrist.", "Helps you grip and hold things."],
        "glutes": ["Glutes (buttocks)", "Your buttocks, at the back of your hips.", "Powers walking, running and standing up from a chair."],
        "hamstrings": ["Hamstrings", "Back of your thigh.", "Bends your knee."],
        "lats": ["Lats (side back)", "Sides of your back, under the armpits.", "Pulls things toward you, like in a pull-up."],
        "lower back": ["Lower back", "Around your waist, at the back.", "Keeps your spine straight and strong."],
        "middle back": ["Middle back", "Between your shoulder blades.", "Pulls your shoulders back and helps good posture."],
        "neck": ["Neck", "Your neck.", "Holds up and moves your head."],
        "quadriceps": ["Quads (quadriceps)", "Front of your thigh.", "Straightens your knee when you stand, squat or run."],
        "shoulders": ["Shoulders (deltoids)", "The round top of your arm.", "Lifts your arm up and to the side."],
        "traps": ["Traps (trapezius)", "From your neck to your shoulders and upper back.", "Shrugs your shoulders up."],
        "triceps": ["Triceps", "Back of your upper arm.", "Straightens your elbow."],
    },
}

muscle_short = {
    "mn": {
        "chest": "Цээж", "shoulders": "Мөр", "biceps": "Бицепс", "triceps": "Трицепс", "forearms": "Шуу",
        "abdominals": "Хэвлий", "traps": "Трапец", "lats": "Өргөн булчин", "middle back": "Нуруу (дунд)",
        "lower back": "Бүсэлхий", "neck": "Хүзүү", "glutes": "Өгзөг", "quadriceps": "Гуя (урд)",
        "hamstrings": "Гуя (ар)", "adductors": "Гуя (дотор)", "abductors": "Гуя (гадна)", "calves": "Шилбэ",
    },
    "en": {
        "chest": "Chest", "shoulders": "Shoulders", "biceps": "Biceps", "triceps": "Triceps", "forearms": "Forearms",
        "abdominals": "Abs", "traps": "Traps", "lats": "Lats", "middle back": "Mid back",
        "lower back": "Low back", "neck": "Neck", "glutes": "Glutes", "quadriceps": "Quads",
        "hamstrings": "Hamstrings", "adductors": "Inner thigh", "abductors": "Outer thigh", "calves": "Calves",
    },
}

# ---------- 2. Body picture (smooth shapes drawn with SVG) ----------
def smooth_shape(points):
    count = len(points)
    path = "M" + str(points[0][0]) + "," + str(points[0][1])
    for i in range(count):
        p0 = points[(i - 1) % count]
        p1 = points[i]
        p2 = points[(i + 1) % count]
        p3 = points[(i + 2) % count]
        c1x = round(p1[0] + (p2[0] - p0[0]) / 6, 1)
        c1y = round(p1[1] + (p2[1] - p0[1]) / 6, 1)
        c2x = round(p2[0] - (p3[0] - p1[0]) / 6, 1)
        c2y = round(p2[1] - (p3[1] - p1[1]) / 6, 1)
        path += "C" + str(c1x) + "," + str(c1y) + " " + str(c2x) + "," + str(c2y) + " " + str(p2[0]) + "," + str(p2[1])
    return path + "Z"


def mirror_points(points):
    mirrored = []
    for point in points:
        mirrored.append((210 - point[0], point[1]))
    return mirrored


def both_sides(points):
    return smooth_shape(points) + smooth_shape(mirror_points(points))


body_left = [(94, 68), (78, 74), (60, 80), (46, 90), (38, 110), (34, 140), (30, 172), (26, 204), (24, 228),
             (30, 241), (40, 238), (44, 216), (48, 190), (53, 160), (58, 132), (63, 116), (64, 140), (68, 170),
             (66, 196), (58, 214), (56, 250), (60, 290), (64, 320), (62, 350), (64, 380), (66, 404), (58, 420),
             (66, 431), (92, 431), (98, 418), (97, 404), (98, 380), (98, 350), (100, 320), (103, 280), (105, 236)]
body_right = mirror_points(body_left[1:])
body_points = list(body_left)
for index in range(len(body_right) - 1, -1, -1):
    body_points.append(body_right[index])
body_outline = smooth_shape(body_points)

shoulder_points = [(70, 78), (58, 76), (46, 86), (42, 102), (46, 116), (56, 114), (66, 102), (72, 90)]
upper_arm_points = [(46, 112), (40, 126), (38, 142), (42, 156), (50, 156), (56, 142), (58, 126), (54, 114)]
forearm_points = [(40, 164), (36, 180), (33, 200), (34, 218), (41, 220), (46, 204), (48, 184), (48, 166)]
abductor_points = [(66, 206), (60, 216), (58, 246), (60, 276), (65, 282), (68, 256), (68, 224)]
neck_points = [(95, 54), (115, 54), (118, 70), (105, 77), (92, 70)]

front_shapes = {
    "neck": smooth_shape(neck_points),
    "traps": both_sides([(92, 70), (78, 76), (70, 84), (84, 89), (96, 80)]),
    "shoulders": both_sides(shoulder_points),
    "chest": both_sides([(104, 92), (90, 88), (76, 90), (66, 100), (66, 112), (74, 124), (90, 129), (104, 122)]),
    "abdominals": smooth_shape([(96, 132), (114, 132), (118, 150), (118, 175), (113, 196), (105, 202), (97, 196), (92, 175), (92, 150)]),
    "biceps": both_sides(upper_arm_points),
    "forearms": both_sides(forearm_points),
    "abductors": both_sides(abductor_points),
    "quadriceps": both_sides([(90, 212), (78, 214), (68, 234), (66, 264), (70, 296), (80, 312), (88, 304), (92, 280), (93, 240)]),
    "adductors": both_sides([(94, 216), (104, 216), (104, 262), (100, 292), (95, 282), (93, 244)]),
    "calves": both_sides([(80, 326), (70, 336), (68, 358), (72, 384), (82, 392), (90, 378), (92, 350), (90, 332)]),
}

back_shapes = {
    "neck": smooth_shape(neck_points),
    "traps": smooth_shape([(105, 64), (120, 68), (136, 82), (128, 102), (116, 116), (105, 126), (94, 116), (82, 102), (74, 82), (90, 68)]),
    "shoulders": both_sides(shoulder_points),
    "lats": both_sides([(84, 108), (94, 124), (96, 150), (92, 172), (82, 168), (72, 150), (68, 124), (72, 110)]),
    "middle back": smooth_shape([(97, 120), (113, 120), (116, 136), (113, 150), (105, 154), (97, 150), (94, 136)]),
    "lower back": smooth_shape([(96, 154), (114, 154), (118, 172), (114, 192), (105, 196), (96, 192), (92, 172)]),
    "triceps": both_sides(upper_arm_points),
    "forearms": both_sides(forearm_points),
    "glutes": both_sides([(105, 198), (88, 196), (72, 206), (68, 224), (76, 240), (92, 242), (104, 232), (106, 214)]),
    "abductors": both_sides(abductor_points),
    "hamstrings": both_sides([(100, 246), (86, 246), (72, 254), (68, 278), (72, 306), (84, 316), (96, 308), (100, 280)]),
    "calves": both_sides([(82, 326), (70, 334), (66, 354), (70, 380), (80, 394), (92, 384), (94, 356), (90, 336)]),
}

abs_lines = "M105,136L105,198M96,150L114,150M95,166L115,166M96,182L114,182"

# ---------- 2. Body picture (dark style) ----------
svg_defs = (
    "<defs>"
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#232838"/><stop offset="1" stop-color="#131720"/></linearGradient>'
    '<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#323a50"/><stop offset="1" stop-color="#262d3f"/></linearGradient>'
    '<linearGradient id="muscle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a5772"/><stop offset="1" stop-color="#3b4660"/></linearGradient>'
    '<linearGradient id="hot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a6b"/><stop offset="1" stop-color="#d9332a"/></linearGradient>'
    '<linearGradient id="warm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffc46b"/><stop offset="1" stop-color="#f08c00"/></linearGradient>'
    "</defs>"
)


def draw_body(shapes, primary_list, secondary_list, is_front):
    body = '<ellipse cx="105" cy="437" rx="52" ry="5" fill="#000000" fill-opacity="0.35"/>'
    body += '<ellipse cx="105" cy="34" rx="19" ry="23" fill="url(#skin)" stroke="#4a5470" stroke-width="1"/>'
    body += '<path d="' + body_outline + '" fill="url(#skin)" stroke="#4a5470" stroke-width="1.2" stroke-linejoin="round"/>'
    for muscle in shapes:
        if muscle not in primary_list and muscle not in secondary_list:
            body += '<path d="' + shapes[muscle] + '" fill="url(#muscle)" stroke="#5b6785" stroke-width="0.8"/>'
    if is_front:
        body += '<path d="' + abs_lines + '" fill="none" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1.4" stroke-linecap="round"/>'
    for muscle in secondary_list:
        if muscle in shapes and muscle not in primary_list:
            body += '<path d="' + shapes[muscle] + '" fill="#ffb347" fill-opacity="0.3" stroke="#ffb347" stroke-opacity="0.3" stroke-width="7" stroke-linejoin="round"/>'
            body += '<path d="' + shapes[muscle] + '" fill="url(#warm)" stroke="#b86a00" stroke-width="1.1"/>'
    for muscle in primary_list:
        if muscle in shapes:
            body += '<path d="' + shapes[muscle] + '" fill="#ff5a4d" fill-opacity="0.3" stroke="#ff5a4d" stroke-opacity="0.3" stroke-width="9" stroke-linejoin="round"/>'
            body += '<path d="' + shapes[muscle] + '" fill="url(#hot)" stroke="#a31f18" stroke-width="1.3"/>'
    return body


def make_body_svg(primary_list, secondary_list, front_word, back_word):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 480">' + svg_defs
    svg += '<rect width="420" height="480" rx="20" fill="url(#bg)"/>'
    svg += "<g>" + draw_body(front_shapes, primary_list, secondary_list, True) + "</g>"
    svg += '<g transform="translate(210,0)">' + draw_body(back_shapes, primary_list, secondary_list, False) + "</g>"
    svg += '<rect x="60" y="448" width="90" height="24" rx="12" fill="#2d3550"/>'
    svg += '<rect x="270" y="448" width="90" height="24" rx="12" fill="#2d3550"/>'
    svg += '<text x="105" y="465" font-size="13" font-weight="bold" text-anchor="middle" fill="#c9d1e3">' + front_word + "</text>"
    svg += '<text x="315" y="465" font-size="13" font-weight="bold" text-anchor="middle" fill="#c9d1e3">' + back_word + "</text>"
    svg += "</svg>"
    return svg


# ---------- 2b. Small helper functions ----------
level_colors = {"beginner": "#22c55e", "intermediate": "#f59e0b", "expert": "#ef4444"}


def make_chip(label, color):
    return '<span class="chip" style="background: ' + color + '33; color: ' + color + ';">' + label + "</span>"


def draw_bars(count_dict, unit=""):
    biggest = max(count_dict.values())
    bars = ""
    for name in count_dict:
        number = count_dict[name]
        percent = number / biggest * 100
        bars += '<div style="display: flex; align-items: center; margin-bottom: 9px;">'
        bars += '<div style="width: 45%; font-size: 14px; padding-right: 10px;">' + name + "</div>"
        bars += '<div style="flex: 1; background: rgba(128, 128, 128, 0.18); border-radius: 8px;">'
        bars += '<div style="width: ' + str(round(percent, 1)) + '%; min-width: 34px; box-sizing: border-box; '
        bars += 'background: linear-gradient(90deg, #34d399, #10b981); color: #06281d; font-weight: 600; '
        bars += 'font-size: 13px; padding: 4px 10px; border-radius: 8px;">' + str(number) + unit + "</div></div></div>"
    return '<div class="panel">' + bars + "</div>"


def get_mean(number_list):
    total = 0
    for number in number_list:
        total += number
    return total / len(number_list)


def get_median(number_list):
    sorted_list = sorted(number_list)
    middle = len(sorted_list) // 2
    if len(sorted_list) % 2 == 1:
        return sorted_list[middle]
    else:
        return (sorted_list[middle - 1] + sorted_list[middle]) / 2


def get_std(number_list):
    mean = get_mean(number_list)
    total = 0
    for number in number_list:
        total += (number - mean) ** 2
    return math.sqrt(total / (len(number_list) - 1))


def sort_dict(count_dict):
    pairs = []
    for name in count_dict:
        pairs.append((count_dict[name], name))
    pairs.sort(reverse=True)
    sorted_dict = {}
    for pair in pairs:
        sorted_dict[pair[1]] = pair[0]
    return sorted_dict


def draw_columns(count_dict):
    biggest = max(count_dict.values())
    chart = '<div class="panel"><table class="columns-chart"><tr>'
    for key in count_dict:
        value = count_dict[key]
        height = round(value / biggest * 170)
        chart += '<td><div class="col-value">' + str(value) + "</div>"
        chart += '<div class="col-bar" style="height: ' + str(height) + 'px;"></div></td>'
    chart += "</tr><tr>"
    for key in count_dict:
        chart += '<td><div class="col-label">' + str(key) + "</div></td>"
    chart += "</tr></table></div>"
    return chart


def draw_ranges(range_dict, scale_max):
    chart = '<div class="panel">'
    for name in range_dict:
        low = range_dict[name][0]
        high = range_dict[name][1]
        mean = range_dict[name][2]
        left = round(low / scale_max * 100, 1)
        width = max(round((high - low) / scale_max * 100, 1), 2)
        dot = round(mean / scale_max * 100, 1)
        chart += '<div class="range-row"><div class="range-name">' + name + "</div>"
        chart += '<div class="range-track"><div class="range-fill" style="left: ' + str(left) + "%; width: " + str(width) + '%;"></div>'
        chart += '<div class="range-dot" style="left: ' + str(dot) + '%;"></div></div>'
        chart += '<div class="range-text">' + str(low) + " – " + str(high) + " · " + str(round(mean, 2)) + "</div></div>"
    chart += "</div>"
    return chart


@st.cache_data
def get_image(image_path):
    url = IMAGE_URL + image_path
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read()
    except Exception:
        pass
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(url, timeout=10, context=context) as response:
            return response.read()
    except Exception as error:
        print("Photo error:", error)
        return None


# ---------- 3. Load and prepare the data ----------
data = pd.read_json("exercises.json")
columns_original = len(data.columns)
missing_equipment = int(data["equipment"].isnull().sum())
missing_mechanic = int(data["mechanic"].isnull().sum())
missing_force = int(data["force"].isnull().sum())
data["equipment"] = data["equipment"].fillna("other")
data["mechanic"] = data["mechanic"].fillna("unknown")

muscles_count_list = []
for index in range(len(data)):
    all_muscles = []
    for muscle in data["primaryMuscles"][index]:
        if muscle not in all_muscles:
            all_muscles.append(muscle)
    for muscle in data["secondaryMuscles"][index]:
        if muscle not in all_muscles:
            all_muscles.append(muscle)
    muscles_count_list.append(len(all_muscles))
data["muscles_count"] = muscles_count_list

photo_total = 0
no_photo_count = 0
duplicate_count = 0
for index in range(len(data)):
    photo_total += len(data["images"][index])
    if len(data["images"][index]) == 0:
        no_photo_count += 1
    for muscle in data["secondaryMuscles"][index]:
        if muscle in data["primaryMuscles"][index]:
            duplicate_count += 1
            break

muscles_name = ["chest", "shoulders", "biceps", "triceps", "forearms", "abdominals",
                "traps", "lats", "middle back", "lower back", "neck",
                "glutes", "quadriceps", "hamstrings", "adductors", "abductors", "calves"]

equipments_name = []
for equipment in data["equipment"]:
    if equipment not in equipments_name:
        equipments_name.append(equipment)
equipments_name.sort()
equipments_name.insert(0, "all")


# ---------- 3b. Numbers for the About page ----------
compound_total = 0
compound_number = 0
isolation_total = 0
isolation_number = 0
for index in range(len(data)):
    if data["mechanic"][index] == "compound":
        compound_total += data["muscles_count"][index]
        compound_number += 1
    elif data["mechanic"][index] == "isolation":
        isolation_total += data["muscles_count"][index]
        isolation_number += 1
compound_mean = round(compound_total / compound_number, 2)
isolation_mean = round(isolation_total / isolation_number, 2)


# ---------- 3c. Exercise page (opens when you click "details") ----------
def open_exercise_page(index):
    st.session_state["open_exercise"] = index
    st.rerun()


def show_exercise_page(index):
    if st.button(t["back"], key="back_button"):
        st.session_state["open_exercise"] = None
        st.rerun()

    level_text = t["levels"][data["level"][index]]
    if data["equipment"][index] in t["equipments"]:
        equipment_text = t["equipments"][data["equipment"][index]]
    else:
        equipment_text = data["equipment"][index]
    if data["mechanic"][index] in t["mechanics"]:
        mechanic_text = t["mechanics"][data["mechanic"][index]]
    else:
        mechanic_text = t["unknown"]
    if data["force"][index] in t["forces"]:
        force_text = t["forces"][data["force"][index]]
    else:
        force_text = t["unknown"]
    category_text = t["categories"][data["category"][index]]

    title_html = '<div class="tag">' + category_text + "</div>"
    title_html += '<div style="font-size: 38px; font-weight: 800; margin: 4px 0 12px 0; line-height: 1.2;">' + html.escape(data["name"][index]) + "</div>"
    title_html += make_chip(level_text, level_colors[data["level"][index]])
    title_html += '<span class="chip">' + equipment_text + "</span>"
    title_html += '<span class="chip">' + mechanic_text + "</span>"
    title_html += '<span class="chip">' + force_text + "</span>"
    st.markdown(title_html, unsafe_allow_html=True)
    st.write("")

    left_col, right_col = st.columns([6, 5])

    # left side: two photos and the steps
    photo_cols = left_col.columns(2)
    image_list = data["images"][index]
    if len(image_list) > 0:
        image_bytes = get_image(image_list[0])
        if image_bytes is not None:
            photo_cols[0].image(image_bytes, caption=t["start_pose"])
    if len(image_list) > 1:
        image_bytes = get_image(image_list[1])
        if image_bytes is not None:
            photo_cols[1].image(image_bytes, caption=t["end_pose"])

    steps_html = '<div class="section-title">' + t["steps_word"] + "</div>"
    step_list = data["instructions"][index]
    for number in range(len(step_list)):
        steps_html += '<div class="step"><div class="step-num">' + str(number + 1) + "</div>"
        steps_html += '<div class="step-text">' + html.escape(step_list[number]) + "</div></div>"
    left_col.markdown(steps_html, unsafe_allow_html=True)

    # right side: score, body picture, muscles, comparison
    better_than = 0
    for other in range(len(data)):
        if data["muscles_count"][other] < data["muscles_count"][index]:
            better_than += 1
    percent = round(better_than / len(data) * 100)

    score_html = '<div class="panel">'
    score_html += '<div class="tag">' + t["score_title"] + "</div>"
    score_html += '<div class="big-score" style="margin: 10px 0;">' + str(percent) + "%</div>"
    score_html += '<div class="meter"><div style="width: ' + str(percent) + '%;"></div></div>'
    score_html += '<p style="font-size: 14px;">' + t["score_a"] + str(percent) + t["score_b"] + "</p>"
    score_html += '<p style="font-size: 14px; opacity: 0.8;">' + t["worked"] + " <b>" + str(data["muscles_count"][index]) + "</b></p>"
    score_html += "</div>"
    right_col.markdown(score_html, unsafe_allow_html=True)

    primary_list = data["primaryMuscles"][index]
    secondary_list = data["secondaryMuscles"][index]
    helper_list = []
    for muscle in secondary_list:
        if muscle not in primary_list:
            helper_list.append(muscle)

    right_col.write("")
    right_col.image(make_body_svg(primary_list, secondary_list, t["front"], t["back"]), width=400)
    right_col.caption(t["legend"])

    chips_html = '<div class="section-title" style="margin-top: 0;">' + t["primary_word"] + "</div>"
    for muscle in primary_list:
        chips_html += make_chip(muscle_info[language][muscle][0], "#ff6b5e")
    if len(helper_list) > 0:
        chips_html += '<div class="section-title">' + t["secondary_word"] + "</div>"
        for muscle in helper_list:
            chips_html += make_chip(muscle_info[language][muscle][0], "#f0a020")
    right_col.markdown(chips_html, unsafe_allow_html=True)

    if len(primary_list) > 0:
        first_muscle = primary_list[0]
        same_total = 0
        same_number = 0
        for other in range(len(data)):
            if first_muscle in data["primaryMuscles"][other]:
                same_total += data["muscles_count"][other]
                same_number += 1

        compare_dict = {}
        compare_dict[t["this_exercise"]] = data["muscles_count"][index]
        compare_dict[t["avg_same"] + muscle_info[language][first_muscle][0]] = round(same_total / same_number, 2)
        compare_dict[t["avg_all"]] = round(data["muscles_count"].mean(), 2)

        right_col.markdown('<div class="section-title">' + t["compare_title"] + "</div>", unsafe_allow_html=True)
        right_col.markdown(draw_bars(compare_dict), unsafe_allow_html=True)


# ---------- 4. Top bar: brand, navigation, language ----------
if "lang_choice" not in st.session_state:
    st.session_state["lang_choice"] = "Монгол"
if "nav_choice" not in st.session_state:
    st.session_state["nav_choice"] = "explorer"
if "muscle_key" not in st.session_state:
    st.session_state["muscle_key"] = "chest"
if "open_exercise" not in st.session_state:
    st.session_state["open_exercise"] = None

if st.session_state["lang_choice"] == "English":
    language = "en"
else:
    language = "mn"
t = text[language]


def nav_label(key):
    return t["nav_" + key]


bar_left, bar_mid, bar_right = st.columns([3, 5, 2])
bar_left.markdown('<div class="brand">💪 ' + t["brand"] + "</div>", unsafe_allow_html=True)
nav_choice = bar_mid.segmented_control("nav", ["explorer", "analysis", "about"], format_func=nav_label, key="nav_choice", label_visibility="collapsed")
bar_right.segmented_control("lang", ["Монгол", "English"], key="lang_choice", label_visibility="collapsed")
if nav_choice is None:
    nav_choice = "explorer"

# when you open another page, close the exercise page
if st.session_state.get("last_nav") != nav_choice:
    st.session_state["last_nav"] = nav_choice
    st.session_state["open_exercise"] = None

level_keys = ["all", "beginner", "intermediate", "expert"]
level_display = []
for level in level_keys:
    level_display.append(t["levels"][level])

equipment_display = []
for equipment in equipments_name:
    if equipment in t["equipments"]:
        equipment_display.append(t["equipments"][equipment])
    else:
        equipment_display.append(equipment)

# ---------- 5. Pages ----------
if st.session_state["open_exercise"] is not None:
    show_exercise_page(st.session_state["open_exercise"])

# ===== Page 1: muscle explorer =====
elif nav_choice == "explorer":
    st.markdown('<div class="page-title">' + t["page_title"] + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="page-sub">' + t["page_sub"] + "</div>", unsafe_allow_html=True)

    filter_box = st.container(border=True)
    filter_cols = filter_box.columns(3)
    level_chosen = filter_cols[0].selectbox(t["level"], level_display)
    level_selected = level_keys[level_display.index(level_chosen)]
    equipment_chosen = filter_cols[1].selectbox(t["equipment"], equipment_display)
    equipment_selected = equipments_name[equipment_display.index(equipment_chosen)]
    number_shown = filter_cols[2].slider(t["how_many"], 3, 30, 9, step=3)

    muscle_selected = st.session_state["muscle_key"]
    info = muscle_info[language][muscle_selected]

    matching_index_list = []
    for index in range(len(data)):
        if muscle_selected in data["primaryMuscles"][index]:
            if level_selected == "all" or data["level"][index] == level_selected:
                if equipment_selected == "all" or data["equipment"][index] == equipment_selected:
                    matching_index_list.append(index)

    filtered = data.loc[matching_index_list]
    filtered = filtered.sort_values("muscles_count", ascending=False)

    st.write("")
    left_col, right_col = st.columns([5, 6])
    left_col.image(make_body_svg([muscle_selected], [], t["front"], t["back"]), width=440)

    card = '<div class="panel"><div class="tag">' + muscle_selected + "</div>"
    card += "<h2>" + info[0] + "</h2>"
    card += "<p>📍 <b>" + t["where"] + "</b> " + info[1] + "</p>"
    card += "<p>💪 <b>" + t["use"] + "</b> " + info[2] + "</p>"
    if len(filtered) > 0:
        card += '<div class="mini-row">'
        card += '<div class="mini"><b>' + str(len(filtered)) + "</b><span>" + t["found"] + "</span></div>"
        card += '<div class="mini"><b>' + str(round(filtered["muscles_count"].mean(), 1)) + "</b><span>" + t["average"] + "</span></div>"
        card += '<div class="mini"><b>' + str(filtered["muscles_count"].max()) + "</b><span>" + t["best"] + t["muscles_word"] + "</span></div>"
        card += "</div>"
    card += "</div>"
    right_col.markdown(card, unsafe_allow_html=True)

    right_col.markdown('<div class="section-title">' + t["click"] + "</div>", unsafe_allow_html=True)
    for start in range(0, len(muscles_name), 6):
        tile_cols = right_col.columns(6)
        for number in range(6):
            position = start + number
            if position < len(muscles_name):
                muscle = muscles_name[position]
                if muscle == muscle_selected:
                    tile_type = "primary"
                else:
                    tile_type = "secondary"
                if tile_cols[number].button(muscle_short[language][muscle], key="tile_" + muscle, type=tile_type):
                    st.session_state["muscle_key"] = muscle
                    st.rerun()

    if len(filtered) == 0:
        st.warning(t["none"])
    else:
        st.markdown('<div class="section-title">' + t["top"] + info[0] + "</div>", unsafe_allow_html=True)
        st.caption(t["caption"])

        rank = 0
        for index in list(filtered.head(number_shown).index):
            rank += 1
            with st.container(border=True):
                photo_col, text_col, action_col = st.columns([3, 6, 2])

                image_list = data["images"][index]
                image_bytes = None
                if len(image_list) > 0:
                    image_bytes = get_image(image_list[0])
                if image_bytes is not None:
                    photo_col.image(image_bytes)
                else:
                    photo_col.write("🖼️ " + t["no_photo"])

                level_text = t["levels"][data["level"][index]]
                if data["equipment"][index] in t["equipments"]:
                    equipment_text = t["equipments"][data["equipment"][index]]
                else:
                    equipment_text = data["equipment"][index]

                helper_names = []
                for secondary in data["secondaryMuscles"][index]:
                    if secondary not in data["primaryMuscles"][index]:
                        helper_names.append(muscle_short[language][secondary])

                text_html = '<div class="ex-name"><span class="rank">' + str(rank) + "</span>" + html.escape(data["name"][index]) + "</div>"
                text_html += make_chip(level_text, level_colors[data["level"][index]])
                text_html += '<span class="chip">' + equipment_text + "</span>"
                if len(helper_names) > 0:
                    text_html += '<div class="meter-label">' + t["also"] + "</div>"
                    for helper_name in helper_names[:5]:
                        text_html += '<span class="chip">' + helper_name + "</span>"
                text_col.markdown(text_html, unsafe_allow_html=True)

                bar_percent = min(data["muscles_count"][index] / 10 * 100, 100)
                score_html = '<div class="score-box"><div class="big-score" style="font-size: 44px;">' + str(data["muscles_count"][index]) + "</div>"
                score_html += "<span>" + t["muscles_label"] + "</span></div>"
                score_html += '<div class="meter"><div style="width: ' + str(bar_percent) + '%;"></div></div>'
                action_col.markdown(score_html, unsafe_allow_html=True)
                if action_col.button(t["details"], key="detail_" + str(index), type="primary"):
                    open_exercise_page(index)

# ===== Page 2: data analysis =====
elif nav_choice == "analysis":
    st.markdown('<div class="page-title">' + t["nav_analysis"] + "</div>", unsafe_allow_html=True)
    sub1, sub2, sub3, sub4 = st.tabs([t["sub1"], t["sub2"], t["sub3"], t["sub4"]])

    # ===== Part 1: overview, cleaning, distribution =====
    with sub1:
        overview = '<div class="panel"><div class="mini-row" style="margin-top: 0;">'
        overview += '<div class="mini"><b>' + str(len(data)) + "</b><span>" + t["ov_rows"] + "</span></div>"
        overview += '<div class="mini"><b>' + str(columns_original) + "</b><span>" + t["ov_cols"] + "</span></div>"
        overview += '<div class="mini"><b>' + str(photo_total) + "</b><span>" + t["hero_photos"] + "</span></div>"
        overview += '<div class="mini"><b>' + str(round(data["muscles_count"].mean(), 2)) + "</b><span>" + t["ov_avg"] + "</span></div>"
        overview += "</div></div>"
        st.markdown(overview, unsafe_allow_html=True)

        st.markdown('<div class="section-title">' + t["clean_title"] + "</div>", unsafe_allow_html=True)
        st.caption(t["clean_note"])
        clean_items = [(missing_equipment, "clean1"), (missing_mechanic, "clean2"), (missing_force, "clean3"),
                       (duplicate_count, "clean4"), (no_photo_count, "clean5")]
        clean_html = ""
        for item in clean_items:
            clean_html += '<div class="clean-row"><div class="clean-num">' + str(item[0]) + "</div>"
            clean_html += '<div class="clean-text"><b>' + t[item[1]][0] + "</b><br>✔ " + t[item[1]][1] + "</div></div>"
        st.markdown(clean_html, unsafe_allow_html=True)

        st.markdown('<div class="section-title">' + t["hist_title"] + "</div>", unsafe_allow_html=True)
        st.caption(t["hist_note"])
        muscles_count_all = list(data["muscles_count"])
        biggest_count = max(muscles_count_all)

        hist_dict = {}
        for number in range(1, biggest_count + 1):
            how_many = 0
            for item in muscles_count_all:
                if item == number:
                    how_many += 1
            hist_dict[number] = how_many

        most_common = 1
        for number in hist_dict:
            if hist_dict[number] > hist_dict[most_common]:
                most_common = number

        small_total = 0
        for item in muscles_count_all:
            if item <= 3:
                small_total += 1
        small_percent = round(small_total / len(muscles_count_all) * 100)

        st.markdown(draw_columns(hist_dict), unsafe_allow_html=True)

        facts = '<div class="panel" style="margin-top: 12px;"><div class="mini-row" style="margin-top: 0;">'
        facts += '<div class="mini"><b>' + str(round(get_mean(muscles_count_all), 2)) + "</b><span>" + t["mean_word"] + "</span></div>"
        facts += '<div class="mini"><b>' + str(get_median(muscles_count_all)) + "</b><span>" + t["median_word"] + "</span></div>"
        facts += '<div class="mini"><b>' + str(most_common) + "</b><span>" + t["mode_word"] + "</span></div>"
        facts += '<div class="mini"><b>' + str(biggest_count) + "</b><span>" + t["max_word"] + "</span></div>"
        facts += "</div>"
        facts += '<p style="margin-top: 14px;">💡 ' + t["hist_a"] + str(small_percent) + t["hist_b"] + "</p></div>"
        st.markdown(facts, unsafe_allow_html=True)

    # ===== Part 2: comparison and t-test =====
    with sub2:
        compound_list = []
        isolation_list = []
        for index in range(len(data)):
            if data["mechanic"][index] == "compound":
                compound_list.append(data["muscles_count"][index])
            elif data["mechanic"][index] == "isolation":
                isolation_list.append(data["muscles_count"][index])

        compound_name = t["mechanics"]["compound"]
        isolation_name = t["mechanics"]["isolation"]

        mean1 = get_mean(compound_list)
        mean2 = get_mean(isolation_list)
        std1 = get_std(compound_list)
        std2 = get_std(isolation_list)
        n1 = len(compound_list)
        n2 = len(isolation_list)

        hyp = '<div class="panel"><div class="tag">' + t["hyp_title"] + "</div>"
        hyp += '<p style="font-size: 18px; margin-top: 8px;">' + t["hyp_text"] + "</p></div>"
        st.markdown(hyp, unsafe_allow_html=True)

        st.markdown('<div class="section-title">' + t["stats_title"] + "</div>", unsafe_allow_html=True)
        table = '<div class="panel"><table class="stat-table"><tr><th></th><th>' + compound_name + "</th><th>" + isolation_name + "</th></tr>"
        table += "<tr><td>" + t["count_word"] + "</td><td>" + str(n1) + "</td><td>" + str(n2) + "</td></tr>"
        table += "<tr><td>" + t["mean_word"] + "</td><td>" + str(round(mean1, 2)) + "</td><td>" + str(round(mean2, 2)) + "</td></tr>"
        table += "<tr><td>" + t["median_word"] + "</td><td>" + str(get_median(compound_list)) + "</td><td>" + str(get_median(isolation_list)) + "</td></tr>"
        table += "<tr><td>" + t["std_word"] + "</td><td>" + str(round(std1, 2)) + "</td><td>" + str(round(std2, 2)) + "</td></tr>"
        table += "<tr><td>" + t["min_word"] + "</td><td>" + str(min(compound_list)) + "</td><td>" + str(min(isolation_list)) + "</td></tr>"
        table += "<tr><td>" + t["max_word"] + "</td><td>" + str(max(compound_list)) + "</td><td>" + str(max(isolation_list)) + "</td></tr>"
        table += "</table></div>"
        st.markdown(table, unsafe_allow_html=True)

        st.markdown('<div class="section-title">' + t["range_title"] + "</div>", unsafe_allow_html=True)
        range_dict = {}
        range_dict[compound_name] = (min(compound_list), max(compound_list), mean1)
        range_dict[isolation_name] = (min(isolation_list), max(isolation_list), mean2)
        st.markdown(draw_ranges(range_dict, max(compound_list)), unsafe_allow_html=True)

        # t-test (Welch) and effect size, calculated by hand
        t_value = (mean1 - mean2) / math.sqrt(std1 ** 2 / n1 + std2 ** 2 / n2)
        p_value = math.erfc(abs(t_value) / math.sqrt(2))
        pooled = math.sqrt(((n1 - 1) * std1 ** 2 + (n2 - 1) * std2 ** 2) / (n1 + n2 - 2))
        d_value = (mean1 - mean2) / pooled

        if p_value < 0.001:
            p_text = "< 0.001"
        else:
            p_text = str(round(p_value, 3))

        if abs(d_value) >= 0.8:
            effect_text = t["effect_large"]
        elif abs(d_value) >= 0.5:
            effect_text = t["effect_mid"]
        else:
            effect_text = t["effect_small"]

        st.markdown('<div class="section-title">' + t["test_title"] + "</div>", unsafe_allow_html=True)
        test = '<div class="panel"><div class="mini-row" style="margin-top: 0;">'
        test += '<div class="mini"><b>' + str(round(t_value, 1)) + "</b><span>" + t["t_word"] + "</span></div>"
        test += '<div class="mini"><b>' + p_text + "</b><span>" + t["p_word"] + "</span></div>"
        test += '<div class="mini"><b>' + str(round(d_value, 2)) + "</b><span>" + t["d_word"] + " · " + effect_text + "</span></div>"
        test += "</div>"
        test += '<p style="margin-top: 14px; opacity: 0.8; font-size: 14px;">' + t["p_explain"] + "</p>"
        if p_value < 0.05 and mean1 > mean2:
            test += '<div class="verdict">✅ ' + t["verdict_yes"] + "</div>"
        else:
            test += '<div class="verdict" style="border-left-color: #f59e0b;">⚠️ ' + t["verdict_no"] + "</div>"
        test += "</div>"
        st.markdown(test, unsafe_allow_html=True)

        compare1, compare2 = st.columns(2)

        level_average = {}
        for level in ["beginner", "intermediate", "expert"]:
            level_list = []
            for index in range(len(data)):
                if data["level"][index] == level:
                    level_list.append(data["muscles_count"][index])
            level_average[t["levels"][level]] = round(get_mean(level_list), 2)
        compare1.markdown('<div class="section-title">' + t["by_level"] + "</div>", unsafe_allow_html=True)
        compare1.markdown(draw_bars(level_average), unsafe_allow_html=True)

        equipment_average = {}
        for equipment in equipments_name[1:]:
            equipment_list = []
            for index in range(len(data)):
                if data["equipment"][index] == equipment:
                    equipment_list.append(data["muscles_count"][index])
            if equipment in t["equipments"]:
                equipment_average[t["equipments"][equipment]] = round(get_mean(equipment_list), 2)
            else:
                equipment_average[equipment] = round(get_mean(equipment_list), 2)
        compare2.markdown('<div class="section-title">' + t["data3"] + "</div>", unsafe_allow_html=True)
        compare2.markdown(draw_bars(sort_dict(equipment_average)), unsafe_allow_html=True)

        muscle_average = {}
        for muscle in muscles_name:
            muscle_list = []
            for index in range(len(data)):
                if muscle in data["primaryMuscles"][index]:
                    muscle_list.append(data["muscles_count"][index])
            muscle_average[muscle_info[language][muscle][0]] = round(get_mean(muscle_list), 2)
        st.markdown('<div class="section-title">' + t["by_muscle"] + "</div>", unsafe_allow_html=True)
        st.markdown(draw_bars(sort_dict(muscle_average)), unsafe_allow_html=True)

        st.info(t["note"])

    # ===== Part 3: which muscles work together =====
    with sub3:
        row_total = {}
        pair_count = {}
        for index in range(len(data)):
            for primary in data["primaryMuscles"][index]:
                if primary in row_total:
                    row_total[primary] += 1
                else:
                    row_total[primary] = 1
                for helper in data["secondaryMuscles"][index]:
                    if helper != primary:
                        key = primary + "|" + helper
                        if key in pair_count:
                            pair_count[key] += 1
                        else:
                            pair_count[key] = 1

        st.markdown('<div class="section-title" style="margin-top: 0;">' + t["heat_title"] + "</div>", unsafe_allow_html=True)
        st.caption(t["heat_note"])

        heat = '<div class="panel" style="overflow-x: auto;"><table class="heat"><tr><th></th>'
        for helper in muscles_name:
            heat += '<th class="vert"><span>' + muscle_short[language][helper] + "</span></th>"
        heat += "</tr>"
        for primary in muscles_name:
            heat += '<tr><th class="rowhead">' + muscle_short[language][primary] + "</th>"
            for helper in muscles_name:
                key = primary + "|" + helper
                if key in pair_count:
                    percent = round(pair_count[key] / row_total[primary] * 100)
                    alpha = round(percent / 100 * 0.95, 2)
                    if percent >= 5:
                        cell_text = str(percent)
                    else:
                        cell_text = ""
                    heat += '<td style="background: rgba(16, 185, 129, ' + str(alpha) + ');">' + cell_text + "</td>"
                else:
                    heat += '<td style="background: rgba(128, 128, 128, 0.06);"></td>'
            heat += "</tr>"
        heat += "</table></div>"
        st.markdown(heat, unsafe_allow_html=True)

        pair_list = []
        for key in pair_count:
            parts = key.split("|")
            percent = round(pair_count[key] / row_total[parts[0]] * 100)
            pair_list.append((percent, parts[0], parts[1]))
        pair_list.sort(reverse=True)

        pairs_dict = {}
        for pair in pair_list[:8]:
            pairs_dict[muscle_short[language][pair[1]] + " → " + muscle_short[language][pair[2]]] = pair[0]
        st.markdown('<div class="section-title">' + t["pairs_title"] + "</div>", unsafe_allow_html=True)
        st.markdown(draw_bars(pairs_dict, "%"), unsafe_allow_html=True)

    # ===== Part 4: top 10 exercises =====
    with sub4:
        st.markdown('<div class="section-title" style="margin-top: 0;">' + t["top_title"] + "</div>", unsafe_allow_html=True)
        st.caption(t["top_note"])

        top_filter1, top_filter2 = st.columns(2)
        top_level_chosen = top_filter1.selectbox(t["level"], level_display)
        top_level_selected = level_keys[level_display.index(top_level_chosen)]
        top_equipment_chosen = top_filter2.selectbox(t["equipment"], equipment_display)
        top_equipment_selected = equipments_name[equipment_display.index(top_equipment_chosen)]

        top_index_list = []
        for index in range(len(data)):
            if top_level_selected == "all" or data["level"][index] == top_level_selected:
                if top_equipment_selected == "all" or data["equipment"][index] == top_equipment_selected:
                    top_index_list.append(index)

        if len(top_index_list) == 0:
            st.warning(t["none"])
        else:
            top_table = data.loc[top_index_list].sort_values("muscles_count", ascending=False).head(10)
            rank = 0
            for index in top_table.index:
                rank += 1
                with st.container(border=True):
                    row_cols = st.columns([1, 6, 4, 3])
                    row_cols[0].markdown('<div class="big-score" style="font-size: 34px;">' + str(rank) + "</div>", unsafe_allow_html=True)

                    level_text = t["levels"][data["level"][index]]
                    if data["equipment"][index] in t["equipments"]:
                        equipment_text = t["equipments"][data["equipment"][index]]
                    else:
                        equipment_text = data["equipment"][index]
                    name_html = '<div class="ex-name" style="min-height: 0; margin: 0 0 6px 0;">' + html.escape(data["name"][index]) + "</div>"
                    name_html += make_chip(level_text, level_colors[data["level"][index]]) + '<span class="chip">' + equipment_text + "</span>"
                    row_cols[1].markdown(name_html, unsafe_allow_html=True)

                    bar_percent = min(data["muscles_count"][index] / 12 * 100, 100)
                    bar_html = '<div class="meter-label">' + t["worked"] + " <b>" + str(data["muscles_count"][index]) + "</b></div>"
                    bar_html += '<div class="meter"><div style="width: ' + str(bar_percent) + '%;"></div></div>'
                    row_cols[2].markdown(bar_html, unsafe_allow_html=True)

                    if row_cols[3].button(t["details"], key="top_" + str(index), type="primary"):
                        open_exercise_page(index)


# ===== Page 3: about the project =====
else:
    st.markdown('<div class="page-title">' + t["nav_about"] + "</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top: 8px;">' + t["about_goal_title"] + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><p style="margin: 0;">' + t["about_goal"] + "</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_question_title"] + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><p style="margin: 0; font-size: 18px;">' + t["about_question"] + "</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_data_title"] + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><p style="margin: 0;">' + t["about_data"] + "</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_columns_title"] + "</div>", unsafe_allow_html=True)
    columns_html = '<div class="panel"><table class="stat-table"><tr><th>' + t["about_col_head"][0] + "</th><th>" + t["about_col_head"][1] + "</th></tr>"
    for pair in t["about_columns"]:
        columns_html += "<tr><td><b>" + pair[0] + "</b></td><td>" + pair[1] + "</td></tr>"
    columns_html += "</table></div>"
    st.markdown(columns_html, unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_method_title"] + "</div>", unsafe_allow_html=True)
    method_html = ""
    number = 0
    for method_step in t["about_method"]:
        number += 1
        method_html += '<div class="step"><div class="step-num">' + str(number) + "</div>"
        method_html += '<div class="step-text">' + method_step + "</div></div>"
    st.markdown(method_html, unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_results_title"] + "</div>", unsafe_allow_html=True)
    results_html = '<div class="panel"><div class="mini-row" style="margin-top: 0;">'
    results_html += '<div class="mini"><b>' + str(compound_mean) + "</b><span>" + t["mechanics"]["compound"] + "</span></div>"
    results_html += '<div class="mini"><b>' + str(isolation_mean) + "</b><span>" + t["mechanics"]["isolation"] + "</span></div>"
    results_html += "</div>"
    results_html += '<p style="margin-top: 14px;">' + t["about_res_a"] + str(compound_mean) + t["about_res_b"] + str(isolation_mean) + t["about_res_c"] + "</p></div>"
    st.markdown(results_html, unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_limits_title"] + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><p style="margin: 0;">' + t["about_limits"] + "</p></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">' + t["about_tech_title"] + "</div>", unsafe_allow_html=True)
    tech_html = ""
    for tech in ["Python", "pandas", "Streamlit", "GitHub"]:
        tech_html += make_chip(tech, "#34d399")
    st.markdown(tech_html, unsafe_allow_html=True)

st.markdown('<div class="footer">' + t["footer"] + "</div>", unsafe_allow_html=True)