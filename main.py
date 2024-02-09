import os
import argparse
import gradio as gr

import ParseSchedules


def clean_up():
    # force delete and then create output_json folder (windows and linux agnostic way)
    os.system("rmdir /s /q output_json")
    os.system("mkdir output_json")
    
    # delete archive with results if it exists
    if os.path.exists("output_json.zip"):
        os.remove("output_json.zip")

def convert(group_into_folders, files):
    clean_up()
    
    ParseSchedules.extract_all_schedules(files, group_into_folders, group_size=20)
    
    # list all files in output_json folder and subfolders
    output_json = []
    for root, dirs, files in os.walk("output_json"):
        for file in files:
            output_json.append(os.path.join(root, file))
    
    # get absolute paths
    output_json = [os.path.abspath(file) for file in output_json]
    # filter out non-json files
    output_json = [file for file in output_json if file.endswith(".json")]
    
    return make_zip_with_results()
    
def make_zip_with_results():
    # zips all the files in the output_json folder and returns the path to the zip file
    os.system("powershell Compress-Archive -Path output_json/* -DestinationPath output_json.zip")
    
    return os.path.abspath("output_json.zip")
    

demo = gr.Interface(
    fn=convert,
    inputs=[gr.Checkbox(value=True, label = "Групувати в папки"), gr.Files(label = ".docx розклади", file_types=[".docx"])],
    outputs=[gr.Files(label = ".json розклади (zip архів)")],
    title=".docx розклади --> .json розклади",
    description="Інтерфейс для витягування .json розкладів зі вордівських розкладів",
    allow_flagging=False,
)

if __name__ == "__main__":
    
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-s",
        "--share",
        action="store_true",
        help="Whether to make interface public or not. Default is False.",
    )
    
    args = vars(ap.parse_args())

    should_share = args["share"]
    demo.launch(share = should_share)  # Launch the interface
