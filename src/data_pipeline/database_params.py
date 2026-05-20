from configparser import ConfigParser
class database_params:
    def __init__(self):
        self.filename='/zfs/dzrptlab/CDSS/config/database.ini'
        self.section='postgresql'
        
    def config(self):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)

        # get section, default to postgresql
        db = {}

        # Checks to see if section (postgresql) parser exists
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]

        # Returns an error if a parameter is called that is not listed in the initialization file
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db
