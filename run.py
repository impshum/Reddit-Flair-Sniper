import praw
from time import sleep
import schedule
import configparser
import pickledb
from requests import get
from requests.exceptions import ConnectionError


def wait_until_online(timeout, slumber):
    offline = 1
    t = 0
    while offline:
        try:
            r = get('https://google.com', timeout=timeout).status_code
        except ConnectionError:
            r = None
        if r == 200:
            offline = 0
        else:
            t += 1
            if t > 3:
                quit()
            else:
                print('BOT OFFLINE')
                sleep(slumber)


def do_db(db, id, sub):
    if not db.exists(id):
        db.set(id, sub)
        db.dump()
        return True


def sniper(reddit, main_target_subreddit, send_replies, crosspost, sniper_config, test_mode, db):
    wait_until_online(10, 3)
    for submission in reddit.subreddit(main_target_subreddit).new(limit=None):
        for conf in sniper_config:
            target_flair = conf['target_flair']
            if submission.link_flair_text == target_flair:
                target_subreddit = conf['target_subreddit']
                if not test_mode:
                    if do_db(db, submission.id, target_subreddit):
                        if crosspost:
                            submission.crosspost(
                                subreddit=target_subreddit, send_replies=send_replies)
                        else:
                            reddit.subreddit(target_subreddit).submit(
                                submission.title, selftext=submission.selftext, send_replies=send_replies)
                        print(f'{target_flair} → r/{target_subreddit}')


def main():
    db = pickledb.load('history.db', False)
    config = configparser.ConfigParser()
    config.read('conf.ini')
    main_target_subreddit = config['SETTINGS']['main_target_subreddit']
    send_replies = config['SETTINGS'].getboolean('send_replies')
    crosspost = config['SETTINGS'].getboolean('crosspost')
    test_mode = config['SETTINGS'].getboolean('test_mode')
    reddit = praw.Reddit(
        username=config['REDDIT']['reddit_user'],
        password=config['REDDIT']['reddit_pass'],
        client_id=config['REDDIT']['reddit_client_id'],
        client_secret=config['REDDIT']['reddit_client_secret'],
        user_agent='Flair Sniper (by u/impshum)'
    )

    sniper_config = []

    for i in range(1, 99):
        sniper_i = f'SNIPER_{i}'
        if config.has_option(sniper_i, 'target_subreddit'):
            sniper_config.append(
                {'target_flair': config[sniper_i]['target_flair'], 'target_subreddit': config[sniper_i]['target_subreddit']})

    if test_mode:
        print('\nTEST MODE\n')

    sniper(reddit, main_target_subreddit, send_replies,
           crosspost, sniper_config, test_mode, db)
    schedule.every().hour.do(sniper, reddit=reddit, main_target_subreddit=main_target_subreddit,
                             send_replies=send_replies, crosspost=crosspost, sniper_config=sniper_config, test_mode=test_mode, db=db)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':
    main()
