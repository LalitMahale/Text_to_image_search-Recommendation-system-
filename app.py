import streamlit as st
from src.multimodelsearch import MultiModelSearch
st.set_page_config(
    layout="wide",
    page_title="Recommendation_engine"
)


def main():
    st.markdown("<h1 style = 'text-align:center; color:black;'>Recommendation_engine</h1>",unsafe_allow_html=True)
    
    multimodelserch = MultiModelSearch()

    query = st.text_input("Enter Your Query")

    if st.button("Search") and len(query) > 0:
        result = multimodelserch.search(query=query)
        st.info(f"Your query : {query}")
        st.subheader("Search Results")
        col1,col2,col3 = st.columns(3)

        with col1:
            st.write(f"Score: {round(result[0].score*100)}%")
            st.image(result[0].content,use_column_width=True)
    
        with col2:
            st.write(f"Score: {round(result[1].score*100)}%")
            st.image(result[1].content,use_column_width=True)

        with col3:
            st.write(f"Score: {round(result[2].score*100)}%")
            st.image(result[2].content,use_column_width=True)

    else:
        st.warning("Please Enter query.......")

if __name__ == "__main__":
    main()