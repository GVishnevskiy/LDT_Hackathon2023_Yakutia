KATE_MOBILE = 2685278
GROUP_ACESS_RIGHTS = 262144


def get_acess_token():
    base_url = f"https://oauth.vk.com/authorize?client_id={KATE_MOBILE}"

    url_params = {
        "redirect_uri": "close.html",
        "display": "page",
        "scope": GROUP_ACESS_RIGHTS,
        "response_type": "token",
    }
    param_url = ""
    for key, value in url_params.items():
        param_url += f"&{key}={value}"

    return base_url + param_url
