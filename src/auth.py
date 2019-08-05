# Original by https://github.com/philipperemy/Deep-Learning-Tinder/blob/master/tinder_token.py
# Modified 2019

import re
import robobrowser
import requests


MOBILE_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"

FB_AUTH = f"https://m.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y"


def get_fb_access_token(email, password):
    browser = robobrowser.RoboBrowser(history=True, user_agent=MOBILE_USER_AGENT, parser="lxml")
    browser.open(FB_AUTH)
    # First we submit the login form
    f = browser.get_form("login_form")
    f["email"] = email
    f["pass"] = password
    browser.submit_form(f)

    try:
        # Now we *should* be redirected to the Tinder app dialogue. If we don't see this
        # form that means that the user did not type the right password
        f = browser.get_form("platformDialogForm")
        if f is None:
            return {"error": "Login failed. Check your username and password."}
        browser.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        access_token = re.search(r"access_token=([\w\d]+)", browser.response.content.decode()).groups()[0]
        return access_token
    # FIXME: Learn how to submit the form correctly so that we don't have to do this
    # clowny exception handling
    except requests.exceptions.InvalidSchema as e:
        access_token = re.search(r"access_token=([\w\d]+)", str(e)).groups()[0]
        return access_token
    except Exception as e:
        return {"error": f"access token could not be retrieved: {repr(e)}"}


def get_fbid(access_token):
    if "error" in access_token:
        return {"error": "get_fbid requires valid access token"}
    """Gets facebook ID from access token"""
    req = requests.get('https://graph.facebook.com/me?access_token=' + access_token)
    return req.json()["id"]
