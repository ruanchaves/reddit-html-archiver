## reddit html archiver image plugin

This is an image downloader plugin for the [reddit html archiver](https://github.com/libertysoft3/reddit-html-archiver).

### motivation

After subreddits get banned or deleted, nobody knows for how long their images will stay on Reddit's servers.
reddit-html-archiver downloads just the html and the image links, but not the actual images.

This plugin follows through the links and downloads the images to your computer. 
Failed download attempts will be registered to a log file.

### install

Move the output folder of reddit-html-archiver to this folder. 

```
conda create --name redditenv python=3.7
conda activate redditenv
pip install -r requirements.txt
```

You can skip the first two commands and just run `sudo -H pip install -r requirements.txt` on this folder if you don't wish to run this plugin on a virtual environment.

After that, `python image_plugin.py` will download all images to this folder.

Then you can just `conda env remove -n redditenv` if you don't plan on using this plugin again any time soon.