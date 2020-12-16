import TwitterBot


def main():
    TwitterBot.notifications.get_notifications()
    TwitterBot.followers.get_followers()
    TwitterBot.following.get_following()

if __name__ == "__main__":
    main()
