import sys
import requests
from bs4 import BeautifulSoup
import math
import matplotlib
import matplotlib.dates as dates
import matplotlib.pyplot as plot
import matplotlib.patheffects
from adjustText import adjust_text
import dateutil.parser


def download_timestamps():
    thread_list = [  # Update this list with new threads
        "https://desuarchive.org/mlp/thread/33700529/",
        "https://desuarchive.org/mlp/thread/33729880/",
        "https://desuarchive.org/mlp/thread/33745916/",
        "https://desuarchive.org/mlp/thread/33779583/",
        "https://desuarchive.org/mlp/thread/33854142/",
        "https://desuarchive.org/mlp/thread/33963949/",
        "https://desuarchive.org/mlp/thread/34019408/",
        "https://desuarchive.org/mlp/thread/34080783/",
        "https://desuarchive.org/mlp/thread/34189328/",
        "https://desuarchive.org/mlp/thread/34300569/",
        "https://desuarchive.org/mlp/thread/34427076/",
        "https://desuarchive.org/mlp/thread/34514258/",
        "https://desuarchive.org/mlp/thread/34611670/",
        "https://desuarchive.org/mlp/thread/34637665/",
        "https://desuarchive.org/mlp/thread/34659201/",
        "https://desuarchive.org/mlp/thread/34698483/",
        "https://desuarchive.org/mlp/thread/34729063/",
        "https://desuarchive.org/mlp/thread/34748129/",
        "https://desuarchive.org/mlp/thread/34767284/",
        "https://desuarchive.org/mlp/thread/34778298/",
        "https://desuarchive.org/mlp/thread/34789903/",
    ]

    posts_file = open("ppp_posts", "w")
    for i, t in enumerate(thread_list):
        print("Scraping thread " + str(i + 1) + "...")
        thread = requests.get(t)
        posts = BeautifulSoup(thread.content, "html.parser").find_all(
            "div", {"class": "post_data"}
        )
        for p in posts:
            time = p.select("span[class=time_wrap] > time")[0]["datetime"]
            pid = p.select("a[data-function=quote]")[0].contents[0]
            if not "," in pid:
                posts_file.write(time + "," + pid + "\n")


def plot_timestamps(arrow_list):
    def date(d):
        return dates.date2num(dateutil.parser.parse(d))

    print("Plotting data...")
    posts_file = open("ppp_posts", "r").readlines()
    posts_file.sort()
    timestamps = []
    post_ids = []
    for p in posts_file:
        timestamps.append(date(p.split(",")[0]))
        post_ids.append(int(p.split(",")[1]))
    matplotlib.rc("font", family="Equestria")
    plot.plot_date(
        timestamps, list(range(1, len(timestamps) + 1)), "b-", color="#673888",
    )
    plot.title("Pony Preservation Project", fontsize=30)
    plot.ylabel("Post count (total " + str(len(timestamps)) + ")", fontsize=20)
    plot.grid(True)
    plot.ylim(0, math.ceil(len(timestamps) / 1000) * 1000)
    plot.xlim(
        date("2019-04-01"), timestamps[-1],
    )
    plot.yticks(range(0, math.ceil(len(timestamps) / 1000) * 1000 + 1, 1000))
    texts = []
    for a, b in arrow_list:
        index = post_ids.index(b)
        texts.append(plot.text(timestamps[index], index + 1, a, color="#00000066"))
        texts[-1].set_path_effects(
            [matplotlib.patheffects.withStroke(linewidth=2, foreground="#ffffff88")]
        )
    adjust_text(
        texts, arrowprops=dict(arrowstyle="-|>",),
    )
    plot.gcf().set_size_inches(7, 5)
    plot.savefig("ppp_plot.png", dpi=160)
    print("Done!")


if "--update" in sys.argv:
    download_timestamps()
else:
    print("Plotting old post data. Run with --update to download posts.")
plot_timestamps(
    [("15's first post", 34627577),]
)  # ("TwAIlight's first word", 33925824),
