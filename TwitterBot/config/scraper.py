from ._base import CONFIG_DIR, CONFIG_FILE, Config


class ScraperConfig(Config):
    def __init__(self):
        self.path = CONFIG_DIR + CONFIG_FILE['scraper']
        self.get_config_data()

    def get_twitter_config(self):
        return self.config['Twitter']
    
    def get_twitter_credentials(self):
        return self.get_twitter_config()['Credentials']
    
    def get_twitter_username(self):
        return self.get_twitter_credentials()['username']
    
    def get_twitter_password(self):
        return self.get_twitter_credentials()['password']
    
    def get_twitter_paths(self):
        return self.get_twitter_config()['Paths']
    
    def get_twitter_domain(self):
        return self.get_twitter_paths()['domain']
    
    def get_twitter_login(self):
        return self.get_twitter_paths()['login']
    
    def get_twitter_session(self):
        return self.get_twitter_paths()['session']
    
    def get_twitter_profile(self):
        return self.get_twitter_paths()['profile']
    
    def get_twitter_followers(self):
        return self.get_twitter_paths()['followers']
    
    def get_twitter_following(self):
        return self.get_twitter_paths()['following']

    def get_twitter_notifications(self):
        return self.get_twitter_paths()['notifications']

    def get_browser_config(self):
        return self.config['Browser']

    def get_browser_headers(self):
        return self.get_browser_config()['Headers']

    def get_database_config(self):
        return self.config['Database']
    
    def get_database_type(self):
        return self.get_database_config()['type']
    
    def get_database_uri(self):
        return self.get_database_config()['uri']

    def get_logger_config(self):
        return self.config['Logger']
    
    def get_logger_path(self):
        return self.get_logger_config()['path']
    
    def get_logger_size(self):
        return self.get_logger_config()['size']

    def get_logger_max_rollover(self):
        return self.get_logger_config()['max_rollover']

