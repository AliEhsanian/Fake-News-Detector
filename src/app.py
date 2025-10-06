"""
Main Streamlit application for Fake News Detector
"""


import streamlit as st
from config import Config
from scraper import GoogleSearchScraper
from analyzer import NewsAnalyzer
from utils import validate_input


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Fake News Detector",
        page_icon="🔍",
        layout="wide"
    )

    st.image("src/images/banner.png", use_container_width=True)

    st.title("🔍 Fake News Detector")
    st.markdown("Analyze news headlines and claims for credibility using AI")

    # Initialize components
    config = Config()

    # Validate configuration
    if not config.validate():
        st.error("Please configure your OpenAI API key in the .env file")
        st.stop()

    scraper = GoogleSearchScraper(config.google_api_key, config.google_cse_id)
    analyzer = NewsAnalyzer(config.openai_api_key, config.model_name)

    # Input section
    with st.container():
        claim = st.text_area(
            "Enter a news headline or claim to verify:",
            placeholder="Example: Scientists discover new planet made entirely of diamonds",
            height=100
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🔎 Analyze", type="primary", use_container_width=True)
        with col2:
            st.empty()

    # Analysis section
    if analyze_button and claim:
        if not validate_input(claim):
            st.warning("Please enter a valid claim (at least 10 characters)")
            return

        with st.spinner("Searching for relevant information..."):
            try:
                # Search for information
                search_results = scraper.search(claim, num_results=5)
                #links = search_google(claim)
                #search_results = prepare_context(links)

                if not search_results:
                    st.error("Could not retrieve search results. Please try again.")
                    return

                # Display search results
                with st.expander("📰 Sources Found", expanded=False):
                    for idx, result in enumerate(search_results, 1):
                        st.markdown(f"**{idx}. [{result['title']}]({result['link']})**")
                        st.caption(result['snippet'])
                        st.divider()

                # Analyze credibility
                with st.spinner("Analyzing credibility..."):
                    analysis = analyzer.analyze_claim(claim, search_results)

                # Display results
                display_results(analysis)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your configuration and try again.")


def display_results(analysis):
    """Display analysis results in a formatted way"""
    if not analysis:
        st.error("Could not complete the analysis")
        return

    # Credibility score
    col1, col2, col3 = st.columns(3)

    with col1:
        score = analysis.get('credibility_score', 0)
        score_color = get_score_color(score)
        st.metric(
            "Credibility Score",
            f"{score}/10",
            delta=None,
            help="Higher score indicates higher credibility"
        )
        st.progress(score / 10)

    with col2:
        verdict = analysis.get('verdict', 'Unknown')
        verdict_color = get_verdict_color(verdict)
        st.metric("Verdict", verdict)

    with col3:
        confidence = analysis.get('confidence', 'Low')
        st.metric("Confidence Level", confidence)

    # Detailed analysis
    st.subheader("📊 Detailed Analysis")

    # Key findings
    if 'key_findings' in analysis:
        st.markdown("**Key Findings:**")
        for finding in analysis['key_findings']:
            st.markdown(f"• {finding}")

    # Explanation
    if 'explanation' in analysis:
        st.markdown("**Analysis:**")
        st.info(analysis['explanation'])

    # Red flags or supporting evidence
    col1, col2 = st.columns(2)

    with col1:
        if 'red_flags' in analysis and analysis['red_flags']:
            st.markdown("**⚠️ Red Flags:**")
            for flag in analysis['red_flags']:
                st.markdown(f"• {flag}")

    with col2:
        if 'supporting_evidence' in analysis and analysis['supporting_evidence']:
            st.markdown("**✅ Supporting Evidence:**")
            for evidence in analysis['supporting_evidence']:
                st.markdown(f"• {evidence}")


def get_score_color(score):
    """Get color based on credibility score"""
    if score >= 7:
        return "green"
    elif score >= 4:
        return "orange"
    else:
        return "red"


def get_verdict_color(verdict):
    """Get color based on verdict"""
    verdict_lower = verdict.lower()
    if "likely true" in verdict_lower or "credible" in verdict_lower:
        return "green"
    elif "uncertain" in verdict_lower or "mixed" in verdict_lower:
        return "orange"
    else:
        return "red"


if __name__ == "__main__":
    main()
