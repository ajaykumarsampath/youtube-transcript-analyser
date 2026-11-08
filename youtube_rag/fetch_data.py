# this file is used to fetch data from youtube and store it in a json file
from dataclasses import dataclass
import dataclasses
import os
import json
import yt_dlp


@dataclass
class VideoData:
    video_id: str
    title: str
    url: str
    duration: float
    view_count: int


def fetch_podcast_list_from_channel(
        channel_url: str = "https://www.youtube.com/@ThePrintIndia/podcasts", podcast_name = 'cut the clutter with') -> list[VideoData]:
    """
    Fetches the list of videos for a given YouTube channel URL.

    Args:
        channel_url (str): The YouTube channel URL.
        podcast_name (str): Name of the podcast to filter videos by.

    Returns:
        list[VideoData]: A list of VideoData objects containing video details.
    """
    channel_url = "https://www.youtube.com/@ThePrintIndia/podcasts"

    options = {
        "extract_flat": "in_playlist",
        "skip_download": True,
        "quiet": True,
    }

    podcast_details = []

    with yt_dlp.YoutubeDL(options) as ydl:
        podcast_result = ydl.extract_info(channel_url, download=False)

        for video in podcast_result.get("entries", []):
            if video:
                # print(video.get("id"), video.get("title"))
                podcast_details.append(VideoData(
                    video_id=video.get("id"),
                    title=video.get("title"),
                    url=video.get("url", None),
                    duration=video.get("duration"),
                    view_count=video.get("view_count")
                ))

    cut_the_clutter_podcast = [p for p in podcast_details if podcast_name.lower() in p.title.lower()]

    with yt_dlp.YoutubeDL(options) as ydl:
        cc_result = ydl.extract_info(cut_the_clutter_podcast[0].url, download=False)

    cc_details = [
        VideoData(
            video_id=video.get("id"),
            title=video.get("title"),
            url=video.get("url", None),
            duration=video.get("duration"),
            view_count=video.get("view_count")
        )
        for video in cc_result.get("entries", []) if video
    ]

    return cc_details


def remove_initial_ads_in_transcript(transcript_raw: str) -> str | None:
    try:
        with open(transcript_raw, "r", encoding="utf-8") as f:
            import re
            fetched_transcript = json.load(f)
            # text = ' '.join([transcript['text'] for transcript in fetched_transcript])
            # music_transcript = [transcript for transcript in fetched_transcript if 'music' in transcript['text'].lower()]

            carefully_transcript = [transcript for transcript in fetched_transcript if 'carefully' in transcript['text'].lower()]
            # print([transcript for transcript in fetched_transcript if transcript['text'] == '[music]' or 'related documents carefully' in transcript['text']])
            filter_transcript = [transcript for transcript in fetched_transcript if transcript['start'] > carefully_transcript[0]['start']]
            text = ' '.join([t['text'] for t in filter_transcript])
            text = re.sub(r">+", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            text = re.sub(r"\[music\]", "", text, flags=re.IGNORECASE)
            return text
    except FileNotFoundError:
        pass