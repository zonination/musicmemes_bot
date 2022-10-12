# Import python libraries
import praw
import prawcore
import time

# Import custom libraries
import rlogin

# Login to reddit
r = rlogin.mm()
r.validate_on_submit = True
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Define initial conditions
subs = ['ClassicalMemes', 'MetalMemes', 'Audiomemes', 'lingling40hrs', 'Bandmemes']


def chkinbox():
    # print('Checking mail...')
    for message in r.inbox.unread(limit=10):
        try:
            # Skip non-messages and some accounts
            if not message.fullname.startswith("t4_") or message.author in ['mod_mailer', 'reddit', 'ModNewsletter']:
                message.mark_read()
                print('Marked as read: One of those annoying fucking Snoosletters.')
                continue
            # Skip non-subreddit messages
            if not message.subreddit:
                message.mark_read()
                print('Marked as read: non-subreddit message.')
                continue
        except praw.exceptions.APIException:
            print('  Probably a false alarm...')
        except (KeyboardInterrupt, SystemExit):
            raise

# Main loop
while True:
    try:
        
        # Scout the subreddits for music-related material
        for sub in subs:
            for post in r.subreddit(sub).top('week', limit=1):
                
                # Load records (threads IDs that have already been operated on)
                f=open('.log.txt', 'r')
                slist=f.read().split(' ')
                f.close
                
                # Check to see our conditions for posting are sufficient
                if (post.is_self == False) and (post.id not in slist):
                    # Design the title
                    posttext='{0} [{2} on /r/{1}]'.format(post.title, post.subreddit.display_name, post.author.name)
                    if len(posttext) >= 300:
                        posttext='{0} ... [{2} on /r/{1}]'.format(post.title[:240], post.subreddit.display_name, post.author.name)
                    
                    # Make a crosspost
                    print('{0}\n'.format(posttext))
                    post.crosspost(subreddit='musicmemes', title=posttext, send_replies=False)
                    
                    # Log the event
                    f=open('.log.txt', 'a')
                    f.write('{0} '.format(post.id))
                    f.close()
        
        chkinbox()
        # Timeout
        time.sleep(600)
        
    # Exception list for when Reddit inevitably screws up
    except praw.exceptions.APIException:
        print('\nAn API exception happened.\nTaking a coffee break.\n')
        time.sleep(30)
    except prawcore.exceptions.InvalidToken:
        print('\n401 error: Token needs refreshing.\nTaking a coffee break.\n')
        time.sleep(30)
    except prawcore.exceptions.ServerError:
        print('\nReddit\'s famous 503 error occurred.\nTaking a coffee break.\n')
        time.sleep(180)
    except prawcore.exceptions.RequestException:
        print('.')
        time.sleep(180)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as inst:
        print(type(inst))
        print(inst.args)        
        print('')
        time.sleep(30)
#    except:
#        print('\nException happened (MusicMemes).\nTaking a coffee break.\n')
#        time.sleep(30)
