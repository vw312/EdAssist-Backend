import mitocw
import nptel
import udacity
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery


def courseSearcher(request, q):
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


def subjectidNptelInformation(request, subjectid):
    """Sends lectures and extra_downloads info for a subjectid."""
    lectures = nptel.models.Lectures.objects.filter(
        subjectid__exact=subjectid).order_by('lecture_number').values()
    extra_downloads = nptel.models.ExtraDownloads.objects.filter(
        subjectid__exact=subjectid).values()

    result_dict = {'lectures': list(
        lectures), 'extra_downloads': list(extra_downloads)}

    return JsonResponse(result_dict)
