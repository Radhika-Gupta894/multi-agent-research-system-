import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem;}
    .hero {
        padding: 1.8rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #1e3a8a);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {margin: 0;}
    .hero p {color: #dbeafe; margin-top: .6rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🔎 Multi-Agent Research System</h1>
        <p>Search → Scrape → Write → Critique</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Pipeline")
    st.markdown(
        """
        **1. 🔍 Search Agent**

        Tavily searches the web for relevant sources.

        **2. 📖 Reader Agent**

        BeautifulSoup scrapes a relevant source.

        **3. ✍️ Writer Chain**

        LCEL generates the research report.

        **4. 🧐 Critic Chain**

        LCEL reviews the report.
        """
    )
    st.divider()
    st.caption("LangChain • Mistral • Tavily • BeautifulSoup")

st.subheader("Research Topic")

topic = st.text_area(
    "Enter the topic you want to research:",
    placeholder="Example: Recent developments in Generative AI",
    height=100,
)

if st.button("🚀 Start Research", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        with st.status("Running multi-agent research...", expanded=True) as status:
            st.write("🔍 Search Agent is working...")
            st.write("📖 Reader Agent is working...")
            st.write("✍️ Writer Chain is generating the report...")
            st.write("🧐 Critic Chain is reviewing the report...")

            try:
                result = run_research_pipeline(topic.strip())

                status.update(
                    label="✅ Research completed!",
                    state="complete",
                    expanded=False,
                )

                st.session_state["result"] = result
                st.session_state["topic"] = topic.strip()

            except Exception as e:
                status.update(
                    label="❌ Pipeline failed",
                    state="error",
                    expanded=True,
                )
                st.exception(e)

if "result" in st.session_state:
    result = st.session_state["result"]
    research_topic = st.session_state["topic"]

    st.divider()
    st.subheader(f"📊 Research Results: {research_topic}")

    st.markdown("## 📄 Final Research Report")

    report = result.get(
        "report",
        "No report generated."
    )

    st.markdown(report)

    st.download_button(
        "⬇️ Download Report",
        data=report,
        file_name="research_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    search_tab, scrape_tab, critic_tab = st.tabs(
        [
            "🔍 Search Results",
            "📖 Scraped Content",
            "🧐 Critic Review",
        ]
    )

    with search_tab:
        st.markdown("### Web Search Results")
        st.write(
            result.get(
                "search_results",
                "No search results available."
            )
        )

    with scrape_tab:
        st.markdown("### Scraped Content")
        st.write(
            result.get(
                "scraped_content",
                "No scraped content available."
            )
        )

    with critic_tab:
        st.markdown("### Critic Review")
        st.write(
            result.get(
                "critic_review",
                "No critic review available."
            )
        )

    st.divider()
    st.subheader("🧩 Pipeline")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info("🔍 Search Agent\n\nTavily Web Search")

    with c2:
        st.info("📖 Reader Agent\n\nBeautifulSoup")

    with c3:
        st.info("✍️ Writer Chain\n\nLCEL")

    with c4:
        st.info("🧐 Critic Chain\n\nLCEL")
