import TwitterBot



def main():
    sc = TwitterBot.ScraperConfig()

    TwitterBot.notifications.get_notifications()
    TwitterBot.followers.get_followers()
    TwitterBot.following.get_following()

    db = TwitterBot.Database(
        sc.get_database_type(), dbname=sc.get_database_uri()
        )


if __name__ == "__main__":
    main()
