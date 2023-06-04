from src.config import Config

DAILY_SHUFFLE_PATH_BASE: str = "daily_shuffle"

DADDY_JOKES_PATH: str = "daddy_jokes"

HOME_SITE: str = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Daily random people order</title>
        <style type="text/css">
          body {
            margin: 40px auto;
            max-width: 650px;
            line-height: 1.6;
            font-size: 18px;
            color: #444;
            padding: 0 10px
          }

          h1,
          h2,
          h3 {
            line-height: 1.2
          }
        </style>
      </head>
      <body>
        <header>
          <h1>Daily random team order</h1>
        </header>
        <h2>
          Endpoints:
        </h2>
        <ul>
            {list_of_sites}
        </ul>

        <p>Site design inspired by the geniuses behind <a href="http://bettermotherfuckingwebsite.com/">this site</a>. </p>
        </br>

        <hr>
        <center><span style="color: silver">We are on a mission from God!</span></center>
      </body>
    </html/
    """

SHUFFLE_SITE: str = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{team_name} random team order</title>
        <style type="text/css">
          body {
            margin: 40px auto;
            max-width: 650px;
            line-height: 1.6;
            font-size: 18px;
            color: #444;
            padding: 0 10px
          }
          button {
            color: black;
            text-align: center;
            font-size: 16px;
            margin: 4px 2px;
            padding: 4px 8px;
         }

          h1,
          h2,
          h3 {
            line-height: 1.2
          }
        </style>
      </head>
      <body>
        <header>
          <h1>{team_name} random team order</h1>
          {quote}
        </header>
        <h2>Order</h2>
            <ul> {people_order} </ul>
        <left><span style="color: silver"> [daily-shuffle@team ~#]$ ⬆⬆⬇⬇⬅➡⬅➡🅱🅰</span></left>
            {joke}
        <hr>
        <center><span style="color: silver;text-align: center">We are on a mission from God!</span></center>
      </body>
    </html>
    """

DAILY_SHUFFLE_DADDY_JOKE_SITE_PART: str = """
    <h2>Daddy joke</h2>
        <h3>Newest</h2>
            {newest_joke}
        <h3>Something older...</h2>
            {joke}
    """

DADDY_JOKE_SITE: str = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Daddy Joke site</title>
        <style type="text/css">
          body {
            margin: 40px auto;
            max-width: 650px;
            line-height: 1.6;
            font-size: 18px;
            color: #444;
            padding: 0 10px
          }
          button {
            color: black;
            text-align: center;
            font-size: 16px;
         }

          h1,
          h2,
          h3 {
            line-height: 1.2
          }
        </style>
      </head>
      <header>
        <h1>Daddy jokes site</h1>
      </header>
      <body>
        {joke}
        <center><span style="color: white">VWDQ LV QRW ZKDW KH VHHPV</span></center>
        <hr>
        <center><span style="color: silver">We are on a mission from God!</span></center>
      </body>
    </html>
    """


def get_home_site(config: Config) -> str:
    """
    Get home site from ``HOME_SITE`` with additional list of links to
    other available sites.
    """
    list_of_sites_string: str = ""

    # link to all team shuffle sites
    for s in config.shuffle_sites_configs:
        site_link = f' <li> <a href="{DAILY_SHUFFLE_PATH_BASE}/{s.site_path}">/{s.site_path}</a>'
        description = f"- {s.team_name} daily random order </li>\n"
        list_of_sites_string = list_of_sites_string + site_link + description

    # link for daddy jokes site
    daddy_jokes = f' <li> <a href="/{DADDY_JOKES_PATH}">/{DADDY_JOKES_PATH}</a>'
    description_daddy_jokes = "- daddy jokes site </li>\n"
    list_of_sites_string = list_of_sites_string + daddy_jokes + description_daddy_jokes

    return HOME_SITE.replace("{list_of_sites}", list_of_sites_string, 1)
