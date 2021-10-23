# rheed-viz

Database, dimensionality reduction, and visualization dashboard for RHEED data

To setup the environment, run conda env update --file env.cpu.yml, which will create a conda environment called rheed-viz

### Launching app
Streamlit frontend uses `requirements.txt`
Run locally with `streamlit run app.py`

### RHEED jpg data
* Process AVI movies by installing ffmpeg and doing `ffmpeg -i MovieName.avi -vf  fps=<num_fps>  c01_%04d.jpg -hide_banner`
* https://figshare.com/s/73b8ab6cb131acbbe9d4
