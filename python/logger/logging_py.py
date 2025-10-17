import logging

logging.basicConfig(level=logging.INFO)
logging.info("This is an info message")
logging.error("This is an error message")
logging.debug("This is a debug message")

# basicConfig
logging.basicConfig(
    filename='app.log',               # Log to file instead of console
    filemode='a',                     # 'a' = append, 'w' = overwrite
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format of each log
    datefmt='%Y-%m-%d %H:%M:%S',      # Timestamp format
    level=logging.DEBUG               # Minimum level to capture
)
# Logger levels
logging.debug("This is debug")
logging.info("Informational")
logging.warning("Something odd")
logging.error("Something failed")
logging.critical("App crashed!")

# Logger Hierarchy
logger = logging.getLogger("myapp.database")
logger.setLevel(logging.DEBUG)

logger.debug("Database connected")

# 5. Custom Handlers
class CustomHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # Custom logic for handling the log entry
        print(f"Custom log entry: {log_entry}")

custom_handler = CustomHandler()
custom_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(custom_handler)

logging.error("This is an error message")

#StreamHandler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logging.getLogger().addHandler(stream_handler) 
logging.warning("This is a warning message")

#FileHandler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)
logging.info("This is an info message logged to file")


#RotatingFileHandler
rotating_handler = logging.handlers.RotatingFileHandler('app_rotating.log', maxBytes=2000, backupCount=5)
rotating_handler.setLevel(logging.DEBUG)
rotating_handler.setFormatter(formatter)
logging.getLogger().addHandler(rotating_handler)
for i in range(100):
    logging.debug(f"Log entry {i} for rotating file handler")


#TImeRotatingFileHandler
time_rotating_handler = logging.handlers.TimedRotatingFileHandler('app_time_rotating.log', when='midnight', interval=1, backupCount=7)
time_rotating_handler.setLevel(logging.DEBUG)
time_rotating_handler.setFormatter(formatter)
logging.getLogger().addHandler(time_rotating_handler)
logging.info("This is an info message for time rotating file handler")