import streamlit as st
from urllib.parse import urlparse, parse_qs
st.dropdown('Test', '-Changelogs-')
st.title("Dynamic Page Input Example")
if main_option == 'Test':
  st.dropdown 
  query_params = st.experimental_get_query_params()
  default_text = query_params.get("input", [""])[0]
  user_input = st.text_input("Enter your text:", value=default_text)
  st.write(f"You entered: {user_input}")
  st.experimental_set_query_params(input=user_input)
  st.write(f"Current URL: `https://mcaddon-manager.streamlit.app/?input={user_input}'")

if main_option == '-Changelogs-':
    
    st.markdown("## **`Addon Manager | 0.14`:**")
    st.markdown("- Patched a bug causing no 'variants' to be added if the user didn't check the 'Customized futher' checkmark.\n - Date: *10/24/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.13`:**")
    st.markdown("- Added bundles and colored bundles as receivable items on Random Item Skyblock.\n - Added the option for users to modify the chance of receiving certain items on Random Item Skyblock.\n  - Date: *10/23/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.12`:**")
    st.markdown("- Fixed a formatting issue in Random Item Skybock's 'manifest.json' (in the pack description) that was causing the pack to not work on realms.\n - Renamed 'RIS' to 'RandomItemSkyblock' and moved it to 'Packs/LOstDev404/RandomItemSkyblock'.\n - Made the web icon have MCAddon logo, and MCAddon Manager text.\n - Date: *10/20/2024*")
    st.write("---")
    st.markdown("## **`Addon Manager | 0.11`:**")
    st.markdown("- Added changelogs.\n - Date: *10/19/2024*")
