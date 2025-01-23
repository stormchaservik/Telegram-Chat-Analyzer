# Telegram-Chat-Analyzer

There are 3 scripts:
- `analyze.py`: Outputs a quick analysis with interesting metrics
- `cloud.py`: Generates word clouds for each of the chat's participants (color palette can be customized in the code)
- `sentiment.py`: Generates a pie-chart with sentiment data for the entire chat history

## Instructions to run
Initial setup:
On the Telegram Desktop app, export the chat history to be analyzed (choose `JSON: Machine-readable` output in the export options). Once the export is complete, place the `result.json` file in the same directory as the scripts.

Download the repository and unzip the contents.

Ensure Python 3.7+ is installed. Then run `pip install requirements.txt`, in the directory where the scripts are located, to get the required dependencies.

Finally, run `python script_name.py` where `script_name` is the name of the script you wish to run.

## Further Enhancements
This project is barebones at the moment. Expect more analysis options to be added in the future along with improvements to user-experience for users who are not familiar with programming environments. If you have suggestions or requests, feel free to open an issue in the Issues tab!
