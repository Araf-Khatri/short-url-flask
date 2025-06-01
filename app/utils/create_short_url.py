base62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def create_short_url(total_url):
  count = total_url
  short_url = ""
  while count > 0:
    count, rem =  divmod(count, 62)
    short_url = base62[rem] + short_url

  return short_url
