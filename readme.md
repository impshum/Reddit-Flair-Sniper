## Reddit Flair Sniper

Reposts or crossposts submissions with certain flairs to different subreddits. Runs every hour.

### Instructions

-   Install requirements `pip install -r requirements.txt`
-   Create Reddit (script) app at https://www.reddit.com/prefs/apps/ and get keys
-   Edit conf.ini with your details
-   Run it `python run.py`

#### Settings Info

-   `main_target_subreddit` - Main Subreddit to search
-   `crosspost` - Crosspost or repost (on = crosspost)
-   `send_replies` - Send comment replies to inbox from new submission
-   `test_mode` - Runs the bot without posting

#### Sniper Settings Config

Add each target flair and subreddit to conf.ini like so

    [SNIPER_1]
    target_flair = XXXX
    target_subreddit = XXXX

Note the numbered title: ```SNIPER_1```. To add another create an entry underneath the first just the same just increment the number in the title like so

    [SNIPER_2]
    target_flair = XXXX
    target_subreddit = XXXX

    [SNIPER_3]
    target_flair = XXXX
    target_subreddit = XXXX

You can add up to 99 sniper configs.

#### Tip

BTC - 1AYSiE7mhR9XshtS4mU2rRoAGxN8wSo4tK
