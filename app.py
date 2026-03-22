import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="CineAI — Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# 🎨 CINEMATIC LUXURY CSS
# ═══════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080a0e !important;
    color: #e8e0d4 !important;
    font-family: 'Outfit', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(180, 130, 60, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(120, 60, 30, 0.08) 0%, transparent 55%),
        #080a0e !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
footer { display: none !important; }

/* ── Main Content ── */
.main .block-container {
    max-width: 1280px;
    padding: 0 2.5rem 4rem !important;
    margin: 0 auto;
}

/* ── Hero Section ── */
.hero-wrapper {
    text-align: center;
    padding: 4.5rem 0 3rem;
    position: relative;
}

.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a84c;
    margin-bottom: 1.2rem;
    opacity: 0.9;
}

.hero-title {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(3.2rem, 7vw, 5.8rem);
    font-weight: 300;
    letter-spacing: -0.01em;
    line-height: 1.05;
    color: #f0ebe3;
    margin-bottom: 0.6rem;
}

.hero-title em {
    font-style: italic;
    color: #c9a84c;
}

.hero-subtitle {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: rgba(232, 224, 212, 0.5);
    letter-spacing: 0.04em;
    margin-top: 0.8rem;
}

.hero-divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 2rem auto 0;
}

/* ── Selector Section ── */
.selector-section {
    max-width: 680px;
    margin: 0 auto 3rem;
    text-align: center;
}

.selector-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(201, 168, 76, 0.7);
    margin-bottom: 0.8rem;
    display: block;
}

/* ── Streamlit Selectbox Overrides ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(201, 168, 76, 0.25) !important;
    border-radius: 4px !important;
    color: #e8e0d4 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 300 !important;
    padding: 0.75rem 1.2rem !important;
    transition: border-color 0.25s ease !important;
    backdrop-filter: blur(8px);
}

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(201, 168, 76, 0.65) !important;
    background: rgba(255,255,255,0.06) !important;
}

[data-testid="stSelectbox"] svg { color: #c9a84c !important; }

div[data-baseweb="popover"] {
    background: #12151c !important;
    border: 1px solid rgba(201, 168, 76, 0.2) !important;
    border-radius: 4px !important;
}

div[data-baseweb="popover"] li {
    background: transparent !important;
    color: rgba(232, 224, 212, 0.8) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 300 !important;
}

div[data-baseweb="popover"] li:hover {
    background: rgba(201, 168, 76, 0.12) !important;
    color: #e8e0d4 !important;
}

/* ── CTA Button ── */
[data-testid="stButton"] > button {
    display: block !important;
    margin: 1.5rem auto 0 !important;
    background: transparent !important;
    border: 1px solid rgba(201, 168, 76, 0.5) !important;
    color: #c9a84c !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.9rem 2.8rem !important;
    border-radius: 2px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stButton"] > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, rgba(201,168,76,0.1), rgba(201,168,76,0.05)) !important;
    opacity: 0 !important;
    transition: opacity 0.3s ease !important;
}

[data-testid="stButton"] > button:hover {
    border-color: #c9a84c !important;
    color: #f0d98a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(201, 168, 76, 0.18) !important;
    background: rgba(201, 168, 76, 0.06) !important;
}

/* ── Section Header ── */
.results-header {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 2.2rem;
    margin-top: 1rem;
}

.results-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(201,168,76,0.35), transparent);
}

.results-header-line.right {
    background: linear-gradient(270deg, rgba(201,168,76,0.35), transparent);
}

.results-header-text {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(201, 168, 76, 0.85);
}

/* ── Movie Cards ── */
.movie-card-outer {
    position: relative;
    cursor: pointer;
}

.movie-card {
    background: #0f1218;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 6px;
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                border-color 0.35s ease,
                box-shadow 0.35s ease;
    position: relative;
}

.movie-card:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: rgba(201, 168, 76, 0.4);
    box-shadow:
        0 24px 60px rgba(0,0,0,0.6),
        0 0 0 1px rgba(201, 168, 76, 0.15),
        0 -1px 0 rgba(201, 168, 76, 0.3) inset;
}

.poster-wrapper {
    position: relative;
    width: 100%;
    padding-top: 150%;
    overflow: hidden;
    background: #12151c;
}

.poster-wrapper img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.movie-card:hover .poster-wrapper img {
    transform: scale(1.06);
}

.poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to bottom,
        transparent 45%,
        rgba(8, 10, 14, 0.5) 70%,
        rgba(8, 10, 14, 0.92) 100%
    );
    z-index: 1;
}

.rating-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(8,10,14,0.82);
    border: 1px solid rgba(201, 168, 76, 0.4);
    border-radius: 3px;
    padding: 3px 8px;
    font-size: 0.7rem;
    font-weight: 500;
    color: #c9a84c;
    z-index: 2;
    letter-spacing: 0.05em;
    backdrop-filter: blur(4px);
}

.movie-number {
    position: absolute;
    bottom: 12px;
    left: 12px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.5rem;
    font-weight: 300;
    color: rgba(201, 168, 76, 0.15);
    line-height: 1;
    z-index: 2;
}

.card-body {
    padding: 1rem 1rem 1.1rem;
}

.card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.87rem;
    font-weight: 500;
    color: #e8e0d4;
    line-height: 1.35;
    margin-bottom: 0.55rem;
    letter-spacing: 0.01em;
}

.card-overview {
    font-size: 0.72rem;
    font-weight: 300;
    color: rgba(232, 224, 212, 0.45);
    line-height: 1.55;
    letter-spacing: 0.01em;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: rgba(201, 168, 76, 0.7) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.12em !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(201, 168, 76, 0.25); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201, 168, 76, 0.45); }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# 🔧 FUNCTIONS
# ═══════════════════════════════════════════════════════
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url, timeout=8).json()
        poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if data.get('poster_path') else ""
        rating = round(data.get('vote_average', 0), 1)
        overview = data.get('overview', "No synopsis available.")
        genres = [g['name'] for g in data.get('genres', [])[:2]]
        return poster, rating, overview, genres
    except Exception:
        return "", "N/A", "No synopsis available.", []


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    results = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, rating, overview, genres = fetch_movie_details(movie_id)
        results.append({
            "title": title,
            "poster": poster,
            "rating": rating,
            "overview": overview,
            "genres": genres
        })
    return results


# ═══════════════════════════════════════════════════════
# 📦 LOAD DATA
# ═══════════════════════════════════════════════════════
movies    = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# ═══════════════════════════════════════════════════════
# 🎬 HERO SECTION
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrapper">
    <p class="hero-eyebrow">AI-Powered Discovery</p>
    <h1 class="hero-title">Find Your Next<br><em>Favourite Film</em></h1>
    <p class="hero-subtitle">Curated recommendations, tailored to your taste</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🎥 SELECTOR
# ═══════════════════════════════════════════════════════
st.markdown('<div class="selector-section">', unsafe_allow_html=True)
st.markdown('<span class="selector-label">Select a title</span>', unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("", movie_list, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 🚀 RECOMMEND BUTTON
# ═══════════════════════════════════════════════════════
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    recommend_clicked = st.button("Discover Films")

# ═══════════════════════════════════════════════════════
# 🎞 RESULTS
# ═══════════════════════════════════════════════════════
if recommend_clicked:
    with st.spinner("Curating your selection…"):
        results = recommend(selected_movie)

    st.markdown("""
    <div class="results-header">
        <div class="results-header-line"></div>
        <span class="results-header-text">Recommended for You</span>
        <div class="results-header-line right"></div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="small")
    for idx, (col, movie) in enumerate(zip(cols, results)):
        with col:
            genres_html = " · ".join(movie['genres']) if movie['genres'] else ""
            poster_src  = movie['poster'] if movie['poster'] else "https://via.placeholder.com/300x450/12151c/c9a84c?text=No+Poster"
            overview_snippet = movie['overview'][:90] + "…" if len(movie['overview']) > 90 else movie['overview']

            st.markdown(f"""
            <div class="movie-card-outer">
                <div class="movie-card">
                    <div class="poster-wrapper">
                        <img src="{poster_src}" alt="{movie['title']}" loading="lazy" />
                        <div class="poster-overlay"></div>
                        <div class="rating-badge">★ {movie['rating']}</div>
                        <div class="movie-number">0{idx + 1}</div>
                    </div>
                    <div class="card-body">
                        <div class="card-title">{movie['title']}</div>
                        <div class="card-overview">{overview_snippet}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)