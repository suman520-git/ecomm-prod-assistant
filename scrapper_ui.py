

import streamlit as st
from prod_assistant.etl.data_scrapper import FlipkartScraper
from prod_assistant.etl.data_ingestion import DataIngestion
import os

flipkart_scraper = FlipkartScraper()
output_path = "data/product_reviews.csv"
st.title("📦 Product Review Scraper")

if "product_inputs" not in st.session_state:
    st.session_state.product_inputs = [""]

print('st.session_state.product_inputs ',st.session_state.product_inputs )

print('=========================================================================================================' )


def add_product_input():
    st.session_state.product_inputs.append("")

st.subheader("📝 Optional Product Description")
product_description = st.text_area("Enter product description (used as an extra search keyword):")

print('=========================================================================================================' )

print('product_description::',product_description)

print('=========================================================================================================' )

st.subheader("🛒 Product Names")
updated_inputs = []
print('updated_inputs::',updated_inputs)

print('=========================================================================================================' )
for i, val in enumerate(st.session_state.product_inputs):

    print('i',i,"val",val)
    input_val = st.text_input(f"Product {i+1}", value=val, key=f"product_{i}")

    print('=========================================================================================================' )
    print('input_val::',input_val)

    print('=========================================================================================================' )

    updated_inputs.append(input_val)
    print('updated_inputs:2:',updated_inputs)
    print('=========================================================================================================' )

st.session_state.product_inputs = updated_inputs

print('st.session_state.product_inputs::2 ',st.session_state.product_inputs )
print('=========================================================================================================' )

st.button("➕ Add Another Product", on_click=add_product_input)

max_products = st.number_input("How many products per search?", min_value=1, max_value=10, value=1)
review_count = st.number_input("How many reviews per product?", min_value=1, max_value=10, value=2)

print('max_products ',max_products)
print('review_count ',review_count)
print('=========================================================================================================' )

if st.button("🚀 Start Scraping"):
    print('st.session_state.product_inputs::3 ',st.session_state.product_inputs )
    print('=========================================================================================================' )
    
    product_inputs = [p.strip() for p in st.session_state.product_inputs if p.strip()]
    print('=========================================================================================================' )
    print('product_inputs ',product_inputs )
    print('=========================================================================================================' )
    if product_description.strip():

        print('product_description.strip():',product_description.strip() )
        print('=========================================================================================================' )



        product_inputs.append(product_description.strip())

        print('product_inputs::2 ',product_inputs )
        print('=========================================================================================================' )

    if not product_inputs:
        st.warning("⚠️ Please enter at least one product name or a product description.")
    else:
        final_data = []
        print('final_data::',final_data )
        print('=========================================================================================================' )


        for query in product_inputs:

            print('query ',query )
            print('=========================================================================================================' )
            st.write(f"🔍 Searching for: {query}")
            results = flipkart_scraper.scrape_flipkart_products(query, max_products=max_products, review_count=review_count)
            final_data.extend(results)
            print('final_data::2',final_data )
            print('=========================================================================================================' )

        unique_products = {}
        print('unique_products',unique_products)
        print('=========================================================================================================' )
        for row in final_data:
            print('row',row)

            if row[1] not in unique_products:
                unique_products[row[1]] = row
        print('list(unique_products.values())',list(unique_products.values()))
        print('=========================================================================================================' )
        final_data = list(unique_products.values())

        print('final_data::3',final_data )
        print('=========================================================================================================' )
        st.session_state["scraped_data"] = final_data  # store in session
        print('st.session_state["scraped_data"] ',st.session_state["scraped_data"]  )
        print('=========================================================================================================' )

        flipkart_scraper.save_to_csv(final_data, output_path)
        st.success("✅ Data saved to `data/product_reviews.csv`")
        st.download_button("📥 Download CSV", data=open(output_path, "rb"), file_name="product_reviews.csv")

# This stays OUTSIDE "if st.button('Start Scraping')"
if "scraped_data" in st.session_state and st.button("🧠 Store in Vector DB (AstraDB)"):
    with st.spinner("📡 Initializing ingestion pipeline..."):
        try:
            ingestion = DataIngestion()
            st.info("🚀 Running ingestion pipeline...")
            ingestion.run_pipeline()
            st.success("✅ Data successfully ingested to AstraDB!")
        except Exception as e:
            st.error("❌ Ingestion failed!")
            st.exception(e)
