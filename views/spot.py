from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
import oauth2
import simplejson as json

from django.http import HttpResponse


def SpotView(request, spot_id, return_json=False):
    # Required settings for the client
    if not hasattr(settings, 'SS_WEB_SERVER_HOST'):
        raise(Exception("Required setting missing: SS_WEB_SERVER_HOST"))
    if not hasattr(settings, 'SS_WEB_OAUTH_KEY'):
        raise(Exception("Required setting missing: SS_WEB_OAUTH_KEY"))
    if not hasattr(settings, 'SS_WEB_OAUTH_SECRET'):
        raise(Exception("Required setting missing: SS_WEB_OAUTH_SECRET"))

    consumer = oauth2.Consumer(key=settings.SS_WEB_OAUTH_KEY, secret=settings.SS_WEB_OAUTH_SECRET)
    client = oauth2.Client(consumer)

    url = "{0}/api/v1/spot/{1}".format(settings.SS_WEB_SERVER_HOST, spot_id)

    resp, content = client.request(url, 'GET')

    if resp.status == 404:
        response = HttpResponse("Not found")
        response.status_code = 404
        return response
    elif resp.status != 200:
        response = HttpResponse("Error loading spot")
        response.status_code = resp.status_code
        return response

    spot_json = json.loads(content)

    params = {
        "type": spot_json["type"],
        "name": spot_json["name"],
        "capacity": spot_json["capacity"],
        "location_description": spot_json["extended_info"]["location_description"],
        #"has_natual_light": spot_json["extended_info"]["has_natural_light"],
        #"noise_level": spot_json["extended_info"]["noise_level"],
        #"food_nearby": spot_json["extended_info"]["food_nearby"],

        #"has_computers": spot_json["extended_info"]["has_computers"],
        #"has_displays": spot_json["extended_info"]["has_displays"],
        #"has_outlets": spot_json["extended_info"]["has_outlets"],
        #"has_printing": spot_json["extended_info"]["has_printing"],
        #"has_projector": spot_json["extended_info"]["has_projector"],
        #"has_scanner": spot_json["extended_info"]["has_scanner"],
        #"has_whiteboards": spot_json["extended_info"]["has_whiteboards"],
        "attribute_list": []
    }

    for attribute in spot_json["extended_info"]:
        params["attribute_list"].append({"name": attribute, "value": spot_json["extended_info"][attribute]})

    if return_json:
        return HttpResponse(content, mimetype='application/json')
    else:
        return render_to_response('space.html', params, context_instance=RequestContext(request))
