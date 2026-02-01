import logging
from dotenv import load_dotenv
import dagshub


load_dotenv()


# Initialize Dagshub with credentials
dagshub.init(repo_owner="anderson.paschoalon", repo_name="Online-Courses_Udemy_MLOPs")

# Configure the logging strategy
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
