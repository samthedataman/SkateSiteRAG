import streamlit as st
import weaviate
import pandas as pd
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
from streamlit_player import st_player

# load_dotenv()


# Access keys from Streamlit configuration
weaviate_key = st.secrets["weaviate_key"]
openai_key = st.secrets["openai_key"]
weaviate_url = st.secrets["weaviate_url"]


auth_config = weaviate.AuthApiKey(api_key=weaviate_key)

# Setting up client
client = weaviate.Client(
    url = weaviate_url,
    auth_client_secret=auth_config,
    additional_headers={
         "X-OpenAI-Api-Key": openai_key, # Replace with your OpenAI key,
    })

# Assume the functions get_semantic_results is defined above

# Number of results to fetch
num_results = 50  # Update this number as needed

# Set page configuration
st.set_page_config(page_title="The worlds best skate video search engine (powered by weaviate and openai)", layout="wide")

# Streamlit app layout
st.title("Skate Video Search")

# Search bar
search_text = st.text_input("Search for a Skate Video, Skater, Place, Company, Product, or Song", placeholder="Enter a video title or attribute")

def get_semantic_results(qq):

  response = client.query.get("SKATESITERAG2",
            [ 'title', 
              'fullLength', 
              'videoType', 
              'production',
              'watchOnlineDescription', 
              'skaterCameo', 
              'thrasherCover',
              'locations', 
              'soundtrack', 
              'skaters', 
              'coverArt_description',
              'coverArtImageLink', 
              'youtubeLink', 
              'skateSiteLink'
             ]).with_near_text({
            "concepts": [qq]}).do()

  # df = pd.json_normalize(response['data']['Get']['SKATESITERAG2'])

  return response 


if search_text:
    results = get_semantic_results(search_text)

    if results:
        # Convert JSON data to DataFrame
        df = pd.json_normalize(results['data']['Get']['SKATESITERAG2'])  # Replace 'YourClassName'

        num_videos = len(df)
        metrics_per_row = 2  # Set the number of columns per row for the grid
        num_containers = (num_videos // metrics_per_row) + (num_videos % metrics_per_row > 0)
    
        video_index = 0
        for container_index in range(num_containers):
            with st.container():
                cols = st.columns(metrics_per_row)
                for metric_index in range(metrics_per_row):
                    if video_index < num_videos:
                        video_info = df.iloc[video_index]
                        with cols[metric_index]:
                            with st.expander(f"{video_info['title']} ({video_info['videoType']})", expanded=True):
                                                        # Displaying the cover art image if available
                                
                                if video_info['youtubeLink']:
                        
                                    st_player(video_info['youtubeLink'])
                                    # st.video(video_info['youtubeLink'], format="video/mp4", start_time=0)

                                # # YouTube and Skate Site Links
                                # elif video_info['coverArtImageLink']:
                                #     st.image(video_info['coverArtImageLink'], caption="Cover Art")
                                # YouTube and Skate Site Links
    
                                st.write(f"**Cover Art Description:** {video_info['coverArt_description']}")
    
                                st.write(f"**Skaters:** {video_info['skaters']}")
                                st.subheader("Video Information:")
                                st.write(f"**Title:** {video_info['title']}")
                                st.write(f"**Full Length:** {video_info['fullLength']} minutes")
                                st.write(f"**Video Type:** {video_info['videoType']}")
                                # if video_info['youtubeLink']:
                                #     st.markdown(f"[YouTube Link]({video_info['youtubeLink']})")
                                #     st.video(video_info['youtubeLink'])
                                # else:
                                #   print("no link")
                                st.write(f"**Production:** {video_info['production']}")
                                st.write(f"**Watch Online Description:** {video_info['watchOnlineDescription']}")
                                st.write(f"**Skater Cameo:** {video_info['skaterCameo']}")
                                st.write(f"**Thrasher Cover:** {video_info['thrasherCover']}")
                                st.write(f"**Locations:** {video_info['locations']}")
                                st.write(f"**Soundtrack:** {video_info['soundtrack']}")
                                

        # num_videos = len(df)
        # metrics_per_row = 2  # Adjust the number of videos per row as needed
        # num_rows = -(-num_videos // metrics_per_row)  # Ceiling division to ensure all videos are included
        
        # for i in range(0, num_videos, metrics_per_row):
        #     cols = st.columns(metrics_per_row)
        #     for j in range(metrics_per_row):
        #         video_index = i + j
        #         if video_index < num_videos:
        #             video_info = df.iloc[video_index]
        #             with cols[j]:
        #                 with st.expander(f"{video_info['title']} ({video_info['videoType']})", expanded=True):
        #                     if pd.notnull(video_info['coverArtImageLink']):
        #                         st.image(video_info['coverArtImageLink'], caption="Cover Art")
        
        #                     if pd.notnull(video_info['youtubeLink']):
        #                         st.video(video_info['youtubeLink'])
        
        #                     st.markdown("### Video Information")
        #                     st.write(f"**Title:** {video_info['title']}")
        #                     st.write(f"**Full Length:** {video_info['fullLength']} minutes")
        #                     st.write(f"**Video Type:** {video_info['videoType']}")
        
        #                     # Handling dictionaries and lists correctly
        #                     if isinstance(video_info['production'], dict):
        #                         production_info = ", ".join([f"{key}: {value}" for key, value in video_info['production'].items()])
        #                         st.write(f"**Production:** {production_info}")
        #                     else:
        #                         st.write(f"**Production:** {video_info['production']}")
        
        #                     # Displaying lists as comma-separated strings
        #                     if isinstance(video_info['skaters'], list):
        #                         st.write("### Skaters")
        #                         st.write(", ".join(video_info['skaters']))
        #                     else:
        #                         st.write(f"**Skaters:** {video_info['skaters']}")
        
        #                     if isinstance(video_info['locations'], list):
        #                         st.write("### Locations")
        #                         st.write(", ".join(video_info['locations']))
        #                     else:
        #                         st.write(f"**Locations:** {video_info['locations']}")
        
        #                     if isinstance(video_info['soundtrack'], list):
        #                         st.write("### Soundtrack")
        #                         for track in video_info['soundtrack']:
        #                             st.write(f"- {track}")
        #                     else:
        #                         st.write(f"**Soundtrack:** {video_info['soundtrack']}")
        #                 video_index += 1
    
        # num_videos = len(df)
        # metrics_per_row = 2  # Set the number of columns per row for the grid
        # num_containers = (num_videos // metrics_per_row) + (num_videos % metrics_per_row > 0)
    
        # video_index = 0
        # for container_index in range(num_containers):
        #     with st.container():
        #         cols = st.columns(metrics_per_row)
        #         for metric_index in range(metrics_per_row):
        #             if video_index < num_videos:
        #                 video_info = df.iloc[video_index]
        #                 with cols[metric_index]:
        #                     with st.expander(f"{video_info['title']} ({video_info['videoType']})", expanded=True):
        #                                                 # Displaying the cover art image if available
                                
        #                         if video_info['coverArtImageLink']:
                                    
        #                             st_player(video_info['youtubeLink'])
        #                             # st.video(video_info['youtubeLink'], format="video/mp4", start_time=0)


        #                         # YouTube and Skate Site Links
    
        #                             # st.image(video_info['coverArtImageLink'], caption="Cover Art")
        #                         # YouTube and Skate Site Links
    
        #                         st.write(f"**Cover Art Description:** {video_info['coverArt_description']}")
    
        #                         st.write(f"**Skaters:** {video_info['skaters']}")
        #                         st.subheader("Video Information:")
        #                         st.write(f"**Title:** {video_info['title']}")
        #                         st.write(f"**Full Length:** {video_info['fullLength']} minutes")
        #                         st.write(f"**Video Type:** {video_info['videoType']}")
        #                         # if video_info['youtubeLink']:
        #                         #     st.markdown(f"[YouTube Link]({video_info['youtubeLink']})")
        #                         #     st.video(video_info['youtubeLink'])
        #                         # else:
        #                         #   print("no link")
        #                         st.write(f"**Production:** {video_info['production']}")
        #                         st.write(f"**Watch Online Description:** {video_info['watchOnlineDescription']}")
        #                         st.write(f"**Skater Cameo:** {video_info['skaterCameo']}")
        #                         st.write(f"**Thrasher Cover:** {video_info['thrasherCover']}")
        #                         st.write(f"**Locations:** {video_info['locations']}")
        #                         st.write(f"**Soundtrack:** {video_info['soundtrack']}")


        #                 video_index += 1





# # Create tabs
# tab_videos, tab_skaters, tab_companies, tab_filmmakers = st.tabs(["Videos", "Skaters", "Companies", "Sountracks"])

# # Tab for Videos
# with tab_videos:
#     num_videos = len(results['title'].unique())

#     metrics_per_row = 2
#     num_containers = (num_videos // metrics_per_row) + (num_videos % metrics_per_row > 0)

#     video_index = 0
#     for container_index in range(num_containers):
#         with st.container():
#             cols = st.columns(metrics_per_row)
#             for metric_index in range(metrics_per_row):
#                 if video_index < num_videos:
#                     video_info = results.iloc[video_index]
#                     with cols[metric_index]:
#                         with st.expander(f"{video_info['title']} ({video_info.get('production.Year', 'Year Unknown')})", expanded=True):
#                             # Display video information
#                             st.image(video_info['coverArtImageLink'], caption=video_info['watchOnlineDescription'])
#                             # ... rest of your video display logic
#                     video_index += 1

# # Tab for Skaters
# with tab_skaters:
#     st.write("Skaters content goes here")  # Replace with logic to display skaters

# # Tab for Companies
# with tab_companies:
#     st.write("Companies content goes here")  # Replace with logic to display companies

# # Tab for Filmmakers
# with tab_filmmakers:
#     st.write("Filmmakers content goes here")  # Replace with logic to display filmmakers or a message if none

# You can add more content within each tab as needed by repeating the `with tab_name:` structure


    # if results:
    #     # Convert JSON data to DataFrame
    #     df = pd.json_normalize(results['data']['Get']['SKATESITERAG2'])  # Replace 'YourClassName'

    #     num_videos = len(df)
    #     metrics_per_row = 2  # Set the number of columns per row for the grid
    #     num_containers = (num_videos // metrics_per_row) + (num_videos % metrics_per_row > 0)

    #     video_index = 0
    #     for container_index in range(num_containers):
    #         with st.container():
    #             cols = st.columns(metrics_per_row)
    #             for metric_index in range(metrics_per_row):
    #                 if video_index < num_videos:
    #                     video_info = df.iloc[video_index]
    #                     with cols[metric_index]:
    #                         with st.expander(f"{video_info['title']} ({video_info['videoType']})", expanded=True):
    #                                                     # Displaying the cover art image if available
                                
    #                             if video_info['coverArtImageLink']:
    #                                 st.image(video_info['coverArtImageLink'], caption="Cover Art")
    #                             # YouTube and Skate Site Links

    #                                 # st.image(video_info['coverArtImageLink'], caption="Cover Art")
    #                             # YouTube and Skate Site Links

    #                             st.write(f"**Cover Art Description:** {video_info['coverArt_description']}")

    #                             st.write(f"**Skaters:** {video_info['skaters']}")
    #                             st.subheader("Video Information:")
    #                             st.write(f"**Title:** {video_info['title']}")
    #                             st.write(f"**Full Length:** {video_info['fullLength']} minutes")
    #                             st.write(f"**Video Type:** {video_info['videoType']}")
    #                             # if video_info['youtubeLink']:
    #                             #     st.markdown(f"[YouTube Link]({video_info['youtubeLink']})")
    #                             #     st.video(video_info['youtubeLink'])
    #                             # else:
    #                             #   print("no link")
    #                             st.write(f"**Production:** {video_info['production']}")
    #                             st.write(f"**Watch Online Description:** {video_info['watchOnlineDescription']}")
    #                             st.write(f"**Skater Cameo:** {video_info['skaterCameo']}")
    #                             st.write(f"**Thrasher Cover:** {video_info['thrasherCover']}")
    #                             st.write(f"**Locations:** {video_info['locations']}")
    #                             st.write(f"**Soundtrack:** {video_info['soundtrack']}")


    #                     video_index += 1

