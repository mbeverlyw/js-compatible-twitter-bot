from ._base import CONFIG_DIR, CONFIG_FILE, Config


class ActionsConfig(Config):
    def __init__(self):
        self.path = CONFIG_DIR + CONFIG_FILE['actions']
        self.get_config_data()

    def get_command_legend(self):
        return self.config['Command Legend']
    
    def get_available_actions(self):
        return self.config['Available Actions']
    
    def get_exception_responses(self):
        return self.config['Exception Responses']
