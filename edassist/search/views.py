import requests
import os

import mitocw
import nptel
import udacity
from . import nlp
from xml.etree import ElementTree

from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.postgres.search import SearchVector, SearchQuery
import googleapiclient.discovery


def course_searcher(request, q):
    if request.headers['User-Agent'] != 'EdAssist-Qt':
        return HttpResponseForbidden("<h1>Forbidden</h1>")
    vector = SearchVector('title', 'description',
                          'department', 'instructors', config='english')
    query = SearchQuery(q, config='english')
    result_mitocw = mitocw.models.Courses.objects.annotate(
        search=vector).filter(search=query).values()

    vector = SearchVector('subjectname', 'disciplinename',
                          'coordinators', config='english')
    result_nptel = nptel.models.Courses.objects.annotate(
        search=vector).filter(search=query).values()

    vector = SearchVector('title', 'school', config='english')
    result_udacity = udacity.models.Courses.objects.annotate(
        search=vector).filter(search=query).values()

    result_dict = {'mitocw': list(result_mitocw), 'nptel': list(
        result_nptel), 'udacity': list(result_udacity)}

    return JsonResponse(result_dict)


def subjectid_nptel_information(request, subjectid):
    """Sends lectures and extra_downloads info for a subjectid."""
    if request.headers['User-Agent'] != 'EdAssist-Qt':
        return HttpResponseForbidden("<h1>Forbidden</h1>")
    lectures = nptel.models.Lectures.objects.filter(
        subjectid__exact=subjectid).order_by('lecture_number').values()
    extra_downloads = nptel.models.ExtraDownloads.objects.filter(
        subjectid__exact=subjectid).values()

    result_dict = {'lectures': list(
        lectures), 'extra_downloads': list(extra_downloads)}

    return JsonResponse(result_dict)


def caption_nptel(request, youtube_video_id, subjectid):
    """Uses the Youtube Data Api to obtain subtitles of a particular video"""
    if request.headers['User-Agent'] != 'EdAssist-Qt':
        return HttpResponseForbidden("<h1>Forbidden</h1>")

    # check if the requested captions are already available
    db_manager = nptel.models.YoutubeStuff.objects
    if db_manager.filter(youtube_id__exact=youtube_video_id).exists():
        result = list(db_manager.filter(youtube_id__exact=youtube_video_id).values('caption_name', 'captions'))
        return JsonResponse(result, safe=False)

    # if not fetch them using Youtube Data API
    captions = get_captions(youtube_video_id)

    return JsonResponse(captions, safe=False)


def important_words_nptel(request, subjectid, youtube_video_id):
    """Returns important words with timestamps for that particular lecture"""
    if request.headers['User-Agent'] != 'EdAssist-Qt':
        return HttpResponseForbidden("<h1>Forbidden</h1>")

    # check if requested info is available
    db_manager = nptel.models.YoutubeStuff.objects
    if db_manager.filter(youtube_id__exact=youtube_video_id).exists():  # check whether the captions for this
        # video_is exist
        words = list(db_manager.values('important_words').filter(youtube_id__exact=youtube_video_id))  # if yes, query
        # to check whether important_words field is not null
        if words[0]['important_words']:
            return JsonResponse(words[0]['important_words'])

    # obtain the important words using ml
    # first obtain the captions for all lectures in the subject
    video_ids = nptel.models.Lectures.objects.filter(subjectid__exact=subjectid).values('youtube_id').distinct()
    for video_id in video_ids:  # video_id is a dictionary with key as 'youtube_id'
        if not db_manager.filter(youtube_id__exact=video_id['youtube_id']).exists():
            get_captions(video_id['youtube_id'])

    # call the nlp function
    dictionary = extract_important_words(subjectid)
    for video_id, value in dictionary.items():
        db_manager.filter(youtube_id__exact=video_id).update(important_words=value)

    return JsonResponse(dictionary[youtube_video_id])


# ---------------------------------------------------------------------------------------------------------------------#
# helper functions ahead, not views
# ---------------------------------------------------------------------------------------------------------------------#

def get_captions(video_id):
    """Uses Youtube data api to find the captions to fetch.
    Saves the fetched captions into the database"""
    db_manager = nptel.models.YoutubeStuff.objects

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ['YOUTUBE_API_KEY']

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.captions().list(
        part="snippet",
        videoId=video_id
    )
    response = request.execute()

    # iterate through the obtained response and consider only english subtitles
    captions_available = response['items']
    to_download = [(video_id, caption['snippet']['name']) for caption in captions_available if (
            caption['snippet']['language'] == 'en' and caption['snippet']['trackKind'] != 'ASR')]
    captions = [{'caption_name': name, 'captions': download_captions(video_id, name)} for (video_id, name) in
                to_download]  # captions is a array of dictionaries

    # put these captions into the database
    for dictionary in captions:
        db_manager.create(youtube_id=video_id, caption_name=dictionary['caption_name'],
                          captions=dictionary['captions'])

    return captions


def extract_important_words(subjectid):
    """Implements the nlp pipeline to extract important words from captions of all videos of subject
    For the time being only for nptel lectures. Returns a dictionary with key as the video_id."""
    db_manager = nptel.models.YoutubeStuff.objects

    # video_ids is a list of dictionaries
    video_ids = nptel.models.Lectures.objects.filter(subjectid__exact=subjectid).values('youtube_id').distinct()
    captions = []
    for video_id in video_ids:
        temp = list(db_manager.filter(youtube_id__exact=video_id['youtube_id']).values('captions'))
        if temp:
            captions.append(temp[0]['captions'])

    cleaned_captions = [caption.replace('<br />', ' ') for caption in captions]  # br tag cause problems
    documents = [nlp.extract_document(caption) for caption in cleaned_captions]
    important_words = nlp.important_words(documents)

    # cleaned_captions and important_words should be of the same size. There may be videos for which no captions
    # exist (online). 'captions' will not have them so they need to be ignored here
    result = {video_ids[i]['youtube_id']: find_timestamps(cleaned_captions[i], important_words[i])
              for i in range(0, len(cleaned_captions)) if
              db_manager.filter(youtube_id__exact=video_ids[i]['youtube_id']).exists()}

    return result


def download_captions(video_id, name):
    """Downloads captions using requests library"""
    parameters = {'v': video_id, 'lang': 'en', 'name': name,
                  'fmt': 'ttml', 'xorb': 2, 'xobt': 3, 'xovt': 3}
    r = requests.get('https://www.youtube.com/api/timedtext', params=parameters)
    captions = r.text
    return captions


def find_timestamps(caption, words):
    """Returns a dictionary with the key as the word and its first occurrence time as value"""
    ns = {'ttml': 'http://www.w3.org/ns/ttml'}
    xml_document = ElementTree.fromstring(caption)
    div = xml_document.find('ttml:body', ns).find('ttml:div', ns)
    ptags = div.findall('ttml:p', ns)

    dictionary = dict()
    for word in words:  # compute timestamp for each word
        for ptag in ptags:
            if word in ptag.text:
                dictionary[word] = ptag.attrib['begin']
                break

    return dictionary
